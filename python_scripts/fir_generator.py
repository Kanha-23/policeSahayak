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

def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
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
        offense_type = "cognizable" if most_similar_section and most_similar_section["Cognizable"].lower() == "cognizable" else "non-cognizable"
        print(offense_type)
        return

    # Determine whether to generate FIR or Warrant
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

# import sys
# import json
# from difflib import SequenceMatcher
# from fpdf import FPDF
# from pymongo import MongoClient


# def similar(a, b):
#     return SequenceMatcher(None, a, b).ratio()

# def find_most_similar_section(complaint, sections):
#     max_similarity = 0
#     most_similar_section = None
    
#     for section in sections:
#         similarity = similar(complaint, section["Offense"])
#         if similarity > max_similarity:
#             max_similarity = similarity
#             most_similar_section = section

#     return most_similar_section

# def generate_fir_pdf(complainant_info, offense_info):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     # pdf.cell(200, 10, txt="First Information Report (FIR)", ln=1, align="C")
#     # pdf.ln(10)

#     pdf.multi_cell(0, 10, txt=complainant_info, align="L")
#     pdf.ln(10)

#     pdf.multi_cell(0, 10, txt=offense_info, align="L")

#     pdf.output("public/pdfs/FIR_Report.pdf")

# def main():
#     # Ensure the correct number of command line arguments
#     if len(sys.argv) != 2:
#         print("Usage: python fir_generator.py <complaint>")
#         sys.exit(1)

#     complaint_id = sys.argv[1]
#     print("Searching for complaint:", complaint_id)


#     # Connect to MongoDB
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['RJPOLICE_HACK']  # Your database name
#     collection = db['complains']  # Your collection name

#     # Load data from a JSON file containing offense sections
#     with open("csvjson.json", "r", encoding="utf-8") as file:
#         data = json.load(file)

#     most_similar_section = find_most_similar_section(complaint_id, data)
    
#     offense_info = ""  # Declare offense_info outside the if-else blocks

#     if most_similar_section and most_similar_section["Cognizable"].lower() == "cognizable":
#         # Retrieve complainant information from the database
#         # Change the query to use _id
#         complainant_data = collection.find_one({ "dis": complaint_id })

#         print("Complaint Data:", complainant_data)
#         if complainant_data:
#             complainant_name = complainant_data["name"]
#             complainant_age = complainant_data["age"]
#             complainant_occupation = complainant_data["occupation"]
#             complainant_city = complainant_data["city"]
#             complainant_pincode = complainant_data["pin"]
#             complainant_contact = complainant_data["number"]
#             complainant_date = complainant_data["date"].strftime("%B %d, %Y") if complainant_data["date"] else ""
#             complainant_dis = complainant_data["dis"]
#             complainant_loc = complainant_data["loc"]
#             complainant_details = complainant_data["detail"]
#             accused_name=complainant_data["aname"]
#             accused_age=complainant_data["aage"]
#             accused_occupation=complainant_data["aoccupation"]
#             accused_city=complainant_data["acity"]
#             accused_address=complainant_data["aaddress"]


#             # Update the complainant_info string with dynamic values
#             complainant_info = f"""
#                                                    First Information Report (FIR)  

                                                    
#             [Complainant Information]
#             Name: {complainant_name}
#             Age: {complainant_age}
#             Occupation: {complainant_occupation}
#             City: {complainant_city}
#             Pin Code: {complainant_pincode}
#             Contact Information: {complainant_contact}
#             Date: {complainant_date}
            
            
#             To,

#             The Officer in Charge,
#             {complainant_city} Police,


#             Sir/Madam,

#             [{complainant_name}], [{complainant_age}], [{complainant_occupation}], residing at [{complainant_city}], [{complainant_pincode}], contactable at [{complainant_contact}], would like to file an FIR against {accused_name}, {accused_age}, {accused_occupation}, residing at {accused_address}, {accused_city} , for the following criminal offenses committed on {complainant_date} at {complainant_loc}:

            

            
#             Subject: {complainant_dis}
            
#             [Description of the Offense]

#             {complainant_details}


