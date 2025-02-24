from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import *
import os
from langchain_google_genai import GoogleGenerativeAI



app = Flask(__name__)



llm = GoogleGenerativeAI(
    model='gemini-pro' ,
    api_key = "AIzaSyDIly_Uvnhh1i5acecax8gwfRoZUYx1YSY",
    temperature=0.4, 
    max_tokens= 500
)
os.environ["PINECONE_API_KEY"] = "pcsk_6Y8jK5_GXfQEuDxvySif3Ae6CW6nLSQjRPzpW2QfGNsX3kWyixVJ8riLjZ7Pew8gp3ZkeZ"

embeddings = download_hugging_face_embeddings()


index_name = "medchatbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)