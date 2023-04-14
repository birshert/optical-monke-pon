from io import BytesIO

from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from model import Predictor

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Instrumentator().instrument(app).expose(app)

model = Predictor()


@app.get("/")
async def root():
    return {"message": "пон"}


@app.post("/predict")
async def classify_image(file: UploadFile = File(...)):
    pil_image = Image.open(BytesIO(await file.read()))
    return {"price": model.predict(pil_image)}
