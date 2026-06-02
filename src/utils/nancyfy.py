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
  "nancy-sleep",
  "handdrawn-hearts",
  "handdrawn-flame",
  "handdrawn-star",
  "nancy-blah",
  "nancy-blush",
  "nancy-goof",
  "nancy-happy-face",
  "nancy-joy-tears",
  "nancy-love",
  "nancy-mad",
  "nancy-music",
  "nancy-naive",
  "nancy-navel",
  "nancy-smooch",
  "nancy-star-eyes",
  "nancy-surprised",
  "nancy-suspicious",
  "nancy-think",
  "nancy-think2",
  "nancy-tongue",
  "nancyception",
  "spark",
  "universal-s",
  "windy",
  "starry-night",
  "ring-signal",
  "scourge",
  "red-snake",
  "meowl"
]

def nancyfy(text):
  return text+" :nancy-wink:"

def nancymoji():
  return nancymojis[random.randint(0,len(nancymojis))]
