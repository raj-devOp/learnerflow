"""Minimal web layer for LearnerFlow.

Serves the data-quality report over HTTP by reusing the existing
validation engine. No validation logic is duplicated here.
"""
import csv

from flask import Flask, jsonify, render_template_string

from validate import validate_learner

app = Flask(__name__)

import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "learners.csv")

PAGE = """
<!doctype html>
<title>LearnerFlow</title>
<h1>LearnerFlow — Data Quality Report</h1>
<p>Total records: {{ total }}</p>
<p>Passed: {{ passed }}</p>
<p>Failed: {{ failed }}</p>
<p>Pass rate: {{ rate }}%</p>
{% if failures %}
<h2>Failures</h2>
<ul>
{% for f in failures %}<li>{{ f }}</li>{% endfor %}
</ul>
{% endif %}
"""

def run_validation():
    total = passed = 0
    failures = []
    with open(DATA_FILE, newline="") as fh:
        for row in csv.DictReader(fh):
            total += 1
            errors = validate_learner(row)
            if errors:
                for e in errors:
                    failures.append(f"{row['learner_id']}: {e}")
            else:
                passed += 1
    rate = round(passed / total * 100, 1) if total else 0
    return total, passed, total - passed, rate, failures

@app.route("/")
def report():
    total, passed, failed, rate, failures = run_validation()
    return render_template_string(
        PAGE, total=total, passed=passed, failed=failed, rate=rate, failures=failures
    )

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
