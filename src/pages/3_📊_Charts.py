import time
import streamlit as st
import plotly.graph_objects as go
from navigation import make_sidebar
from chat_history_db import fetch_model_details, fetch_model_votes
from streamlit_server_state import server_state

session = server_state.get('session')


make_sidebar(session)
def create_bar_chart(data, y_key, title, num_steps=50, step_delay=0.005, highlight_max=True):
    if not data:
        st.warning(f"No data available for {title}.")
        return
    
    model_names = [model['model_name'] for model in data]
    final_values = [model[y_key] for model in data]

    highlight_value = max(final_values) if highlight_max else min(final_values) if final_values else 0

    placeholder = st.empty()
    fig = go.Figure(layout={
        "title": title,
        "xaxis": {"title": "Models"},
        "yaxis": {"range": [0, max(final_values) * 1.1] if final_values else [0, 1]},
        "template": "plotly_dark"
    })
    
    for step in range(1, num_steps + 1):
        current_values = [(value * (step / num_steps)) for value in final_values]
        colors = ['green' if value == highlight_value and step == num_steps else 'lightslategray' for value in final_values]
        
        # Enhanced format for display
        if 'cost' in y_key:
            # Format for cost metrics with a dollar sign and to two decimal places
            text_format = [f"${value:.6f}" if step == num_steps else "" for value in current_values]
        elif 'time' in y_key:
            # Format for time metrics with an 's' at the end and to two decimal places
            text_format = [f"{value:.2f}s" if step == num_steps else "" for value in current_values]
        else:
            # Default format to two decimal places
            text_format = [f"{value:.2f}" if step == num_steps else "" for value in current_values]
        
        fig.data = []  # Clear the existing data
        fig.add_trace(
            go.Bar(
                x=model_names,
                y=current_values,
                marker_color=colors,
                text=[text_format[i] if step == num_steps else "" for i, value in enumerate(final_values)],
                textposition='auto'
            )
        )
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(step_delay)

def main():
    model_name = fetch_model_details().keys()
    data = []

    model_votes = fetch_model_votes()
    
    for i in model_name:
        if i in st.session_state and i in st.session_state['selected_models']:
            model_data = st.session_state[i]
            data.append({
                "model_name": i,
                "prompt_tokens": model_data['prompt_token'],
                "response_tokens": model_data['response_token'],
                "total_tokens": model_data['total_tokens'],
                "current_cost": model_data['cost'],
                "total_cost": model_data['total_cost'],
                "time_taken": model_data['time_taken']
            })

    st.title('Model Metrics Visualization')
    # Main Tabs for Token Metrics and Cost Metrics
    main_tab1, main_tab2, main_tab3 = st.tabs(["Token Metrics", "Cost and Time Metrics", "Users Votings"])
    
    with main_tab1:
        token_metric = st.selectbox(
            "Choose a token metric:",
            options=["prompt_tokens", "response_tokens", "total_tokens"],
            index=0,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        create_bar_chart(data, token_metric, f'{token_metric.replace("_", " ").title()} per Model', highlight_max=False)
    
    with main_tab2:
        cost_time_metric = st.selectbox(
            "Choose a cost metric:",
            options=["current_cost", "total_cost", "time_taken"],
            index=0,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        create_bar_chart(data, cost_time_metric, f'{cost_time_metric.replace("_", " ").title()} per Model', highlight_max=False)
    
    with main_tab3:
        st.header("User Votes for Models")
        create_bar_chart(model_votes, 'total_votes', 'Total Votes per Model', highlight_max=True)

    #Mainting session state between pages.
    if len(data) != 0:
        st.session_state['selected_models'] = [i['model_name'] for i in data]


if __name__ == "__main__":
    main()