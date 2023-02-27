from transformers import pipeline , Conversation 

class chatModelBlender():
    
    def __init__(self):
      
        chatbot = pipeline("conversational", model = "facebook/blenderbot-400M-distill")
        self.chatbot = chatbot
        session_prompt = """ You are talking to a human-like chatbot. I am curious about humans feelings and will always ask questions after responding to the person to keep the conversation going."""

        
        self.session_prompt = session_prompt

        self.chat_log = None

    def respond(self, user_input, conversation = None, ):
        
        if not(conversation):
           past_user_inputs = None
           generated_responses = None
        
        conversation = Conversation(user_input, past_user_inputs=past_user_inputs, generated_responses=generated_responses)
        response = self.chatbot(conversation).generated_responses[-1]
        print(response)

        return response


model = chatModelBlender()
        
def get_modelB():
    return model
