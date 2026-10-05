from database import SessionLocal, DepartmentSeat

def check_seat_availability(branch_name: str) -> str:
    """
    Looks up seat counts from the database by department code (e.g. CSE)
    or department name (e.g. Mechanical).
    """
    db = SessionLocal()
    clean_query = branch_name.strip().upper()

    # Search for an exact code match (CSE) or partial name match (Mechanical)
    dept = db.query(DepartmentSeat).filter(
        (DepartmentSeat.department_code == clean_query) | 
        (DepartmentSeat.department_name.ilike(f"%{clean_query}%"))
    ).first()

    db.close()

    # If the user asks for a branch we do not offer
    if not dept:
        return f"We could not find any branch matching '{branch_name}'. Our available branches are CSE, AI-DS, ECE, and Mechanical."

    # If seats are left
    if dept.available_seats > 0:
        return f"Yes, seats are available! {dept.department_name} currently has {dept.available_seats} out of {dept.total_seats} seats remaining."
    
    # If the department is completely full
    return f"Admissions for {dept.department_name} are currently full for this intake."


# Quick test runs right inside your terminal:
if __name__ == "__main__":
    print("--- Test 1 (CSE): ---")
    print(check_seat_availability("CSE"))

    print("\n--- Test 2 (Mechanical): ---")
    print(check_seat_availability("Mechanical"))

    print("\n--- Test 3 (Civil - Not offered): ---")
    print(check_seat_availability("Civil"))
    