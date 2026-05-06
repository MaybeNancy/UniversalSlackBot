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

model = "google/gemma-2-2b-it"
url = f"https://api-inference.huggingface.co/models/{model}"

async def call_ai(prompt):
  hf_client = InferenceClient(token=r_hug_token())
  client = return_client()

  response = hf_client.text_generation(
    prompt=prompt,
    model=model,
    max_new_tokens=100,
    temperature=0.7
  )

  print(response)
  return response
