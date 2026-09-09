from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


DOCUMENTS_DIR = Path("data/documents")
CHROMA_DIR = "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def extract_pdf_text(pdf_path):

    reader = PdfReader(str(pdf_path))

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    return splitter.split_text(text)


def create_vector_database():

    print("\n[RAG] Starting document ingestion...")

    all_chunks = []
    metadatas = []

    pdf_files = list(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:

        raise FileNotFoundError(
            "No PDF found inside data/documents/"
        )

    for pdf_path in pdf_files:

        print(
            f"[RAG] Reading: {pdf_path.name}"
        )

        text = extract_pdf_text(pdf_path)

        chunks = split_text(text)

        print(
            f"[RAG] Created {len(chunks)} chunks"
        )

        for chunk in chunks:

            all_chunks.append(chunk)

            metadatas.append({
                "source": pdf_path.name
            })

    print(
        f"\n[RAG] Total chunks: {len(all_chunks)}"
    )

    print(
        "\n[RAG] Loading local embedding model..."
    )

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print(
        "[RAG] Local embedding model loaded."
    )

    vector_store = Chroma(
        collection_name="edupilot_knowledge",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    print(
        "\n[RAG] Creating embeddings..."
    )

    vector_store.add_texts(
        texts=all_chunks,
        metadatas=metadatas
    )

    print(
        "\n[RAG] Knowledge base created successfully."
    )


if __name__ == "__main__":
    create_vector_database()