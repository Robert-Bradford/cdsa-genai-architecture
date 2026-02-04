# test_user_input.py

from schema_model import ClinicalInput, Patient, Vitals, Labs
from pubmed_evidence_summary_final import generate_evidence_summary
from utils import parse_height
from datetime import datetime, timezone
import re

# ----------------- Validation Functions ----------------- #

def validate_patient_id(pid: str):
    """Patient ID must be alphanumeric and contain at least one number."""
    if not re.fullmatch(r"(?=.*[0-9])[A-Za-z0-9_-]+", pid):
        raise ValueError("Patient ID must be alphanumeric and contain at least one number (no spaces or full names).")

def check_for_names(text: str):
    """Basic heuristic to prevent full names in notes or symptoms."""
    words = text.split()
    capitalized = [w for w in words if w.istitle()]
    if len(capitalized) > 1:
        raise ValueError("Names are not allowed in this field.")

# ----------------- Input Function ----------------- #

def get_user_input():
    """Prompt user to enter patient data with validation."""
    print("\nEnter patient information:")

    # Patient ID
    while True:
        try:
            pid = input("Patient ID: ").strip()
            validate_patient_id(pid)
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    # Age
    while True:
        try:
            age = int(input("Age: "))
            if age <= 0:
                raise ValueError("Age must be positive.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    # Sex
    while True:
        sex = input("Sex (male/female): ").strip().lower()
        if sex in ["male", "female"]:
            break
        print("Invalid input: enter 'male' or 'female'.")

    # Height (feet'inches)
    while True:
        height_str = input("Height (e.g., 5'9): ").strip()
        try:
            height_in = parse_height(height_str)
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    # Weight
    while True:
        try:
            weight_lb = float(input("Weight (lb): "))
            if weight_lb <= 0:
                raise ValueError("Weight must be positive.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    # Optional inputs
    bp_pattern = re.compile(r"^\d{2,3}/\d{2,3}$")
    blood_pressure = input("Blood pressure (e.g., 120/80, leave blank if unknown): ").strip() or None
    if blood_pressure and not bp_pattern.fullmatch(blood_pressure):
        print("Invalid BP format — clearing value.")
        blood_pressure = None

    heart_rate = input("Heart rate (bpm, leave blank if unknown): ").strip() or None
    heart_rate = int(heart_rate) if heart_rate and heart_rate.isdigit() else None

    hba1c = input("HBA1C (leave blank if unknown): ").strip() or None
    hba1c = float(hba1c) if hba1c else None

    ldl = input("LDL (leave blank if unknown): ").strip() or None
    ldl = float(ldl) if ldl else None

    # Symptoms
    while True:
        try:
            symptoms_input = input("Symptoms (comma-separated): ").strip()
            if symptoms_input:
                check_for_names(symptoms_input)
                symptoms = [s.strip() for s in symptoms_input.split(",")]
            else:
                symptoms = []
            break
        except ValueError as e:
            print(f"Invalid input: {e}")

    notes = input("Additional notes: ").strip() or None
    if notes:
        try:
            check_for_names(notes)
        except ValueError as e:
            print(f"Invalid input: {e}")
            notes = None

    patient = Patient(id=pid, age=age, sex=sex, height_in=height_in, weight_lb=weight_lb)
    vitals = Vitals(blood_pressure=blood_pressure, heart_rate=heart_rate)
    labs = Labs(hba1c=hba1c, ldl=ldl)

    return ClinicalInput(
        patient=patient,
        vitals=vitals,
        labs=labs,
        symptoms=symptoms,
        notes=notes,
        timestamp=datetime.now(timezone.utc)
    )

# ----------------- Main Loop ----------------- #

def main():
    while True:
        clinical_input = get_user_input()
        summary = generate_evidence_summary(clinical_input)

        print("\n========================================")
        print(f"Patient ID: {summary['patient_id']}")
        print("\n📄 Evidence Snippet:\n")
        print(summary["snippet"])
        print("========================================\n")

        if input("Enter another patient? (y/n): ").strip().lower() != "y":
            break

if __name__ == "__main__":
    main()
