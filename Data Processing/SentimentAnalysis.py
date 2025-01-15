"""
Sentiment Analysis on Marketing Feedback
----------------------------------------
This script reads text feedback from a CSV file, uses a pre-trained sentiment
analysis model (from the "textblob" library), and outputs sentiment scores and
labels to a new CSV file.

Dependencies:
    pip install pandas textblob

Usage:
    1. Create a CSV file called 'feedback.csv' with a column named "Feedback".
    2. Run this script to generate an output file 'feedback_with_sentiment.csv'.
    3. You can further use these sentiment scores to filter or group responses.
"""

import pandas as pd
from textblob import TextBlob

def analyze_sentiment(text):
    """
    Uses TextBlob to analyze the sentiment of the given text.
    
    Args:
        text (str): The feedback text to analyze.
        
    Returns:
        dict: A dictionary containing polarity and a sentiment label (Positive, Negative, or Neutral).
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Range is [-1.0, 1.0] where -1 is negative and 1 is positive.

    if polarity > 0:
        sentiment_label = "Positive"
    elif polarity < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return {"polarity": polarity, "label": sentiment_label}

def main():
    try:
        df = pd.read_csv("feedback.csv")
    except FileNotFoundError:
        print("Could not find 'feedback.csv'. Please create a CSV file with a column named 'Feedback'.")
        return

    # Create new columns for polarity and sentiment label
    df["Polarity"] = None
    df["SentimentLabel"] = None

    for idx, row in df.iterrows():
        text = str(row["Feedback"])  # Convert to str to avoid errors if there's any non-string data
        result = analyze_sentiment(text)
        df.at[idx, "Polarity"] = result["polarity"]
        df.at[idx, "SentimentLabel"] = result["label"]

    # Save the updated DataFrame to a new CSV
    df.to_csv("feedback_with_sentiment.csv", index=False)
    print("Sentiment analysis complete. Results stored in 'feedback_with_sentiment.csv'.")

if __name__ == "__main__":
    main()
