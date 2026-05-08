import json
import os
from datetime import datetime
from typing import List, Dict, Any

from config import STATS_FILE, DATA_DIR


class StatsManager:
    """Manages persistent statistics stored in stats.json."""

    _DEFAULT: Dict[str, Any] = {
        "total_tests": 0,
        "best_score": 0,
        "avg_percent": 0.0,
        "all_percents": [],
        "category_results": {},
        "wrong_question_ids": [],
        "last_test_date": None,
    }

    def __init__(self):
        self.stats: Dict[str, Any] = {}
        self.load_stats()

    def load_stats(self) -> None:
        """Load stats from JSON, or initialise with defaults. Will be extended in Step 6."""
        os.makedirs(DATA_DIR, exist_ok=True)
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                self.stats = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.stats = dict(self._DEFAULT)

    def save_stats(self) -> None:
        """Persist current stats to disk."""
        try:
            with open(STATS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except OSError as e:
            print(f"[StatsManager] Could not save stats: {e}")

    def get_wrong_ids(self) -> List[int]:
        return self.stats.get("wrong_question_ids", [])

    def record(self, results: Dict[str, Any]) -> None:
        """Update persistent stats after a completed quiz session.

        results keys expected:
            total (int), correct (int), wrong_ids (List[int]),
            results (list of {question, selected, correct})
        """
        total: int = results.get("total", 0)
        correct: int = results.get("correct", 0)
        if total == 0:
            return

        percent = round((correct / total) * 100, 1)

        # Totals
        self.stats["total_tests"] = self.stats.get("total_tests", 0) + 1
        all_p: list = self.stats.setdefault("all_percents", [])
        all_p.append(percent)
        self.stats["avg_percent"] = round(sum(all_p) / len(all_p), 1)
        self.stats["best_score"] = max(self.stats.get("best_score", 0), int(percent))
        self.stats["last_test_date"] = datetime.now().strftime("%Y-%m-%d")

        # Wrong question IDs – add newly wrong, remove newly correct
        new_wrong_ids: List[int] = results.get("wrong_ids", [])
        correctly_answered_ids: List[int] = [
            r["question"].id for r in results.get("results", []) if r["correct"]
        ]
        existing: set = set(self.stats.get("wrong_question_ids", []))
        existing.update(new_wrong_ids)
        existing.difference_update(correctly_answered_ids)
        self.stats["wrong_question_ids"] = sorted(existing)

        self.save_stats()
