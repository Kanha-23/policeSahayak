import sys
import json
from pymongo import MongoClient
from fpdf import FPDF
from difflib import SequenceMatcher
from fir_template import generate_fir_text
from warrant_template import generate_warrant_text
from bson import ObjectId

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def find_most_similar_section(complaint, sections):
    max_similarity = 0
    most_similar_section = None
    
    for section in sections:
        similarity = similar(complaint, section["Offense"])
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_section = section

    return most_similar_section

class CustomPDF(FPDF):
    def header(self):
        """ Set background color for all pages """
        self.set_fill_color(255, 232, 168)  #  background
        self.rect(0, 0, 210, 297, 'F')  # Full page A4 background

    def add_formatted_text(self, content):
        """ Add formatted text to the PDF """
        self.set_text_color(0, 0, 0)  # Black text
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, content, align='L')

def generate_pdf(content, filename):
    pdf = CustomPDF()
    pdf.add_page()
    
    title = "First Information Report (FIR)" if "FIR" in filename else "SEARCH WARRANT"
    
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10,title, ln=True, align='C')
    pdf.ln(10)  # Line break

    pdf.set_font("Arial", size=12)
    pdf.add_formatted_text(content)

    pdf.output(f"public/pdfs/{filename}")



def main():
    if len(sys.argv) < 2:
        print("Usage: python fir_generator.py <complaint_id> [--check-only] [--warrant]")
        sys.exit(1)

    complaint_id = sys.argv[1]
    check_only = "--check-only" in sys.argv
    warrant_mode = "--warrant" in sys.argv

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['RJPOLICE_HACK']
    collection = db['complains']

    try:
        # Fetch complaint details from MongoDB
        complainant_data = collection.find_one({"_id": ObjectId(complaint_id)})  # Ensure correct MongoDB lookup
    except:
        complainant_data = collection.find_one({"_id": complaint_id})  # If not ObjectId, try as string

    if not complainant_data:
        print("Complaint not found")
        return

    complaint_text = complainant_data.get("dis", "")  # Extract the description field

    # Load offense sections
    with open("csvjson.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    # Match offense using the actual complaint description (not ID)
    most_similar_section = find_most_similar_section(complaint_text, data)

    if check_only:
        similarity_score = similar(complaint_text, most_similar_section["Offense"]) if most_similar_section else 0
        offense_type = "cognizable" if most_similar_section and most_similar_section["Cognizable"].lower() == "cognizable" else "non-cognizable"
        
        print(f"{offense_type} | {similarity_score:.2f}")  # Output both type and similarity score
        return

    # Generate FIR or Warrant based on request
    if warrant_mode or (most_similar_section and most_similar_section["Cognizable"].lower() != "cognizable"):
        content = generate_warrant_text(complainant_data)
        generate_pdf(content, "Warrant_Report.pdf")
        print("Warrant PDF generated.")
    else:
        content = generate_fir_text(complainant_data, most_similar_section)
        generate_pdf(content, "FIR_Report.pdf")
        print("FIR PDF generated.")

if __name__ == "__main__":
    main()
