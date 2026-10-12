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

from ..globals import r_hug_client, r_or_client

def weekly_ai(info_table):
    hf_client = r_hug_client()

    try:
        response = hf_client.chat_completion(
            messages=info_table,
            max_tokens=100,
            temperature=1
        )
        
        return response
    except:
        print("an error ocurred in hugging face!")
        return False
    return False
  
def daily_ai(info_table):
    or_client = r_or_client()
    try:
      response = or_client.chat.completions.create(
        model="openrouter/free",
        messages=info_table,
        extra_body={
            "reasoning":{
               "enabled":True
            }
         }
      )
      return response
    except Exception as e:
        print("ai error from open router!",repr(e))
        return weekly_ai(info_table)
    return False

def call_ai(info_table):
  return daily_ai(info_table)
