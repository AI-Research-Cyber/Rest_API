from random import choice
import os
import openai

from dotenv import load_dotenv

class chatModel():
# Existing 4 personalities:
#   1 - Marcus Aurelius
#   2 - Travel Guide
#   3 - Astrologer
#   4 - Social Media Influence    
    def __init__(self):
        
        load_dotenv()
        openai.api_key = os.environ['OPENAI_KEY']
        completion = openai.ChatCompletion()


        session_prompt = """ You are talking to a human-like chatbot. I am curious about humans feelings and will always ask questions after responding to the person to keep the conversation going."""

        self.completion = completion
        self.personalities = ["You are Marcus Aurelius. You have the exact same traits. And you always quote him.", "I want you to act as a travel guide. I will write you my location and you will suggest a place to visit near my location. In some cases, I will also give you the type of places I will visit. You will also suggest me places of similar type that are close to my first location.", "I want you to act as an astrologer. You will learn about the zodiac signs and their meanings, understand planetary positions and how they affect human lives, be able to interpret horoscopes accurately, and share your insights with those seeking guidance or advice.", "I want you to act as a social media influencer. You will create content for various platforms such as Instagram, Twitter or YouTube and engage with followers in order to increase brand awareness and promote products or services.", "You are a doctor specialized in mentalhealth assistance. You give advice to people who have psychological issues. Your advices should be concise and friendly and you always listen to the patient and try your best to be helpful."]

        self.chat_log = None


    def respond(self, chatlog, personality_index):
        print(chatlog)
        #  [{'Sender': 'ME', 'message': 'Hi'}, {'Sender': 'bot', 'message': 'How can I help?'}]*//
        if personality_index == 5:
         messages = [{"role": "system", "content": self.personalities[4]}]

         messages += [{'role': 'assistant', 'content': x.replace('Bot:', '')} if (i % 2) else ({'role': 'user', 'content': x.replace('You:', '')}) for i, x in enumerate(chatlog) ]

        else:
            messages = [{"role": "system", "content": self.personalities[personality_index]}]

            messages += [{'role': 'assistant', 'content': x['message'].replace('Bot:', '')} if (x['sender'] == "bot") else ({'role': 'user', 'content': x['message'].replace('You:', '')}) for x in chatlog ]

        response = openai.ChatCompletion.create(
            
            model ="gpt-3.5-turbo",
            messages = messages 

        )
        
        return response['choices'][0]['message']['content']

model = chatModel()
        
def get_model():
    return model
