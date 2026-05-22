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


# Master Database of UBC Science Specialization Requirements & Quotas
majors_database = {
    "Data Science": {
        "cutoffs": {2025: 76.0},  # New specialization entry option as of 2025
        "first_year_reqs": ["MATH 100", "DSCI 100", "CPSC 103"]
    },
    "Biochemistry": {
        "cutoffs": {2025: 76.7, 2024: 65.9, 2023: 76.4, 2022: 71.0, 2021: 71.4},
        "first_year_reqs": ["BIOL 112", "CHEM 121", "CHEM 123", "MATH 100"]
    }
}

