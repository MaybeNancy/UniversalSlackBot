"""
Any code related to validate
any json
"""
from jsonschema import validate

schema = {
  "type": "object"
  "properties":{
     "type": {"type": "string"},
     "token": {"type": "string"},
     "team_id": {"type": "string"},
     "api_app_id":{"type": "string"},
     "event": {"type": "object"}
  },
  "required": ["type","token","team_id","api_app_id","event"]
}

def checkjson(json):
  try: 
    validate(instance=json,schema=schema)
  except: 
      raise HTTPException(status_code=401, detail="incorrect json")
