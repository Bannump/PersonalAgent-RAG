"""
Core RAG Engine that combines vector store retrieval with LLM generation
"""
from typing import List, Dict, Any, Optional
from src.my_personal_agent.core.vector_store import VectorStore
from src.my_personal_agent.core.llm_client import LLMClient


class RAGEngine:
    """Retrieval-Augmented Generation Engine"""
    
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm_client: Optional[LLMClient] = None,
    ):
        self.llm_client = llm_client or LLMClient()
        self.vector_store = vector_store or VectorStore(llm_client=self.llm_client)
    
    def query(
        self,
        question: str,
        context_collection: Optional[str] = None,
        max_context_docs: int = 5,
        temperature: float = 0.7,
        system_prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query the RAG engine with a question
        
        Args:
            question: User's question
            context_collection: Optional collection name for context-specific queries
            max_context_docs: Maximum number of relevant documents to retrieve
            temperature: LLM temperature parameter
            system_prompt: Optional system prompt to guide the response
        
        Returns:
            Dictionary with 'answer', 'sources', and 'metadata'
        """
        # Retrieve relevant context
        relevant_docs = self.vector_store.search(
            query=question,
            n_results=max_context_docs,
        )
        
        # Build context from retrieved documents
        context = "\n\n".join([doc["document"] for doc in relevant_docs])
        
        # Build messages
        system_message = system_prompt or (
            "You are a helpful personal assistant. Use the provided context to answer questions. "
            "If the context doesn't contain enough information, say so and provide the best answer you can."
        )
        
        user_message = f"""Context:
{context}

Question: {question}

Please provide a comprehensive answer based on the context above."""
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]
        
        # Generate answer
        answer = self.llm_client.chat_completion(
            messages=messages,
            temperature=temperature,
        )
        
        return {
            "answer": answer,
            "sources": [
                {
                    "content": doc["document"][:200] + "..." if len(doc["document"]) > 200 else doc["document"],
                    "metadata": doc["metadata"],
                }
                for doc in relevant_docs
            ],
            "metadata": {
                "num_sources": len(relevant_docs),
                "question": question,
            },
        }
    
    def add_knowledge(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
    ) -> List[str]:
        """Add knowledge to the vector store"""
        return self.vector_store.add_documents(texts=texts, metadatas=metadatas)
    
    def vision_query(
        self,
        question: str,
        image_path: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
    ) -> str:
        """
        Query with an image using vision capabilities
        
        Args:
            question: User's question about the image
            image_path: Path to the image file
            system_prompt: Optional system prompt
            temperature: LLM temperature parameter
        
        Returns:
            Answer as a string
        """
        system_message = system_prompt or (
            "You are a helpful assistant that can analyze images and provide detailed, actionable advice. "
            "Provide specific solutions and next steps when relevant."
        )
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": question},
        ]
        
        answer = self.llm_client.vision_completion(
            messages=messages,
            image_path=image_path,
        )
        
        return answer

