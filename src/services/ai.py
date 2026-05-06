"""
AI billing considerations:

@Monthly credits, like railway

*Prefer CPU models for development, 
batch small requests, and set conservative
parameters (max_tokens, shorter prompts).

*Use small models for prototyping and only
switch to large/GPU models when necessary.

*Monitor usage in the billing/usage dashboard
and set org spending limits if available.

Hub APIs -> 1k requests
Resolvers -> 5k requests
Pages -> 200 requests

Rate limits are applied over 5-minute intervals. 
"""
import asyncio
from ..globals import return_client, r_hug_token

from huggingface_hub import InferenceClient

token = r_hug_token()
model = "Qwen/Qwen3-0.6B"
url = f"https://api-inference.huggingface.co/models/{model}"

async def call_ai(prompt):
  
  client = return_client()

  headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
  }
  
  payload = {
    "inputs": prompt, 
    "parameters": 
        {
          "max_new_tokens": 150
        }
  }
  
  print(url)
  print(token) 

  resp = await client.post(url, headers=headers, json=payload)
  resp.raise_for_status()
  
  try:
      print(resp.json())
  except Exception:
            pass
  return resp.json()
