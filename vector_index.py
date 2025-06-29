from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pinecone.grpc import PineconeGRPC
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.helper import load_files, text_splitter
from dotenv import load_dotenv
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

logger.info("starting text exxtraction...")
extracted_data = load_files("data")

logger.info("Chunking text...")
text_chunks = text_splitter(extracted_data)

logger.info("setting embedding model...")
embeddingModel = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

logger.info(f'count of chunks: {len(text_chunks)}')


logger.info("Indexing to pinecone...")
index_name = "chatbot"
pc = PineconeGRPC(api_key=PINECONE_API_KEY)
pc.create_index(
    name=index_name,
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

batch_size = 100 # size that keeps the request under 2MB
for i in range(0, len(text_chunks), batch_size):
    batch_documents = text_chunks[i:i + batch_size]
    document_search = PineconeVectorStore.from_documents(
        documents=batch_documents,
        embedding=embeddingModel,
        index_name=index_name
    )
    logger.info(f"Documents indexed in Pinecone: {batch_size * i} ({round((batch_size * i)/len(batch_documents) * 100, 2)})%")