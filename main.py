from dotenv import load_dotenv
load_dotenv()
import os
from langchain_cerebras import ChatCerebras
from langchain_core.messages import HumanMessage, SystemMessage


def create_holiday_planner():
    """Initialize the Cerebras chat model for holiday planning."""
    llm = ChatCerebras(
        model="llama-3.3-70b",
        temperature=0.7,    
    )
    return llm


def create_system_prompt():
    """Create a specialized system prompt for holiday planning."""
    return """You are an expert travel and holiday planner with extensive knowledge of destinations around the world. 
Your role is to create detailed, personalized itineraries based on user preferences.

When creating an itinerary, you should:
1. Provide day-by-day breakdown of activities
2. Include specific recommendations for restaurants, attractions, and experiences
3. Give practical tips about transportation, best times to visit, and local customs
4. Consider budget constraints in your recommendations
5. Balance various interests (adventure, culture, relaxation, food, etc.)
6. Include estimated costs where relevant
7. Suggest packing tips and weather considerations
8. Provide local insights and hidden gems

Format your response clearly with sections for each day, and include a summary section with practical tips.

IMPORTANT: At the end of your itinerary, add a section called "FOLLOW-UP QUESTIONS" with 3-4 specific questions that would help refine the itinerary further. Format these questions clearly for user input."""


def generate_itinerary(llm, user_prompt, conversation_history):
    """Generate itinerary with streaming output."""
    
    system_message = SystemMessage(content=create_system_prompt())
    
    # Build messages with conversation history
    messages = [system_message] + conversation_history + [HumanMessage(content=user_prompt)]
    
    print("\n" + "="*60)
    print("✈️  GENERATING YOUR PERSONALIZED ITINERARY...")
    print("="*60 + "\n")
    
    full_response = ""
    
    # Stream the response
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    
    print("\n\n" + "="*60)
    print("✅ Itinerary Generation Complete!")
    print("="*60)
    
    return full_response


def refine_itinerary(llm, refinement_prompt, conversation_history):
    """Refine the itinerary based on user feedback."""
    
    system_message = SystemMessage(content=create_system_prompt())
    
    # Build messages with conversation history
    messages = [system_message] + conversation_history + [HumanMessage(content=refinement_prompt)]
    
    print("\n" + "="*60)
    print("🔄 REFINING YOUR ITINERARY...")
    print("="*60 + "\n")
    
    full_response = ""
    
    # Stream the response
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    
    print("\n\n" + "="*60)
    print("✅ Itinerary Refinement Complete!")
    print("="*60)
    
    return full_response


def save_itinerary(filename, itinerary_content):
    """Save the generated itinerary to a file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(itinerary_content)
        print(f"\n💾 Itinerary saved to: {filename}")
    except Exception as e:
        print(f"\n⚠️  Could not save file: {e}")


def get_safe_filename(user_input):
    """Generate a safe filename from user input."""
    # Take first 30 chars and replace spaces with underscores
    safe_name = user_input[:30].replace(" ", "_").replace("/", "_").replace("\\", "_")
    return f"itinerary_{safe_name}.txt"


def main():
    """Main function to run the holiday planner chatbot."""
    try:
        # Check API key
        if not os.getenv("CEREBRAS_API_KEY"):
            print("❌ Error: CEREBRAS_API_KEY not found in environment variables")
            print("Please set your Cerebras API key in the .env file")
            return
        
        # Initialize the LLM
        llm = create_holiday_planner()
        
        # Display welcome message
        print("\n" + "="*60)
        print("🌍 WELCOME TO AI HOLIDAY PLANNER 🌍")
        print("="*60)
        print("\n✨ Tell me about your dream holiday!\n")
        print("Describe your ideal trip, including details like:")
        print("  • Destination or type of trip")
        print("  • Duration")
        print("  • Budget")
        print("  • Interests and activities")
        print("  • Any specific preferences\n")
        
        # Conversation history for multi-turn context
        conversation_history = []
        itinerary_filename = None
        
        # First prompt from user
        user_prompt = input("📝 Describe your ideal holiday: ").strip()
        if not user_prompt:
            print("❌ Please provide holiday details to continue.")
            return
        
        # Generate initial itinerary
        response = generate_itinerary(llm, user_prompt, conversation_history)
        
        # Add to conversation history
        conversation_history.append(HumanMessage(content=user_prompt))
        conversation_history.append(SystemMessage(content=response))
        
        # Generate filename from user input
        itinerary_filename = get_safe_filename(user_prompt)
        
        # Refinement loop
        while True:
            print("\n" + "-"*60)
            print("What would you like to do?")
            print("  1. Answer follow-up questions to refine")
            print("  2. Save itinerary")
            print("  3. Start over")
            print("  4. Exit")
            print("-"*60)
            
            choice = input("\nYour choice (1-4): ").strip()
            
            if choice == "1":
                refinement_input = input("\n💬 Your response or additional requirements: ").strip()
                if refinement_input:
                    # Create refinement prompt that maintains context
                    refinement_prompt = f"Based on my previous request and your itinerary, here's my feedback/answer: {refinement_input}\n\nPlease refine the itinerary accordingly and include updated FOLLOW-UP QUESTIONS at the end."
                    
                    response = refine_itinerary(llm, refinement_prompt, conversation_history)
                    
                    # Add to conversation history
                    conversation_history.append(HumanMessage(content=refinement_prompt))
                    conversation_history.append(SystemMessage(content=response))
                else:
                    print("⚠️  Please provide feedback or answers to refine the itinerary.")
            
            elif choice == "2":
                save_itinerary(itinerary_filename, response)
            
            elif choice == "3":
                print("\n🔄 Starting over...\n")
                conversation_history = []
                
                user_prompt = input("📝 Describe your ideal holiday: ").strip()
                if not user_prompt:
                    print("❌ Please provide holiday details to continue.")
                    continue
                
                response = generate_itinerary(llm, user_prompt, conversation_history)
                conversation_history.append(HumanMessage(content=user_prompt))
                conversation_history.append(SystemMessage(content=response))
                itinerary_filename = get_safe_filename(user_prompt)
            
            elif choice == "4":
                print("\n🎉 Thank you for using AI Holiday Planner!")
                break
            
            else:
                print("⚠️  Invalid choice. Please select 1, 2, 3, or 4.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please ensure your Cerebras API key is valid and you have internet connectivity.")


if __name__ == "__main__":
    main()