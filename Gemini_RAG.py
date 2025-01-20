 import os
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
import codecs
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader,UnstructuredWordDocumentLoader as DocxLoader

# Set your OpenAI API key in environment variable OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = "Enter your key here"

# Define paths
FILE_PATH = "Enter your pdf_folder path"
FAISS_DB_PATH = os.path.join(FILE_PATH, "faiss_index")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
chat_model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)

def convert_to_utf8(file_path):
    temp_file = f"{file_path}.utf8"
    with codecs.open(file_path, "r", encoding="latin-1", errors="ignore") as source_file:
        with open(temp_file, "w", encoding="utf-8") as target_file:
            target_file.write(source_file.read())
    return temp_file
# Function to load and split documents
def load_documents(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".pdf":
        loader = PyPDFLoader(file_path)
    elif file_extension == ".docx":
        loader = DocxLoader(file_path)
    elif file_extension == ".txt":
        file_path = convert_to_utf8(file_path)
        loader = TextLoader(file_path)
    elif file_extension == ".csv":
        loader = CSVLoader(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return []
    return loader.load_and_split()

# Retrieve metadata from existing FAISS index
def get_existing_files_metadata(faiss_index):
    existing_files_metadata = {}
    for doc_id, doc_meta in faiss_index.docstore._dict.items():
        file_name = doc_meta.metadata.get("source", "")
        file_size = doc_meta.metadata.get("size", 0)
        print(f"Doc ID: {doc_id}")
        if file_name:
            existing_files_metadata[file_name] = file_size
        print(f"Current metadata map: {existing_files_metadata}")
    return existing_files_metadata

def add_new_files_to_faiss(faiss_index):
    print("Checking for updates in the FAISS index...")
    existing_files_metadata = get_existing_files_metadata(faiss_index)
    
    supported_extensions = [".pdf", ".docx", ".txt", ".csv"]
    all_files = [os.path.join(FILE_PATH, f) for f in os.listdir(FILE_PATH) if os.path.splitext(f)[1].lower() in supported_extensions]
    documents_to_add = []

    for file in all_files:
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file)

        if file_name in existing_files_metadata and existing_files_metadata[file_name] == file_size:
            print(f"Skipping file '{file_name}' as it already exists in the FAISS index.")
            continue

        print(f"Processing new or updated file: {file_name}")
        try:
            documents = load_documents(file)
        except Exception as e:
            print(f"Error while loading file '{file_name}': {e}")
            continue

        for doc in documents:
            doc.metadata["source"] = file_name
            doc.metadata["size"] = file_size
        documents_to_add.extend(documents)

    if documents_to_add:
        print("Adding new documents to the FAISS index...")
        faiss_index.add_documents(documents_to_add)
        faiss_index.save_local(FAISS_DB_PATH)
        print("FAISS database updated successfully!")
    else:
        print("No new files found to add to the database.")


 # Load or create FAISS index
def load_or_create_faiss():
    if os.path.exists(FAISS_DB_PATH):
        print("Loading existing FAISS database...")
        faiss_index = FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        add_new_files_to_faiss(faiss_index)
        # Reload after adding new files
        faiss_index = FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        return faiss_index
    else:
        print("Creating a new FAISS database...")
        supported_extensions = [".pdf", ".docx", ".txt", ".csv"]
        all_files = [os.path.join(FILE_PATH, f) for f in os.listdir(FILE_PATH) if os.path.splitext(f)[1].lower() in supported_extensions]
        documents = []
        for file in all_files:
            documents.extend(load_documents(file))

        faiss_index = FAISS.from_documents(documents, embeddings)
        faiss_index.save_local(FAISS_DB_PATH)
        return faiss_index

# Get chatbot response
def get_chatbot_response(query, chat_history=[]):
    faiss_db = load_or_create_faiss()
    retriever = faiss_db.as_retriever(search_kwargs={"k": 5})

    response_chain = ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=retriever,
        return_source_documents=False
    )

    try:
        # Get the AI response
        response = response_chain.invoke({"question": query, "chat_history": chat_history})

    except Exception as e:
        print(f"Validation failed or error encountered: {e}")
        response = {"answer": "Sorry, I can't help with that."}

    answer = response.get("answer", "Sorry, no answer was found.")
    return answer
    
    

if __name__ == "__main__":
    while True:
        user_query = input("Ask a question: ")
        if user_query.lower() in ["exit", "quit"]:
            break
        answer = get_chatbot_response(user_query)
        print(f"Bot: {answer}")
