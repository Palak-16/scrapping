import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

# Function to fetch and extract article title and text
def extract_article_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Assuming the article title is within <h1> tag and article text within <p> tags
    title = soup.find('h1', class_='entry-title')
    if not title:
        title = soup.find('h1', class_='tdb-title-text')
    
    title = title.get_text()

    paragraphs = soup.find('div',class_='td-post-content')
    if not paragraphs:
        paragraphs = soup.find('div',class_='tdb-block-inner')

    article_text = paragraphs.get_text()
    
    return title, article_text

# Load the input file
input_file_path = './input.csv'
df = pd.read_csv(input_file_path)

# Create a directory to save the articles if it doesn't exist
output_dir = './output pdfs'
os.makedirs(output_dir, exist_ok=True)

# Process each URL
for index, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    try:
        title, article_text = extract_article_text(url)
        
        # Save the article text in a text file named with URL_ID
        file_path = os.path.join(output_dir, f"{url_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"{title}\n\n{article_text}")
        
        print(f"Saved article: {url_id}")
    except Exception as e:
        print(f"Failed to process URL {url}: {e}")

print("All articles have been processed.")

