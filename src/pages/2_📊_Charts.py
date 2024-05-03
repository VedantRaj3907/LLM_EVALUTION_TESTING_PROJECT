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
    
    with st.popover('asd'):
        st.title('Model Metrics Visualization')
        tab1, tab2 = st.tabs(["Token Metrics", "Cost Metrics"])

        with tab1:
            st.header("Token Comparison for Models")
            create_bar_chart(data, token_metric, f'{token_metric.replace("_", " ").title()} per Model')

        with tab2:
            st.header("Cost Comparison for Models")
            create_bar_chart(data, token_metric, f'{token_metric.replace("_", " ").title()} per Model')

if __name__ == "__main__":
    main()