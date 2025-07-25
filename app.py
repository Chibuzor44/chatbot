from flask import Flask, render_template, request, jsonify
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from src.prompt import system_prompt
from dotenv import load_dotenv
from operator import itemgetter
import os
import logging

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_NAME = "chatbot"

app = Flask(__name__)
model = OpenAI(openai_api_key=OPENAI_API_KEY)


embeddingModel = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

document_search = PineconeVectorStore(
    index_name=INDEX_NAME,
    embedding=embeddingModel
)

retriever = document_search.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k":5, "score_threshold": 0.4}
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}"),
    ]
)

# question_answer_chain = (
#     {
#         "context": itemgetter("context"), 
#         "question": itemgetter("question")
#     }
#     | prompt 
#     | model
#     | StrOutputParser()
# )

question_answer_chain = (
    {
        "context": retriever, 
        "question": RunnablePassthrough()
    }
    | prompt 
    | model
    | StrOutputParser()
)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    logger.info(f"Received message: {msg}")
    
    # input_variables = {"question": msg, "context": retriever.invoke(msg)}
    # print(f"context: {input_variables['context']}")
    
    # response = question_answer_chain.invoke(input_variables)
    response = question_answer_chain.invoke(msg)
    
    logger.info(f"Response: {response}")
    # response_split = response.strip().split('\n')
    # for line in response_split:
    #     if line.startswith('System:'):
    #         logger.info(f"System Response: {line.replace('System:', '')}")
    #         return line.replace('System:', '')
    #     elif line.startswith('answer:'):
    #         logger.info(f"System Response: {line.replace('answer:', '')}")
    #         return line.replace('System:', '')
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)