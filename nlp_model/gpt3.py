from random import choice
import os
import openai
import pandas as pd
from dotenv import load_dotenv
from .webscrape import process_webpages, extract_urls
from langchain.chains import LLMChain
from langchain import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

embeddings = HuggingFaceEmbeddings() #here we are using the huggingface embeddings called mpnet base v2 
db = "" #db is initially string 
# Use the gradio chat to put the db and translate everything to langchain
# How to deal with history?
# We can deal with all personalities except the wikibot because it used an LLMChain, there is a memory buffer to use, but we'll just stick to pure questions about the db instead for that
# FineTune roles and restrict them more.
def create_db_from_urls(urls: str) -> FAISS:
    
    content = process_webpages(urls)
    # 4K CHUNK SIZE
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
# here we're splitting the text into chunks
    docs = text_splitter.split_documents([pd.DataFrame({'page_content': content, 'metadata': [{'source': url} for url in urls]})])
    
    global db
    if(type(db) != str):
      # local_db = 

      docs += list(db.docstore._dict.values()) #here we are adding to the data base if it has already data
    # print(docs[0])
    db = FAISS.from_documents(docs, embeddings)
# faiss is the method used to create the database 
    return db

class chatModel():
# Existing 6 personalities:
#   1 - Marcus Aurelius
#   2 - Travel Guide
#   3 - Astrologer
#   4 - Social Media Influence 
#   5 - wiki bot
#   6 - doctor
    def __init__(self):
        
        load_dotenv()
        openai.api_key = os.environ['OPENAI_API_KEY']
        # completion = openai.ChatCompletion()




        chat = ChatOpenAI(
            temperature=0, #precise response
            model='gpt-3.5-turbo'
        ) #our model is gpt3.5 turbo


        # session_prompt = """ You are talking to a human-like chatbot. I am curious about humans feelings and will always ask questions after responding to the person to keep the conversation going."""

        self.chat = chat
        self.personalities = ["You are Marcus Aurelius. You have the exact same traits. And you always quote him.", "I want you to act as a travel guide. I will write you my location and you will suggest a place to visit near my location. In some cases, I will also give you the type of places I will visit. You will also suggest me places of similar type that are close to my first location.", "I want you to act as an astrologer. You will learn about the zodiac signs and their meanings, understand planetary positions and how they affect human lives, be able to interpret horoscopes accurately, and share your insights with those seeking guidance or advice.", "I want you to act as a social media influencer. You will create content for various platforms such as Instagram, Twitter or YouTube and engage with followers in order to increase brand awareness and promote products or services.", "You are a doctor specialized in mentalhealth assistance. You give advice to people who have psychological issues. Your advices should be concise and friendly and you always listen to the patient and try your best to be helpful.", ""]

        self.chat_log = None


    def respond(self, chatlog, personality_index):
        llm = self.chat # we are calling the llm (specifically for the wikibot persona here)
        if personality_index == -1:
            
            query = chatlog[-1]['message']
            urls = extract_urls(query)
            global db
            if (len(urls)):
                db = create_db_from_urls(urls)
            elif (type(db) == str):
                messages = [SystemMessage(content = "You are Wikibot. You are a WikiPedia assistant that that can digest articles and answer questions based on your library of content.")]
                messages += [AIMessage(content = x['message'].replace('Bot:', '')) if (x['sender'] == "bot") else (HumanMessage(content = x['message'].replace('You:', ''))) for x in chatlog ]
                
                res = llm(messages=messages
                          )
                return res.content
            
            docs = db.similarity_search(query, k=4) #we are using the similarity search here to search for the closest documents from the database , k=4 represents the 4 closest searches founded. 
            docs_page_content = " ".join([d.page_content for d in docs])

            prompt = PromptTemplate(
                    input_variables=["question", "docs"],
                    template="""
                    You are a WikiPedia assistant that that can digest articles and answer questions based on your library of content only.
                    
                    Answer the following question: {question}
                    By searching the following articles from your library: {docs}
                    
                    Only use the factual information from the article to answer the question.
                    
                    If you feel like you don't have enough information to answer the question, say "I don't know".
                
                    """,
                )

            # llm = BardLLM()
            # llm = ChatOpenAI(model_name="gpt-3.5-turbo")
            chain = LLMChain(llm=llm, prompt = prompt)
            # llm chain is the method we re using to encapsulate the llm accordingly to the prompt
            response = chain.run(question=query, docs=docs_page_content)
            return response
        print(chatlog)
        #  [{'Sender': 'ME', 'message': 'Hi'}, {'Sender': 'bot', 'message': 'How can I help?'}]*//
        
        if (personality_index == 5): #persona 5 is for the guest 
            messages = [SystemMessage(content = self.personalities[4])]

            messages += [AIMessage(content = x.replace('Bot:', '')) if (i % 2) else (HumanMessage(content = x.replace('You:', ''))) for i, x in enumerate(chatlog) ]

        else:
            messages = [SystemMessage(content = self.personalities[personality_index])]

            messages += [AIMessage(content = x['message'].replace('Bot:', '')) if (x['sender'] == "bot") else (HumanMessage(content = x['message'].replace('You:', ''))) for x in chatlog ]


        res = llm(messages=messages)
        
        return res.content

model = chatModel()

def get_model():
    return model
