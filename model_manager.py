"""
Model Manager for handling multiple AI providers
"""

from typing import Optional, List, Dict
from langchain_cerebras import ChatCerebras
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_mistralai import ChatMistral
from langchain_cohere import ChatCohere
from langchain_core.language_models import BaseChatModel

from config import settings, ModelProviderConfig


class ModelManager:
    """Manages initialization and switching between different AI models"""
    
    def __init__(self):
        self.current_provider = settings.DEFAULT_PROVIDER
        self.current_model = settings.DEFAULT_MODEL
        self._llm_cache: Dict[str, BaseChatModel] = {}
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return settings.list_available_providers()
    
    def get_available_models(self, provider: str) -> List[str]:
        """Get available models for a provider"""
        return settings.list_available_models(provider)
    
    def get_provider_info(self, provider: str) -> Optional[ModelProviderConfig]:
        """Get provider configuration"""
        return settings.get_provider_config(provider)
    
    def initialize_model(
        self, 
        provider: Optional[str] = None, 
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> BaseChatModel:
        """Initialize an LLM with the specified provider and model"""
        
        provider = provider or self.current_provider
        model = model or self.current_model
        temperature = temperature or settings.MODEL_TEMPERATURE
        max_tokens = max_tokens or settings.MODEL_MAX_TOKENS
        
        # Check cache
        cache_key = f"{provider}:{model}"
        if cache_key in self._llm_cache:
            return self._llm_cache[cache_key]
        
        config = settings.get_provider_config(provider)
        if not config:
            raise ValueError(f"Provider '{provider}' not found or API key not configured")
        
        llm = self._create_llm(provider, model, temperature, max_tokens)
        self._llm_cache[cache_key] = llm
        
        self.current_provider = provider
        self.current_model = model
        
        return llm
    
    def _create_llm(
        self, 
        provider: str, 
        model: str,
        temperature: float,
        max_tokens: int
    ) -> BaseChatModel:
        """Create LLM instance based on provider"""
        
        if provider == "cerebras":
            return ChatCerebras(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        elif provider == "openai":
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        elif provider == "google_genai":
            return ChatGoogleGenerativeAI(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        elif provider == "groq":
            return ChatGroq(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        elif provider == "mistral":
            return ChatMistral(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        elif provider == "cohere":
            return ChatCohere(
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def switch_provider(self, provider: str, model: Optional[str] = None) -> BaseChatModel:
        """Switch to a different provider"""
        available = self.get_available_providers()
        if provider not in available:
            raise ValueError(f"Provider '{provider}' not available. Available: {available}")
        
        if model is None:
            config = settings.get_provider_config(provider)
            model = config.default_model if config else None
        
        if model is None:
            raise ValueError(f"No default model found for provider '{provider}'")
        
        return self.initialize_model(provider, model)
    
    def get_current_model_info(self) -> Dict[str, str]:
        """Get information about current model"""
        config = settings.get_provider_config(self.current_provider)
        return {
            "provider": self.current_provider,
            "provider_name": config.name if config else "Unknown",
            "model": self.current_model,
        }


# Global model manager instance
model_manager = ModelManager()