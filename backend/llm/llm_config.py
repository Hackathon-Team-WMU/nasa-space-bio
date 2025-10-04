import os
from openai import OpenAI

client = OpenAI(
    base_url="https://api.studio.nebius.com/v1/",
    api_key=os.environ.get("NEBIUS_API_KEY")
)

response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3-0324-fast",
    max_tokens=512,
    temperature=0.3,
    top_p=0.95,
    messages=[]
)

print(response.to_json())
