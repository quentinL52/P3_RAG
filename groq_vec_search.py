import os
from dotenv import load_dotenv
from langchain_community.embeddings import SentenceTransformerEmbeddings
# from langchain.embeddings import SentenceTransformerEmbeddings
pinecone_api_key = os.getenv("PINECONE_API_KEY")
groq_api = os.getenv('GROQ_API_KEY')
load_dotenv()
import langchain
from langchain_groq import ChatGroq
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore  
from typing import List
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate,ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
import warnings
warnings.filterwarnings('ignore')

from langchain_community.embeddings import SentenceTransformerEmbeddings
embeddings = SentenceTransformerEmbeddings(model_name='sentence-transformers/LaBSE')
vectorstore = PineconeVectorStore(index_name='jobsdata', embedding=embeddings)
docsearch = PineconeVectorStore(index_name='cv', embedding=embeddings)


def chat_groq(t = 0, choix ="llama3-70b-8192", api = "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" ) :
  return ChatGroq(temperature = t, model_name=choix,groq_api_key = api)
model_chat = chat_groq()

message = """
tu es un assistant de recherche emploi, du dois tenir compte de mes skills et de l'experience pr recommander les emploi les plus approprié.
tu sera pertinent dans ta reponse et respectera la logique d'experience du cv ainsi que les skills et competences.
à ma demande tu me retournera 4 jobs les plus proche dans ma base de données.
utilise ce contexte pour repondre. si tu n'as pas de réponse dis le
redonne tous les détails de chaque job ainsi que le lien vers l'annonce d'origine.
{question}

Context:
{context}
{cv}
"""
retrier = vectorstore.as_retriever()
doc_runnable = docsearch.as_retriever()
# doc_runnable = RunnablePassthrough(cv) # probleme avec le parsing llamaparse, il faut que le parsing retourne un print pour fonctionner mais ne fonctionne plus
prompt = ChatPromptTemplate.from_messages([("human", message)])

rag_chain = {"context": retrier, "cv": doc_runnable, "question": RunnablePassthrough()} | prompt | model_chat
r = rag_chain.invoke("je cherche une alternance")
print(r.content)