import streamlit as st
import requests
import json 
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

API_ENDPOINT = "https://app.explorium.ai/api/bundle/v1/enrich/company-ratings-by-employees"
API_ENDPOINT1 = "https://app.explorium.ai/api/bundle/v1/enrich/technographics"

API_HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "API_KEY": "2e7fa66d-22e5-4ff2-9f1a-3f6f73e55c5a"
}

def get_company_ratings_by_employees(url):
    payload = [{"domain": url}]
    response = requests.post(API_ENDPOINT, json=payload, headers=API_HEADERS)
    data = response.json()[0]
    # Parse the trend string into a dictionary
    data['Trend'] = json.loads(data['Trend'])
    return data


def create_plots(ratings):
    # Overall Rating Bar Chart
    overall_rating = round(ratings['Overall Ratings '], 1)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = overall_rating,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 5]},
                 'steps' : [
                     {'range': [0, 1], 'color': 'red'},
                     {'range': [1, 2], 'color': 'orange'},
                     {'range': [2, 3], 'color': 'yellow'},
                     {'range': [3, 4], 'color': 'lightgreen'},
                     {'range': [4, 5], 'color': 'green'}],
                 'bar': {'color': 'black'}
                },
        title = {'text': "<b>Overall Rating</b>", 'font': {'size': 20}}
    ))
    
    # Line Chart
    trend = ratings["Trend"]
    dates = list(trend.keys())
    values = list(trend.values())
    
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Scatter(x=dates, y=values, name="Overall Rating Trend"), secondary_y=False)
    fig2.add_trace(go.Scatter(x=dates, y=[overall_rating]*len(dates), name="Overall Rating"), secondary_y=True)
    fig2.update_yaxes(title_text="<b>Overall Rating</b>", range=[0, 5], secondary_y=False)
    fig2.update_yaxes(title_text="<b>Overall Rating</b>", range=[0, 5], secondary_y=True)
    fig2.update_layout(title="<b>Overall Rating Trend</b>", xaxis_tickangle=-45, height=600)
    
    # Compensation Benefits Rating Gauge
    compensation_rating = round(ratings['Compensation benefits rating'], 1)
    fig3 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = compensation_rating,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 5]},
                 'steps' : [
                     {'range': [0, 1], 'color': 'red'},
                     {'range': [1, 2], 'color': 'orange'},
                     {'range': [2, 3], 'color': 'yellow'},
                     {'range': [3, 4], 'color': 'lightgreen'},
                     {'range': [4, 5], 'color': 'green'}],
                 'bar': {'color': 'black'}
                },
        title = {'text': "<b>Compensation Benefits Rating</b>", 'font': {'size': 20}}
    ))

    # Diversity Inclusion Rating Gauge
    diversity_rating = round(ratings['Diversity inclusion rating'], 1)
    fig4 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = diversity_rating,
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [None, 5]},
                'steps' : [ 
                    {'range': [0, 1], 'color': 'red'},
                    {'range': [1, 2], 'color': 'orange'},
                    {'range': [2, 3], 'color': 'yellow'},
                    {'range': [3, 4], 'color': 'lightgreen'},
                    {'range': [4, 5], 'color': 'green'}],
                'bar': {'color': 'black'}
                },
        title = {'text': "<b>Diversity Inclusion Rating</b>", 'font': {'size': 20}}
    ))

    return fig, fig2, fig3, fig4

def main():
    st.set_page_config(page_title='Company Ratings', page_icon=':guardsman:', layout='wide')
    st.title("Company Ratings by Employees")
    st.write("Enter the company's website URL below to see ratings by employees.")
    url = st.text_input("URL")

    if url:
        try:
            ratings = get_company_ratings_by_employees(url)
            st.write(f"**{ratings['Number of ratings']}** ratings | **{ratings['Total reviews count']}** reviews")
            st.write(f"**Overall Rating:** {round(ratings['Overall Ratings '], 1)}/5")
            st.write(f"**Work Life Balance Rating:** {round(ratings['Work life balance rating'], 1)}/5")
            st.write(f"**Culture Values Rating:** {round(ratings['Culture values rating'], 1)}/5")
            st.write(f"**Senior Management Rating:** {round(ratings['Senior management rating'], 1)}/5")
            st.write(f"**Compensation Benefits Rating:** {round(ratings['Compensation benefits rating'], 1)}/5")
            st.write(f"**Diversity Inclusion Rating:** {round(ratings['Diversity inclusion rating'], 1)}/5")
            st.write(f"**CEO Approval Rating:** {round(ratings['CEO approval rating']*100, 1)}%")
            
            fig, fig2, fig3, fig4 = create_plots(ratings)
            st.plotly_chart(fig, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
            st.plotly_chart(fig3, use_container_width=True)
            st.plotly_chart(fig4, use_container_width=True)
            
        except IndexError:
            st.error("The provided URL is not valid or has no rating data available.")

    if st.button("get technographics"):
        payload = [{"url": url}]
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "API_KEY": '2e7fa66d-22e5-4ff2-9f1a-3f6f73e55c5a'
        }
        
        response = requests.post(API_ENDPOINT1, json=payload, headers=headers)

        if response.ok:
            data = response.json()[0]
            st.write(f"Technographics enrichment for {data['INPUT_url']}:\n")
            df = pd.DataFrame(data.items(), columns=["Key", "Value"])
            st.dataframe(df.set_index("Key"))
        else:
            st.write("Error occurred while retrieving technographics data.")

if __name__ == "__main__":
    if "access_token" in st.session_state: 
        main()
    else:
        st.error("Please Login First")

