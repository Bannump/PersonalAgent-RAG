"""
LLM Client abstraction for multiple providers (OpenAI, Anthropic)
"""
import base64
from typing import Optional, List, Dict, Any
from abc import ABC, abstractmethod
import openai
from anthropic import Anthropic
from src.my_personal_agent.config import settings


class BaseLLMClient(ABC):
    """Abstract base class for LLM clients"""
    
    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion"""
        pass
    
    @abstractmethod
    def vision_completion(
        self,
        messages: List[Dict[str, Any]],
        image_path: str,
        model: Optional[str] = None,
    ) -> str:
        """Generate vision-based completion with image"""
        pass
    
    @abstractmethod
    def get_embeddings(self, text: str, model: Optional[str] = None) -> List[float]:
        """Get text embeddings"""
        pass


class OpenAILLMClient(BaseLLMClient):
    """OpenAI LLM client implementation"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
        self.default_model = settings.default_model
        self.embedding_model = settings.embedding_model
    
    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion using OpenAI"""
        model = model or self.default_model
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    
    def vision_completion(
        self,
        messages: List[Dict[str, Any]],
        image_path: str,
        model: Optional[str] = None,
    ) -> str:
        """Generate vision-based completion with image using GPT-4 Vision"""
        import base64
        
        # Read and encode image
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Prepare vision message
        vision_messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": messages[-1]["content"]},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        # Add previous messages (excluding the last one which we modified)
        if len(messages) > 1:
            vision_messages = messages[:-1] + vision_messages
        
        model = model or "gpt-4o"  # Updated to gpt-4o which supports vision
        response = self.client.chat.completions.create(
            model=model,
            messages=vision_messages,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    
    def get_embeddings(self, text: str, model: Optional[str] = None) -> List[float]:
        """Get text embeddings using OpenAI"""
        model = model or self.embedding_model
        response = self.client.embeddings.create(
            model=model,
            input=text,
        )
        return response.data[0].embedding


class AnthropicLLMClient(BaseLLMClient):
    """Anthropic Claude LLM client implementation"""
    
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.default_model = "claude-3-opus-20240229"
    
    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion using Anthropic"""
        model = model or self.default_model
        max_tokens = max_tokens or 4096
        
        # Convert messages format for Anthropic
        system_message = None
        anthropic_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                anthropic_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_message,
            messages=anthropic_messages,
        )
        return response.content[0].text
    
    def vision_completion(
        self,
        messages: List[Dict[str, Any]],
        image_path: str,
        model: Optional[str] = None,
    ) -> str:
        """Generate vision-based completion with image using Claude"""
        import base64
        
        # Read and encode image
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine media type
        image_ext = image_path.split('.')[-1].lower()
        media_type = f"image/{image_ext if image_ext in ['jpeg', 'jpg', 'png', 'gif', 'webp'] else 'jpeg'}"
        
        model = model or "claude-3-opus-20240229"
        user_message_content = messages[-1]["content"]
        
        response = self.client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": user_message_content,
                        },
                    ],
                }
            ],
        )
        return response.content[0].text
    
    def get_embeddings(self, text: str, model: Optional[str] = None) -> List[float]:
        """Anthropic doesn't provide embeddings API, use OpenAI as fallback"""
        raise NotImplementedError(
            "Anthropic doesn't provide embeddings. Use OpenAI client for embeddings."
        )


class LLMClient:
    """Unified LLM client that supports multiple providers"""
    
    def __init__(
        self,
        provider: str = None,
        openai_key: str = None,
        anthropic_key: str = None,
    ):
        self.provider = provider or settings.default_llm_provider
        self.openai_key = openai_key or settings.openai_api_key
        self.anthropic_key = anthropic_key or settings.anthropic_api_key
        
        # Initialize clients (with validation)
        self.openai_client = None
        self.anthropic_client = None
        self.active_client = None
        
        # Initialize OpenAI client if key is provided
        if self.openai_key:
            try:
                self.openai_client = OpenAILLMClient(self.openai_key)
            except Exception as e:
                print(f"WARNING: Failed to initialize OpenAI client: {e}")
        
        # Initialize Anthropic client if key is provided
        if self.anthropic_key:
            try:
                self.anthropic_client = AnthropicLLMClient(self.anthropic_key)
            except Exception as e:
                print(f"WARNING: Failed to initialize Anthropic client: {e}")
        
        # Set active client based on provider preference
        if self.provider == "openai" and self.openai_client:
            self.active_client = self.openai_client
        elif self.provider == "anthropic" and self.anthropic_client:
            self.active_client = self.anthropic_client
        elif self.openai_client:
            self.active_client = self.openai_client
        elif self.anthropic_client:
            self.active_client = self.anthropic_client
        
        if not self.active_client:
            print("WARNING: No LLM client initialized. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")
    
    def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate chat completion using active provider"""
        if not self.active_client:
            raise RuntimeError("No LLM client available. Please set OPENAI_API_KEY environment variable.")
        return self.active_client.chat_completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    def vision_completion(
        self,
        messages: List[Dict[str, Any]],
        image_path: str,
        model: Optional[str] = None,
    ) -> str:
        """Generate vision-based completion with image"""
        if not self.active_client:
            raise RuntimeError("No LLM client available. Please set OPENAI_API_KEY environment variable.")
        return self.active_client.vision_completion(
            messages=messages,
            image_path=image_path,
            model=model,
        )
    
    def get_embeddings(self, text: str, model: Optional[str] = None) -> List[float]:
        """Get text embeddings (always uses OpenAI for embeddings)"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not available. Please set OPENAI_API_KEY environment variable.")
        return self.openai_client.get_embeddings(text, model)

