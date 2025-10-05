import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324-fast",
    max_tokens=512,
    temperature=0.3,
    top_p=0.95,
    messages=[
            {"role": "system", "content": "You are an AI assistant for NASA bioscience research."},
            {"role": "user", "content": "Summarize the goal of NASA’s bioscience research in space."}
        ]
)

print(response.choices[0].message.content)
