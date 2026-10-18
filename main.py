import jwt, uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

ISS = "https://idp.exam.local"
AUD = "tds-rjwm4q39.apps.exam.local"
EMAIL = "24f3003515@ds.study.iitm.ac.in"

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2okOHspNjgA+2rTLbeuYcxiP/hG8C6Sb9iwg3yiLAA4HCnpITcbWCSelbvbYGuc3EbNy4xFyf5Cbj5DHJMIDEkryOgyd2giIIIBOUBj8S63uGcnRpOBh9NFatfNwheKuzsPuVNldu6A9cNteNpXcWyJjG2axVfmq7i6SuKr1JoWYG7xTTAvKPujSl4OtsQfO3h5NepzdfXpr28oNnzfWed+zclR6BcmNNo/WVfJ4xyCLSf0BCOgdTgW6PdaChd1l9VDetJZVEgC5tkyvXsfISI6iyrYbKR0NEBSqq4XkadEjsCs4F1RncsS4LlgniT7GlkL9Mce3b0wGLs9/7ZIXdQIDAQAB
-----END PUBLIC KEY-----"""


@app.get("/")
async def root():
    return {"status": "ok"}


@app.post("/verify")
async def verify(request: Request):
    body = await request.json()
    token = body.get("token", "")
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"], issuer=ISS, audience=AUD)
    except jwt.ExpiredSignatureError:
        return JSONResponse(content={"valid": False}, status_code=401)
    except jwt.InvalidAudienceError:
        return JSONResponse(content={"valid": False}, status_code=401)
    except jwt.InvalidIssuerError:
        return JSONResponse(content={"valid": False}, status_code=401)
    except Exception:
        return JSONResponse(content={"valid": False}, status_code=401)

    return JSONResponse(content={
        "valid": True,
        "email": payload.get("email", EMAIL),
        "sub": payload.get("sub", ""),
        "aud": payload.get("aud", ""),
    }, headers={"X-Request-ID": str(uuid.uuid4())})
