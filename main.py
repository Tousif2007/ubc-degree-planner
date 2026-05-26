# UBC Degree Planner - Core Engine

my_transcript = {
    "CPSC 103": [3.0, 71],
    "MATH 100": [3.0, 71],
    "PHYS 131": [3.0, 77],
    "SCIE 113": [3.0, 82],
    "DSCI 100": [3.0, 62],
    "CPSC 107": [3.0, 76],
    "MATH 101": [3.0, 69],
    "ENGL 110":  [3.0, 80],
    "BIO 111":  [3.0, 92],
    "PHYS 119": [1.0, 83]
}

def calculate_stats(transcript):
    total_credits = 0.0
    total_weighted_grades = 0.0 
    for course, data in transcript.items():
        credits = data[0]
        grade = data[1]
        total_credits += credits
        total_weighted_grades += credits * grade
    average = total_weighted_grades / total_credits
    return total_credits, average



# Database of UBC Science specializations, their history, and what you need to get in
# Each entry maps out both the entry barrier (cutoffs) and the full 4-year path
majors_database = {
    "Data Science": {
        "cutoffs": {2025: 76.0},
        # Need one course from each group listed below 
        "first_year_reqs": [["MATH 100", "MATH 102", "MATH 104", "MATH 180"], "DSCI 100", ["CPSC 103", "CPSC 110"]],
        "grad_requirements": {
            # The core courses you'll need to take in second year and beyond
            "Second Year Core": ["DSCI 200", "DSCI 220", "DSCI 221", ["MATH 200", "MATH 226"], ["MATH 221", "MATH 152"], ["STAT 201", "STAT 200"]],
            "Upper Year Core": ["CPSC 330", "CPSC 368", "DSCI 310", "DSCI 320", "DSCI 430", "STAT 301"]
        }
    },
    "Biochemistry": {
        "cutoffs": {2025: 76.7, 2024: 65.9, 2023: 76.4, 2022: 71.0, 2021: 71.4},
        # You need these specific required courses to start the major
        "first_year_reqs": ["BIOL 112", ["CHEM 121", "CHEM 111"], ["MATH 100", "MATH 102", "MATH 104", "MATH 180"]],
        "grad_requirements": {
            # The required classes to get your degree in Biochem
            "Second Year Core": [["BIOC 202", "BIOL 201"], "BIOL 200", ["CHEM 203", "CHEM 233"], ["CHEM 213", "CHEM 235"], "CHEM 205"],
            "Upper Year Core": ["BIOC 301", "BIOC 302", "BIOC 303", "BIOC 402", "BIOC 403", "BIOL 335"]
        }
    },
    "Physics": {
        "cutoffs": None,
        "first_year_reqs": [
            "SCIE 113",
            ["CHEM 121", "CHEM 111"],
            ["MATH 100", "MATH 102", "MATH 104", "MATH 180"],
            ["MATH 101", "MATH 103", "MATH 105"],
            ["PHYS 117", "PHYS 106", "PHYS 107"],
            ["PHYS 118", "PHYS 108"],
            "PHYS 119"
        ],
        "grad_requirements": {
            "Second Year Core": ["MATH 200", ["MATH 215", "MATH 221"], ["PHYS 200", "PHYS 216"], ["PHYS 219", "PHYS 229"], "PHYS 210"],
            "Upper Year Core": ["MATH 317", "PHYS 203", ["PHYS 309", "PHYS 319"], ["PHYS 312", "MATH 316"], "PHYS 304"]
        }
    },
    "Mathematics": {
        "cutoffs": {2025: None, 2024: 67.0, 2023: 76.3, 2022: 69.1, 2021: 65.1},
        "first_year_reqs": [
            "SCIE 113",
            ["MATH 100", "MATH 102", "MATH 104", "MATH 120", "MATH 180", "MATH 184"],
            ["MATH 101", "MATH 103", "MATH 105", "MATH 121"],
            "PHYS 100-level",
            ["CPSC 110", "CPSC 103"]
        ],
        "grad_requirements": {
            "Second Year Core": ["MATH 200", "MATH 220", ["MATH 221", "MATH 223", "MATH 215"], ["CPSC 210", "MATH 210"]],
            "Upper Year Core": ["MATH 300-level", "MATH/STAT/CPSC 300-level"]
        }
    }
}
    





import re # This allows us to use pattern matching for "PHYS 100-level"

def check_requirement(req, transcript):
    """
    Determines if a course requirement is satisfied.
    - Handles 'OR' logic for lists.
    - Handles 'Category' logic (e.g., 'PHYS 100-level').
    - Handles standard single course requirements.
    """
    
    # CASE 1: 'OR' logic
    if isinstance(req, list):
        return any(check_requirement(r, transcript) for r in req)
    
    # CASE 2: Special 'Category' logic (e.g., 'PHYS 100-level')
    if "-level" in req:
        # Splits 'PHYS 100-level' into "PHYS" and "1"
        subject, level_info = req.replace("-level", "").split(" ")
        pattern = rf"^{subject} {level_info[0]}"
        # Checks if any course in your transcript matches the pattern
        return any(re.match(pattern, course) for course in transcript)
        
    # CASE 3: Standard single course check
    return req in transcript
    
    
def audit_major(major_name, transcript):
    """
    Performs a check against the majors_database to find missing courses.
    Provides a status report per requirement.
    """
    if major_name not in majors_database:
        print(f"Error: {major_name} not found in database.")
        return
    
    major_data = majors_database[major_name]
    print(f"\n--- Progress Review: {major_name} ---")
    
    # Iterate through first-year requirements and validate against transcript
    for req in major_data["first_year_reqs"]:
        
        # Check if the requirement is satisfied
        if check_requirement(req, transcript):
            status = "Met"
        else:
            status = "MISSING"
            
        print(f"Requirement {req}: {status}")

audit_major("Biochemistry", my_transcript)
audit_major("Data Science", my_transcript) 
audit_major("Physics", my_transcript)
audit_major("Mathematics", my_transcript)