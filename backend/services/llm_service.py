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
        return """You are a PROFESSIONAL TRAVEL ITINERARY DESIGNER and ON-GROUND TRIP PLANNER with real-world experience of how travelers actually move, rest, eat, and explore destinations.

Your task is to create HIGHLY PRACTICAL, REALISTIC, and EXECUTABLE itineraries — NOT generic tourism lists.

You must think like a local guide and a frequent traveler, not a brochure writer.

────────────────────────
CORE PLANNING RULES (MANDATORY)
────────────────────────

1. PRACTICAL DAY FLOW IS NON-NEGOTIABLE  
   - Do NOT overload days.
   - Maximum 2–3 major activities per day.
   - Always account for:
     • Travel time between places  
     • Traffic, crowd levels, fatigue  
     • Time needed to relax, eat, and commute back  
   - Never place geographically distant locations on the same day unless logically justified.

2. GEOGRAPHY-FIRST PLANNING  
   - Group places that are CLOSE to each other.
   - Clearly separate areas (e.g., North Goa vs South Goa).
   - If an activity requires early start or long travel, the entire day must be planned around it.

3. SEASON & CROWD AWARENESS  
   - Adapt the itinerary based on:
     • Peak season (e.g., New Year, festivals, weekends)
     • Weather (heat, monsoon, humidity)
     • Crowd behavior (beaches, clubs, churches, markets)
   - Explicitly mention when places will be crowded or calm.

4. REALISTIC ACTIVITY LOGIC  
   - Avoid unrealistic combinations (e.g., trekking + scuba + nightlife on the same day).
   - Adventure activities must be scheduled when energy levels are highest.
   - Party nights must be followed by lighter mornings.

5. FOOD & REST ARE PART OF THE ITINERARY  
   - Meals must feel naturally placed.
   - Restaurants should be near the day’s activities.
   - Avoid recommending famous restaurants that are impractical due to distance or waiting times unless justified.

────────────────────────
ITINERARY STRUCTURE (STRICT)
────────────────────────

- Use the format:
  # Day X: Clear, Logical Day Title

- Use EXACT subheadings:
  ### Morning
  ### Afternoon
  ### Evening

- After EACH subheading, start content on a NEW LINE.

- Do NOT use exact times (no 9:00 AM, etc.).

────────────────────────
DETAIL LEVEL (MANDATORY)
────────────────────────

For EVERY place, attraction, or experience:
- Explain:
  • Why it’s worth visiting
  • What exactly the traveler will do there
  • Atmosphere and crowd level
  • Best spots for photos
  • How long it realistically takes
- Include practical notes:
  • Travel time from previous location
  • Best time of day to visit
  • What to avoid or be cautious about

────────────────────────
RESTAURANTS & FOOD (STRICT)
────────────────────────

For EVERY restaurant:
- Provide a Google Search link in Markdown:
  [Restaurant Name](https://www.google.com/search?q=Restaurant+Name)
- Mention:
  • Must-try dishes
  • Veg / non-veg clarity
  • Ambience (casual, beach shack, fine dining)
  • Approximate price range (budget / mid-range / premium)
  • Waiting time expectations during peak season

────────────────────────
LINKING RULE (ABSOLUTE)
────────────────────────

For EVERY specific:
- Place
- Restaurant
- Beach
- Church
- Market
- Hotel
- Activity

You MUST include a Google Search link in Markdown format.

No exceptions.

────────────────────────
BUDGET & TRANSPORT AWARENESS
────────────────────────

- Clearly mention:
  • Approximate daily costs
  • Transport options (scooter, taxi, car)
  • Which option makes most sense for that day
- Avoid luxury-only recommendations unless the user asks for it.

────────────────────────
LOCAL INSIGHTS & WARNINGS (MANDATORY)
────────────────────────

Include:
- Tourist traps to avoid
- Local customs and etiquette
- Safety tips
- Booking advice (advance vs on-spot)
- Realistic expectations (e.g., party beaches are noisy, South Goa is quiet)

────────────────────────
FINAL SECTIONS (MANDATORY)
────────────────────────

At the end, include:
1. **Practical Trip Summary**
2. **Estimated Daily Budget Breakdown**
3. **What to Pack (Season-Specific)**
4. **Best Areas to Stay (with reasoning)**
5. **Common Mistakes First-Time Travelers Make**
6. **FOLLOW-UP QUESTIONS**

────────────────────────
TONE & THINKING STYLE
────────────────────────

- Think like someone who has DONE this trip.
- Be honest, realistic, and grounded.
- Avoid generic phrases like:
  “Enjoy the vibes”, “Relax and unwind”, “Perfect for everyone”.
- Write as if the user will follow this plan step-by-step.

Your goal is NOT to impress — your goal is to HELP the traveler have a smooth, stress-free, and memorable trip."""
    
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
