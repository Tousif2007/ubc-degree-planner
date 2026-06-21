# UBC Degree Planner - Core Engine
from pathlib import Path

def load_transcript(filename):
    """
    Reads a text file and converts it into a transcript dictionary.
    Expects comma-separated lines: 'Course Code, Credits, Grade'
    """
    new_transcript = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Skipping empty lines or spaces
                if not line.strip():
                    continue
                # Split line by comma and removing extra padding whitespace
                parts = [p.strip() for p in line.split(',')]
                if len(parts) == 3:
                    course_code, credits, grade = parts
                    new_transcript[course_code] = [float(credits), float(grade)]
        return new_transcript
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return {}
    
# Find the exact folder where main.py is saved, then look inside it for transcript.txt
transcript_path = Path(__file__).parent / "transcript.txt"
my_transcript = load_transcript(transcript_path)



def calculate_stats(transcript):
    # If the transcript is empty, stop early and return zeros safely
    if not transcript:
        return 0.0, 0.0
    
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

    "Astronomy": {
         "cutoffs": None,
        "first_year_reqs": [
            "SCIE 113",
            ["CHEM 121", "CHEM 111"],
            ["MATH 100", "MATH 102", "MATH 104", "MATH 110", "MATH 180", "MATH 184", "MATH 120"],
            ["MATH 101", "MATH 103", "MATH 105", "MATH 121"],
            ["PHYS 117", "PHYS 106", "PHYS 107"],
            ["PHYS 118", "PHYS 108"],
            ["PHYS 119", "PHYS 109"]
        ],
        "grad_requirements": {
            "Second Year Core": [
                "ASTR 200", "ASTR 205",
                "MATH 200", "MATH 317",
                ["MATH 221", "MATH 223"], "MATH 215",
                "PHYS 200", "PHYS 219", "PHYS 229",
                "PHYS 210"
            ],
            "Upper Year Core": [
                "ASTR 300",
                ["MATH 316", "PHYS 312"],
                "PHYS 203",
                "PHYS 301", "PHYS 216",
                "PHYS 408",
                ["ASTR 406", "ASTR 407"],
                "ASTR 404", "ASTR 405",
                "PHYS 304", "PHYS 403"
            ]
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
    





import re # Enables pattern matching to handle broad course requirements like 'PHYS 100-level'

def check_requirement(req, transcript):
    """
    Determines if a course requirement is satisfied.
    - Handles 'OR' logic for lists.
    - Handles 'X00-level' logic: Checks if any course in the subject 
      is equal to or greater than the specified level.
    - Handles standard single course requirements.
    """
    
    # CASE 1: 'OR' logic
    if isinstance(req, list):
        return any(check_requirement(r, transcript) for r in req)
    
# CASE 2: Numerical level logic (e.g., '300-level')
    if "-level" in req:
        subject, level_str = req.replace("-level", "").split(" ")
        threshold = int(level_str)
        
        for course in transcript:
            parts = course.split(" ")
            # Ensure it is a valid course format (e.g., "MATH 302")
            if len(parts) == 2 and parts[0] in subject.split("/"):
                # Compare the course number numerically
                if int(parts[1]) >= threshold:
                    return True
        return False
        
    # CASE 3: Standard single course check
    return req in transcript
    
    
def audit_major(major_name, transcript, mode='first'):
    if major_name not in majors_database:
        print(f"I couldn't find {major_name} in our records.")
        return
    
    major_data = majors_database[major_name]
    
    # Decide which requirements to pull based on the mode
    if mode == 'first':
        reqs_to_check = major_data["first_year_reqs"]
        title = f"First Year Progress: {major_name}"
    else:
        # Flatten all requirements into one list for the full audit
        reqs_to_check = (major_data["first_year_reqs"] + 
                         major_data["grad_requirements"]["Second Year Core"] + 
                         major_data["grad_requirements"]["Upper Year Core"])
        title = f"Full Degree Progress: {major_name}"
    
    print(f"\n--- {title} ---")

    total_credits, gpa_average = calculate_stats(transcript)
    print(f"Credits Completed: {total_credits:.1f}  |  Current Cumulative Average: {gpa_average:.1f}%")
    print("-" * (len(title) + 8))

   # --- LIVE COMPETITIVE CUTOFF CHECK ---
    cutoffs = major_data.get("cutoffs")
    if cutoffs:
        # Filter out years that are None, and find the most recent year left
        valid_years = [year for year, gpa in cutoffs.items() if gpa is not None]
        
        if valid_years:
            latest_year = max(valid_years)
            cutoff_gpa = cutoffs[latest_year]
            diff = gpa_average - cutoff_gpa
            
            print(f"Historical Cutoff ({latest_year}): {cutoff_gpa:.1f}%")
            if diff >= 0:
                print(f"Admission Status       : Competitive! 🎉 (+{diff:.1f}% above cutoff)")
            else:
                print(f"Admission Status       : Catching Up 🚀 ({abs(diff):.1f}% below cutoff)")
        else:
            print("Historical Cutoff      : No competitive cutoff cap (Minimum requirements apply).")
    else:
        print("Historical Cutoff      : No competitive cutoff data available.") 

    met_reqs = 0
    for req in reqs_to_check:
        if check_requirement(req, transcript):
            print(f"Requirement {req}: [✓] Completed")
            met_reqs += 1
        else:
            options = f" (Needs one of: {req})" if isinstance(req, list) else ""
            print(f"Requirement {req}: [ ] MISSING{options}")
            
    # Progress Bar
    total = len(reqs_to_check)
    percentage = (met_reqs / total) * 100
    bar = '█' * int(10 * met_reqs // total) + '░' * (10 - int(10 * met_reqs // total))
    
    print(f"\nOverall Progress: |{bar}| {percentage:.0f}%")

def check_breadth_requirements(transcript):
    """
    Prints out Faculty Communication & Breadth requirements to the terminal.
    Includes logic to prevent double-counting.
    """
    used_courses = set() # Tracker for no double-counting
    
    print("\n" + "="*50)
    print("      FACULTY BREADTH & COMMUNICATION AUDIT      ")
    print("="*50)
    
    # 1. Communication Evaluator
    has_scie113 = "SCIE 113" in transcript
    if has_scie113: used_courses.add("SCIE 113")
    
    additional_comm_subjects = ["ENGL", "WRDS", "ASTU"]
    additional_comm_course = None
    
    for course in transcript.keys():
        subject = course.split(" ")[0]
        if subject in additional_comm_subjects and course != "SCIE 113":
            additional_comm_course = course
            used_courses.add(course) # Mark as used
            break
            
    print("\n1. COMMUNICATION REQUIREMENT STATUS:")
    print("-" * 40)
    print(f"  SCIE 113          : {'[✓] Completed' if has_scie113 else '[ ] MISSING'}")
    print(f"  Additional Comm.  : {f'[✓] Completed ({additional_comm_course})' if additional_comm_course else '[ ] MISSING'}")
    print(f"  Overall Status    : {'✅ SATISFIED' if (has_scie113 and additional_comm_course) else '░ IN PROGRESS'}")

    # 2. Arts Breadth Evaluator
    arts_subjects = ["CRWR", "PHIL", "PSYC", "ECON", "SOCI", "HIST", "ANTH", "ASIA", "FREN", "SPAN"]
    arts_credits = 0.0
    arts_counted = []
    
    for course, data in transcript.items():
        if course in used_courses: continue # SKIP if already used
        
        subject = course.split(" ")[0]
        if subject in arts_subjects:
            arts_credits += data[0]
            arts_counted.append(f"{course} ({data[0]} cr)")
            used_courses.add(course) # Mark as used
            
    print("\n2. ARTS BREADTH REQUIREMENT (Target: 12.0 Credits):")
    print("-" * 40)
    print(f"  Total Arts Credits: {arts_credits:.1f} / 12.0")
    if arts_counted:
        print(f"  Counted Courses   : {', '.join(arts_counted)}")
    print(f"  Status            : {'✅ Requirement Met!' if arts_credits >= 12.0 else f'❌ Needs {12.0 - arts_credits:.1f} more credits'}")

    # 3. Science Breadth Evaluator
    categories = {
        "1. Mathematics" : ["MATH"],
        "2. Chemistry"   : ["CHEM"],
        "3. Physics"     : ["PHYS"],
        "4. Life Science": ["BIOL", "BIO", "MICB", "CAPS", "BIOC"],
        "5. Statistics"  : ["STAT", "DSCI", "MATH 302", "BIOL 300"],
        "6. Computer Sci": ["CPSC"],
        "7. Earth & Plan": ["EOSC", "ATSC", "ASTR", "GEOB", "ENVR"]
    }
    categories_filled = {cat_name: [] for cat_name in categories.keys()}
    
    for course in transcript.keys():
        if course in used_courses: continue # SKIP if already used
        
        subject = course.split(" ")[0]
        for cat_name, prefixes in categories.items():
            if subject in prefixes:
                categories_filled[cat_name].append(course)
                used_courses.add(course) # Mark as used
                break
                
    print("\n3. SCIENCE BREADTH REQUIREMENT (Target: 6 of 7 Categories):")
    print("-" * 40)
    categories_hit_count = 0
    for cat_name, courses in categories_filled.items():
        if courses:
            categories_hit_count += 1
            print(f"  [✓] {cat_name:<16} : Met by {', '.join(courses)}")
        else:
            print(f"  [ ] {cat_name:<16} : Empty")
    print(f"\n  Total Categories Cleared: {categories_hit_count} / 6 Required")
    print(f"  Status                  : {'✅ SATISFIED' if categories_hit_count >= 6 else '❌ IN PROGRESS'}")
    print("="*50)

    
def export_report(transcript):
    print("\nGenerating your comprehensive degree report file...")
    total_credits, gpa_average = calculate_stats(transcript)
    
    with open("degree_plan_report.txt", "w", encoding="utf-8") as f:
        f.write("="*60 + "\n")
        f.write("         UBC SCIENCE DEGREE PLAN COMPREHENSIVE REPORT      \n")
        f.write("="*60 + "\n")
        f.write(f"Current Cumulative Stats: {total_credits:.1f} credits completed at {gpa_average:.1f}%\n")
        f.write("-" * 60 + "\n\n")
        
        # 1. FIRST YEAR SPECIALIZATION MAJORS PROGRESS
        f.write("1. FIRST YEAR SPECIALIZATION MAJORS PROGRESS:\n")
        f.write("-" * 60 + "\n")
        for major_name, major_data in majors_database.items():
            reqs_to_check = major_data["first_year_reqs"]
            completed_reqs = []
            missing_reqs = []
            for req in reqs_to_check:
                if check_requirement(req, transcript):
                    completed_reqs.append(req)
                else:
                    missing_reqs.append(req)
            
            total = len(reqs_to_check)
            met_reqs = len(completed_reqs)
            percentage = (met_reqs / total) * 100 if total > 0 else 0
            bar = '█' * int(10 * met_reqs // total) + '░' * (10 - int(10 * met_reqs // total))
            
            f.write(f"\n  {major_name:<15} : |{bar}| {percentage:.0f}% requirements met\n")
            if completed_reqs:
                completed_strs = ["/".join(str(item) for item in r) if isinstance(r, list) else str(r) for r in completed_reqs]
                f.write(f"    ✔ Completed: {', '.join(completed_strs)}\n")
            if missing_reqs:
                missing_strs = ["/".join(str(item) for item in r) if isinstance(r, list) else str(r) for r in missing_reqs]
                f.write(f"    ❌ Missing  : {', '.join(missing_strs)}\n")
                
        f.write("\n" + "="*60 + "\n\n")
        
        # 2. COMMUNICATION REQUIREMENT STATUS
        # Use direct key lookup from the transcript dictionary
        has_scie113 = "SCIE 113" in transcript
        additional_comm_subjects = ["ENGL", "WRDS", "ASTU"]
        additional_comm_course = None
        
        for course_code in transcript.keys():
            subject = course_code.split(" ")[0]
            if subject in additional_comm_subjects and course_code != "SCIE 113":
                additional_comm_course = course_code
                break
                
        f.write("2. COMMUNICATION REQUIREMENT STATUS:\n")
        f.write("-" * 60 + "\n")
        f.write(f"  Status: {'✅ SATISFIED' if has_scie113 and additional_comm_course else '░ IN PROGRESS'}\n")
        f.write(f"    • SCIE 113  : {'✅ Completed' if has_scie113 else '❌ Missing'}\n")
        f.write(f"    • Additional: {'✅ Completed (' + additional_comm_course + ')' if additional_comm_course else '❌ Missing'}\n")
        
        f.write("\n" + "="*60 + "\n\n")
        
        # 3. ARTS BREADTH REQUIREMENT
        arts_credits = 0.0
        arts_subjects = ["CRWR", "PHIL", "PSYC", "ECON", "SOCI", "HIST", "ANTH", "ASIA", "FREN", "SPAN"]
        arts_counted_items = []
        for course, data in transcript.items():
            subject = course.split(" ")[0]
            if subject in arts_subjects:
                arts_credits += data[0]
                arts_counted_items.append(f"{course} ({data[0]} cr)")
        
        arts_progress = min(arts_credits, 12.0)
        arts_bar = '█' * int(arts_progress / 1.2) + '░' * (10 - int(arts_progress / 1.2))
        f.write("3. ARTS BREADTH REQUIREMENT (Target: 12.0 Credits):\n")
        f.write("-" * 60 + "\n")
        f.write(f"  Progress: |{arts_bar}| {arts_credits:.1f}/12.0 credits\n")
        if arts_counted_items: f.write(f"  Counted : {', '.join(arts_counted_items)}\n")
        f.write(f"  Status  : {'✅ Requirement Met!' if arts_credits >= 12.0 else f'❌ Needs {12.0 - arts_credits:.1f} more credits'}\n")
        
        f.write("\n" + "="*60 + "\n\n")
        
        # 4. SCIENCE BREADTH REQUIREMENT
        categories = {
            "1. Mathematics" : ["MATH"],
            "2. Chemistry"   : ["CHEM"],
            "3. Physics"     : ["PHYS"],
            "4. Life Science": ["BIOL", "BIO", "MICB", "CAPS", "BIOC"],
            "5. Statistics"  : ["STAT", "DSCI", "MATH 302", "BIOL 300"],
            "6. Computer Sci": ["CPSC"],
            "7. Earth & Plan": ["EOSC", "ATSC", "ASTR", "GEOB", "ENVR"]
        }
        categories_filled = {cat_name: [] for cat_name in categories.keys()}
        for course_code in transcript.keys():
            subject = course_code.split(" ")[0]
            if "PHYS 100" in course_code or "CHEM 100" in course_code or "CHEM 300" in course_code: continue
            if "MATH 302" in course_code or "BIOL 300" in course_code:
                categories_filled["5. Statistics"].append(course_code)
                continue
            for cat_name, prefixes in categories.items():
                if subject in prefixes:
                    categories_filled[cat_name].append(course_code)
                    break
        
        categories_hit_count = sum(1 for c in categories_filled.values() if len(c) > 0)
        f.write("4. SCIENCE BREADTH REQUIREMENT (Target: 6 of 7 Categories):\n")
        f.write("-" * 60 + "\n")
        for cat_name, courses in categories_filled.items():
            if courses:
                f.write(f"    ✅ {cat_name:<16} : Met by {', '.join(courses)}\n")
            else:
                f.write(f"    ░ {cat_name:<16} : Empty\n")
        f.write(f"\n  Total Categories Cleared: {categories_hit_count} / 6 Required\n")
        f.write(f"  Status: {'✅ SATISFIED' if categories_hit_count >= 6 else '❌ IN PROGRESS'}\n")
        f.write("="*60 + "\n")

    print("🎉 Success! 'degree_plan_report.txt' has been populated with accurate framework breadth data.")
    
def run_target_calculator(transcript):
    print("\n" + "="*45)
    print("         COMPETITIVE GRADE TARGETER          ")
    print("="*45)
    
    total_credits, gpa_average = calculate_stats(transcript)
    if total_credits == 0:
        print("[!] Your transcript is currently empty. Cannot calculate target paths.")
        return

    print("Which major are you targeting?")
    majors_list = list(majors_database.keys())
    for idx, major in enumerate(majors_list, 1):
        print(f"  {idx}. {major}")
    
    major_idx = input(f"\nPick a number (1-{len(majors_list)}): ").strip()
    if not (major_idx.isdigit() and 1 <= int(major_idx) <= len(majors_list)):
        print("[!] Invalid selection. Returning to menu.")
        return
        
    selected_major = majors_list[int(major_idx) - 1]
    major_data = majors_database[selected_major]
    cutoffs = major_data.get("cutoffs")
    
    if not cutoffs:
        print(f"\n[i] {selected_major} does not have a competitive cutoff quota.")
        print("    Minimum faculty passing requirements apply to declare this major!")
        return
        
    valid_years = [year for year, gpa in cutoffs.items() if gpa is not None]
    if not valid_years:
        print(f"\n[i] No historical competitive cutoff benchmarks found for {selected_major}.")
        return
        
    latest_year = max(valid_years)
    target_cutoff = cutoffs[latest_year]
    
    print(f"\nTarget Major       : {selected_major}")
    print(f"Historic Cutoff    : {target_cutoff:.1f}%")
    print(f"Your Current Stats : {total_credits:.1f} credits at {gpa_average:.1f}%")
    print("-" * 45)
    
    try:
        rem_input = input("How many credits are you taking in your upcoming session? ").strip()
        remaining_credits = float(rem_input)
        if remaining_credits <= 0:
            print("[!] Planned credits must be greater than 0.")
            return
    except ValueError:
        print("[!] Invalid input. Please enter a numerical credit value (e.g., 12 or 15).")
        return
        
    total_future_credits = total_credits + remaining_credits
    required_points = (target_cutoff * total_future_credits) - (gpa_average * total_credits)
    required_gpa = required_points / remaining_credits
    
    print("\n" + "-"*45)
    if gpa_average >= target_cutoff:
        print(f"🎉 Your current average is already above the historic cutoff of {target_cutoff}%!")
        print(f"To keep it there, you need to maintain a sessional average of:")
        print(f"👉 {max(50.0, required_gpa):.1f}% across your next {remaining_credits:.1f} credits.")
    else:
        print(f"🚀 To reach the competitive milestone threshold of {target_cutoff}%:")
        if required_gpa > 100:
            print(f"⚠️ Out of reach for this specific session (Requires a {required_gpa:.1f}%).")
            print("\nAlternative Strategic Pathways:")
            print("  1. Change of Specialization Route:")
            print("     Declare a lower-cutoff major for Year 2, shadow the target program's")
            print("     courses, and use your Year 2 sessional average to switch for Year 3.")
            print("  2. Stay in First Year via Credit Cap:")
            print("     Keep total attempted credits under 48 to stay in Year 1 standing.")
            print("     This bypasses the June declaration deadline to give you another year")
            print("     to establish a higher GPA base cushion.")
        elif required_gpa < 50:
            print(f"✅ Highly achievable! You only need a passing sessional average of:")
            print(f"👉 50.0% across your next {remaining_credits:.1f} credits.")
        else:
            print(f"🎯 You need to hit a sessional average target of:")
            print(f"👉 {required_gpa:.1f}% across your next {remaining_credits:.1f} credits.")
    print("="*45)
    
def interactive_menu():
    while True:
        print("\n=================================")
        print("    UBC SCIENCE MAJOR PLANNER    ")
        print("=================================")
        print("1. Check my overall average & credits")
        print("2. Check requirements for a specific major")
        print("3. Compare all majors side-by-side")
        print("4. Run 'What-If' Sessional Grade Targeter")
        print("5. Check Faculty Breadth & Comm Reqs")
        print("6. Export my full report to a text file")
        print("7. Close the program")
        print("---------------------------------")
        
        choice = input("Pick an option (1-7): ").strip()
        
        
        
        if choice == "1":
            total_credits, gpa_average = calculate_stats(my_transcript)
            print("\n" + "="*35)
            print("           YOUR STATS            ")
            print("="*35)
            print(f" Total Credits Completed : {total_credits:.1f}")
            print(f" Current Average         : {gpa_average:.1f}%")
            print("="*35)
            input("\nPress Enter to go back to the main menu...")

        elif choice == "2":
            print("\nWhich major do you want to check?")
            majors_list = list(majors_database.keys())
            for idx, major in enumerate(majors_list, 1):
                print(f"  {idx}. {major}")
            
            major_idx = input(f"\nPick a number (1-{len(majors_list)}): ").strip()
            
            if major_idx.isdigit() and 1 <= int(major_idx) <= len(majors_list):
                selected_major = majors_list[int(major_idx) - 1]
                
                print("\nWhat do you want to check for this major?")
                print("  1. Just first year requirements (for moving to 2nd year)")
                print("  2. Every requirement needed to graduate")
                scope_choice = input("Pick 1 or 2: ").strip()
                
                mode = 'first' if scope_choice == "1" else 'full'
                audit_major(selected_major, my_transcript, mode=mode)
                input("\nPress Enter to go back to the main menu...")
            else:
                print("\n[!] Invalid choice. Going back to the main menu.")
                
        elif choice == "3":
            print("\n" + "="*45)
            print("        MAJOR PROGRESS COMPARISON        ")
            print("="*45)
            print("First Year Progress for each major:")
            print("-" * 45)
            
            # Loop through every major in the database to compare them
            for major_name, major_data in majors_database.items():
                reqs_to_check = major_data["first_year_reqs"]
                met_reqs = 0
                for req in reqs_to_check:
                    if check_requirement(req, my_transcript):
                        met_reqs += 1
                
                total = len(reqs_to_check)
                percentage = (met_reqs / total) * 100
                bar = '█' * int(10 * met_reqs // total) + '░' * (10 - int(10 * met_reqs // total))
                print(f" {major_name:<15} : |{bar}| {percentage:.0f}% finished")
                
            print("="*45)
            input("\nPress Enter to go back to the main menu...")

        elif choice == "4":
            run_target_calculator(my_transcript)
            input("\nPress Enter to go back to the main menu...")

        elif choice == "5":
            check_breadth_requirements(my_transcript)
            input("\nPress Enter to go back to the main menu...")

        elif choice == "6":
            export_report(my_transcript)
            input("\nPress Enter to go back to the main menu...")

        elif choice == "7":
            print("\nClosing the planner. Good luck with your UBC School Year!")
            break
        else:
            print("\n[!] That wasn't an option. Please type 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    interactive_menu()