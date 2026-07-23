"""
AI billing considerations:

*Prefer CPU models for development, 
batch small requests, and set conservative
parameters (max_tokens, shorter prompts).

*Use small models for prototyping and only
switch to large/GPU models when necessary.

*Monitor usage in the billing/usage dashboard
and set org spending limits if available.

@@@@@@@@@Hugging Face (Monthly credits), like railway

Hub APIs -> 1k requests
Resolvers -> 5k requests
Pages -> 200 requests

Rate limits are applied over 5-minute intervals. 

@@@@@@@@@Open Router (Daily credits, priotize first)

50 -> requests per day
20 -> requests per minute
"""
import asyncio
from ..globals import r_hug_token, r_or_token

from huggingface_hub import InferenceClient
from openai import OpenAI

model = "deepseek-ai/DeepSeek-V4-Pro:novita"

def message(prompt):
    default=[
        {
            "role": "user", 
            "content": prompt
        }
    ]
    return default

def weekly_ai(prompt):
    hf_client = InferenceClient(
        token=r_hug_token(),
        timeout=30,
        model=model
    )

    try:
        response = hf_client.chat_completion(
            message(prompt),
            max_tokens=100,
            temperature=1
        )
        
        return response.choices[0].message.content
    except:
        print("an error ocurred in hugging face!")

    return "No AI :<, Sleeping... :nancy-sleep:"
  
def daily_ai(prompt):
    or_client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=r_or_token()
    )

    try:
      response = or_client.chat.completions.create(
        model="openrouter/free",
        message(prompt),
        extra_body={
            "reasoning":{
               "enabled":True
            }
         }
      )
      return response.choices[0].message
    except:
        print("ai error from open router!")
        
    return weekly_ai(prompt)

def call_ai(prompt):
  return daily_ai(prompt)
