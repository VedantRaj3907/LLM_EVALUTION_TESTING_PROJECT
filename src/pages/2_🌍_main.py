import sys
import os
import time
import threading
import streamlit as st
import concurrent.futures
from navigation import make_sidebar
from eval import OPENAI_EVAL, GOOGLE_EVAL
from models import openai_model, gemini_model
from streamlit_extras.grid import grid
from streamlit_server_state import server_state
SCRIPT_DIR = os.path.dirname(os.path.abspath('assests'))
sys.path.append(os.path.dirname(SCRIPT_DIR))
sys.path.append('./VersionControl')
from streamlit_extras.bottom_container import bottom
from VersionControl.SaveVersion import Saving_Version
from streamlit.runtime.scriptrunner import add_script_run_ctx
from chat_history_db import append_message, get_history, fetch_model_details, fetch_user_prompts, insert_saved_prompt, fetch_saved_prompt_titles, insert_version_prompt
from streamlit.runtime.scriptrunner.script_run_context import get_script_run_ctx
################################################################################################################
MAX_HISTORY_LENGTH = 5

st.set_page_config(layout='wide')

session = server_state.get('session')

make_sidebar(session)
# set_column_style() 
MODEL_DETAILS = fetch_model_details()
MODEL_CHOICES = list(MODEL_DETAILS.keys())
openai_eval = OPENAI_EVAL()
google_eval = GOOGLE_EVAL()

################################################################################################################

def call_chain(ctx, model_name, prompt):
    if prompt != '':
        model_id = MODEL_DETAILS.get(model_name)
        add_script_run_ctx(threading.current_thread(), ctx)
        try:
            # Retrieve settings from session state
            temperature = st.session_state.get(f"{model_name}_temperature", 0.5)
            p_value = st.session_state.get(f"{model_name}_pvalue", 0.5)
            max_tokens = st.session_state.get(f"{model_name}_max_output_tokens", 150)

            # Pass these settings to the model function call
            response_content = ""  # Initialize to accumulate streamed response
            if 'gpt' in model_name:
                response, messages, response_time = openai_model(model_name, model_id, user_id, prompt, temperature=temperature, p_value=p_value, max_tokens=max_tokens)

                for i in response:
                    res = i.choices[0].delta.content
                    if res is not None:
                        response_content += res  # Accumulate response
                        yield res
                        
                prompt_token = openai_eval.openai_token_count(model_name, prompt)
                response_token = openai_eval.openai_token_count(model_name, response_content)
                cost = openai_eval.cal_pricing_token(model_name, prompt_token, response_token)
                
            elif 'gemini' in model_name:
                gemini_models, response, messages, response_time = gemini_model(model_name, model_id, user_id, prompt, temperature, p_value, max_tokens)

                try:
                    for chunk in response:
                        for j in chunk.text:
                            res = j
                            if res is not None:
                                response_content += res  # Accumulate response
                                yield res
                                time.sleep(0.001)

                    prompt_token = google_eval.gemini_token_count(gemini_models, prompt)
                    response_token = google_eval.gemini_token_count(gemini_models, response_content)
                    cost = 0

                except Exception as e:
                    st.warning("Low Max_Output_Tokens")
                    prompt_token = 0
                    response_token = 0
                    cost = 0
                    response_time = 0
        

            if model_name in st.session_state:
                st.session_state[model_name] = {
                    'prompt_token': prompt_token,
                    'response_token': response_token,
                    'cost': cost,
                    'total_cost':  st.session_state[model_name]['total_cost'] + cost,
                    'total_tokens':  st.session_state[model_name]['total_cost'] + prompt_token + response_token,
                    'time_taken': response_time
                }
            else:
                st.session_state[model_name] = {
                    'prompt_token': prompt_token,
                    'response_token': response_token,
                    'cost': cost,
                    'total_cost':  cost,
                    'total_tokens': prompt_token + response_token,
                    'time_taken': response_time
                }

            append_message(user_id, model_id, prompt, response_content)
        except Exception as e:
            yield f"Error: {str(e)}"

        return [prompt_token, response_token, cost]
################################################################################################################

def threading_output(prompt):
    ctx = get_script_run_ctx()


    # Assuming model settings keys are prefixed with 'model_'
    models_to_remove = [key for key in st.session_state.keys() if key.startswith('model_') and key.split('_')[1] not in selected_models]
    for key in models_to_remove:
        del st.session_state[key]

    
    
    if len(selected_models) > 1:
        # Create a list of containers with fixed height for scrollable content
        container = st.container()
        my_grid = grid(2, 2)
        scroll_containers = [my_grid.container(border=True, height=400) for _ in range(len(selected_models))]
    else:
        # If only one model is selected, use a single scrollable container
        scroll_containers = [st.container(border=True, height=500)]


    with concurrent.futures.ThreadPoolExecutor(max_workers=len(selected_models)) as executor:
        future_to_col = {}  # Map futures to corresponding scrollable container


        for i, model in enumerate(selected_models):
            model_id = MODEL_DETAILS.get(model)
            generator = call_chain(ctx, model, prompt)
            # Submit task to executor, mapping it to the corresponding scrollable container
            future = executor.submit(give_output, ctx, generator, scroll_containers[i], model_id, prompt, model)
            future_to_col[future] = scroll_containers[i]
        
        # Handle completed futures
        for future in concurrent.futures.as_completed(future_to_col):
            col = future_to_col[future]
            try:
                future.result()  # We are just calling result to trigger exception handling if any
            except Exception as exc:
                col.error(f'Generator raised an exception: {exc}')
            except BaseException as exc:  # BaseException to capture other potential system-level exceptions
                col.error(f'Unhandled exception in the generator: {exc}')

