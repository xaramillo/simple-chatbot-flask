from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv()

# Set OpenAI API key (you can also use environment variables for security)
# Alternatively, use os.getenv('OPENAI_API_KEY')
load_dotenv()


# Initialize Flask app
app = Flask(__name__)

# Define the OpenAI API call
def chat_with_bot(prompt):
    response = openai.Completion.create(
        model="gpt-4o",  # You can use "gpt-3.5-turbo" as well
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Chat route to handle messages from user
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    response = chat_with_bot(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
