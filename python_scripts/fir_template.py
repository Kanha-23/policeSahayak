def generate_fir_text(complainant_data, most_similar_section):
    return f"""
    First Information Report (FIR)  

    [Complainant Information]
    Name: {complainant_data["name"]}
    Age: {complainant_data["age"]}
    Occupation: {complainant_data["occupation"]}
    City: {complainant_data["city"]}
    Pin Code: {complainant_data["pin"]}
    Contact Information: {complainant_data["number"]}
    Date: {complainant_data["date"].strftime("%B %d, %Y") if complainant_data["date"] else ""}
    
    To,

    The Officer in Charge,
    {complainant_data["city"]} Police,

    Subject: {complainant_data["dis"]}

    [Description of the Offense]
    {complainant_data["detail"]}

    [Section Applied]: {most_similar_section["Section"]} - {most_similar_section["Description"]}

    I request the police to take immediate action against the accused and conduct a thorough investigation.

    Yours faithfully,
    {complainant_data["name"]}
    {complainant_data["number"]}
    """
