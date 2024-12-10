import pandas as pd
from tqdm import tqdm
from transformers import pipeline

# Hugging Face login (ensure you have already run `huggingface-cli login` in your terminal)

# Load the text-generation pipeline
pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B")

# Define input file path and load the dataset
file_path = "data/reviews.csv"
df = pd.read_csv(file_path)

# Define column name containing reviews
review_column = "Review"

# Ensure the correct column exists
if review_column not in df.columns:
    raise ValueError(f"Column '{review_column}' not found in the dataset!")

# Define candidate labels and initialize output columns
candidate_labels = [
    "Talks about driving experience",
    "Talks about features",
    "Talks about value for money",
    "Talks about issues",
    "Other"
]
df["talks_about"] = ""
df["sentiment"] = ""

# Classification logic
def classify_review(review_text):
    prompt = (
        f"Review: {review_text}\n\n"
        "Classify the review into one of the following categories:\n"
        f"{', '.join(candidate_labels)}.\n"
        "Also, determine whether the sentiment is Positive or Negative."
    )
    
    # Generate text using the pipeline
    response = pipe(prompt, max_length=200, num_return_sequences=1)
    generated_text = response[0]['generated_text']
    
    # Extract category and sentiment from the response
    category = next((label for label in candidate_labels if label in generated_text), "Other")
    sentiment = "Positive" if "Positive" in generated_text else "Negative"
    return category, sentiment

# Apply classification with progress bar
print("Classifying reviews...")
for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
    category, sentiment = classify_review(row[review_column])
    df.at[idx, "talks_about"] = category
    df.at[idx, "sentiment"] = sentiment

# Save the classified data
output_file = "data/reviews_with_sentiments_llama.csv"
df.to_csv(output_file, index=False)
print(f"Classification complete. Results saved to '{output_file}'.")
