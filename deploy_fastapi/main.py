from io import BytesIO

from PIL import Image
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
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
    try:
        price = model.predict(pil_image)
    except:
        price = 3750

    return {"price": price}


@app.post("/variate")
async def variate_image(file: UploadFile = File(...)):
    pil_image = Image.open(BytesIO(await file.read())).convert("RGB")

    images = variation.predict(pil_image)

    result = Image.new('RGB', (512, 512 * len(images)))

    for i, image in enumerate(images):
        result.paste(image, (0, 512 * i))

    result.save("tmp.png")

    return FileResponse("tmp.png")
