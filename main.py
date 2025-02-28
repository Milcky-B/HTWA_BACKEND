from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

URL="https://api.mymemory.translated.net/get"


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/translate/")
async def translate_text(text: str, lang: str):
    params = {
        "q": text,
        "langpair": f"en|{lang}",
    }

    response = requests.get(URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error calling MyMemory API")

    data = response.json()
    if "responseData" not in data or "translatedText" not in data["responseData"]:
        raise HTTPException(status_code=500, detail="Invalid response from MyMemory API")

    translated_text = data["responseData"]["translatedText"]
    return {"translated_text": translated_text}

