import collections

def solve_stable_matching(students_prefs, companies_prefs):
    """
    Solves the Stable Matching problem using the Gale-Shapley algorithm.
    This version assumes students propose to companies.

    Args:
        students_prefs (dict): A dictionary where keys are student names (e.g., 'S1')
                               and values are their ordered list of preferred companies
                               (e.g., ['C1', 'C2', 'C3']).
        companies_prefs (dict): A dictionary where keys are company names (e.g., 'C1')
                                and values are their ordered list of preferred students
                                (e.g., ['S2', 'S1', 'S3']).

    Returns:
        dict: A dictionary of stable matches, with company names as keys
              and their matched student as the value (e.g., {'C1': 'S2'}).
    """
    
    # --- Setup ---
    
    # Get a list of all students. We'll use this as a queue of "free" students.
    # We use a deque for efficient pop/append from the left.
    free_students = collections.deque(students_prefs.keys())
    
    # Track the current matches. {company_name: student_name}
    current_matches = {}
    
    # Track which companies each student has already proposed to.
    # {student_name: index_of_next_company_to_propose_to}
    student_proposal_index = {student: 0 for student in students_prefs}
    
    # For companies to make quick decisions, it's better to have a ranking map.
    # {company_name: {student_name: rank_number}}
    # e.g., if C1's prefs are ['S2', 'S1'], map is {'C1': {'S2': 0, 'S1': 1}}
    company_rankings = {}
    for company, prefs in companies_prefs.items():
        company_rankings[company] = {student: rank for rank, student in enumerate(prefs)}

    print("--- Starting Matching Process ---")

    # --- Algorithm Loop ---
    
    # Loop as long as there is a free student who still has companies to propose to
    while free_students:
        student = free_students.popleft() # Get the next free student
        
        # Get this student's preference list
        student_prefs_list = students_prefs[student]
        
        # Find the next company this student hasn't proposed to yet
        proposal_idx = student_proposal_index[student]
        
        if proposal_idx >= len(student_prefs_list):
            # This student has proposed to everyone on their list and is still free.
            # This can happen in versions with unequal numbers or incomplete lists.
            # For this simple version, we'll just log it.
            print(f"Student {student} has run out of companies to propose to and remains unmatched.")
            continue
            
        company = student_prefs_list[proposal_idx]
        
        # Mark that this student has now proposed to this company
        student_proposal_index[student] += 1
        
        print(f"Student {student} proposes to Company {company}...")

        # --- Decision Logic ---
        
        if company not in current_matches:
            # Case 1: Company is free. They tentatively accept.
            current_matches[company] = student
            print(f"  > Company {company} is free and accepts {student} (tentatively).")
            
        else:
            # Case 2: Company is already matched. They must decide.
            current_student = current_matches[company]
            
            # Get the company's ranking for the new proposer and the current match
            rank_of_new_student = company_rankings[company].get(student, float('inf'))
            rank_of_current_student = company_rankings[company].get(current_student, float('inf'))
            
            if rank_of_new_student < rank_of_current_student:
                # Company prefers the new student
                current_matches[company] = student
                # The old student is now free. Add them back to the queue.
                free_students.append(current_student)
                print(f"  > Company {company} prefers {student} over {current_student}.")
                print(f"  > {student} is now matched with {company}. {current_student} is now free.")
            else:
                # Company prefers their current student
                # The proposing student is still free. Add them back to the queue
                # to propose to their next choice.
                free_students.append(student)
                print(f"  > Company {company} rejects {student}, preferring {current_student}.")

    print("--- Matching Process Complete ---")
    return current_matches

# --- Example Usage ---
if __name__ == "__main__":
    
    # Define the preferences
    
    # Students' preferences (most preferred to least preferred)
    students = {
        'Alice': ['CompanyA', 'CompanyB', 'CompanyC'],
        'Bob':   ['CompanyB', 'CompanyA', 'CompanyC'],
        'Charlie': ['CompanyA', 'CompanyC', 'CompanyB']
    }
    
    # Companies' preferences (most preferred to least preferred)
    companies = {
        'CompanyA': ['Bob', 'Alice', 'Charlie'],
        'CompanyB': ['Alice', 'Charlie', 'Bob'],
        'CompanyC': ['Charlie', 'Bob', 'Alice']
    }

    # Solve the matching
    matches = solve_stable_matching(students, companies)
    
    # Print the final results
    print("\n--- Final Stable Matches ---")
    if not matches:
        print("No matches were made.")
    else:
        for company, student in matches.items():
            print(f"{company} is matched with {student}")
