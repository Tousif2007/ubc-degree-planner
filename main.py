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
}

