from dataclasses import dataclass, field
from typing import List


@dataclass
class Question:
    id: int
    type: str           # single_choice, multiple_choice, true_false, code_reading, fill_blank, matching, uml
    category: str
    difficulty: str     # easy, medium, hard
    question: str
    answers: List[str]
    correct: List[int]  # always a list, even for single_choice
    explanation: str

    def is_correct(self, selected: List[int]) -> bool:
        """Returns True if the selected answer indices exactly match the correct ones."""
        return sorted(selected) == sorted(self.correct)

    def is_partial(self, selected: List[int]) -> bool:
        """Returns True if at least one correct answer was selected (for multiple_choice feedback)."""
        return any(i in self.correct for i in selected)
