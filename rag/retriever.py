import os

# Force Hugging Face libraries to work offline.
# The embedding model must already exist in the local cache.
os.environ["HF_HUB_OFFLINE"] = "1"

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_DIR = "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "local_files_only": True
        }
    )


@lru_cache(maxsize=1)
def get_vector_store():

    embeddings = get_embeddings()

    return Chroma(
        collection_name="edupilot_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )


def retrieve_knowledge(
    query,
    k=4
):

    vector_store = get_vector_store()

    documents = vector_store.similarity_search(
        query,
        k=k
    )

    results = []

    for document in documents:

        results.append({
            "content": document.page_content,
            "source": document.metadata.get(
                "source",
                "Unknown"
            )
        })

    return results