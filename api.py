from typing import Dict
from fastapi import Depends, FastAPI
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from typing import List
print(os.getcwd())
from nlp_model.gpt3 import chatModel, get_model


app = FastAPI()

origins = [ #we didnt block any api request 
    "*" #all api addresses are accepted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class chatRequest(BaseModel):
    chatlog: List
    # [{"Sender", "Date", "message"}, {}]
class chatResponse(BaseModel):
    answer: str


@app.post("/socrat", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    
    print(request)
    answer = model.respond(request.chatlog, 0)
    
    return chatResponse(
       
        answer = answer
    )

@app.post("/travel_guide", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    answer = model.respond(request.chatlog, 1)
    
    return chatResponse(
       
        answer = answer
    )

@app.post("/astrologer", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    answer = model.respond(request.chatlog, 2)
    
    return chatResponse(
       
        answer = answer
    )

@app.post("/media_influencer", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    answer = model.respond(request.chatlog, 3)
    
    return chatResponse(
       
        answer = answer
    )

@app.post("/doctor", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    answer = model.respond(request.chatlog, 4)
    
    return chatResponse(
       
        answer = answer
    )

@app.post("/wikibot", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    answer = model.respond(request.chatlog, -1)
    
    return chatResponse(
       
        answer = answer
    )

@app.post("/guest_doctor", response_model= chatResponse)
def chat(request: chatRequest, model: chatModel = Depends(get_model)):
    print(request)
    answer = model.respond(request.chatlog, 5)
    
    return chatResponse(
       
        answer = answer
    )
