"""Exposed structural regression fixtures, not CI or deployment outcomes."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("apr_dependency_subject", ROOT / "skills/pipeline/scripts/apr.py")
apr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(apr)


def fixture():
    return {"apr": {"version": "1.0", "stages": [
        {"name": "inspect", "jobs": [{"name": "inspect-job", "runner": "fixture", "timeout_minutes": 1,
                                        "steps": [{"type": "run", "command": "fictional-inspection"}]}]},
        {"name": "verify", "depends_on": ["inspect"], "jobs": [
            {"name": "verify-job", "depends_on": ["inspect-job"], "runner": "fixture", "timeout_minutes": 1,
             "steps": [{"type": "run", "command": "fictional-verification"}]}]},
    ]}}


class DependencyShapeTests(unittest.TestCase):
    def test_falsey_top_level_non_arrays_are_not_empty_declarations(self):
        for field in ("secrets", "artifacts", "environments"):
            for value in (False, 0, "", {}):
                with self.subTest(field=field, value=value):
                    doc = fixture()
                    doc["apr"][field] = value
                    result = apr.validate(doc)
                    self.assertFalse(result["valid"], result)
                    self.assertIn(field.capitalize() + " must be an array", result["errors"])

    def test_optional_empty_and_real_declarations_preserve_valid_references(self):
        for field in ("secrets", "artifacts", "environments"):
            for value in (None, []):
                doc = fixture()
                doc["apr"][field] = value
                self.assertTrue(apr.validate(doc)["valid"])
        doc = fixture()
        doc["apr"]["secrets"] = [{"name": "FICTIONAL_TOKEN", "required_for": ["verify-job"]}]
        doc["apr"]["stages"][1]["jobs"][0]["steps"][0]["secrets"] = ["FICTIONAL_TOKEN"]
        doc["apr"]["artifacts"] = [{"name": "fixture", "produced_by": "inspect-job", "consumed_by": ["verify-job"]}]
        doc["apr"]["environments"] = [{"name": "staging", "requires_approval": True}]
        doc["apr"]["stages"][1]["environment"] = "staging"
        self.assertTrue(apr.validate(doc)["valid"])

    def test_falsey_non_arrays_are_rejected_without_erasing_edges(self):
        for level in ("stage", "job"):
            for value in (False, 0, "", {}):
                with self.subTest(level=level, value=value):
                    doc = fixture()
                    subject = doc["apr"]["stages"][1]
                    if level == "job":
                        subject = subject["jobs"][0]
                    subject["depends_on"] = value
                    result = apr.validate(doc)
                    self.assertFalse(result["valid"], result)
                    self.assertTrue(any("dependencies must be names" in message for message in result["errors"]))

    def test_schema_nullable_and_empty_dependencies_remain_supported(self):
        for value in (None, []):
            with self.subTest(value=value):
                doc = fixture()
                doc["apr"]["stages"][1]["depends_on"] = copy.deepcopy(value)
                doc["apr"]["stages"][1]["jobs"][0]["depends_on"] = copy.deepcopy(value)
                self.assertTrue(apr.validate(doc)["valid"])

    def test_positive_order_and_cross_stage_cycle_control(self):
        doc = fixture()
        self.assertTrue(apr.validate(doc)["valid"])
        doc["apr"]["stages"][0]["jobs"][0]["depends_on"] = ["verify-job"]
        self.assertFalse(apr.validate(doc)["valid"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
