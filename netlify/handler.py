# netlify/handler.py
import base64
from io import BytesIO
from werkzeug.wrappers import Response
from werkzeug.test import EnvironBuilder
from main import app   # import your Flask app

def handler(event, context):
    # ---------- 1️⃣ Build the WSGI environ ----------
    # Netlify may give the body as a string (plain) or base64‑encoded.
    raw_body = event.get("body", "")
    if event.get("isBase64Encoded"):
        raw_body = base64.b64decode(raw_body)

    # Build the environ; we feed the raw bytes directly.
    builder = EnvironBuilder(
        method=event.get("httpMethod", "GET"),
        path=event.get("path", "/"),
        query_string=event.get("queryStringParameters", {}),
        headers=event.get("headers", {}),
        data=raw_body,                     # <-- raw bytes, not a string
        environ_base={"wsgi.input_terminated": True},
    )
    env = builder.get_environ()

    # ---------- 2️⃣ Run the Flask app ----------
    resp = Response.from_app(app, env)

    # ---------- 3️⃣ Return Netlify‑compatible dict ----------
    return {
        "statusCode": resp.status_code,
        "headers": dict(resp.headers),
        "body": resp.get_data(as_text=True),
        "isBase64Encoded": False,
    }
