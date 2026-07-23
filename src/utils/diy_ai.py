#We got out of ai points!

#Running backup plan!

"""
Homemade ai:

Just an algorith that produces
sentences in a simple way based
on english syntaxis
"""

import random

person = [
  "I'm",
  "I am",
  "me"
]

verb = [
  "sleeping",
  "on my bed",
  "on vacations",
  "out",
  "busy",
  "dreaming",
  "at mcdonalds",
  "in brazil",
  "outa here"
]

word = [
  "no",
  "hey!"
  "ok",
  "good night",
  ""
  ":<",
  "hmm",
  "3-dots",
  "welp :3-dots",
  "nah"
  "shh I'm trying to sleep"
  "Do it yourself",
  "zzzzzz",
  "maybe later",
  "yup"
]

def r(max):
  return random.rand(0,max)

def unavailable():
  type = r(1)
  reply = ""
  if type==0:
     reply += word[r(len(word))] + " "
     reply += person[r(len(person))] + " "
     reply += verb[r(len(verb))]
     return reply
  else:
     return word[r(len(word))]
