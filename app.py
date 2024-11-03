#pip install groq gradio

import os

os.environ['GROQ_API_KEY'] = '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'

# Import necessary libraries
from groq import Groq  # Groq API for AI model interaction
import gradio as gr   # Gradio for creating a simple user interface

# Define Model Parameters for the Chatbot
MODEL = "llama3-8b-8192"  # Specifies the AI model to use
TEMPERATURE = 1           # Controls randomness of responses (higher = more random)
MAX_TOKENS = 1024         # Limits the number of tokens in the response
TOP_P = 1                 # Cumulative probability threshold (higher values for more diverse outputs)

# Customizable System Prompt
SYSTEM_PROMPT = """
You are an AI chatbot trained to generate humorous, convoluted responses using Gen Z and Gen Alpha slang.
Use slang, memes, and references that might confuse even those familiar with Gen Z language.
Conclude with a clear, simple answer.
"""

# Define the function to generate a response from the chatbot
def generate_response(question: str) -> str:
    """
    This function interacts with the Groq API to generate a response to the user's question.
    It uses a complex, humorous prompt that guides the AI to answer in Gen Z slang.
    """
    client = Groq()  # Initialize the Groq client

    # Create a completion request with the specified model and prompt
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},  # Provides instructions for the AI
            {"role": "user", "content": question}          # The user's question
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        stream=True,  # Stream results for efficiency
    )

    # Concatenate the response text from the stream
    response = ""
    try:
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""  # Append each part of the response
    except Exception as e:
        return f"Error generating response: {e}"  # Error handling if API call fails
    return response

# Define a Gradio interface function that uses the chatbot function
def chatbot_interface(question):
    """
    Wrapper function for Gradio interface to call the chatbot and return its response.
    """
    return generate_response(question)

# Set up the Gradio interface with input and output components
iface = gr.Interface(
    fn=chatbot_interface,       # Function to call when a question is asked
    inputs="text",              # Single text input for user questions
    outputs="text",             # Text output to display the chatbot's answer
    title="Gen Z Slang Chatbot",    # Title of the Gradio interface
    description="Ask a question and get a hilariously convoluted answer in Gen Z slang!"
)

# Launch the Gradio interface
iface.launch(debug=True)
