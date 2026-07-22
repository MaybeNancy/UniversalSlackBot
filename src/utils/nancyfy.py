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
  "nancy-frustration",
  "nancy-blah",
  "nancy-blush",
  "nancy-goof",
  "nancy-sad",
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
  "nancy-speechless",
  "nancy's-moneybag",
  "nancy-think",
  "nancy-think2",
  "nancy-tongue",
  "nancyception",
  "nancy-laugh",
  "nancy-ouch",
  "spark",
  "universal-s",
  "windy",
  "starry-night",
  "ring-signal",
  "scourge",
  "red-snake",
  "tracker",
  "meowl",
  "me-in-japan",
  "crying-peak-guy",
  "exclamation-mark",
  "intensity-sign"
  "handdrawn-hearts",
  "handdrawn-flame",
  "handdrawn-star",
  "cube",
  "silly-box",
  "samantha",
  "portal-spin"
]

def nancyfy(text):
  return text+" :nancy-wink:"

def nancymoji():
  return nancymojis[random.randint(0,len(nancymojis))]