################################################################################################################
def display_chat_history(ctx, col, model_id, model_name):
    add_script_run_ctx(threading.current_thread(), ctx)

    with col.container():
        st.header(model_name, divider='green')

    #OPENAI MODEL
    chat_history_for_model = get_history(user_id, model_id, 50, model_name)
    
    for message in chat_history_for_model:

        if 'gpt' in model_name:
            role, content = message["role"], message["content"]
            avatar_path = '../assests/openai.png'
        
        elif 'gemini' in model_name:
            role, content = message['role'], message['parts'][0]['text']
            avatar_path = '../assests/google.png'
            
        if role == "user" and content != '':
            with col.chat_message("Human", avatar='../assests/user.png'):
                st.markdown(content)
        elif role == 'assistant' or role == 'model':
            with col.chat_message("AI",avatar=avatar_path):
                st.markdown(content)

def display_message(ctx, col, prompt, generator, model_name):
    add_script_run_ctx(threading.current_thread(), ctx)

    if prompt != '':
        if 'gpt' in model_name:
            avatar_path = '../assests/openai.png'
        elif 'gemini' in model_name:
            avatar_path = '../assests/google.png'

        with col.chat_message("HUMAN", avatar='../assests/user.png'):
            st.markdown(prompt)
        with col.chat_message("AI",avatar=avatar_path):
            st.write(generator)


#For Popover menus
def submitted_button(model_name, temperature, p_value, max_tokens, col):
    with col.container():
        st.session_state[f'{model_name}_temperature'] = temperature
        st.session_state[f'{model_name}_pvalue'] = p_value
        st.session_state[f'{model_name}_max_output_tokens'] = max_tokens


def display_popovers(ctx, col, model_name, model_data=None):
    """
    Display popovers for model metadata and properties.
    
    Parameters:
        col (Column): Streamlit column object for layouts.
        model_data (dict, optional): Data about the model including tokens and cost. Defaults to None.
    """
    add_script_run_ctx(threading.current_thread(), ctx)
    default_data = {'prompt_token': 0, 'response_token': 0, 'cost': 0, 'total_cost':0, 'total_tokens':0, 'time_taken': 0}
    data = model_data if model_data else default_data
    
    with col.container():
        with st.popover("💰"):
            st.markdown(f"**Prompt Tokens**: {data['prompt_token']}")
            st.markdown(f"**Response Tokens**: {data['response_token']}")
            st.markdown(f"**Total Tokens**: {int(data['total_tokens'])}")
            st.markdown(f"**Cost**: ${data['cost']:.4f}")
            st.markdown(f"**Total Cost**: ${data['total_cost']:.4f}")
            st.markdown(f"**Time Taken**: {data['time_taken']:.4f}s")
        with st.popover("⛭ Properties"):
            with st.form(key=f'{model_name}_settings_form'):
                # Define sliders within the form
                temperature = st.slider("Temperature:", min_value=0.0, max_value=1.0, value=st.session_state[f'{model_name}_temperature'], step=0.01)
                p_value = st.slider("P Value:", min_value=0.0, max_value=1.0, value=st.session_state[f'{model_name}_p_value'], step=0.01)
                max_tokens = st.slider("Max Output Tokens:", min_value=16, max_value=1000, value=st.session_state[f'{model_name}_max_output_tokens'], step=10)

                # Submit button for the form
                st.form_submit_button("Submit Settings", on_click=submitted_button, args=(model_name, temperature, p_value, max_tokens, col))

def give_output(ctx, generator, col, model_id, prompt, model_name):

    display_chat_history(ctx, col, model_id, model_name)

    display_message(ctx,col, prompt, generator, model_name)

    if model_name in st.session_state:
        model_data = st.session_state[model_name]
        display_popovers(ctx, col, model_name, model_data)
    else:
        display_popovers(ctx, col, model_name)
################################################################################################################
# Sidebar Creation

if "selected_models" not in st.session_state:
    # Default model selection (you can set it to empty if you want no defaults)
    st.session_state["selected_models"] = ["gpt-3.5-turbo"]

for model_name in MODEL_CHOICES:
    if f'{model_name}_temperature' not in st.session_state:
        st.session_state[f'{model_name}_temperature'] = 0.5
        st.session_state[f'{model_name}_p_value'] = 0.5
        st.session_state[f'{model_name}_max_output_tokens'] = 150