#             I request the police to take immediate action against the accused and conduct a thorough investigation into the matter. I am willing to cooperate fully and provide any necessary information to assist in the investigation.

#             Enclosed herewith are any supporting documents, if applicable.

#             Thank you for your prompt attention to this matter.

#             Yours faithfully,
#             {complainant_name}
#             {complainant_contact}
#             """

#             offense_info = f"""
#             Category of: {most_similar_section["Cognizable"]}

#             """

#             generate_fir_pdf(complainant_info, offense_info)
#             print("FIR PDF generated successfully.")

#         else:
#             print("Complainant data not found in the database.")
#     else:
#         print("No matching or non-cognizable section found.")
#         complainant_data = collection.find_one({ "dis": complaint_id })

#         if complainant_data:
#             complainant_name = complainant_data["name"]
#             complainant_age = complainant_data["age"]
#             complainant_occupation = complainant_data["occupation"]
#             complainant_city = complainant_data["city"]
#             complainant_pincode = complainant_data["pin"]
#             complainant_contact = complainant_data["number"]
#             complainant_date = complainant_data["date"].strftime("%B %d, %Y") if complainant_data["date"] else ""
#             complainant_dis = complainant_data["dis"]
#             complainant_loc = complainant_data["loc"]
#             complainant_details = complainant_data["detail"]
#             accused_name = complainant_data["aname"]
#             accused_age = complainant_data["aage"]
#             accused_occupation = complainant_data["aoccupation"]
#             accused_city = complainant_data["acity"]
#             accused_address = complainant_data["aaddress"]

#             # Update the complainant_info string with dynamic values for court warrant or FIR
#             complainant_info = f"""
#             AS FOLLOWING COMPLAIN FALLS UNDER NON COGNIZABLE OFFENCES SEARCH WARRANT APPROVAL REQUIRE TO START INVESTIGATION ABOUT THIS CASE. FILL THE DETAILS AS GUIDED

#                                                [Your Police Department's Letterhead]

#                                                            SEARCH WARRANT


#             To: __________________[Judge's Full Name]
#                 __________________[Judge's Title]
#                 __________________[Address of the Court]

#             Application for a Search Warrant

#             I, ________________[Your Full Name], __________________[Your Rank/Title] of the ____________________[Your Police Department], hereby apply for a search warrant to search the premises located at:

#             [{accused_address} , {accused_city}]___________

#             This application is based upon the following grounds:

#             1. [{complainant_dis}]

#             2. ______________________________________________________[Provide specific information justifying the need for a search]

#             3. ______________________________________________________[Include any witness statements or other supporting evidence]

#             I believe that the following items related to the criminal activity are present on the premises:

#             ___________________________________________________________[List the items to be searched for, e.g., illegal substances, weapons, etc.]

#             The supporting affidavit and any other documents are attached herewith.

#             I request that the search warrant be issued to authorize [Your Name] and other officers named in the attached affidavit to enter the premises, search for the items described, and seize any evidence related to the criminal activity.
#             I declare under penalty of perjury that the foregoing is true and correct.

#             Date: [Current Date]
#             Place: [City/Location]

#             ____________________[Your Full Name]
#             ____________________[Your Rank/Title]
#             ____________________[Your Signature]

#             ---------------
#             [Judge's Response Section]

#             Search Warrant

#             To: ______________________________[Your Full Name]
#                 ______________________________[Your Rank/Title]
#                 ______________________________[Your Police Department]

#             Upon consideration of the application and supporting affidavit, I find probable cause to believe that the items described are located on the premises identified. Therefore, you are hereby authorized to execute the search warrant at the premises listed above.

#             This warrant is valid for execution between [Start Date and Time] and [End Date and Time].

#             ___________________[Judge's Full Name]
#             ___________________[Judge's Signature]
#             ___________________[Date Issued]

#             """
#             # offense_info can be populated with relevant information for court warrant or FIR

#             generate_fir_pdf(complainant_info, offense_info)
#             print("Court Warrant / FIR PDF generated successfully.")
#         else:
#             print("Complainant data not found in the database.")

# if __name__ == "__main__":
#     main()
