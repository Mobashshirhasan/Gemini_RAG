 <h1>Document Chatbot with FAISS and Google Generative AI</h1>
A powerful document-based question-answering system that uses FAISS (Facebook AI Similarity Search) for efficient vector storage and Google's Generative AI for embeddings and chat completions. This chatbot can process and answer questions from multiple document formats including PDF, DOCX, TXT, and CSV files.
<h1>Features</h1>

<h4>Multiple Document Format Support:</h4>

PDF files
Word documents (DOCX)
Text files (TXT)
CSV files


<h3>Efficient Document Processing:</h3>

Automatic document splitting
UTF-8 encoding conversion for text files
Incremental updates to the vector database
File change detection to avoid reprocessing unchanged documents


<h3>Vector Search Integration:</h3>

FAISS-based vector storage for efficient similarity search
Document metadata tracking
Persistent storage of embeddings


<h3>Google AI Integration:</h3>

Uses Google's Generative AI embeddings (models/embedding-001)
Powered by Gemini 1.5 Pro for chat completions
Temperature setting of 0.3 for balanced responses



<h1>Prerequisites</h1>

Python 3.x
Google API Key

Required Dependencies
bashCopypip install langchain-community
pip install faiss-cpu
pip install langchain-google-genai
pip install unstructured
pip install python-magic-bin  # For document loading
Environment Setup

<h3>Set your Google API key:</h3>

pythonCopyos.environ["GOOGLE_API_KEY"] = "your-api-key-here"

<h3>Configure the document directory:</h3>

pythonCopyFILE_PATH = "path/to/your/documents"
Usage

Place your documents in the configured directory
Run the chatbot:

bashCopypython your_script_name.py

<h3>Start asking questions about your documents : </h3>

CopyAsk a question: What does the financial report say about Q3 earnings?

Type 'exit' or 'quit' to end the session

How It Works

<h3>Document Processing:</h3>

Documents are loaded and split into chunks
Text files are automatically converted to UTF-8 encoding
Each document chunk is processed with metadata including source and file size


<h3>Vector Database Management:</h3>

Creates a new FAISS index if none exists
Updates existing index with new or modified documents
Maintains document metadata for efficient updates


<h3>Query Processing:</h3>

Converts user questions into embeddings
Retrieves relevant document chunks using FAISS
Generates contextual responses using Google's Generative AI



Features in Detail
Document Change Detection
The system tracks document changes by:

Storing file metadata (name and size)
Comparing existing files with stored metadata
Only processing new or modified files

UTF-8 Conversion
Automatically handles encoding issues by:

Converting text files to UTF-8
Creating temporary converted files
Ensuring compatibility across different text encodings

Error Handling
<h3>Robust error handling for: </h3>

File loading issues
API communication errors
Invalid document formats

Contributing
Feel free to submit issues and enhancement requests!
