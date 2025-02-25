from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from inference import classify_image




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/classify")
async def classify(file: UploadFile = File(...)):
    result = classify_image(file)
    return result
