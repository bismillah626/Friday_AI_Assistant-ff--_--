import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema.retriever import BaseRetriever
from langchain.memory import ConversationBufferMemory

class MemoryManager:
    """Manages conversational memory and long term vector memory."""
    def __init__(self):
        #initializing the embedding model
        self.embedding_function = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2")
        
        #initializing ChromaDB for persiistent long term memory
        self.db_client = chromadb.PersistentClient(path="./chroma_db")
        self.vector_store = Chroma(
            collection_name="friday_memory",
            embedding_function=self.embedding_function,
            client=self.db_client
        )
        #initializing short term conversational memory
        self.conversational_memory = ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history"
        )

    def get_vector_retriever(self) -> BaseRetriever:
        
        """Returns the vector store as a retriever for similarity searches."""
        return self.vector_store.as_retriever(search_kwargs={"k": 3})

    def save_interaction(self, user_input: str, ai_response: str):
        """Saves a user-AI interaction to the vector store."""
        interaction_text = f"User asked: {user_input}\nFriday responded: {ai_response}"
        self.vector_store.add_texts([interaction_text])
        print(f"[Memory] Saved interaction to Vector DB.")