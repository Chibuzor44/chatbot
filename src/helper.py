from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_files(path):
    loader = DirectoryLoader(path, 
                             glob="*.pdf", 
                             loader_cls=PyPDFLoader)
    documents = loader.load()
    return documents

def text_splitter(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    chunks = text_splitter.split_documents(text)
    return chunks
