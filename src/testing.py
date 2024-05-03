# # from sentence_transformers import SentenceTransformer, util

# # model = SentenceTransformer('gtr-t5-xxl')

# # # Example data
# # prompt = "Write a poem about harry potter in 100 words"
# # model_responses = ['''In Hogwarts' hallowed halls, a hero's tale unfolds
# # Of magic, mystery, and courage to be told
# # Harry Potter, the boy who lived, with heart so bright
# # Confronts the Dark Lord, with a will to fight

# # With Ron and Hermione, his loyal friends by his side
# # Together they embark, on a perilous ride
# # Through trials and tribulations, they stand as one
# # Against the forces of darkness, their bond has just begun

# # Wands at the ready, they face the darkest night
# # Their bravery and love, will be the wizarding world's light''', '''In a world of magic, a boy with a scar,
# # Harry Potter, the chosen one from afar.
# # With friends by his side, Ron and Hermione,
# # They face dark wizards and unravel mysteries.
# # At Hogwarts, they learn spells and potions galore,
# # Quidditch matches and house points to score.
# # But danger lurks in the form of Voldemort,
# # A dark lord seeking power to extort.
# # Through trials and losses, Harry grows strong,
# # Guided by love, he rights the wrong.
# # In the end, good triumphs over evil's might,
# # And Harry's tale becomes a legend, shining bright.''', '''In Hogwarts, a boy with lightning scar,
# # Brave Harry Potter, shining star.
# # Wizardry and magic in his blood,
# # Facing darkness like a flood.

# # With friends like Hermione and Ron,
# # Together they face battles won.
# # Against Voldemort, the dark lord,
# # Their courage and love, never ignored.

# # In a world of enchantment and spells,
# # Their story in our hearts forever dwells.
# # Through trials and triumphs, they stand tall,
# # Harry Potter, the greatest of all.''']

# # # Embed the prompt and responses
# # prompt_embedding = model.encode(prompt, convert_to_tensor=True)
# # response_embeddings = model.encode(model_responses, convert_to_tensor=True)

# # # Calculate cosine similarities
# # similarities = util.pytorch_cos_sim(prompt_embedding, response_embeddings)

# # print("Similarity scores:", similarities)



# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from dotenv import load_dotenv
# import time
# from langchain_community.callbacks import get_openai_callback
# import tiktoken
# from langchain_core.prompts import MessagesPlaceholder

# load_dotenv()
# # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
# # # Initialize the chat model
# # llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0,max_tokens=150)

# # # Define the input template with model-specific history
# # input_template = ChatPromptTemplate.from_messages([
# #     ("system", "helpful assistant"),
# #     ("human", "{input}")
# # ])
# # print("Format: -",input_template.format(input = 'Write code to add two numbers'))
# # # Create the conversation chain
# # chain = input_template | llm
# # # Define the prompt (input from the user)
# # prompt = "write code to add two numbers"

# # start_time = time.time()
# # # # Stream the conversation and print the output
# # with get_openai_callback() as cb:
# #     a = chain.invoke({'input':prompt})
# # #     # for i in chain.stream({'input': prompt}):
# # #     #     print(i, cb)
# # print(cb, a)
# # end_time = time.time()

# # print(end_time-start_time)


# # from openai import OpenAI
# # from dotenv import load_dotenv

# # load_dotenv()
# # from openai import OpenAI
# # client = OpenAI()
# # # response = client.chat.completions.create(
# # #             model='gpt-3.5-turbo',
# # #             messages=[
# # #                 {"role": "system", "content": "helpful assistant."},
# # #                 {"role": "user", "content": 'Write code to add two numbers'}
# # #             ],
# # #             max_tokens=150,
# # #         )
# # #         # Correctly accessing the content of the message from the response
# # # print(response)

# # # print(len(encoding.encode('''System: helpful assistant
# # # Human: Write code to add two numbers''')))


#     # example token count from the OpenAI API
# # response = client.chat.completions.create(model='gpt-3.5-turbo',
# #     messages=example_messages,
# #     temperature=0,
# #     max_tokens=1)
# # print(f'{response.usage.prompt_tokens} prompt tokens counted by the OpenAI API.')
# # print()

# # from langchain.callbacks.base import BaseCallbackHandler

# # class TokenCounterCallbackHandler(BaseCallbackHandler):
# #     def __init__(self):
# #         self.tokens_used = 0

# #     def on_llm_new_token(self, token: str, **kwargs):
# #         self.tokens_used += 1

# # from langchain.llms import OpenAI
# # from langchain.callbacks import StreamingStdOutCallbackHandler
# # token_counter = TokenCounterCallbackHandler()
# # callbacks = [StreamingStdOutCallbackHandler(), token_counter]
# # llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0, streaming=True, max_tokens=150, callbacks=callbacks)

# #         # Use model specific history
# # input = ChatPromptTemplate.from_messages(
# #             [
# #                 ("system", "helpful assistant"),
# #                 ("human", "{input}")
# #             ])
# # chain = input | llm

# # for i in chain.stream({'input': 'hi'}):
# #     print(i)

# # print(f"Total tokens used: {token_counter.tokens_used}")

# import streamlit as st
# from streamlit_extras.bottom_container import bottom
# from streamlit_extras.card import card
# from streamlit_extras.customize_running import center_running
# from streamlit_extras.grid import grid
# from streamlit_modal import Modal
# from streamlit_extras.stateful_chat import chat
# from streamlit_extras.stateful_chat import add_message
# modal = Modal(key="Demo Key",title="test")
# count = 0
# def example():

#     st.write("This is the main container")



#     with bottom():
#         pass
#     with bottom():
#         st.chat_input("ASD")
# def example3():

