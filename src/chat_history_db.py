from supabase import create_client, Client
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(url, key)



def format_interaction_history(data):
    """
    Format a list of interaction dictionaries into a chat history for a chat model.

    Args:
    data (list of dicts): List containing interaction data where each dictionary has
                          'user_message' and 'ai_message' keys.

    Returns:
    list: Formatted chat history list suitable for models.
    """
    if not data.data:
         return [{"role": "user", "content": ''}]
    else:
        chat_history_for_model = []
        for interaction in data.data[::-1]:
            chat_history_for_model.append({"role": "user", "content": interaction["user_message"]})
            chat_history_for_model.append({"role": "assistant", "content": interaction["ai_message"]})
        return chat_history_for_model

def format_interaction_history_gemini(data):
     if not data.data:
         return []
     else:
        chat_history_for_model = []
        for interaction in data.data[::-1]:
            chat_history_for_model.append({"parts": [{"text": interaction['user_message']}], "role": "user"})
            chat_history_for_model.append({"parts": [{"text": interaction['ai_message']}], "role": "model"})
        return chat_history_for_model
             
def append_message(user_id, model_id, user_message, ai_message):
        data = {
            "user_id": user_id,
            "model_id": model_id,
            "user_message": user_message,
            "ai_message": ai_message
        }
        response = supabase.table("chat_history").insert(data).execute()
        return response


def get_history(user_id, model_id,MAX_HISTORY_LENGTH, model_name):
    messages = supabase.table("chat_history")\
        .select("*").eq("user_id", user_id)\
        .eq("model_id", model_id)\
        .order("created_at", desc=True)\
        .limit(MAX_HISTORY_LENGTH)\
        .execute()
    
    if 'gpt' in model_name:
        return format_interaction_history(messages)
    elif 'gemini' in model_name:
        return format_interaction_history_gemini(messages)


def fetch_model_details():
    # Fetch data from the 'models' table in Supabase
    response = supabase.table("models").select("model_id, model_name").execute()
    # Create a dictionary to map model names to their IDs
    model_details = {model['model_name']: model['model_id'] for model in response.data}
    return model_details