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

credits, avg = calculate_stats(my_transcript)
print(f"Total Credits: {credits} | Cumulative Average: {avg:.2f}%")
