from __future__ import annotations

import unittest

from mainpy.stats import build_health_report


class StatsTests(unittest.TestCase):
    def test_health_report_marks_healthy_system_as_excellent(self) -> None:
        snapshot = {
            "cpu_percent": 20.0,
            "memory_percent": 42.0,
            "disk_percent": 55.0,
        }

        report = build_health_report(snapshot)

        self.assertEqual(report["score"], 100)
        self.assertEqual(report["status"], "Excellent")

    def test_health_report_marks_strained_system_as_critical(self) -> None:
        snapshot = {
            "cpu_percent": 95.0,
            "memory_percent": 97.0,
            "disk_percent": 98.0,
        }

        report = build_health_report(snapshot)

        self.assertLessEqual(report["score"], 20)
        self.assertEqual(report["status"], "Critical")
        self.assertGreaterEqual(len(report["recommendations"]), 3)


if __name__ == "__main__":
    unittest.main()
