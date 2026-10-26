"""
server.py -- FastAPI backend.

Start with:  python app/backend/server.py
Then open:   http://localhost:8000

Build the frontend first:
    cd app/frontend && npm run build
"""
import io, pathlib, sys

HERE = pathlib.Path(__file__).parent      # app/backend/
ROOT = HERE.parent.parent                 # repo root

sys.path.insert(0, str(HERE))
from model import load_model, predict as _predict

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image

app = FastAPI(title="AI Detector", docs_url="/api/docs")

# Allow the Vite dev server during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once at startup
WEIGHTS = str(ROOT / "models" / "resnet50_finetuned_best.pth")
print(f"Loading model from {WEIGHTS} ...")
MODEL = load_model(WEIGHTS)
print("Model ready.")

MAX_BYTES = 10 * 1024 * 1024
ALLOWED   = {"image/jpeg", "image/png", "image/webp"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED:
        raise HTTPException(415,
            f"Unsupported type. Send jpg, png, or webp.")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File too large. Maximum is 10 MB.")
    try:
        image = Image.open(io.BytesIO(data))
    except Exception:
        raise HTTPException(422, "Could not decode the image.")
    return _predict(MODEL, image)


# Sample images
SAMPLES_DIR = ROOT / "samples"
SAMPLES_DIR.mkdir(exist_ok=True)

@app.get("/samples/{name}")
def get_sample(name: str):
    if "/" in name or ".." in name:
        raise HTTPException(400, "Invalid filename.")
    path = SAMPLES_DIR / name
    if not path.exists():
        raise HTTPException(404, "Sample not found.")
    return FileResponse(str(path))


# Serve built frontend (catch-all must come last)
STATIC = HERE / "static"
if STATIC.exists():
    assets = STATIC / "assets"
    if assets.exists():
        app.mount("/assets", StaticFiles(directory=str(assets)), name="assets")

    @app.get("/{full_path:path}")
    def spa(full_path: str):
        return FileResponse(str(STATIC / "index.html"))
else:
    @app.get("/")
    def no_build():
        return {"message": "Run: cd app/frontend && npm run build"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=False)
