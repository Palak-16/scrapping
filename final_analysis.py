import os
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

# Ensure necessary resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Function to load stop words from a directory
def load_stop_words(stop_words_dir):
    stop_words = set()
    for filename in os.listdir(stop_words_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(stop_words_dir, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    stop_words.update(file.read().split())
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as file:
                    stop_words.update(file.read().split())
    return stop_words

# Define function to clean and tokenize text by removing only stop words
def clean_and_tokenize(text, stop_words):
    words = word_tokenize(text)  # Tokenize without converting to lowercase or removing punctuation
    cleaned_words = [word for word in words if word.lower() not in stop_words]
    return cleaned_words

# Define function to clean text files
def clean_text_files(text_files_dir, output_dir, stop_words):
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(text_files_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_files_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            cleaned_words = clean_and_tokenize(text, stop_words)
            cleaned_text = ' '.join(cleaned_words)
            
            output_file_path = os.path.join(output_dir, filename)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(cleaned_text)
            
            print(f"Cleaned file: {filename}")

# Function to load word lists from a file
def load_word_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            words = set(file.read().split())
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin-1') as file:
            words = set(file.read().split())
    return words

# Function to tokenize text
def tokenize_text(text):
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    return words

# Function to calculate sentiment scores
def calculate_sentiment_scores(tokens, positive_words, negative_words):
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

# Function to count syllables in a word
def count_syllables(word):
    word = word.lower()
    syllables = 0
    vowels = "aeiou"
    if word[0] in vowels:
        syllables += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllables += 1
    if word.endswith("es") or word.endswith("ed"):
        syllables -= 1
    if syllables == 0:
        syllables += 1
    return syllables

# Function to count complex words
def count_complex_words(tokens):
    return sum(1 for word in tokens if count_syllables(word) > 2)

# Function to analyze text files and calculate various metrics
def analyze_text_files(input_df, text_files_dir, output_file, positive_words, negative_words):
    results = []
    
    for index, row in input_df.iterrows():
        url_id = row['URL_ID']
        filename = f"{url_id}.txt"
        file_path = os.path.join(text_files_dir, filename)
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            tokens = tokenize_text(text)
            sentences = sent_tokenize(text)
            
            # Calculate Sentiment Scores
            positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(tokens, positive_words, negative_words)
            
            # Calculate Word Count
            word_count = len(tokens)
            
            # Calculate Complex Word Count
            complex_word_count = count_complex_words(tokens)
            
            # Calculate Average Sentence Length (based on characters)
            total_characters = sum(len(sentence) for sentence in sentences)
            avg_sentence_length_chars = total_characters / len(sentences)
            
            # Calculate Average Number of Words Per Sentence
            avg_sentence_length_words = word_count / len(sentences)
            
            # Calculate Percentage of Complex Words
            percent_complex_words = complex_word_count / word_count
            
            # Calculate Fog Index
            fog_index = 0.4 * (avg_sentence_length_words + percent_complex_words)
            
            # Calculate Syllables per Word
            syllable_count = sum(count_syllables(word) for word in tokens)
            syllables_per_word = syllable_count / word_count
            
            # Calculate Personal Pronouns
            personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
            
            # Calculate Average Word Length
            avg_word_length = sum(len(word) for word in tokens) / word_count
            
            results.append({
                'URL_ID': url_id,
                'URL': row['URL'],
                'positive_score': positive_score,
                'negative_score': negative_score,
                'polarity_score': polarity_score,
                'subjectivity_score': subjectivity_score,
                'word_count': word_count,
                'complex_word_count': complex_word_count,
                'avg_sentence_length_chars': avg_sentence_length_chars,
                'avg_sentence_length_words': avg_sentence_length_words,
                'percent_complex_words': percent_complex_words,
                'fog_index': fog_index,
                'syllables_per_word': syllables_per_word,
                'personal_pronouns': personal_pronouns,
                'avg_word_length': avg_word_length
            })
    
    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Analysis results saved to {output_file}")

# Specify the directories and files
stop_words_dir = './StopWords'  # Directory containing stop words files
text_files_dir = './output pdfs'  # Directory containing text files to be cleaned
cleaned_text_files_dir = './cleaned_stopWords_files'  # Directory for cleaned text files
positive_words_file = './sentiment/positive-words.txt'
negative_words_file = './sentiment/negative-words.txt'
input_file = './input.csv'  # Input CSV file with URL_ID and URL
output_file = './final_output.csv'  # Output CSV file for analysis results

# Load input file
input_df = pd.read_csv(input_file)

# Load stop words
stop_words = load_stop_words(stop_words_dir)

# Clean the text files
clean_text_files(text_files_dir, cleaned_text_files_dir, stop_words)

# Load positive and negative word lists
positive_words = load_word_list(positive_words_file)
negative_words = load_word_list(negative_words_file)

# Analyze the text files and calculate all metrics
analyze_text_files(input_df, cleaned_text_files_dir, output_file, positive_words, negative_words)
