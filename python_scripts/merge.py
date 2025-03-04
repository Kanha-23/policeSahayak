import sys
import pytesseract
from pytesseract import Output
import PIL.Image
import cv2
import json
from difflib import SequenceMatcher

# Global variable to store most similar punishment
most_similar_punishment = None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_top_cognizable_sections(complaint, sections, top_n=4):
    similarities = []

    for section in sections:
        similarity = similar(complaint, section["Offense"])
        if section.get("Cognizable", "").lower() == "cognizable":
            similarities.append((section, similarity))

    # Sort sections based on similarity in descending order
    sorted_sections = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Take the top N sections
    top_sections = sorted_sections[:top_n]

    return top_sections

def store_most_similar_punishment(top_sections):
    global most_similar_punishment
    if top_sections:
        most_similar_punishment = top_sections[0][0]["Punishment"]

def get_most_similar_punishment():
    global most_similar_punishment
    return most_similar_punishment

def ocr(image_path):
    myconfig = r"--psm 3 --oem 3"
    img = cv2.imread(image_path)
    extracted_text = pytesseract.image_to_string(PIL.Image.open(image_path), config=myconfig)
    print(extracted_text)
    return extracted_text

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

    # Get the top 4 most similar cognizable sections
    top_sections = find_top_cognizable_sections(extracted_text, section_data, top_n=4)

    # Store the punishment of the most similar section
    store_most_similar_punishment(top_sections)
    
    if top_sections:
        print("\nTop 4 Cognizable Sections with Highest Similarity:")
        for section, similarity in top_sections:
            print("-" * 200)
            print("\nDescription:", section["Description"])
            print("\nSection:", section["IPC-Section"])
            print("\nSection Category:", section["Cognizable"])
            print("\nSection Punishment:", section["Punishment"])
            print("\nSimilarity Score:", similarity)
            print("\n")
        print("-" * 200)
        print("\n\n\n")
    else:
        print("No matching cognizable section found for the extracted text.")

if __name__ == "__main__":
    main()
