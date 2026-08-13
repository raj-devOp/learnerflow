"""Generate synthetic learner records for LearnerFlow.

All data here is fake, produced by Faker. No real learner
data is ever used — this mirrors GDPR-safe practice.
"""
import csv
import random

from faker import Faker

fake = Faker("en_GB")   # UK-style names, addresses, etc.

def generate_learners(count):
    """Return a list of synthetic learner records."""
    learners = []
    for i in range(count):
        learner = {
            "learner_id": f"LRN{1000 + i}",
            "name": fake.name(),
            "date_of_birth": fake.date_of_birth(minimum_age=16, maximum_age=65).isoformat(),
            "email": fake.email(),
            "enrollment_date": fake.date_this_decade().isoformat(),
            "course_code": random.choice(["MATH01", "ENG02", "SCI03", "IT04"]),
        }
        learners.append(learner)
    return learners

def save_to_csv(learners, filename):
    """Write learner records to a CSV file."""
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=learners[0].keys())
        writer.writeheader()
        writer.writerows(learners)
    print(f"Wrote {len(learners)} learners to {filename}")

if __name__ == "__main__":
    records = generate_learners(50)
    save_to_csv(records, "data/learners.csv")
