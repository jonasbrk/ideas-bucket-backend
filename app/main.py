from typing import List
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from tempfile import NamedTemporaryFile
import whisper

app = FastAPI()
model = whisper.load_model("base")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/transcribe")
async def handler(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="only one file is allowed")

    results = []

    for file in files:
        with NamedTemporaryFile(delete=True) as temp:
            with open(temp.name, "wb") as temp_file:
                temp_file.write(file.file.read())

            result = model.transcribe(temp.name)

            results.append(
                {
                    "filename": file.filename,
                    "transcript": result["text"]
                }
            )

    return JSONResponse({
        "results": results
    })
