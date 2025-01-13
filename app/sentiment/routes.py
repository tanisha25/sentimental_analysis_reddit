from flask import Blueprint, request, jsonify
from app.sentiment.fetch_reddit import fetch_reddit_data
from app.sentiment.analysis import analyze_sentiment
from app.sentiment.graphs import generate_graphs

sentiment_bp = Blueprint('sentiment', __name__)

# Route to fetch data from Reddit and analyze sentiment
@sentiment_bp.route('/analyze', methods=['POST'])
def analyze():
    print("Hello world!!")
    data = request.get_json()
    topic = data.get('topic', '')
    
    # Ensure topic is provided
    if not topic:
        return jsonify({"error": "Topic is required"}), 400
    
    # Fetch data from Reddit for the topic
    posts = fetch_reddit_data(topic)
    
    # Perform sentiment analysis
    sentiment_results = analyze_sentiment(posts)
    
    # Generate graphs and pass the topic
    sentiment_graph = generate_graphs(sentiment_results, topic)  # Pass topic here
    
    # Return analysis results and graph
    return jsonify({
        "sentiment_analysis": sentiment_results,
        "sentiment_graph": sentiment_graph
    })
