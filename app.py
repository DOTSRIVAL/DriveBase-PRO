import os
import time
import json
import httpx
from pathlib import Path
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# ── CREDENTIALS (set these in HF Secrets or Render/Railway env vars) ─────────
CLIENT_ID     = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["REFRESH_TOKEN"]

# ── TOKEN CACHE ───────────────────────────────────────────────────────────────
_token_cache = {"token": None, "expiry": 0}

async def get_access_token() -> str:
    if _token_cache["token"] and time.time() < _token_cache["expiry"]:
        return _token_cache["token"]
    async with httpx.AsyncClient() as client:
        r = await client.post("https://oauth2.googleapis.com/token", data={
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type":    "refresh_token",
        })
        d = r.json()
        if "error" in d:
            raise Exception(d.get("error_description", d["error"]))
        _token_cache["token"]  = d["access_token"]
        _token_cache["expiry"] = time.time() + d.get("expires_in", 3600) - 60
        print(f"[TOKEN] Refreshed OK")
        return _token_cache["token"]

CORS_HEADERS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
}

# ── /token ────────────────────────────────────────────────────────────────────
@app.get("/token")
async def token_endpoint():
    try:
        tok = await get_access_token()
        return JSONResponse({"access_token": tok}, headers=CORS_HEADERS)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500, headers=CORS_HEADERS)

# ── /api/* (proxy to Google Drive API) ───────────────────────────────────────
@app.get("/api/{path:path}")
async def api_proxy(path: str, request: Request):
    try:
        token   = await get_access_token()
        api_url = f"https://www.googleapis.com/{path}"
        if request.query_params:
            api_url += "?" + str(request.query_params)
        async with httpx.AsyncClient() as client:
            r = await client.get(api_url, headers={"Authorization": f"Bearer {token}"})
        return Response(
            content=r.content,
            status_code=r.status_code,
            media_type=r.headers.get("content-type", "application/json"),
            headers=CORS_HEADERS,
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500, headers=CORS_HEADERS)

# ── /stream & /download (proxy file from Drive) ───────────────────────────────
@app.get("/stream")
@app.get("/download")
async def stream_file(request: Request, id: str, name: str = "file"):
    is_download = request.url.path == "/download"
    try:
        token   = await get_access_token()
        api_url = f"https://www.googleapis.com/drive/v3/files/{id}?alt=media"
        headers = {"Authorization": f"Bearer {token}"}
        range_h = request.headers.get("range")
        if range_h:
            headers["Range"] = range_h

        async def stream_gen():
            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream("GET", api_url, headers=headers) as r:
                    async for chunk in r.aiter_bytes(65536):
                        yield chunk

        resp_headers = {**CORS_HEADERS, "Accept-Ranges": "bytes"}
        if is_download:
            resp_headers["Content-Disposition"] = f'attachment; filename="{name}"'

        return StreamingResponse(
            stream_gen(),
            status_code=206 if range_h else 200,
            headers=resp_headers,
            media_type="application/octet-stream",
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ── / → serve preview.html ────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
@app.get("/preview.html", response_class=HTMLResponse)
async def index():
    html = Path("preview.html").read_text(encoding="utf-8")
    return HTMLResponse(html)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, reload=False)
