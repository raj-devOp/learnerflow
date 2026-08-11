"""Validation engine for LearnerFlow.

Reads learner records and checks each one against data-quality
rules, mirroring compliance-style validation (e.g. ESFA/ILR).
Produces a report of how many records passed and why others failed.
"""
import csv
import re
from datetime import date


def validate_learner(record):
    """Check one learner record. Return a list of error messages (empty = valid)."""
    errors = []

    # Rule 1: learner_id must match the pattern LRN followed by 4 digits
    if not re.match(r"^LRN\d{4}$", record["learner_id"]):
        errors.append(f"Invalid learner_id format: {record['learner_id']}")

    # Rule 2: name must not be empty
    if not record["name"].strip():
        errors.append("Name is empty")

    # Rule 3: email must contain an @ and a dot
    if "@" not in record["email"] or "." not in record["email"]:
        errors.append(f"Invalid email: {record['email']}")

    # Rule 4: course_code must be one of the allowed values
    allowed_courses = {"MATH01", "ENG02", "SCI03", "IT04"}
    if record["course_code"] not in allowed_courses:
        errors.append(f"Unknown course_code: {record['course_code']}")

    # Rule 5: date_of_birth must be a real past date
    try:
        dob = date.fromisoformat(record["date_of_birth"])
        if dob >= date.today():
            errors.append("Date of birth is not in the past")
    except ValueError:
        errors.append(f"Invalid date_of_birth: {record['date_of_birth']}")

    return errors


def validate_file(filename):
    """Validate every record in a CSV and print a data-quality report."""
    total = 0
    passed = 0
    failures = []

    with open(filename, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            errors = validate_learner(row)
            if errors:
                failures.append((row["learner_id"], errors))
            else:
                passed += 1

    print("=" * 50)
    print("LearnerFlow Data Quality Report")
    print("=" * 50)
    print(f"Total records:  {total}")
    print(f"Passed:         {passed}")
    print(f"Failed:         {len(failures)}")
    if total:
        print(f"Pass rate:      {passed / total * 100:.1f}%")

    if failures:
        print("\nFailures:")
        for learner_id, errors in failures:
            for err in errors:
                print(f"  {learner_id}: {err}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate learner records in a CSV file.")
    parser.add_argument("file", help="Path to the CSV file to validate")
    args = parser.parse_args()

    validate_file(args.file)
