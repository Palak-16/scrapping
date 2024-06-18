import os
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
import pandas as pd

# Ensure necessary resources are downloaded
nltk.download('punkt')

# Function to load word lists from a file
def load_word_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = set(file.read().split())
    return words

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
def analyze_text_files(text_files_dir, output_file):
    results = []
    
    for filename in os.listdir(text_files_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(text_files_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            
            tokens = word_tokenize(text.lower())
            sentences = sent_tokenize(text)
            
            # Calculate Word Count
            word_count = len(tokens)
            
            # Calculate Complex Word Count
            complex_word_count = count_complex_words(tokens)
            
            # Calculate Average Sentence Length
            avg_sentence_length = word_count / len(sentences)
            
            # Calculate Percentage of Complex Words
            percent_complex_words = complex_word_count / word_count
            
            # Calculate Fog Index
            fog_index = 0.4 * (avg_sentence_length + percent_complex_words)
            
            # Calculate Syllables per Word
            syllable_count = sum(count_syllables(word) for word in tokens)
            syllables_per_word = syllable_count / word_count
            
            # Calculate Personal Pronouns
            personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))
            
            # Calculate Average Word Length
            avg_word_length = sum(len(word) for word in tokens) / word_count
            
            results.append({
                'filename': filename,
                'word_count': word_count,
                'complex_word_count': complex_word_count,
                'avg_sentence_length': avg_sentence_length,
                'percent_complex_words': percent_complex_words,
                'fog_index': fog_index,
                'syllables_per_word': syllables_per_word,
                'personal_pronouns': personal_pronouns,
                'avg_word_length': avg_word_length
            })
    
    # Save results to a CSV file
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Readability analysis results saved to {output_file}")

# Specify the directories and files
text_files_dir = './output pdfs'  # Directory containing cleaned text files
output_file = './final_output.csv'  # Output CSV file for readability analysis results

# Analyze the text files and calculate readability metrics
analyze_text_files(text_files_dir, output_file)
