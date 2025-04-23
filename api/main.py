from fastapi import FastAPI,BackgroundTasks,HTTPException,Request,Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .schema import TaskResponse,TranslationRequest,TranslationStatus
import query 
import models
from . import utils
from .db import get_db,engine
models.Base.metadata.create_all(bind=engine)

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

@app.post("/translate", response_model=TaskResponse)
async def translate(request: TranslationRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    task = query.create_translation_task(db, request.text, request.languages)
    utils.perform_translation(task.id, request.text, request.languages, db)
    return {"task_id": task.id}


    
@app.post("/translate/{task_id}", response_model=TranslationStatus)
async def get_translate(task_id: int,db:Session=Depends(get_db)):
    task=query.get_translation_task(db,task_id)
    if not task:
        raise HTTPException(status_code=404, detail="tasks not found")
    return {
    "task_id": task.id,
    "status": task.status,
    "translations": task.translations
}



@app.post("/translate/content/{task_id}", response_model=TranslationStatus)
async def get_translate_content(task_id: int,db:Session=Depends(get_db)):
    task=query.get_translation_task(db,task_id)
    if not task:
        raise HTTPException(status_code=404, detail="tasks not found")
    return task