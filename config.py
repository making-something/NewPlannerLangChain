"""
Application Configuration
Environment variables and settings for multi-model support
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class ModelProviderConfig:
    """Configuration for a single model provider"""
    
    def __init__(
        self,
        provider: str,
        name: str,
        api_key_env: str,
        default_model: Optional[str] = None,
        models: Optional[List[str]] = None,
        base_url: Optional[str] = None,
        enabled: bool = False
    ):
        self.provider = provider
        self.name = name
        self.api_key_env = api_key_env
        self.api_key = os.getenv(api_key_env, "")
        self.default_model = default_model
        self.models = models or []
        self.base_url = base_url
        self.enabled = enabled and bool(self.api_key)


class Settings:
    """Application settings loaded from environment variables"""
    
    # API Keys for all providers
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    CEREBRAS_API_KEY: str = os.getenv("CEREBRAS_API_KEY", "")
    
    # Default Model Configuration
    DEFAULT_PROVIDER: str = os.getenv("DEFAULT_PROVIDER", "cerebras")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama-3.3-70b")
    MODEL_TEMPERATURE: float = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
    MODEL_MAX_TOKENS: int = int(os.getenv("MODEL_MAX_TOKENS", "2048"))
    
    # Holiday Planner specific settings
    SAVE_ITINERARIES: bool = os.getenv("SAVE_ITINERARIES", "true").lower() == "true"
    ITINERARY_OUTPUT_DIR: str = os.getenv("ITINERARY_OUTPUT_DIR", "./itineraries")
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Model Providers Configuration
    MODEL_PROVIDERS: Dict[str, ModelProviderConfig] = {}
    
    def __init__(self):
        self._init_providers()
    
    def _init_providers(self):
        """Initialize all model providers with their configurations"""
        
        self.MODEL_PROVIDERS = {
            # Google Gemini
            "google_genai": ModelProviderConfig(
                provider="google_genai",
                name="Google Gemini",
                api_key_env="GEMINI_API_KEY",
                default_model="gemini-2.0-flash",
                models=["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash"],
                enabled=True
            ),
            
            # OpenAI
            "openai": ModelProviderConfig(
                provider="openai",
                name="OpenAI",
                api_key_env="OPENAI_API_KEY",
                default_model="gpt-4o",
                models=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
                enabled=True
            ),
            
            # Anthropic
            "anthropic": ModelProviderConfig(
                provider="anthropic",
                name="Anthropic Claude",
                api_key_env="ANTHROPIC_API_KEY",
                default_model="claude-3-5-sonnet-20241022",
                models=["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
                enabled=True
            ),
            
            # Groq
            "groq": ModelProviderConfig(
                provider="groq",
                name="Groq",
                api_key_env="GROQ_API_KEY",
                default_model="mixtral-8x7b-32768",
                models=["mixtral-8x7b-32768", "llama2-70b-4096"],
                enabled=True
            ),
            
            # Mistral
            "mistral": ModelProviderConfig(
                provider="mistral",
                name="Mistral AI",
                api_key_env="MISTRAL_API_KEY",
                default_model="mistral-large-latest",
                models=["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"],
                enabled=True
            ),
            
            # Cohere
            "cohere": ModelProviderConfig(
                provider="cohere",
                name="Cohere",
                api_key_env="COHERE_API_KEY",
                default_model="command-r-plus",
                models=["command-r-plus", "command-r"],
                enabled=True
            ),
            
            # Cerebras
            "cerebras": ModelProviderConfig(
                provider="cerebras",
                name="Cerebras",
                api_key_env="CEREBRAS_API_KEY",
                default_model="llama-3.3-70b",
                models=["llama-3.3-70b", "llama-3.1-70b", "llama-3.1-8b"],
                enabled=True
            ),
        }
    
    def get_enabled_providers(self) -> Dict[str, ModelProviderConfig]:
        """Get all providers that have valid API keys"""
        return {
            k: v for k, v in self.MODEL_PROVIDERS.items() 
            if v.enabled
        }
    
    def get_provider_config(self, provider: str) -> Optional[ModelProviderConfig]:
        """Get configuration for a specific provider"""
        config = self.MODEL_PROVIDERS.get(provider)
        if config and config.enabled:
            return config
        return None
    
    def list_available_providers(self) -> List[str]:
        """List all available providers with valid API keys"""
        return list(self.get_enabled_providers().keys())
    
    def list_available_models(self, provider: str) -> List[str]:
        """List available models for a specific provider"""
        config = self.get_provider_config(provider)
        return config.models if config else []


# Initialize settings
settings = Settings()

# Set environment variables for all configured API keys
if settings.GEMINI_API_KEY:
    os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY
    os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY

if settings.OPENAI_API_KEY:
    os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

if settings.ANTHROPIC_API_KEY:
    os.environ["ANTHROPIC_API_KEY"] = settings.ANTHROPIC_API_KEY

if settings.GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY

if settings.MISTRAL_API_KEY:
    os.environ["MISTRAL_API_KEY"] = settings.MISTRAL_API_KEY

if settings.COHERE_API_KEY:
    os.environ["COHERE_API_KEY"] = settings.COHERE_API_KEY

if settings.CEREBRAS_API_KEY:
    os.environ["CEREBRAS_API_KEY"] = settings.CEREBRAS_API_KEY