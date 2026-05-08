import customtkinter as ctk
from typing import List

from config import (
    PRIMARY_COLOR, SECONDARY_COLOR,
    SUCCESS_COLOR, ERROR_COLOR, WARNING_COLOR, TEXT_SECONDARY,
    FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_SMALL, FONT_BUTTON,
)

_GRADE_THRESHOLDS = [
    (90, "🏆", "Kiváló!",       SUCCESS_COLOR),
    (75, "✅", "Jó eredmény!",  "#2d7a3a"),
    (50, "⚠️", "Megfelelt",     WARNING_COLOR),
    ( 0, "❌", "Nem felelt meg", ERROR_COLOR),
]


def _grade(percent: float):
    for threshold, icon, label, color in _GRADE_THRESHOLDS:
        if percent >= threshold:
            return icon, label, color
    return "❌", "Nem felelt meg", ERROR_COLOR


class ResultScreen(ctk.CTkFrame):
    """Full result / summary screen."""

    def __init__(self, parent: ctk.CTk, app, results: dict):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.results = results

        # Save stats immediately
        self.app.stats_manager.record(results)

        self._build_ui()

    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        total: int = self.results.get("total", 0)
        correct: int = self.results.get("correct", 0)
        percent: float = round((correct / total) * 100, 1) if total else 0.0
        mode: str = self.results.get("mode", "")
        detail: List[dict] = self.results.get("results", [])

        icon, label, color = _grade(percent)

        self._build_score_card(icon, label, color, correct, total, percent)
        self._build_action_buttons(mode)
        self._build_divider()
        self._build_question_list(detail)

    # ------------------------------------------------------------------

    def _build_score_card(
        self, icon: str, label: str, color: str,
        correct: int, total: int, percent: float,
    ) -> None:
        card = ctk.CTkFrame(self, fg_color="#1e1e2e", corner_radius=16)
        card.pack(pady=(30, 12), padx=60, fill="x")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(pady=20, padx=30)

        # Big emoji + grade label
        ctk.CTkLabel(inner, text=icon, font=("Segoe UI Emoji", 48)).pack()
        ctk.CTkLabel(inner, text=label, font=FONT_TITLE, text_color=color).pack(pady=(4, 0))

        # Score numbers
        ctk.CTkLabel(
            inner,
            text=f"{correct} / {total} helyes válasz",
            font=FONT_SUBTITLE,
        ).pack(pady=(8, 2))

        # Percentage bar
        bar_frame = ctk.CTkFrame(inner, fg_color="transparent")
        bar_frame.pack(fill="x", pady=6)
        bar = ctk.CTkProgressBar(bar_frame, width=340, height=14, progress_color=color)
        bar.pack()
        bar.set(percent / 100)

        ctk.CTkLabel(
            inner,
            text=f"{percent}%",
            font=("Segoe UI", 20, "bold"),
            text_color=color,
        ).pack()

    # ------------------------------------------------------------------

    def _build_action_buttons(self, mode: str) -> None:
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(pady=10)

        ctk.CTkButton(
            row,
            text="🏠  Főmenü",
            width=160, height=42,
            font=FONT_BUTTON,
            fg_color="transparent",
            border_width=2,
            hover_color="#2a2a3a",
            command=self.app.show_home,
        ).pack(side="left", padx=8)

        category = self.results.get("category")
        ctk.CTkButton(
            row,
            text="🔁  Újra",
            width=160, height=42,
            font=FONT_BUTTON,
            fg_color=PRIMARY_COLOR,
            hover_color="#173f6a",
            command=lambda: self.app.start_quiz(mode, category=category),
        ).pack(side="left", padx=8)

        has_wrong = bool(self.app.stats_manager.get_wrong_ids())
        ctk.CTkButton(
            row,
            text="❌  Hibás kérdések",
            width=180, height=42,
            font=FONT_BUTTON,
            fg_color=ERROR_COLOR if has_wrong else "#3a3a3a",
            hover_color="#922b21" if has_wrong else "#3a3a3a",
            state="normal" if has_wrong else "disabled",
            command=lambda: self.app.start_quiz("mistakes"),
        ).pack(side="left", padx=8)

    # ------------------------------------------------------------------

    def _build_divider(self) -> None:
        ctk.CTkFrame(self, height=2, fg_color=PRIMARY_COLOR).pack(
            fill="x", padx=60, pady=(8, 0)
        )
        ctk.CTkLabel(
            self,
            text="Kérdés-szintű összesítő",
            font=FONT_BODY,
            text_color=TEXT_SECONDARY,
        ).pack(pady=(6, 0))

    # ------------------------------------------------------------------

    def _build_question_list(self, detail: List[dict]) -> None:
        scroll = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=60, pady=(4, 16))

        for i, entry in enumerate(detail, start=1):
            q = entry["question"]
            ok = entry["correct"]
            self._build_question_row(scroll, i, q, ok)

    def _build_question_row(self, parent, num: int, q, ok: bool) -> None:
        bg = "#1a2e1a" if ok else "#2e1a1a"
        icon = "✅" if ok else "❌"
        diff_map = {"easy": "Könnyű", "medium": "Közepes", "hard": "Nehéz"}

        row = ctk.CTkFrame(parent, fg_color=bg, corner_radius=8)
        row.pack(fill="x", pady=3)

        # Left: number + icon
        left = ctk.CTkFrame(row, fg_color="transparent", width=50)
        left.pack(side="left", padx=(10, 0), pady=8)
        left.pack_propagate(False)
        ctk.CTkLabel(left, text=f"{icon}\n{num}.", font=FONT_SMALL, justify="center").pack()

        # Middle: question preview + badges
        mid = ctk.CTkFrame(row, fg_color="transparent")
        mid.pack(side="left", fill="x", expand=True, padx=10, pady=6)

        badge_row = ctk.CTkFrame(mid, fg_color="transparent")
        badge_row.pack(fill="x")
        ctk.CTkLabel(
            badge_row, text=q.category,
            font=FONT_SMALL, fg_color=SECONDARY_COLOR, corner_radius=5, padx=6, pady=2,
        ).pack(side="left", padx=(0, 6))
        ctk.CTkLabel(
            badge_row, text=diff_map.get(q.difficulty, q.difficulty),
            font=FONT_SMALL, text_color=TEXT_SECONDARY,
        ).pack(side="left")

        # Truncate question text to one line
        preview = q.question.replace("\n", " ")
        if len(preview) > 100:
            preview = preview[:97] + "..."
        ctk.CTkLabel(
            mid, text=preview,
            font=FONT_SMALL, anchor="w", justify="left", wraplength=680,
        ).pack(fill="x", pady=(2, 0))

