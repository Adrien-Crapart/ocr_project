import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import psycopg2
import cv2
from datetime import datetime
from collections import Counter

# Replace these with your database credentials
db_config = {
    'dbname': 'data',
    'user': 'adrien',
    'password': 'adrien9583!',
    'host': 'localhost',
    'port': '5432'
}

conn = psycopg2.connect(**db_config)

# Example data
document_name = "2 Projet d'Aménagement et de Développement Durable"
present_tags = ['règlement', 'zone']
source = 'Sample Source'


def definition_of_tags(text):
    words = text.split()
    tags_and_words = {
        "règlement écrit": ["stationnement", "surface", "plancher", "zone", "occupations", "utilisations", "sol", "article"],
        "zonage": ["zone", "stationnement", "occupations", "utilisations"],
        "padd": ["developpement", "services", "secteurs", "protéger", "maitriser", "trame", "préserver", "améliorer", "ville-center", "reconquete", "zones", "équipements", "urbain", ""]
    }

    stop_words = ["de", "du", "les", "des", "et", "ou", "a", "la", "-", "que", "au", "en", "étre", "par", "doit", "est", "une", "tout", "un", "aux",
                  "doivent", "sur", "ainsi", "lequel", "pour", "dans", "vers", "le", "m", "m.", "d'un", "d'une", "d’une", "d’un", "m?", "leur", "leurs", "il", "elle", "ils", "elles",
                  ":", ".", ",", ";", ":", "ne", "=", "/", "|", ""]
    filtered_words = [word for word in words if word.lower() not in stop_words]
    word_counts = Counter(filtered_words)
    top_words = word_counts.most_common(5)
    print(top_words)

    # Initialize a list and a set to store tagged words
    tagged_words = []
    unique_tagged_words = set()

    # Initialize dictionaries to store word counts and tag counts
    word_counts = {}
    tag_counts = {}
    tagged_words_by_tag = {}

    # Iterate through words and apply tags based on word lists
    for word in words:
        for tag, word_list in tags_and_words.items():
            if word.lower() in word_list:
                tagged_word = (word, tag)
                if tag not in tagged_words_by_tag:
                    tagged_words_by_tag[tag] = []
                tagged_words_by_tag[tag].append(tagged_word)
                word_counts[word] = word_counts.get(word, 0) + 1
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # Calculate the total percentage for each tag and store in a dictionary
    tag_percentages = {}
    total_percentage = 0
    for tag, tagged_words in tagged_words_by_tag.items():
        total_count_for_tag = tag_counts[tag]
        tag_percentage = sum(
            word_counts[word] / total_count_for_tag * 100 for word, _ in tagged_words)
        tag_percentages[tag] = tag_percentage
        total_percentage += tag_percentage

    if total_percentage == 0:
        return []
    scaling_factor = 100 / total_percentage
    for tag in tag_percentages:
        tag_percentages[tag] *= scaling_factor
    results = []
    for tag, normalized_percentage in tag_percentages.items():
        results.append(tag)
        print(
            f"Tag: {tag} ({normalized_percentage}%)")

    return results


def extract_txt_from_pdf(conn, document_name, source):
    # Convert PDF to images
    pages = convert_from_path(f'pdfs/{document_name}.pdf')
    postgres_write = True

    # Apply OCR to each page
    if postgres_write == True:
        cursor = conn.cursor()
    for i, page in enumerate(pages):
        extracted_text = pytesseract.image_to_string(page)
        if postgres_write == True:
            cursor.execute(
                """INSERT INTO pdf_text (document_name,
                    page_number,
                    text_content,
                    present_tags,
                    source,
                    upload_date,
                    user_reading
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (document_name, i + 1, extracted_text, definition_of_tags(extracted_text), source, str(datetime.now()), False))
            conn.commit()
        else:
            with open(f'page_{i + 1}.txt', 'w', encoding='utf-8') as text_file:
                text_file.write(extracted_text)

    if postgres_write == True:
        cursor.close()
        conn.close()


extract_txt_from_pdf(conn, document_name, source)
