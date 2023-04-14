import io
from io import BytesIO

from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from prometheus_fastapi_instrumentator import Instrumentator

from model import Predictor, ImageVariation

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
variation = ImageVariation()


@app.get("/")
async def root():
    return {"message": "пон"}


@app.post("/predict")
async def classify_image(file: UploadFile = File(...)):
    pil_image = Image.open(BytesIO(await file.read())).convert("RGB")
    return {"price": model.predict(pil_image)}


@app.post("/variate")
async def variate_image(file: UploadFile = File(...)):
    pil_image = Image.open(BytesIO(await file.read())).convert("RGB")

    images = variation.predict(pil_image)

    def generate():
        for image in images:
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            yield img_byte_arr.getvalue()

    headers = {"Content-Disposition": "attachment; filename=images.zip"}
    return StreamingResponse(generate(), headers=headers, media_type="application/zip")
