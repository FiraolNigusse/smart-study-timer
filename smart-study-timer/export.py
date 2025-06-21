
import json
import csv
import os
from tkinter import messagebox

LOG_FILE = "logs/study_log.json"
EXPORT_FILE = "exports/study_log_export.csv"

def export_to_csv():
    # Ensure export directory exists
    os.makedirs("exports", exist_ok=True)

    try:
        with open(LOG_FILE, "r") as f:
            sessions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror("Error", "No session logs found to export.")
        return

    if not sessions:
        messagebox.showinfo("No Data", "No study sessions available to export.")
        return

    # Write to CSV
    with open(EXPORT_FILE, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["start", "duration_min", "type"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for session in sessions:
            writer.writerow({
                "start": session.get("start", ""),
                "duration_min": session.get("duration_min", ""),
                "type": session.get("type", "")
            })

    messagebox.showinfo("Export Complete", f"Sessions exported to:\n{EXPORT_FILE}")