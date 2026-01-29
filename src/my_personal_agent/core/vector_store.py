"""
Vector Store implementation using ChromaDB for RAG
"""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional, Any
from pathlib import Path
from src.my_personal_agent.config import settings
from src.my_personal_agent.core.llm_client import LLMClient


class VectorStore:
    """Vector store for storing and retrieving document embeddings"""
    
    def __init__(self, collection_name: str = "personal_agent", llm_client: Optional[LLMClient] = None):
        self.collection_name = collection_name
        self.llm_client = llm_client or LLMClient()
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=settings.vector_db_path,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """Add documents to the vector store"""
        if not texts:
            return []
        
        # Generate embeddings
        embeddings = []
        for text in texts:
            embedding = self.llm_client.get_embeddings(text)
            embeddings.append(embedding)
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"doc_{i}_{hash(text)}" for i, text in enumerate(texts)]
        
        # Default metadatas
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )
        
        return ids
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        # Generate query embedding
        query_embedding = self.llm_client.get_embeddings(query)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=filter,
        )
        
        # Format results
        formatted_results = []
        if results["documents"] and len(results["documents"][0]) > 0:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "id": results["ids"][0][i] if results["ids"] else None,
                    "distance": results["distances"][0][i] if results["distances"] else None,
                })
        
        return formatted_results
    
    def delete_collection(self):
        """Delete the entire collection"""
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the collection"""
        count = self.collection.count()
        return {
            "collection_name": self.collection_name,
            "document_count": count,
        }

