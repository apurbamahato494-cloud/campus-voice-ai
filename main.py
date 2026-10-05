import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Campus Admission Voice Backend")

def get_db():
    conn = sqlite3.connect("campus_seats.db")
    conn.row_factory = sqlite3.Row
    return conn

# Ensure tables and default branch data exist on startup
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Departments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT,
            total_seats INTEGER,
            available_seats INTEGER
        )
    """)
    
    # Default departments data
    branches = [
        ("CSE", "Computer Science and Engineering", 120, 14),
        ("AI", "Artificial Intelligence and Data Science", 60, 8),
        ("ECE", "Electronics and Communication Engineering", 120, 25),
        ("ME", "Mechanical Engineering", 60, 19),
        ("CE", "Civil Engineering", 60, 30)
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO departments (code, name, total_seats, available_seats)
        VALUES (?, ?, ?, ?)
    """, branches)

    # 2. Admission Leads table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admission_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            phone_number TEXT,
            department TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# --- Schemas ---
class VapiPayload(BaseModel):
    message: dict

# --- Tool 1: Check Seats ---
@app.post("/voice/check-seats")
async def check_seats_voice(payload: VapiPayload):
    tool_calls = payload.message.get("toolCalls", [])
    if not tool_calls:
        return {"results": [{"toolCallId": "none", "result": "No tool call found."}]}

    tool_call = tool_calls[0]
    call_id = tool_call.get("id")
    dept_query = tool_call.get("function", {}).get("arguments", {}).get("department", "")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments WHERE code LIKE ? OR name LIKE ?", 
                   (f"%{dept_query}%", f"%{dept_query}%"))
    dept = cursor.fetchone()
    conn.close()

    if dept:
        result_text = f"{dept['name']} has {dept['available_seats']} seats available out of {dept['total_seats']}."
    else:
        result_text = f"Sorry, I couldn't find seat details for '{dept_query}'."

    return {"results": [{"toolCallId": call_id, "result": result_text}]}

# --- Tool 2: Book Counseling Lead ---
@app.post("/voice/book-lead")
async def book_lead_voice(payload: VapiPayload):
    tool_calls = payload.message.get("toolCalls", [])
    if not tool_calls:
        return {"results": [{"toolCallId": "none", "result": "No tool call found."}]}

    tool_call = tool_calls[0]
    call_id = tool_call.get("id")
    args = tool_call.get("function", {}).get("arguments", {})

    student_name = args.get("student_name", "Prospective Student")
    phone_number = args.get("phone_number", "Unknown")
    department = args.get("department", "General")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO admission_leads (student_name, phone_number, department) VALUES (?, ?, ?)",
        (student_name, phone_number, department)
    )
    conn.commit()
    conn.close()

    result_text = f"Counseling slot booked successfully for {student_name} interested in {department}."
    return {"results": [{"toolCallId": call_id, "result": result_text}]}