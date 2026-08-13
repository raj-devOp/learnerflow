"""Tests for the LearnerFlow validation engine."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from validate import validate_learner


def make_record(**overrides):
    record = {
        "learner_id": "LRN1000",
        "name": "Test Learner",
        "date_of_birth": "1990-01-01",
        "email": "test@example.com",
        "enrollment_date": "2023-01-01",
        "course_code": "MATH01",
    }
    record.update(overrides)
    return record


def test_valid_record_has_no_errors():
    assert validate_learner(make_record()) == []


def test_bad_learner_id_is_caught():
    errors = validate_learner(make_record(learner_id="XXX"))
    assert any("learner_id" in e for e in errors)


def test_bad_email_is_caught():
    errors = validate_learner(make_record(email="not-an-email"))
    assert any("email" in e for e in errors)


def test_unknown_course_is_caught():
    errors = validate_learner(make_record(course_code="FAKE99"))
    assert any("course_code" in e for e in errors)


def test_empty_name_is_caught():
    errors = validate_learner(make_record(name="   "))
    assert any("Name" in e for e in errors)
