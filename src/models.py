from openai import OpenAI
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from chat_history_db import append_message, get_history, fetch_model_details
import google.generativeai as genai
import os
import time
load_dotenv()
client = OpenAI()

def antropic_model(model_name):
    llm = ChatAnthropic(temperature=0, model_name=model_name, streaming=True)
    return llm

def openai_model(model_name, model_id, user_id, prompt, temperature, p_value, max_tokens):

    start_time = time.time()
    print("*"*10)
    print(f'temperature: - {temperature}\nmax_tokens: - {max_tokens}')
    chat_history_for_model = get_history(user_id, model_id, 5, model_name)
    messages = chat_history_for_model + [
                {"role": "user", "content": prompt}
                ]

    response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=p_value,
            stream=True,

        )
    
    end_time = time.time()
    response_time = end_time - start_time
    return response, messages, response_time

def gemini_model(model_name, model_id, user_id, prompt, temperature, p_value, max_tokens):

    start_time = time.time()

    chat_history_for_model = get_history(user_id, model_id, 5, model_name)
    genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

    modelg = genai.GenerativeModel('gemini-pro',generation_config=genai.types.GenerationConfig(
        temperature=temperature,
        top_p=p_value,
        max_output_tokens=max_tokens
    ))
    chat_history = modelg.start_chat(history=chat_history_for_model)

    response = chat_history.send_message(prompt, stream=True)

    end_time = time.time()
    response_time = end_time - start_time
    return modelg, response, chat_history_for_model, response_time