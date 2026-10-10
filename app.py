import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Read student data from JSON file
with open("attendance.json", "r") as file:
    data = json.load(file)

print("\n===== ATTENDANCE MANAGEMENT SYSTEM =====\n")

report = []

for student in data["students"]:
    name = student["name"]
    roll_no = student["roll_no"]
    attendance = student["attendance"]

    total_days = len(attendance)
    present_days = sum(1 for status in attendance.values() if status is True)
    percentage = (present_days / total_days * 100) if total_days else 0

    print("Name:", name)
    print("Roll No:", roll_no)
    print("Present Days:", present_days)
    print("Total Days:", total_days)
    print("Attendance Percentage:", round(percentage, 2), "%")
    print("-" * 35)

    report.append({
        "name": name,
        "roll_no": roll_no,
        "present_days": present_days,
        "total_days": total_days,
        "percentage": round(percentage, 2)
    })

# Ask Gemini to summarize the attendance report
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=f"Explain this student attendance report in simple language. "
             f"Identify students with attendance below 75%: {json.dumps(report)}"
)

print("\n===== GEMINI AI SUMMARY =====\n")
print(response.text)