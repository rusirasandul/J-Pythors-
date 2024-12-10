import pandas as pd


reviews_df = pd.read_csv("vehicles_cleaned.csv")


print(reviews_df.head())


if 'review' not in reviews_df.columns:
    raise KeyError("'review' column not found in car_reviews.csv")
