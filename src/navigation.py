import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from streamlit_server_state import server_state
from chat_history_db import delete_chat_history
import time

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar(session):
    if get_current_page_name() == "1_🙎‍♂️_UserLogin.py":
        return
    with st.sidebar:
        if session:
            st.title("🤖 LLM EVALUATION")
            st.write("")
            st.write("")

            st.page_link("pages/2_🌍_main.py", label="Chat_Models", icon="🌍")
            st.page_link("pages/3_📊_Charts.py", label="Charts", icon="📊")
            st.page_link("pages/4_📝_Prompts.py", label="Saved_Prompts", icon="📝")

            st.write("")
            st.write("")

            if st.button("Log out"):
                print("LOGGING OUT")
                delete_chat_history(session.user.id)
                st.session_state.clear()
                st.toast('Logged out successfully', icon='✅')
                time.sleep(1)
                server_state['session'] = None

        elif not session:
            st.switch_page("1_🙎‍♂️_UserLogin.py")