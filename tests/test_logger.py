import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from logger import ExecutionLogger, QuestionRunLog


class TestExecutionLogger(unittest.TestCase):
    def test_single_run_with_multiple_attempts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file = Path(tmp_dir) / "logs" / "execution_log.json"
            logger = ExecutionLogger(log_file=log_file)

            run_log = QuestionRunLog(
                scenario_id="scenario_4",
                user_question="מה הממוצע של עומרי באוניברסיטת רייכמן?",
            )
            run_log.add_attempt(
                attempt_number=1,
                candidate_answer="הממוצע של עומרי הוא 95 והוא זכה בפרס נובל.",
                evaluator_decision="rejected",
                feedback="הממוצע לפי המסמכים הוא 99, והטענה על פרס נובל הומצאה.",
            )
            run_log.add_attempt(
                attempt_number=2,
                candidate_answer="הממוצע של עומרי באוניברסיטת רייכמן הוא 99.",
                evaluator_decision="approved",
                feedback="התשובה מדויקת ומבוססת על מקורות הרקע.",
            )
            run_log.final_status = "approved"

            logger.log_run(run_log)

            self.assertTrue(log_file.exists())
            raw_text = log_file.read_text(encoding="utf-8")
            # Verify Hebrew text is saved directly without ASCII escaping
            self.assertIn("מה הממוצע של עומרי", raw_text)

            data = json.loads(raw_text)
            self.assertEqual(len(data), 1)
            entry = data[0]
            self.assertEqual(entry["scenario_id"], "scenario_4")
            self.assertEqual(entry["final_status"], "approved")
            self.assertIn("timestamp", entry)
            self.assertEqual(len(entry["attempts"]), 2)
            self.assertEqual(entry["attempts"][0]["evaluator_decision"], "rejected")
            self.assertEqual(entry["attempts"][1]["evaluator_decision"], "approved")

    def test_appends_multiple_runs_and_technical_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            log_file = Path(tmp_dir) / "execution_log.json"
            logger = ExecutionLogger(log_file=log_file)

            first_run = QuestionRunLog(
                scenario_id="scenario_1",
                user_question="Where does Omri study?",
                final_status="approved",
            )
            first_run.add_attempt(
                attempt_number=1,
                candidate_answer="Omri studies at Reichman University.",
                evaluator_decision="approved",
                feedback="Supported by background documents.",
            )
            logger.log_run(first_run)

            error_run = QuestionRunLog(
                scenario_id="technical_error_test",
                user_question="What projects did Omri build?",
                final_status="technical_error",
            )
            error_run.add_attempt(
                attempt_number=1,
                candidate_answer="Omri built the AI-Powered Grocery List Manager.",
                evaluator_decision="evaluation_not_completed",
                feedback="ValidationError: malformed JSON output from evaluator.",
            )
            logger.log_run(error_run)

            data = json.loads(log_file.read_text(encoding="utf-8"))
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]["scenario_id"], "scenario_1")
            self.assertEqual(data[1]["scenario_id"], "technical_error_test")
            self.assertEqual(data[1]["final_status"], "technical_error")
            self.assertEqual(
                data[1]["attempts"][0]["evaluator_decision"],
                "evaluation_not_completed",
            )


if __name__ == "__main__":
    unittest.main()
