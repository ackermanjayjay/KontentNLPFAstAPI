from typing import Union

from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from preprocessing import preprocessing_text

from loadedModel import Prediction

from database import InsertRecord, allTable

from fastapi.templating import Jinja2Templates

from pydantic import BaseModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to limit access to specific origins if needed
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
        "XMLHttpRequest",
    ],  # Adjust the HTTP methods as needed
    allow_headers=["*"],  # Allow all headers, adjust according to your requirements
)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def read_root():
    fetching = allTable()
    if not fetching:
        return {"Message": "Data not connected or web service turn of", "Response": 400}

    return {"Message": fetching, "Response": 200}


# @app.get("/prediction/{query}")
# def classification(query: str, q: str):
#     simpan = []
#     simpan.append({"Text": q, "Result": preprocessing_text(Prediction(q))})
#     return {"Message": "success", "Response": 200, "Result": simpan}


@app.get("/app", response_class=HTMLResponse )
async def read_item(request: Request):
    fetching = allTable()
    return templates.TemplateResponse(
        "index.html", {"message": fetching, "response": 200, "request": request}
    )


@app.post("/add/prediction/")
def addUsers(query: str = Form("query")):
    hasil = preprocessing_text(Prediction(query))
    InsertRecord(query, prediction=hasil)
    return RedirectResponse(url="http://127.0.0.1:8000/app",status_code=200)

