import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from io import BytesIO
import base64

def generate_graphs(sentiment_results, topic):
    # Extract sentiment labels and scores
    sentiments = [result['sentiment'] for result in sentiment_results]
    scores = [result['score'] for result in sentiment_results]
    
    # Create a barplot for sentiment scores
    plt.figure(figsize=(8, 6))
    sns.barplot(x=sentiments, y=scores, palette="viridis")
    plt.title(f'Sentiment Scores for Reddit Posts on "{topic}"')
    
    # Save the bar plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.read()).decode('utf-8')
    
    # Generate word cloud from content
    text = ' '.join([result['content'] for result in sentiment_results])
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Save wordcloud image to BytesIO
    wc_img = BytesIO()
    wordcloud.to_image().save(wc_img, format='PNG')
    wc_img.seek(0)
    wc_img_b64 = base64.b64encode(wc_img.read()).decode('utf-8')
    
    return img_b64, wc_img_b64
