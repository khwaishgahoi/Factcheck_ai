from dotenv import load_dotenv
import os

load_dotenv()

gemini_key = os.getenv("GEMINI_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")

print("Gemini Key:", gemini_key[:10])
print("Tavily Key:", tavily_key[:10])