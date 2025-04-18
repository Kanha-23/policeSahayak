import sys
import pytesseract
from pytesseract import Output
import PIL.Image
import cv2
import json
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Global variable to store most similar punishment
most_similar_punishment = None
output_data = []

def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_top_cognizable_sections(complaint, sections, top_n=10, threshold=0.3):
    complaint_words = set(complaint.lower().split())
    similarities = []

    # Define relevant keywords
    relevant_keywords = set([
        "theft", "robbery", "steal", "burglary", "dacoity", "looting", "snatch", "purse", "shoplifting",
        "attack", "assault", "injured", "hurt", "grievous", "murder", "homicide", "rape", "kidnapping",
        "fraud", "cheating", "bribery", "extortion", "forgery", "counterfeit", "blackmail", "threat",
        "cyber", "hacking", "phishing", "stalking", "domestic violence", "dowry", "suicide", "narcotics",
        "sedition", "hate speech", "riot", "illegal"
    ])

    # Filter complaint words based on relevant keywords
    filtered_complaint_words = complaint_words.intersection(relevant_keywords)

    if not filtered_complaint_words:
        return []  # No relevant words found

    for section in sections:
        section_text = section["Offense"].lower()
        section_words = set(section_text.split())

        if not section_words:
            continue

        # Calculate maximum similarity score
        similarities_list = [similar(word, section_word) for word in filtered_complaint_words for section_word in section_words]
        max_similarity = max(similarities_list, default=0)

        if max_similarity > threshold and section.get("Cognizable", "").lower() == "cognizable":
            similarities.append((section, max_similarity))

    sorted_sections = sorted(similarities, key=lambda x: x[1], reverse=True)
    return sorted_sections[:top_n]

def store_most_similar_punishment(top_sections):
    global most_similar_punishment
    if top_sections:
        most_similar_punishment = top_sections[0][0].get("Punishment", "Not Available")

def get_most_similar_punishment():
    return most_similar_punishment

def ocr(image_path):
    myconfig = r"--psm 3 --oem 3"
    img = cv2.imread(image_path)
    extracted_text = pytesseract.image_to_string(PIL.Image.open(image_path), config=myconfig)
    return extracted_text.strip().lower()

def main():
    if len(sys.argv) < 2:
        print("Usage: python merge.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    extracted_text = ocr(image_path)

    if not extracted_text:
        print("No relevant text extracted.")
        return

    with open("csvjson.json", "r", encoding="utf-8") as file:
        section_data = json.load(file)

    for section in section_data:
        section["Offense"] = section["Offense"].lower()
        section["Cognizable"] = section.get("Cognizable", "").lower()
        if "Punishment" in section:
            section["Punishment"] = section["Punishment"].lower()

    top_sections = find_top_cognizable_sections(extracted_text, section_data, top_n=4)
    store_most_similar_punishment(top_sections)

    output_data.append({"Extracted_Text": extracted_text})
    
    if top_sections:
        for section, similarity in top_sections:
            output_data.append({
                "Offense": section["Offense"],
                "IPC-Section": section["IPC-Section"],
                "Description": section["Description"],
                "SimilarityScore": round(similarity * 100, 2)
            })

    print(json.dumps(output_data, indent=4))

if __name__ == "__main__":
    main()

