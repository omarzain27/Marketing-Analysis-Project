import pyodbc
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis if not already present.
nltk.download('vader_lexicon')

def fetch_customer_reviews():
    try:
        # Connection string
        conn_str = (
            "Driver={ODBC Driver 17 for SQL Server};"
            "Server=LAPTOP-VT8B7LNE\\SQLEXPRESS;"
            "Database=PortfolioProject_MarketingAnalytics;"
            "Trusted_Connection=yes;"
        )

        # Establish connection using a context manager
        with pyodbc.connect(conn_str) as conn:
            # Define the SQL query
            query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM customer_reviews"

            # Fetch data into a DataFrame
            df = pd.read_sql_query(query, conn)

        # Return the DataFrame
        return df

    except pyodbc.Error as e:
        print(f"Database error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    df = fetch_customer_reviews()
    if df is not None:
        print(df.head())


sia = SentimentIntensityAnalyzer()

def calculate_sentiment(review):
    sentiment = sia.polarity_scores(review)
    return sentiment['compound']


def categorize_sentiment(score, rating):
    # Use both the text sentiment score and the numerical rating to determine sentiment category
    if score > 0.05:  # Positive sentiment score
        if rating >= 4:
            return 'Positive'  # High rating and positive sentiment
        elif rating == 3:
            return 'Mixed Positive'  # Neutral rating but positive sentiment
        else:
            return 'Mixed Negative'  # Low rating but positive sentiment
    elif score < -0.05:  # Negative sentiment score
        if rating <= 2:
            return 'Negative'  # Low rating and negative sentiment
        elif rating == 3:
            return 'Mixed Negative'  # Neutral rating but negative sentiment
        else:
            return 'Mixed Positive'  # High rating but negative sentiment
    else:  # Neutral sentiment score
        if rating >= 4:
            return 'Positive'  # High rating with neutral sentiment
        elif rating <= 2:
            return 'Negative'  # Low rating with neutral sentiment
        else:
            return 'Neutral'  # Neutral rating and neutral sentiment

def sentiment_bucket(score):
    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive sentiment
    elif 0.0 <= score < 0.5:
        return '0.0 to 0.49'  # Mildly positive sentiment
    elif -0.5 <= score < 0.0:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5'  # Strongly negative sentiment

# Apply sentiment analysis to calculate sentiment scores for each review
df['SentimentScore'] = df['ReviewText'].apply(calculate_sentiment)
print(df[['ReviewText','SentimentScore']])


# Apply sentiment categorization using both text and rating
df['SentimentCategory'] = df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

# Apply sentiment bucketing to categorize scores into defined ranges
df['SentimentBucket'] = df['SentimentScore'].apply(sentiment_bucket)

# Display the first few rows of the DataFrame with sentiment scores, categories, and buckets
print(df.head())

# Save the DataFrame with sentiment scores, categories, and buckets to a new CSV file
df.to_csv('fact_customer_reviews_with_sentiment.csv', index=False)
print(df)