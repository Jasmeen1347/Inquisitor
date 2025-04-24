from langchain_community.document_loaders import WebBaseLoader
import getpass
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API key here")

doc_links = [
  {
    "title": "git_doc",
    "links": [
      "https://chaidocs.vercel.app/youtube/chai-aur-git/welcome/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/introduction/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/terminology/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/behind-the-scenes/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/branches/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/diff-stash-tags/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/managing-history/",
      "https://chaidocs.vercel.app/youtube/chai-aur-git/github/",
    ]
  },
  {
    "title": "sql_doc",
    "links": [
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/welcome/",
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/introduction/",
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/postgres/",
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/normalization/",
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/database-design-exercise/",
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/joins-and-keys/",
      "https://chaidocs.vercel.app/youtube/chai-aur-sql/joins-exercise/"
    ]
  }
]

for doc_link in doc_links:
  current_doc = []
  for link in doc_link["links"]:
    loader = WebBaseLoader(link)
    docs = loader.load()
    current_doc.append(docs[0])
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    vector_store = QdrantVectorStore.from_documents(
      documents=[],
      collection_name=doc_link["title"],
      url="http://localhost:6333/",
      embedding=embeddings
    )

    vector_store.add_documents(documents=current_doc)
