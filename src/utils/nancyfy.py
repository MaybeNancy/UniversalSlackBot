"""
Tool made specifically
to add or react nancy emojis
to any text given
based on the tone of the
message, or just to replace
symbols in a funny way :>
"""

import random

nancymojis = [
  "nancy-wink",
  "nancy-cheerful",
  "b-nancy-impact",
  "bandwidth-nancy",
  "nancy-dance1",
  "nancy-dance2",
  "nancy-flirt",
  "nancy-smile",
  "nancy-sleep"
]

def nancyfy(text):
  return text+" :nancy-wink:"

def nancymoji():
  return nancymojis[random.randint(0,len(nancymojis))]
