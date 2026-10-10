import unittest
from gamebench.scoring import aggregate, decisions, validate_report


class ScoringTests(unittest.TestCase):
    def report(self, status="passed", frames=None):
        return {r: {"status": status, "frames": [2, 3] if frames is None else frames}
                for r in ("line_clear", "score_on_clear")}

    def test_fabricated_pass_gets_no_credit(self):
        rows = decisions(self.report(), {"line_clear": "passed", "score_on_clear": "passed"}, {})
        self.assertFalse(any(r["correct"] for r in rows))

    def test_adjacent_certificate_is_required(self):
        cert = {3: {"line_clear": "passed", "score_on_clear": "passed"}}
        self.assertTrue(all(r["correct"] for r in decisions(self.report(),
                       {"line_clear": "passed", "score_on_clear": "passed"}, cert)))
        self.assertFalse(any(r["correct"] for r in decisions(self.report(frames=[1, 3]),
                        {"line_clear": "passed", "score_on_clear": "passed"}, cert)))

    def test_conditional_score_is_excluded(self):
        rows = decisions(self.report("failed"), {"line_clear": "failed", "score_on_clear": None},
                         {3: {"line_clear": "failed"}})
        self.assertEqual(len(rows), 1)
        self.assertTrue(rows[0]["correct"])

    def test_invalid_frames_and_states_are_unscored(self):
        for report in (self.report(frames=[2, 99]), self.report(frames=[True, 3]),
                       self.report("unknown"), self.report([]), self.report(frames=[3, 3])):
            with self.assertRaises(ValueError):
                validate_report(report, 4)

    def test_balanced_metric_and_abstention(self):
        rows = [{"gold": "passed", "status": "passed", "correct": True, "supported": True},
                {"gold": "passed", "status": "unverified", "correct": False, "supported": False},
                {"gold": "failed", "status": "failed", "correct": True, "supported": True}]
        self.assertEqual(aggregate(rows)["score"], 0.75)
        with self.assertRaises(ValueError):
            aggregate(rows[:2])


if __name__ == "__main__":
    unittest.main()
