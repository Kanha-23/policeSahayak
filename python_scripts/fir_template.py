def generate_fir_text(complainant_data, most_similar_section):
   return f"""
   
    COMPLAINANT INFORMATION:
    Name: {complainant_data["name"]}
    Age: {complainant_data["age"]}
    Occupation: {complainant_data["occupation"]}
    City: {complainant_data["city"]}
    Pin Code: {complainant_data["pin"]}
    Contact Information: {complainant_data["number"]}
    Date: {complainant_data["date"].strftime("%B %d, %Y") if complainant_data["date"] else ""}

    POLICE DETAILS:
    To: The Officer in Charge
    {complainant_data["city"]} Police Station

    SUBJECT: {complainant_data["dis"]} 

    DESCRIPTION: 
    {complainant_data["detail"]}

    I request the police to take immediate action against the accused thorough investigation.

    Yours faithfully,
    {complainant_data["name"]}
    Signature:---------------
    """