#We got out of ai points!

#Running backup plan!

"""
Homemade ai:

Just an algorith that produces
sentences in a simple way based
on english syntaxis,

Requires language study to talk
consistently
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
  "No",
  "Hey!"
  "Ok",
  "Good night",
  "Perhaps"
  ":<",
  "Hmm",
  ":3-dots:",
  "Welp :3-dots:",
  "Nah"
  "Shh I'm trying to sleep"
  "Do it yourself",
  "Zzzzzz",
  "Maybe later",
  "Yup",
  "What?"
]

def r(max):
  return random.randint(0,max-1)

def unavailable():
  type = r(1)
  if type==0:
     return (
       f"{word[r(len(word))]} "
       f"{person[r(len(person))]} "
       f"{verb[r(len(verb))]}"
     )
  else:
     return word[r(len(word))]
