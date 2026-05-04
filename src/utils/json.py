"""
Any code related to validate
any json
"""
from jsonschema import validate

schema = {
  "type": "object",
  "properties":{
     "type": {"type": "string"},
     "token": {"type": "string"},
     "team_id": {"type": "string"},
     "api_app_id":{"type": "string"},
     "event": {"type": "object"}
  },
  "required": ["type","token","team_id","api_app_id","event"]
}

def checkjson(data):
  try: 
    validate(instance=data,schema=schema)
  except ValidationError as e: 
      errortxt = "Incorrect Json, " + str(e.message)
      raise HTTPException(status_code=400, detail=errortxt)
