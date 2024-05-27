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

def insert_saved_prompt(user_id, prompt_title, prompt):
    """Inserts a new record into the Saved_Prompts table."""
    data = {
        "user_id": user_id,
        "prompt_title": prompt_title,
        "prompt": prompt
    }
    response = supabase.table("Saved_Prompts").insert(data).execute()
    return response

def fetch_model_details():
    # Fetch data from the 'models' table in Supabase
    response = supabase.table("models").select("model_id, model_name").execute()
    # Create a dictionary to map model names to their IDs
    model_details = {model['model_name']: model['model_id'] for model in response.data}
    return model_details

def fetch_saved_prompts(user_id):
    response = supabase.table("Saved_Prompts").select("*").eq("user_id", user_id).execute()
    return response

def fetch_all_versions_prompt(prompt_id):
    """Fetches all versions of a given prompt from the Version_Prompts table."""
    response = supabase.table("Version_Prompts")\
                  .select("*")\
                  .eq("prompt_id", prompt_id)\
                  .order("version", desc=True)\
                  .execute()
    return response

def get_latest_version_prompt(prompt_id):
    response = supabase.table("Version_Prompts")\
                  .select("*")\
                  .eq("prompt_id", prompt_id)\
                  .order("version", desc=True)\
                  .order("created_at", desc=True)\
                  .limit(1)\
                  .execute()
    return response

def fetch_user_prompts(user_id):
    """Fetches all prompts written by a given user from the chat_history table, excluding the current prompt."""
    response = supabase.table("chat_history")\
                  .select("user_message")\
                  .eq("user_id", user_id)\
                  .execute()
    return response

def fetch_saved_prompt_titles(user_id):
    response = supabase.from_("saved_prompt_titles")\
                       .select('prompt_title, prompt_id, last_version')\
                       .eq('user_id', user_id)\
                       .execute()
    return [{'title': f"{record['prompt_title']} (Last Version {record['last_version']})", 'id': record['prompt_id']} for record in response.data]

def get_latest_version_from_view(prompt_id):
    response = supabase.from_("saved_prompt_titles")\
                  .select("*")\
                  .eq("prompt_id", prompt_id)\
                  .execute()
    return response

def insert_version_prompt(prompt_id, prompt, version):
    data = {
        'prompt_id':prompt_id,
        "prompt": prompt,
        "version": version
    }
    response = supabase.table("Version_Prompts").insert(data).execute()
    return response

def delete_version_prompt(prompt_id, version):
    response = supabase.from_("Version_Prompts")\
                       .delete()\
                       .eq('prompt_id', prompt_id)\
                       .eq('version', version)\
                       .execute()
    return response

def delete_saved_prompt(prompt_id):
    response = supabase.from_("Saved_Prompts")\
                       .delete()\
                       .eq('id', prompt_id)\
                       .execute()
    return response

def delete_all_version_prompts(prompt_id):
    response = supabase.from_("Version_Prompts")\
                       .delete()\
                       .eq('prompt_id', prompt_id)\
                       .execute()
    return response