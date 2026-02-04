import json
from werkzeug.wrappers import Request, Response
from werkzeug.test import EnvironBuilder
from app import app  # the Flask instance from app.py

def handler(event, context):
    """
    Netlify Function entry point.
    `event` contains the HTTP request data.
    """
    # Build a WSGI environ from the Netlify event
    builder = EnvironBuilder(
        method=event.get("httpMethod", "GET"),
        path=event.get("path", "/"),
        query_string=event.get("queryStringParameters", {}),
        headers=event.get("headers", {}),
        data=event.get("body", ""),
        # Netlify may base64‑encode the body
        environ_base={"wsgi.input_terminated": True},
    )
    env = builder.get_environ()
    # If the body was base64‑encoded, decode it
    if event.get("isBase64Encoded"):
        env["wsgi.input"] = BytesIO(base64.b64decode(event["body"]))

    # Run the Flask app with the generated environ
    resp = Response.from_app(app, env)

    # Convert the Werkzeug response back to Netlify format
    return {
        "statusCode": resp.status_code,
        "headers": dict(resp.headers),
        "body": resp.get_data(as_text=True),
        "isBase64Encoded": False,
    }
