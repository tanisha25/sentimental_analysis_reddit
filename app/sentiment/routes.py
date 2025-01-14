from flask import Blueprint, request, jsonify, render_template
from app.sentiment.fetch_reddit import fetch_reddit_data
from app.sentiment.analysis import analyze_sentiment
from app.sentiment.graphs import generate_graphs

sentiment_bp = Blueprint(
    'sentiment', 
    __name__, 
    template_folder='templates'
)

@sentiment_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@sentiment_bp.route('/analyze', methods=['POST'])
def analyze_sentiment_route():
    topic = request.form['topic']
    limit = int(request.form['num_records'])
    
    # Fetch Reddit data
    posts = fetch_reddit_data(topic, limit)
    
    # Analyze sentiment
    sentiment_results = analyze_sentiment(posts)
    
    # Generate graphs (bar chart and word cloud)
    bar_chart_b64, word_cloud_b64 = generate_graphs(sentiment_results, topic)
    
    # Render the template with the data
    return render_template(
        'index.html',
        topic=topic,
        sentiment_results=sentiment_results,
        bar_chart_b64=bar_chart_b64,
        word_cloud_b64=word_cloud_b64
    )
