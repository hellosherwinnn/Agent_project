import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLM_API_KEY")
base_url = os.getenv("LLM_BASE_URL")
model = os.getenv("LLM_MODEL_ID")

print(f"Testing with Model: {model}")
print(f"Base URL: {base_url}")
print(f"API Key (truncated): {api_key[:5]}...{api_key[-5:] if api_key else ''}")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "say hi"}],
        max_tokens=10
    )
    print("Success!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
