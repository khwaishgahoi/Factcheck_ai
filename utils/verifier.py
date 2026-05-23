from tavily import TavilyClient
from groq import Groq
from dotenv import load_dotenv
import os
import json
import time

load_dotenv()

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def verify_claim(claim):

    try:

        # Smaller search
        search_result = tavily.search(
            query=claim,
            search_depth="basic",
            max_results=2
        )

        evidence = ""

        for result in search_result["results"]:

            # Reduce token usage
            content = result["content"][:500]

            evidence += content + "\n"

        prompt = f"""
        Verify this claim using web evidence.

        Claim:
        {claim}

        Evidence:
        {evidence}

        Return ONLY valid JSON:

        {{
          "verdict": "",
          "correct_info": "",
          "explanation": ""
        }}
        """

        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=150
        )

        output = response.choices[0].message.content

        try:
            return json.loads(output)

        except:
            return {
                "verdict": "Error",
                "correct_info": "Parsing failed",
                "explanation": output
            }

    except Exception as e:

        return {
            "verdict": "Rate Limited",
            "correct_info": "Try again in a few seconds",
            "explanation": str(e)
        }