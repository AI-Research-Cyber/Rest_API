from typing import Dict
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import List
print(os.getcwd())
from nlp_model.gpt3 import chatModel, get_model
from nlp_model.blender_chat import chatModelBlender, get_modelB
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class chatRequest(BaseModel):
    prompt: str

class chatRequestBlender(BaseModel):
    user_input: str
    conversation: list

class chatResponseB(BaseModel):
    answer: str

class chatResponse(BaseModel):
    chat_log: str
    answer: str

@app.post("/chat", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    chat_log, answer = model.respond(request.prompt)
    
    return chatResponse(
       chat_log = chat_log,
        answer = answer
    )


@app.post("/chat_blender", response_model= chatResponseB)
def chatB(request: chatRequestBlender, model: chatModelBlender = Depends(get_modelB)):
    print(request)
    
    answer = model.respond(request.user_input, request.conversation)
    
    return chatResponseB(
       
        answer = answer
    )