user_id = session.user.id
with bottom():
    popover_col, input_col, select_col = st.columns([1, 9, 1])

    with input_col:
        user_prompt = st.chat_input("Write a question")
        if user_prompt:
            st.session_state["current_prompt"] = user_prompt  # Update current prompt in session state

    def get_prompts(user_id):
        if "all_prompts" not in st.session_state:
            all_prompts = fetch_user_prompts(user_id)
            all_prompts = [prompt['user_message'] for prompt in all_prompts.data]
            st.session_state['all_prompts'] = all_prompts
        if 'current_prompt' in st.session_state and st.session_state['current_prompt'] != None and (not st.session_state['all_prompts'] or st.session_state['all_prompts'][-1] != st.session_state['current_prompt']):
            st.session_state['all_prompts'].append(st.session_state['current_prompt'])
        return st.session_state['all_prompts']

    with popover_col:
        with st.popover("📖"):
            st.header("Save Prompts")
            # Add your popover menu content here
            options = ["Save Current Prompt", "Save Previous Prompt"]
            selected_option = st.selectbox("\u00A0", options, index=0)  # Set default value to "Save Current Prompt"
            all_prompts = get_prompts(user_id)
            
            if all_prompts:
                current_prompt = st.session_state.get("current_prompt")
                if all_prompts and all_prompts[-1] == current_prompt:
                    previous_prompts = all_prompts[:-1] if len(all_prompts) > 1 else []
                else:
                    previous_prompts = all_prompts
            else:
                current_prompt = ''
                previous_prompts = []

            if selected_option == options[0]:  # Save Current Prompt
                prompt_to_save = current_prompt
            elif selected_option == options[1]:  # Save Previous Prompt
                prompt_to_save = st.selectbox("Select a previous prompt to save:", previous_prompts)

            version_options = ["Save Prompt as New Version", "Add to Existing Version"]
            selected_version_option = st.selectbox("\u00A0", version_options)
            if st.session_state.get('current_prompt') is None:
                st.warning("Please write a prompt to save it.")
            else:
                if selected_version_option == version_options[0]:  # Save Prompt as New Version
                    if prompt_to_save:
                        prompt_title = st.text_input("Enter Prompt Title:", disabled=st.session_state.get('current_prompt') is None)
                        if st.button('Save as New Version'):
                            print(f'{user_id}\n{prompt_title}\n{prompt_to_save}')
                            insert_saved_prompt(user_id, prompt_title, prompt_to_save)  # Save the prompt in the Saved_Prompts table
                            # Refresh the saved prompt titles in the session state
                            st.session_state["saved_prompt_titles"] = fetch_saved_prompt_titles(user_id)
                            st.toast(f'Prompt saved with prompt title: - {prompt_title}', icon='✅')

                            if 'check_rerun_prompts' not in st.session_state:
                                st.session_state['check_rerun_prompts'] = True
                            st.session_state['check_rerun_prompts'] = True

                elif selected_version_option == version_options[1]:  # Add to Existing Version
                    # Check if saved_prompt_titles is already in session state
                    if "saved_prompt_titles" not in st.session_state:
                        # If not, fetch the saved prompt titles and store them in session state
                        st.session_state["saved_prompt_titles"] = fetch_saved_prompt_titles(user_id)
                    # Use the saved prompt titles from session state to populate the selectbox
                    existing_version = st.selectbox("Select existing version:", st.session_state["saved_prompt_titles"], format_func=lambda x: x['title'], disabled=st.session_state.get('current_prompt') is None)
                    if st.button('Add to Existing Version'):

                        new_version_number = Saving_Version(existing_version['id'], prompt_to_save)
                        print(f'Version: - {new_version_number}')
                        insert_version_prompt(existing_version['id'], prompt_to_save, new_version_number)
                        st.session_state["saved_prompt_titles"] = fetch_saved_prompt_titles(user_id)
                        st.toast(f'Prompt saved with verison: - {new_version_number}', icon='✅')

                        if 'check_rerun_prompts' not in st.session_state:
                            st.session_state['check_rerun_prompts'] = True
                        st.session_state['check_rerun_prompts'] = True
                        
    with select_col:
        with st.popover("🤖"):
            selected_models = st.multiselect("Select models:", MODEL_CHOICES, default=st.session_state["selected_models"], placeholder='Choose models', max_selections=4)
            if selected_models != st.session_state["selected_models"]:
                st.session_state["selected_models"] = selected_models  # Update session state
                st.experimental_rerun()  # Manually trigger a rerun
            if len(selected_models) < 1:
                st.write("SELECT AT LEAST ONE MODEL")

if user_prompt and selected_models:
    # Store user input into each model's history
    for model in selected_models:
        model_id = MODEL_DETAILS[model]
    threading_output(user_prompt)
elif not selected_models:
    st.warning("Please select at least one model before proceeding.")
else:
    threading_output('')