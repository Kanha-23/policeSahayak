def generate_warrant_text(complainant_data):
    return f"""
    SEARCH WARRANT

    To: __________________[Judge's Full Name]
        __________________[Judge's Title]
        __________________[Court Address]

    Application for a Search Warrant

    I, ________________[Your Full Name], __________________[Your Rank/Title] of the ____________________[Your Police Department], hereby apply for a search warrant to search the premises located at:

    [{complainant_data["aaddress"]}, {complainant_data["acity"]}]

    Grounds for search:
    1. {complainant_data["dis"]}
    2. Evidence available in the complaint
    
    I request that the search warrant be issued to authorize officers to enter the premises and seize evidence.

    Date: [Current Date]
    Place: [City]

    ____________________[Your Name]
    ____________________[Your Rank]
    ____________________[Signature]
    """
