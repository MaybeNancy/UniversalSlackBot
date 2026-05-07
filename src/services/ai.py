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
from ..globals import r_hug_token

from huggingface_hub import InferenceClient

model = "meta-llama/Meta-Llama-3-8B-Instruct"

def call_ai(prompt):
  hf_client = InferenceClient(
    token=r_hug_token(),
    timeout=30,
    model=model
  )

  messages=[
    {
      "role": "user", 
     "content": prompt
    }
  ]

  response = hf_client.chat_completion(
    messages,
    max_tokens=100,
    temperature=1.125
  )

  txt = response.choices[0].message.content
  
  return txt
