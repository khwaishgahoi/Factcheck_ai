from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_claims(text):

    prompt = f"""
Extract ONLY factual and objectively verifiable claims.

DO NOT extract:
- opinions
- predictions
- motivational statements
- vague business advice
- subjective sentences

GOOD examples:
- Google was founded in 1998
- Eiffel Tower is in Paris

BAD examples:
- Innovation is important
- AI will change the world

Return ONLY claims.
One claim per line.

TEXT:
{text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response.choices[0].message.content

    claims = output.split("\n")

    cleaned_claims = [
        claim.strip("- ").strip()
        for claim in claims
        if claim.strip()
    ]

    return cleaned_claims