import os
import re
import nltk
from nltk.tokenize import word_tokenize
import pandas as pd

# Ensure necessary resources are downloaded
nltk.download('punkt')

# Function to load word lists from a file
def load_word_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = set(file.read().split())
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            words = set(file.read().split())
    return words

# Load positive and negative word lists
positive_words_file = './positive-words.txt'
negative_words_file = './negative-words.txt'

positive_words = load_word_list(positive_words_file)
negative_words = load_word_list(negative_words_file)

# Function to clean and tokenize text
def tokenize_text(text):
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    return words

# Function to calculate sentiment scores
def calculate_sentiment_scores(tokens):
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to analyze text files and calculate sentiment scores
def analyze_text_files(text_files_dir, output_file):
    results = []
    
    for filename in os.listdir(text_files_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_files_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            tokens = tokenize_text(text)
            positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(tokens)
            
            results.append({
                'filename': filename,
                'positive_score': positive_score,
                'negative_score': negative_score,
                'polarity_score': polarity_score,
                'subjectivity_score': subjectivity_score
            })
    
    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Sentiment analysis results saved to {output_file}")

# Specify the directories and files
text_files_dir = './cleaned_stopWords_files'  # Directory containing cleaned text files
output_file = './output_4score.csv'  # Output CSV file for sentiment analysis results

# Analyze the text files and calculate sentiment scores
analyze_text_files(text_files_dir, output_file)