#     click = st.button("Observe where the 🏃‍♂️ running widget is now!")

#     if click:

#         center_running()

#         time.sleep(2)

# import pandas as pd
# import numpy as np

# def example4():
#     # DataFrame for demonstration purposes
#     random_df = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

#     # Creating the grid with two specifications, each with two cells
#     my_grid = grid(2, 2)  # Each row will have two cells with equal width

#     # First row, two cells
#     my_grid.dataframe(random_df, use_container_width=True)  # First cell
#     my_grid.line_chart(random_df, use_container_width=True)  # Second cell

#     # Second row, two cells
#     my_grid.bar_chart(random_df, use_container_width=True)  # First cell
#     my_grid.map(data=random_df, use_container_width=True)   # Second cell

# def example():

#     with chat(key="my_chat"):

#         if prompt := st.chat_input():

#             add_message("user", prompt, avatar="🧑‍💻")



#             def stream_echo():

#                 for word in prompt.split():

#                     yield word + " "

#                     time.sleep(0.15)



#             add_message("assistant", "Echo: ", stream_echo, avatar="🦜")

# import streamlit as st
# from streamlit_extras.bottom_container import bottom

# def example_bottom_row():
#     # Data and settings for the multiselect
#     MODEL_DETAILS = {"model1": "Model 1", "model2": "Model 2", "model3": "Model 3"}
#     MODEL_CHOICES = list(MODEL_DETAILS.keys())
#     # Use the bottom container for placing elements at the bottom
#     with bottom():
#         # Create a row with two columns
#         input_col, select_col = st.columns([10, 1])
        
#         # Text input in the first column
#         with input_col:
#             user_input = st.chat_input("Enter your text here")
        
#         # Multiselect in the second column
#         with select_col:
#             with st.popover("🤖"):
#                 selected_models = st.multiselect("Select models:", MODEL_CHOICES, default=MODEL_CHOICES[0])

# # Running the example function
# st.set_page_config("LLM TEST", layout='wide')

# def sticky_title_column():
#     # Apply custom CSS for sticky header
#     st.markdown(
#         """
#         <style>
#         .sticky-header {
#             position: sticky;
#             top: 0;
#             z-index: 1000;
#             background-color: white;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True
#     )
    
#     col1, col2 = st.columns(2)

#     with col1:
#         # Apply sticky-header class to header
#         st.markdown('<p class="sticky-header">Sticky Column Header</p>', unsafe_allow_html=True)
#         for _ in range(50):  # This is the content that "scrolls"
#             st.text("Scrolling content here...")

#     with col2:
#         st.header("Regular Column Header")
#         st.button("A Button Here")
#         for _ in range(50):
#             st.text("More scrolling content here...")

# # Call the function
# sticky_title_column()
import streamlit as st

# with st.container():
#     st.write("text inside the container")

# with st.popover("HI"):
#     st.markdown(f'<p id="unique_id">This paragraph has a unique ID!</p>', unsafe_allow_html=True)
#     st.markdown("A SECOND CONDE WRITTEN")
# st.markdown(
#     """
# <style>
#     # div[data-testid="stPopoverBody"]{
#     #     background-color: green;
#     # }
#     div[data-testid="stPopoverBody"] div[data-testid="stVerticalBlockBorderWrapper"]{
#         background-color: green;
#     },
# </style>
# """,
#     unsafe_allow_html=True,
# )

import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time

def create_bar_chart(data, y_key, title, num_steps=50, step_delay=0.005):
    model_names = [model['model_name'] for model in data]
    final_values = [model[y_key] for model in data]
    
    max_value = max(final_values)
    placeholder = st.empty()

    fig = go.Figure(layout={
        "title": title,
        "xaxis": {"title": "Models"},
        "yaxis": {"range": [0, max(final_values) * 1.1]},
        "template": "plotly_dark"
    })

    for step in range(1, num_steps + 1):
        current_values = [value * (step / num_steps) for value in final_values]
        colors = ['green' if value == max_value and step == num_steps else 'lightslategray' for value in final_values]
        
        fig.data = []  # Clear the existing data
        fig.add_trace(
            go.Bar(
                x=model_names,
                y=current_values,
                marker_color=colors,
                text=[f"{value:.2f}" if step == num_steps else "" for value in final_values],
                textposition='auto'
            )
        )

        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(step_delay)

def main():
    data = [
        {"model_name": "Model A", "prompt_tokens": 320, "response_tokens": 280, "total_tokens": 600, 
         "current_cost": 400, "total_cost": 1000},
        {"model_name": "Model B", "prompt_tokens": 300, "response_tokens": 290, "total_tokens": 590, 
         "current_cost": 390, "total_cost": 980},
        {"model_name": "Model C", "prompt_tokens": 310, "response_tokens": 270, "total_tokens": 580, 
         "current_cost": 380, "total_cost": 960}
    ]

    st.title('Model Metrics Visualization')

    # Main Tabs for Token Metrics and Cost Metrics
    main_tab1, main_tab2 = st.tabs(["Token Metrics", "Cost Metrics"])

    with main_tab1:
        token_metric = st.selectbox(
            "Choose a token metric:",
            options=["prompt_tokens", "response_tokens", "total_tokens"],
            index=0,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        create_bar_chart(data, token_metric, f'{token_metric.replace("_", " ").title()} per Model')

    with main_tab2:
        cost_metric = st.selectbox(
            "Choose a cost metric:",
            options=["current_cost", "total_cost"],
            index=0,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        create_bar_chart(data, cost_metric, f'{cost_metric.replace("_", " ").title()} per Model')

if __name__ == "__main__":
    main()