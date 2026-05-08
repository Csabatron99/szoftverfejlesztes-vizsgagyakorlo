import customtkinter as ctk
from typing import List

from ui.code_widget import create_code_block
from config import (
    PRIMARY_COLOR, SECONDARY_COLOR,
    SUCCESS_COLOR, ERROR_COLOR, TEXT_SECONDARY,
    FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_SMALL, FONT_BUTTON, FONT_CODE,
    QUIZ_MODES,
)
from models import Question

# Colours used for answer feedback
_CLR_DEFAULT  = "#2b2b3b"   # unselected answer button
_CLR_SELECTED = "#1f538d"   # selected (before submit)
_CLR_CORRECT  = "#2d8a4e"   # correct answer (after submit)
_CLR_WRONG    = "#c0392b"   # wrong selected answer (after submit)
_CLR_MISSED   = "#1a5c35"   # correct answer the user didn't select


class QuizScreen(ctk.CTkFrame):
    """Full quiz question screen with type-aware answer buttons and feedback."""

    def __init__(self, parent: ctk.CTk, app, questions: List[Question], mode: str, category: str | None = None):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.questions = questions
        self.mode = mode
        self._category: str | None = category

        # Per-question state
        self._idx: int = 0
        self._selected: set[int] = set()   # indices of currently selected answers
        self._answered: bool = False

        # Accumulated results
        self._results: list[dict] = []     # one entry per answered question

        # Widget references updated each question
        self._answer_btns: list[ctk.CTkButton] = []
        self._explanation_label: ctk.CTkLabel | None = None
        self._check_btn: ctk.CTkButton | None = None
        self._next_btn: ctk.CTkButton | None = None
        self._progress_bar: ctk.CTkProgressBar | None = None
        self._progress_label: ctk.CTkLabel | None = None
        self._question_label: ctk.CTkLabel | None = None
        self._type_label: ctk.CTkLabel | None = None
        self._hint_label: ctk.CTkLabel | None = None
        self._answer_frame: ctk.CTkScrollableFrame | None = None
        self._content_frame: ctk.CTkScrollableFrame | None = None

        # Timer state
        self._timer_job = None
        self._time_left: int = 0       # seconds remaining (full mode)
        self._elapsed: int = 0         # seconds elapsed (quick/normal)
        self._timer_label: ctk.CTkLabel | None = None

        # Pause state
        self._paused: bool = False
        self._pause_overlay: ctk.CTkFrame | None = None
        self._pause_btn: ctk.CTkButton | None = None

        self._build_skeleton()
        self._setup_timer()
        self._bind_keys()
        self._load_question()

    # ------------------------------------------------------------------
    # Static skeleton (top bar + content area + bottom bar)
    # ------------------------------------------------------------------

    def _build_skeleton(self) -> None:
        # ── Top progress bar ──────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=_CLR_DEFAULT, corner_radius=0)
        top.pack(fill="x")

        top_inner = ctk.CTkFrame(top, fg_color="transparent")
        top_inner.pack(fill="x", padx=30, pady=10)

        mode_name = QUIZ_MODES.get(self.mode, {}).get("name", self.mode)
        ctk.CTkLabel(
            top_inner, text=f"🧩 {mode_name}", font=FONT_BODY
        ).pack(side="left")

        self._progress_label = ctk.CTkLabel(
            top_inner, text="", font=FONT_BODY, text_color=TEXT_SECONDARY
        )
        self._progress_label.pack(side="right")

        self._timer_label = ctk.CTkLabel(
            top_inner, text="", font=("Segoe UI", 13, "bold"), text_color=TEXT_SECONDARY
        )
        self._timer_label.pack(side="right", padx=(0, 20))

        self._pause_btn = ctk.CTkButton(
            top_inner,
            text="⏸  Szünet",
            width=110,
            height=30,
            font=FONT_SMALL,
            fg_color=SECONDARY_COLOR,
            hover_color="#1a4a7a",
            command=self._toggle_pause,
        )
        self._pause_btn.pack(side="left", padx=(20, 0))

        self._progress_bar = ctk.CTkProgressBar(self, height=6, progress_color=PRIMARY_COLOR)
        self._progress_bar.pack(fill="x", padx=0)
        self._progress_bar.set(0)

        # ── Scrollable content area ────────────────────────────────────
        self._content_frame = ctk.CTkScrollableFrame(
            self, fg_color="transparent", corner_radius=0
        )
        self._content_frame.pack(fill="both", expand=True, padx=40, pady=(16, 0))

        # ── Bottom action bar ──────────────────────────────────────────
        bottom = ctk.CTkFrame(self, fg_color=_CLR_DEFAULT, corner_radius=0)
        bottom.pack(fill="x", side="bottom")

        btn_row = ctk.CTkFrame(bottom, fg_color="transparent")
        btn_row.pack(pady=12, padx=30)

        ctk.CTkButton(
            btn_row,
            text="✕  Kilép",
            width=120,
            height=40,
            font=FONT_BUTTON,
            fg_color="transparent",
            border_width=2,
            hover_color="#3a2020",
            command=self._quit_quiz,
        ).pack(side="left", padx=(0, 20))

        self._check_btn = ctk.CTkButton(
            btn_row,
            text="✔  Ellenőrzés",
            width=180,
            height=40,
            font=FONT_BUTTON,
            fg_color=PRIMARY_COLOR,
            state="disabled",
            command=self._submit_answer,
        )
        self._check_btn.pack(side="left", padx=(0, 12))

        self._next_btn = ctk.CTkButton(
            btn_row,
            text="Következő →",
            width=180,
            height=40,
            font=FONT_BUTTON,
            fg_color=SECONDARY_COLOR,
            state="disabled",
            command=self._next_question,
        )
        self._next_btn.pack(side="left")

    # ------------------------------------------------------------------
    # Load / render a single question into the content area
    # ------------------------------------------------------------------

    def _load_question(self) -> None:
        q = self.questions[self._idx]
        total = len(self.questions)

        assert self._content_frame is not None
        assert self._check_btn is not None
        assert self._next_btn is not None
        assert self._progress_label is not None
        assert self._progress_bar is not None

        # Clear previous content
        for w in self._content_frame.winfo_children():
            w.destroy()
        self._answer_btns = []
        self._selected = set()
        self._answered = False

        # Reset bottom buttons
        self._check_btn.configure(text="✔  Ellenőrzés", state="disabled", fg_color=PRIMARY_COLOR)
        self._next_btn.configure(
            text="Befejezés  ✓" if self._idx == total - 1 else "Következő →",
            state="disabled",
        )

        # Progress
        self._progress_label.configure(text=f"Kérdés  {self._idx + 1} / {total}")
        self._progress_bar.set((self._idx) / total)

        # ── Category + difficulty badge row ───────────────────────────
        meta_row = ctk.CTkFrame(self._content_frame, fg_color="transparent")
        meta_row.pack(fill="x", pady=(0, 6))

        diff_colors = {"easy": SUCCESS_COLOR, "medium": "#d68910", "hard": ERROR_COLOR}
        diff_labels = {"easy": "Könnyű", "medium": "Közepes", "hard": "Nehéz"}

        ctk.CTkLabel(
            meta_row,
            text=q.category,
            font=FONT_SMALL,
            fg_color=SECONDARY_COLOR,
            corner_radius=6,
            padx=10, pady=3,
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            meta_row,
            text=diff_labels.get(q.difficulty, q.difficulty),
            font=FONT_SMALL,
            fg_color=diff_colors.get(q.difficulty, PRIMARY_COLOR),
            corner_radius=6,
            padx=10, pady=3,
        ).pack(side="left")

        type_names = {
            "single_choice": "Egy helyes válasz",
            "multiple_choice": "Több helyes válasz",
            "true_false": "Igaz / Hamis",
            "code_reading": "Kódolvasás",
        }
        ctk.CTkLabel(
            meta_row,
            text=type_names.get(q.type, q.type),
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
        ).pack(side="right")

        # ── Question text (prose + optional code block) ─────────────────
        self._render_question_text(q.question, q.type)

        # ── Hint for multiple_choice ───────────────────────────────────
        if q.type == "multiple_choice":
            ctk.CTkLabel(
                self._content_frame,
                text="ℹ️  Jelölj meg minden helyes választ, majd kattints az Ellenőrzésre.",
                font=FONT_SMALL,
                text_color=TEXT_SECONDARY,
                anchor="w",
            ).pack(fill="x", pady=(0, 8))

        # ── Answer buttons ─────────────────────────────────────────────
        for i, ans_text in enumerate(q.answers):
            prefix = ["A)", "B)", "C)", "D)", "E)"][i] if len(q.answers) > 2 else ["✔", "✘"][i]
            btn = ctk.CTkButton(
                self._content_frame,
                text=f"  {prefix}  {ans_text}",
                width=860,
                height=46,
                font=FONT_BODY,
                fg_color=_CLR_DEFAULT,
                hover_color="#3a3a5a",
                corner_radius=8,
                anchor="w",
                command=lambda idx=i: self._toggle_answer(idx),
            )
            btn.pack(fill="x", pady=3)
            self._answer_btns.append(btn)

        # ── Explanation placeholder (hidden until submit) ──────────────
        self._explanation_label = ctk.CTkLabel(
            self._content_frame,
            text="",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
            wraplength=860,
            justify="left",
            anchor="w",
        )
        self._explanation_label.pack(fill="x", pady=(12, 4))

    # ------------------------------------------------------------------
    # Question text renderer (detects embedded code blocks)
    # ------------------------------------------------------------------

    def _render_question_text(self, text: str, q_type: str) -> None:
        """
        Render the question text into self._content_frame.

        If the text contains '\\n\\n', everything before it is rendered as
        prose and everything after as a syntax-highlighted code block.
        Pure prose questions get a plain CTkLabel.
        """
        assert self._content_frame is not None
        if "\n\n" in text:
            prose, code = text.split("\n\n", 1)
            if prose:
                ctk.CTkLabel(
                    self._content_frame,
                    text=prose,
                    font=FONT_BODY,
                    wraplength=860,
                    justify="left",
                    anchor="w",
                ).pack(fill="x", pady=(4, 6))
            block = create_code_block(self._content_frame, code)
            block.pack(fill="x", pady=(0, 14))
        else:
            ctk.CTkLabel(
                self._content_frame,
                text=text,
                font=FONT_BODY,
                wraplength=860,
                justify="left",
                anchor="w",
            ).pack(fill="x", pady=(4, 14))

    # ------------------------------------------------------------------
    # Answer selection
    # ------------------------------------------------------------------

    def _toggle_answer(self, idx: int) -> None:
        if self._answered or self._paused:
            return
        if idx >= len(self._answer_btns):  # guard: keyboard may exceed answer count
            return

        assert self._check_btn is not None
        q = self.questions[self._idx]

        if q.type in ("single_choice", "true_false", "code_reading"):
            # Radio style – deselect all others
            self._selected = {idx}
            for i, btn in enumerate(self._answer_btns):
                btn.configure(fg_color=_CLR_SELECTED if i == idx else _CLR_DEFAULT)
        else:
            # Checkbox style – toggle
            if idx in self._selected:
                self._selected.discard(idx)
                self._answer_btns[idx].configure(fg_color=_CLR_DEFAULT)
            else:
                self._selected.add(idx)
                self._answer_btns[idx].configure(fg_color=_CLR_SELECTED)

        # Enable check button only when something is selected
        state = "normal" if self._selected else "disabled"
        self._check_btn.configure(state=state)

    # ------------------------------------------------------------------
    # Submit & feedback
    # ------------------------------------------------------------------

    def _submit_answer(self) -> None:
        if self._answered:
            return
        self._answered = True

        assert self._explanation_label is not None
        assert self._check_btn is not None
        assert self._next_btn is not None

        q = self.questions[self._idx]
        selected = list(self._selected)
        correct = q.is_correct(selected)

        # Colour all buttons: correct=green, wrong-selected=red, missed=dark-green
        correct_set = set(q.correct)
        for i, btn in enumerate(self._answer_btns):
            if i in correct_set and i in self._selected:
                btn.configure(fg_color=_CLR_CORRECT)          # correctly selected
            elif i in correct_set:
                btn.configure(fg_color=_CLR_MISSED)           # missed correct
            elif i in self._selected:
                btn.configure(fg_color=_CLR_WRONG)            # wrong selection
            else:
                btn.configure(fg_color=_CLR_DEFAULT)

        # Show explanation
        if correct:
            icon = "✅"
        elif q.is_partial(selected):
            icon = "⚠️"
        else:
            icon = "❌"
        self._explanation_label.configure(
            text=f"{icon}  {q.explanation}"
        )

        # Record result
        self._results.append({
            "question": q,
            "selected": selected,
            "correct": correct,
        })

        # Update bottom buttons
        self._check_btn.configure(state="disabled", fg_color="#3a3a3a")
        self._next_btn.configure(state="normal")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _next_question(self) -> None:
        if not self._answered:
            return

        self._idx += 1
        if self._idx >= len(self.questions):
            self._finish()
        else:
            self._load_question()

    def _finish(self) -> None:
        self._cancel_timer()
        self._unbind_keys()
        assert self._progress_bar is not None
        total = len(self.questions)
        correct_count = sum(1 for r in self._results if r["correct"])
        wrong_ids = [
            r["question"].id for r in self._results if not r["correct"]
        ]
        self._progress_bar.set(1.0)
        self.app.show_results({
            "mode": self.mode,
            "category": self._category,
            "total": total,
            "correct": correct_count,
            "wrong_ids": wrong_ids,
            "results": self._results,
        })

    # ------------------------------------------------------------------
    # Timer (full mode only)
    # ------------------------------------------------------------------

    def _setup_timer(self) -> None:
        time_limit = QUIZ_MODES.get(self.mode, {}).get("time_limit")
        if time_limit is not None:
            self._time_left = time_limit * 60
        # Always start ticking (countdown for full, elapsed for others)
        self._timer_job = self.after(1000, self._tick)

    def _tick(self) -> None:
        time_limit = QUIZ_MODES.get(self.mode, {}).get("time_limit")
        if time_limit is not None:
            # ── Countdown (full mode) ─────────────────────────────────
            self._time_left -= 1
            if self._time_left <= 0:
                if self._timer_label:
                    self._timer_label.configure(text="⏱  00:00", text_color=ERROR_COLOR)
                self._finish_timed_out()
                return
            mins, secs = divmod(self._time_left, 60)
            text = f"⏱  {mins:02d}:{secs:02d}"
            if self._time_left < 60:
                color = ERROR_COLOR
            elif self._time_left < 300:
                color = "#d68910"
            else:
                color = "white"
        else:
            # ── Elapsed (quick / normal) ──────────────────────────────
            self._elapsed += 1
            mins, secs = divmod(self._elapsed, 60)
            text = f"⏱  {mins:02d}:{secs:02d}"
            color = TEXT_SECONDARY
        if self._timer_label:
            self._timer_label.configure(text=text, text_color=color)
        self._timer_job = self.after(1000, self._tick)

    def _cancel_timer(self) -> None:
        if self._timer_job is not None:
            self.after_cancel(self._timer_job)
            self._timer_job = None

    # ------------------------------------------------------------------
    # Keyboard shortcuts  (1-5 = select answer, Enter = submit/next)
    # ------------------------------------------------------------------

    def _bind_keys(self) -> None:
        root = self.app
        root.bind("<Return>", self._on_enter_key)
        root.bind("p", self._on_p_key)
        root.bind("P", self._on_p_key)
        root.bind("<Escape>", self._on_escape_key)
        for i in range(5):
            root.bind(str(i + 1), lambda e, idx=i: self._toggle_answer(idx))

    def _unbind_keys(self) -> None:
        root = self.app
        root.unbind("<Return>")
        root.unbind("p")
        root.unbind("P")
        root.unbind("<Escape>")
        for i in range(5):
            root.unbind(str(i + 1))

    def _on_enter_key(self, _event=None) -> None:
        if self._paused:
            return
        if not self._answered:
            if self._selected:
                self._submit_answer()
        else:
            self._next_question()

    def _quit_quiz(self) -> None:
        was_paused = self._paused
        if not self._paused:
            self._cancel_timer()

        dialog = ctk.CTkToplevel(self.app)
        dialog.title("Kilépés megerősítése")
        dialog.geometry("380x170")
        dialog.resizable(False, False)
        dialog.grab_set()

        self.app.update_idletasks()
        mx = self.app.winfo_x() + (self.app.winfo_width() - 380) // 2
        my = self.app.winfo_y() + (self.app.winfo_height() - 170) // 2
        dialog.geometry(f"380x170+{mx}+{my}")

        ctk.CTkLabel(
            dialog,
            text="Biztosan ki szeretnél lépni?\nAz eddigi eredmény nem lesz mentve.",
            font=("Segoe UI", 14),
            wraplength=340,
            justify="center",
        ).pack(expand=True, pady=(20, 8))

        btn_row = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_row.pack(pady=(0, 20))

        def _confirm():
            dialog.destroy()
            self._cancel_timer()
            self._unbind_keys()
            self.app.show_home()

        def _cancel():
            dialog.destroy()
            if not was_paused:
                self._timer_job = self.after(1000, self._tick)

        ctk.CTkButton(
            btn_row, text="Igen, kilépek", width=150, height=38,
            font=FONT_BUTTON, fg_color=ERROR_COLOR, hover_color="#922b21",
            command=_confirm,
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            btn_row, text="Mégsem", width=130, height=38,
            font=FONT_BUTTON, fg_color="transparent", border_width=2,
            hover_color="#2a2a3a", command=_cancel,
        ).pack(side="left", padx=8)

    # ------------------------------------------------------------------
    # Pause / Resume
    # ------------------------------------------------------------------

    def _toggle_pause(self) -> None:
        if self._paused:
            self._resume()
        else:
            self._pause()

    def _pause(self) -> None:
        if self._paused:
            return
        self._paused = True
        self._cancel_timer()
        if self._pause_btn:
            self._pause_btn.configure(text="▶  Folytatás")
        assert self._content_frame is not None
        # Hide the question content and show a pause overlay
        self._content_frame.pack_forget()
        self._pause_overlay = ctk.CTkFrame(self, fg_color="#1e1e2e", corner_radius=0)
        self._pause_overlay.pack(fill="both", expand=True)
        center = ctk.CTkFrame(self._pause_overlay, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(center, text="⏸", font=("Segoe UI Emoji", 52)).pack(pady=(0, 8))
        ctk.CTkLabel(center, text="Szüneteltetve", font=FONT_TITLE).pack()
        ctk.CTkLabel(
            center,
            text="Nyomj P-t, vagy kattints a Folytatásra.",
            font=FONT_BODY,
            text_color=TEXT_SECONDARY,
        ).pack(pady=(6, 0))

    def _resume(self) -> None:
        if not self._paused:
            return
        self._paused = False
        if self._pause_btn:
            self._pause_btn.configure(text="⏸  Szünet")
        if self._pause_overlay:
            self._pause_overlay.destroy()
            self._pause_overlay = None
        assert self._content_frame is not None
        # Restore the content frame in the correct position
        self._content_frame.pack(fill="both", expand=True, padx=40, pady=(16, 0))
        # Restart the timer tick
        self._timer_job = self.after(1000, self._tick)

    # ------------------------------------------------------------------
    # Timer expiry (countdown reaches zero)
    # ------------------------------------------------------------------

    def _finish_timed_out(self) -> None:
        """Auto-finish when the countdown hits zero; unanswered questions count as wrong."""
        # Current question not yet submitted
        if not self._answered and self._idx < len(self.questions):
            self._results.append({
                "question": self.questions[self._idx],
                "selected": [],
                "correct": False,
            })
        # All remaining questions
        for i in range(self._idx + 1, len(self.questions)):
            self._results.append({
                "question": self.questions[i],
                "selected": [],
                "correct": False,
            })
        self._finish()

    # ------------------------------------------------------------------
    # Extra key handlers
    # ------------------------------------------------------------------

    def _on_p_key(self, _event=None) -> None:
        self._toggle_pause()

    def _on_escape_key(self, _event=None) -> None:
        self._quit_quiz()
