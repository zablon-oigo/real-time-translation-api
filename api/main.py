from fastapi import FastAPI,BackgroundTasks,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates


app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
templates=Jinja2Templates(directory="templates")
@app.get('/index', response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})