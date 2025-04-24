
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import ChatGoogleGenerativeAI
import getpass
import os
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

query = "How many types of normalization are there in SQL explain everyone of them?"

SYSTEM_PROMPTS=f"""
You are a helpful AI assistant who select a proper dataset based on user query.
dataset: git_doc and sql_doc
You have to return only the name of the dataset example: git_doc or sql_doc
userQuery: {query}
"""

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)
result = llm.invoke(SYSTEM_PROMPTS)

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

retriver = QdrantVectorStore.from_existing_collection(
  collection_name=result.content,
  url="http://localhost:6333/",
  embedding=embeddings
)

search_result = retriver.similarity_search(
  query=query
)

SYSTEM_PROMPTS_2=f"""
You are an helpful AI assistant who responds user query based on available context.
query:{query}
context:{search_result}
"""


llm2 = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,)
result2 = llm.invoke(SYSTEM_PROMPTS_2)

print(result2.content)