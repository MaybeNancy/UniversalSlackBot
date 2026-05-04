"""
Any code related to validate
any json
"""
from jsonschema import validate

schema = {
  
}

def checkjson(json):
  try: validate(json, schema)
      return true
  except: 
      return false
