import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from typing import List, Optional


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

class create_new_embadding:

    def __init__(self, file_path: str,
                 embadding_collection_name: str,
                 retriever_tool_name : Optional[str] | None = "mytool",
                 retriever_tool_description  : Optional[str] | None = "Searches and returns documents based on given input.") -> None:
        self.file_path = file_path 
        self.embadding_collection_name = embadding_collection_name
        self.retriever_tool_name = retriever_tool_name
        self.retriever_tool_description = retriever_tool_description
        self.emabdding_model = OpenAIEmbeddings()

    def create_embadding(self):
        loader = PyPDFLoader(self.file_path)
        pages = loader.load_and_split()
        vectorstore = Chroma.from_documents(
                documents=pages,
                collection_name=self.embadding_collection_name,
                embedding=self.emabdding_model,
            )
        retriever = vectorstore.as_retriever(k=3)
        return retriever
    
    def create_retriever_tools(self):
        retriever = self.create_embadding()
        retriever_tool = create_retriever_tool(
            retriever,
            self.retriever_tool_name,
            self.retriever_tool_description,
        )
        return retriever_tool
        


