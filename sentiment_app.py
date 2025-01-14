import streamlit as st
import requests
import plotly.graph_objects as go
from io import BytesIO
import base64
from PIL import Image
import os

# Helper function to display the images (Word Cloud & Bar Chart)
def display_image_from_base64(base64_string):
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    st.image(img)

def analyze_sentiment():
    # Display a stylish header
    st.markdown("<h1 style='text-align: center; color: #ff0000;'>Sentiment Analysis from Reddit</h1>", unsafe_allow_html=True)

    # Get the topic from user input with a stylish input box
    topic = st.text_input("Enter a topic to analyze:", "")

    if topic:
        # Set the limit for the number of posts to fetch
        limit = st.slider("Select the number of posts:", 1, 10, 5)
        
        # Use FLASK_URL from environment or default to Render's backend URL
        #flask_url = os.environ.get("FLASK_URL", "https://sentimental-analysis-reddit.onrender.com/")
        flask_url = f"https://sentimental-analysis-reddit.onrender.com/api/sentiment/analyze"

        # Call the Flask API to get sentiment analysis
        try:
            response = requests.post(f"{flask_url}api/sentiment/analyze", json={"topic": topic, "limit": limit})

            if response.status_code == 200:
                data = response.json()

                # Display sentiment analysis results
                for result in data["sentiment_analysis"]:
                    st.markdown(f"#### **{result['title']}**")
                    st.write(f"**Content:** {result['content']}")
                    st.write(f"**Sentiment:** {result['sentiment']} (Score: {result['score']})")
                    st.write("---")  # Divider for better readability

                # Extract sentiment labels and scores for visualization
                sentiment_labels = [result['sentiment'] for result in data["sentiment_analysis"]]
                sentiment_scores = [result['score'] for result in data["sentiment_analysis"]]

                # Create a bar chart to display sentiment scores
                fig = go.Figure(go.Bar(
                    x=sentiment_labels,
                    y=sentiment_scores,
                    name="Sentiment Scores",
                    marker=dict(color='royalblue')
                ))

                fig.update_layout(
                    title="Sentiment Analysis: Scores per Reddit Post",
                    xaxis_title="Sentiment",
                    yaxis_title="Score",
                    template="plotly_dark",
                    height=400,
                    showlegend=False,
                )

                # Display the bar chart
                st.plotly_chart(fig)

                # Display the Word Cloud (from the graph generated in `graphs.py`)
                wordcloud_base64 = data['sentiment_graph'][1]
                display_image_from_base64(wordcloud_base64)

            else:
                st.error(f"Error {response.status_code}: Unable to fetch sentiment analysis results.")

        except requests.exceptions.RequestException as e:
            st.error(f"Error: Unable to connect to the backend service. Details: {e}")

if __name__ == "__main__":
    analyze_sentiment()
