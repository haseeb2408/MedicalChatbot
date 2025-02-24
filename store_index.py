from src.helper import load_pdf_file , text_split , download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
import os
from pinecone import Pinecone




os.environ['PINECONE_API_KEY'] = "Your PineCone APi"
extracted_text = load_pdf_file(data='../Data/')
text_chunks = text_split(extracted_data=extracted_text)
embeddings = download_hugging_face_embeddings()



pc = Pinecone(api_key = "Your Pinecone api")
index_name = "medchatbot"

pc.create_index(
    name=index_name,
    dimension=384, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    ) 
)

docsearch = PineconeVectorStore.from_documents(
    documents = text_chunks , 
    index_name = index_name , 
    embedding = embeddings
)
