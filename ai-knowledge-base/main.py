from typing import Iterator
from pathlib import Path
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document as LCDocument
from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

from typing import Iterable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="AI Document Assistant",
    description="Automating Raw Unstructured data to Structured Document Workflow",
    version="1.0.0"
)

# Include all routes
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "AI Document Assistant - Ready for Hackathon!", "status": "active"}


class DoclingLoader(BaseLoader):
    """Document loader using Docling for various document formats."""

    def __init__(self, file_path: str | list[str]) -> None:
        self._file_paths = file_path if isinstance(file_path, list) else [file_path]
        self._converter = DocumentConverter()

    def lazy_load(self) -> Iterator[LCDocument]:
        for source in self._file_paths:
            dl_doc = self._converter.convert(source).document
            text = dl_doc.export_to_markdown()
            yield LCDocument(page_content=text)


def demonstrate_document_loading() -> Iterable[LCDocument]:
    """Load all supported documents from the Uploads directory."""
    uploads_dir = Path("./Uploads")

    if not uploads_dir.exists():
        print(f"Uploads directory not found: {uploads_dir}")
        return []

    # Common document extensions supported by Docling
    supported_extensions = {'.pdf', '.docx', '.doc', '.pptx', '.ppt', '.xlsx', '.xls', '.txt', '.md'}

    # Find all supported files in the Uploads directory
    file_paths = []
    for file_path in uploads_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            file_paths.append(str(file_path))

    if not file_paths:
        print(f"No supported documents found in {uploads_dir}")
        print(f"Supported extensions: {', '.join(supported_extensions)}")
        return []

    print(f"Found {len(file_paths)} supported document(s):")

    all_documents = []

    # Load each file individually with error handling
    for file_path in file_paths:
        print(f"  - {Path(file_path).name}")

        try:
            print(f"Loading: {Path(file_path).name}")
            docling_loader = DoclingLoader(file_path)
            documents = docling_loader.load()
            all_documents.extend(documents)
            print(f"  ✓ Successfully loaded {len(documents)} document(s) from {Path(file_path).name}")
        except Exception as e:
            print(f"  ✗ Error loading {Path(file_path).name}: {e}")
            continue

    print(f"\nTotal documents loaded: {len(all_documents)}")
    return all_documents


def format_docs(docs: Iterable[LCDocument]) -> Iterable[str]:
    return "\n\n".join(doc.page_content for doc in docs)


def main() -> None:
    print("Starting Docling Document Loader Demo")
    docs = demonstrate_document_loading()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    # embeddings = HuggingFaceEmbeddings(model_name=HF_EMBED_MODEL_ID)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    persist_directory = "./chroma_db"
    # client = MilvusClient(MILVUS_URI)
    # chroma_client = chromadb.Client();
    vectorstore = Chroma.from_documents(
        splits,
        embeddings,
        persist_directory=persist_directory
    )
    # vectorstore = Milvus.from_documents(
    #     splits,
    #     embeddings,
    #     collection_name="langchain_example",
    #     connection_args={"uri": MILVUS_URI}
    # )

    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.environ.get("GOOGLE_API_KEY"),
        temperature=0.7
    )


    retriever = vectorstore.as_retriever()
    prompt = PromptTemplate.from_template("""
You are a helpful AI assistant that answers questions based on provided documents. 

Here is the relevant information from the documents:
{context}

Based on the information above, please answer the following question. If the answer is not found in the provided context, please say so clearly. Be specific and cite relevant details when possible.

Question: {question}

Answer: """)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("\n" + "="*50)
    print("RAG CHAIN RESPONSE:")
    print("="*50)

    result = rag_chain.invoke("How many students from Ms. Hubert’s afterschool took the survey?")

    print(result)

    print("="*50)

if __name__ == '__main__':
    main()
