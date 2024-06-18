import os
import re
import nltk
from nltk.tokenize import word_tokenize

# Ensure necessary resources are downloaded
nltk.download('punkt')

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

# Define function to clean and tokenize text
def clean_and_tokenize(text, stop_words):
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = word_tokenize(text.lower())  # Tokenize and convert to lowercase
    cleaned_words = [word for word in words if word not in stop_words]
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

# Specify the directories
stop_words_dir = './StopWords'  # Directory containing stop words files
text_files_dir = './output pdfs'  # Directory containing text files to be cleaned
output_dir = './cleaned_stopWords_files'  # Output directory for cleaned files

# Load stop words
stop_words = load_stop_words(stop_words_dir)

# Clean the text files
clean_text_files(text_files_dir, output_dir, stop_words)
