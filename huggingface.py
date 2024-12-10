from transformers import pipeline

import pandas as pd


#vehicles_df = pd.read_csv("vehicles_cleaned.csv")





reviews_df = pd.read_csv("car_reviews.csv")


classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
sentiment_analyzer = pipeline("sentiment-analysis")


categories = ["driving experience", "features", "value for money", "issues", "other"]


reviews_df['talks_about'] = reviews_df['review'].apply(
    lambda x: classifier(x, candidate_labels=categories)['labels'][0]
)
reviews_df['sentiment'] = reviews_df['review'].apply(
    lambda x: sentiment_analyzer(x)[0]['label']
)


reviews_df.to_csv("classified_reviews.csv", index=False)
