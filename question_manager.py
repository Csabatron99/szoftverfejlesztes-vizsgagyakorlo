import json
import random
from typing import List, Optional

from models import Question
from config import QUESTIONS_FILE


class QuestionManager:
    """Loads and serves questions from questions.json."""

    def __init__(self):
        self.questions: List[Question] = []
        self.load_questions()

    def load_questions(self) -> None:
        """Load questions from the JSON file. Will be fully used in Step 2."""
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.questions = [Question(**item) for item in data]
        except FileNotFoundError:
            self.questions = []
        except (json.JSONDecodeError, TypeError) as e:
            print(f"[QuestionManager] Failed to load questions: {e}")
            self.questions = []

    def get_categories(self) -> List[str]:
        """Return sorted list of unique categories."""
        return sorted({q.category for q in self.questions})

    def get_by_category(self, category: str) -> List[Question]:
        return [q for q in self.questions if q.category == category]

    def get_by_ids(self, ids: List[int]) -> List[Question]:
        id_set = set(ids)
        return [q for q in self.questions if q.id in id_set]

    def get_random(self, count: Optional[int] = None, category: Optional[str] = None) -> List[Question]:
        """Return a shuffled subset of questions, optionally filtered by category."""
        pool = self.get_by_category(category) if category else list(self.questions)
        random.shuffle(pool)
        if count is not None:
            pool = pool[:count]
        return pool
