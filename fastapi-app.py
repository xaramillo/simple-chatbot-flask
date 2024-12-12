import openai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv()

# Set OpenAI API key
# Or use os.getenv('OPENAI_API_KEY')
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Serve static files (for serving HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define request model for the message
class Message(BaseModel):
    message: str

# Define the OpenAI API call
def chat_with_bot(prompt: str) -> str:
    response = openai.Completion.create(
        model="gpt-4o-mini",  # You can use "gpt-3.5-turbo" as well
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Home route - serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("index.html", "r") as file:
        return file.read()

# Chat route to handle user input and get response from OpenAI
@app.post("/chat")
async def chat(message: Message):
    user_message = message.message
    if not user_message:
        return {"error": "No message provided"}
    
    # Get bot response
    bot_response = chat_with_bot(user_message)
    return {"response": bot_response}

