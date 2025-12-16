import os
from typing import List, Dict, Any
from langchain_cerebras import ChatCerebras
from langchain_core.messages import HumanMessage, SystemMessage

# Optional imports for other providers
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None


class LLMService:
    """Service for handling LLM interactions with multiple providers."""
    
    def __init__(self):
        """Initialize the LLM service."""
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for holiday planning."""
        return """You are an expert travel and holiday planner with extensive knowledge of destinations around the world. 
Your role is to create HIGHLY DETAILED, EXTENSIVE, and personalized itineraries based on user preferences. Do not be brief. Provide rich, descriptive content for every recommendation.

When creating an itinerary, you should:
1. Structure the itinerary clearly:
   - Use "# Day X: [Title]" for each day.
   - Use "### Morning", "### Afternoon", "### Evening" as subheadings for time phases.
   - Ensure the activity details for each phase start on a NEW LINE after the subheading.
   - Do NOT use specific timestamps like "10:00 AM".
2. Provide EXTENSIVE details for each activity:
   - Describe the history, architecture, or significance of the place in depth.
   - Explain exactly what to see and do there.
   - Mention the atmosphere, best photo spots, and unique features.
3. Include ELABORATE recommendations for restaurants:
   - Mention signature dishes to try.
   - Describe the ambiance and price range.
4. For EVERY specific place, restaurant, hotel, or attraction mentioned, you MUST provide a Google Search link in Markdown format. Example: [Place Name](https://www.google.com/search?q=Place+Name).
5. Give practical tips about transportation (travel time between spots), best times to visit, and local customs.
6. Consider budget constraints in your recommendations.
7. Balance various interests (adventure, culture, relaxation, food, etc.).
8. Include estimated costs where relevant.
9. Suggest packing tips and weather considerations.
10. Provide local insights and hidden gems.

Format your response clearly with sections for each day, and include a summary section with practical tips.

IMPORTANT: At the end of your itinerary, add a section called "FOLLOW-UP QUESTIONS" with 3-4 specific questions that would help refine the itinerary further. Format these questions clearly for user input."""
    
    def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get list of available providers and their models based on API keys."""
        providers = []
        
        # Cerebras
        if os.getenv("CEREBRAS_API_KEY"):
            providers.append({
                "provider": "cerebras",
                "name": "Cerebras",
                "models": [
                    {"id": "llama-3.3-70b", "name": "Llama 3.3 70B"}
                ]
            })
            
        # OpenAI
        if os.getenv("OPENAI_API_KEY") and ChatOpenAI:
            providers.append({
                "provider": "openai",
                "name": "OpenAI",
                "models": [
                    {"id": "gpt-4o", "name": "GPT-4o"},
                    {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo"}
                ]
            })
            
        # Groq
        if os.getenv("GROQ_API_KEY") and ChatGroq:
            providers.append({
                "provider": "groq",
                "name": "Groq",
                "models": [
                    {"id": "llama3-70b-8192", "name": "Llama 3 70B"},
                    {"id": "mixtral-8x7b-32768", "name": "Mixtral 8x7B"}
                ]
            })
            
        return providers

    def _create_llm(self, provider: str, model: str):
        """Create LLM instance based on provider and model."""
        if provider == "cerebras":
            if not os.getenv("CEREBRAS_API_KEY"):
                raise ValueError("CEREBRAS_API_KEY not found")
            return ChatCerebras(model=model, temperature=0.7)
            
        elif provider == "openai":
            if not ChatOpenAI:
                raise ValueError("langchain-openai not installed")
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY not found")
            return ChatOpenAI(model=model, temperature=0.7)
            
        elif provider == "groq":
            if not ChatGroq:
                raise ValueError("langchain-groq not installed")
            if not os.getenv("GROQ_API_KEY"):
                raise ValueError("GROQ_API_KEY not found")
            return ChatGroq(model=model, temperature=0.7)
            
        else:
            raise ValueError(f"Provider '{provider}' not supported or configured")

    def generate_itinerary(self, user_description: str, provider: str = "cerebras", model: str = "llama-3.3-70b") -> str:
        """
        Generate an initial itinerary based on user description.
        """
        llm = self._create_llm(provider, model)
        
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_description)
        ]
        
        response = llm.invoke(messages)
        return response.content
    
    def refine_itinerary(self, refinement_prompt: str, history: list, provider: str = "cerebras", model: str = "llama-3.3-70b") -> str:
        """
        Refine an itinerary based on user feedback with conversation history.
        """
        llm = self._create_llm(provider, model)
        
        messages = [SystemMessage(content=self.system_prompt)]
        
        # Add conversation history
        for item in history:
            if item["role"] == "user":
                messages.append(HumanMessage(content=item["content"]))
            else:
                messages.append(SystemMessage(content=item["content"]))
        
        # Add refinement prompt
        messages.append(HumanMessage(content=refinement_prompt))
        
        response = llm.invoke(messages)
        return response.content
    
    @staticmethod
    def save_to_file(filename: str, content: str) -> None:
        """Save itinerary to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Itinerary saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")
