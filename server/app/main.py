from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException

from .config import JWT_SECRET
from .routers import auth, content, flashcards, progress

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not set. Add it to server/.env.")

app = FastAPI(title="DSA Study Lab API")


@app.exception_handler(HTTPException)
async def http_error(_request: Request, exc: HTTPException):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_error(_request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    field = ".".join(str(part) for part in first["loc"][1:]) or "request"
    return JSONResponse({"error": f"Invalid {field}: {first['msg']}"}, status_code=400)


@app.get("/api/health")
def health():
    return {"success": True, "message": "DSA Study Lab API is running!"}


app.include_router(auth.router)
app.include_router(content.router)
app.include_router(progress.router)
app.include_router(flashcards.router)

# In production, serve the built React app from the same server.
dist = Path(__file__).resolve().parents[2] / "dist"

if dist.exists():
    app.mount("/assets", StaticFiles(directory=dist / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str):
        if path.startswith("api/"):
            return JSONResponse({"error": "Not found."}, status_code=404)
        file = (dist / path).resolve()
        if path and file.is_relative_to(dist) and file.is_file():
            return FileResponse(file)
        return FileResponse(dist / "index.html")
