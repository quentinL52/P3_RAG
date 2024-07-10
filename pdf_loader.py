from langchain_community.document_loaders import PyPDFLoader
import time
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from langchain_community.embeddings import SentenceTransformerEmbeddings
import warnings
warnings.filterwarnings('ignore')
import os
from dotenv import load_dotenv
pinecone_api_key = os.getenv("PINECONE_API_KEY")
load_dotenv()

embeddings = SentenceTransformerEmbeddings(model_name='sentence-transformers/LaBSE')
###### ici on charge le pdf ########################
pdf_path = ' '

def pdf_loader(pdf):
    loader = PyPDFLoader(pdf)
    pages = loader.load_and_split()

    return pages


docu_pdf = pdf_loader(pdf_path)

############## lancer l'index pinecone ##############
def cv_index(documents):
  pc = Pinecone(api_key=pinecone_api_key)
  index_name = "cv"
  pc.delete_index(index_name)
  existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

  if index_name not in existing_indexes:
      pc.create_index(
          name=index_name,
          dimension=768, 
          metric="cosine",
          spec=ServerlessSpec(cloud="aws", region="us-east-1"),
      )
      while not pc.describe_index(index_name).status["ready"]:
          time.sleep(1)

  index = pc.Index(index_name)
  docsearch = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name,pinecone_api_key=pc)
  return docsearch

######################## indexage du pdf ###########################

docsearch = cv_index(docu_pdf)


