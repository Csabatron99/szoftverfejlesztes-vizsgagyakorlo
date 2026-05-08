import customtkinter as ctk

from config import (
    APP_TITLE, APP_WIDTH, APP_HEIGHT,
    APPEARANCE_MODE, COLOR_THEME,
    QUIZ_MODES,
)
from question_manager import QuestionManager
from stats_manager import StatsManager


class ExamTrainerApp(ctk.CTk):
    """Root application window. Manages screen transitions."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)

        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(800, 600)
        self._center_window()

        # Managers
        self.question_manager = QuestionManager()
        self.stats_manager = StatsManager()

        # Active screen frame
        self._current_screen: ctk.CTkFrame | None = None

        self.show_home()

    # ------------------------------------------------------------------
    # Window helpers
    # ------------------------------------------------------------------

    def _center_window(self) -> None:
        self.update_idletasks()
        x = (self.winfo_screenwidth()  - APP_WIDTH)  // 2
        y = (self.winfo_screenheight() - APP_HEIGHT) // 2
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

    def _clear_screen(self) -> None:
        if self._current_screen is not None:
            self._current_screen.destroy()
            self._current_screen = None

    # ------------------------------------------------------------------
    # Screen navigation
    # ------------------------------------------------------------------

    def show_home(self) -> None:
        from ui.home_screen import HomeScreen
        self._clear_screen()
        self._current_screen = HomeScreen(self, self)
        self._current_screen.pack(fill="both", expand=True)

    def show_category_select(self) -> None:
        from ui.category_screen import CategoryScreen
        self._clear_screen()
        categories = self.question_manager.get_categories()
        self._current_screen = CategoryScreen(self, self, categories)
        self._current_screen.pack(fill="both", expand=True)

    def start_quiz(self, mode: str, category: str | None = None) -> None:
        if mode == "category":
            self.show_category_select()
            return

        if mode == "mistakes":
            wrong_ids = self.stats_manager.get_wrong_ids()
            if not wrong_ids:
                self._show_info("Nincs mentett hibás kérdés.\nElőbb tölts ki egy tesztet!")
                return
            questions = self.question_manager.get_by_ids(wrong_ids)
        elif mode == "category_run":
            # Started from CategoryScreen with a specific category selected
            questions = self.question_manager.get_random(category=category)
        else:
            count = QUIZ_MODES[mode]["count"]
            questions = self.question_manager.get_random(count=count, category=category)

        if not questions:
            self._show_info("Nincs elérhető kérdés ehhez a módhoz.\nElőbb töltsd be a kérdésbankot!")
            return

        from ui.quiz_screen import QuizScreen
        self._clear_screen()
        self._current_screen = QuizScreen(self, self, questions, mode, category=category)
        self._current_screen.pack(fill="both", expand=True)

    def show_results(self, results: dict) -> None:
        from ui.result_screen import ResultScreen
        self._clear_screen()
        self._current_screen = ResultScreen(self, self, results)
        self._current_screen.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # Utility dialogs
    # ------------------------------------------------------------------

    def _show_info(self, message: str) -> None:
        dialog = ctk.CTkToplevel(self)
        dialog.title("Információ")
        dialog.geometry("420x200")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=message,
            font=("Segoe UI", 14),
            wraplength=370,
            justify="center",
        ).pack(expand=True, pady=20)

        ctk.CTkButton(dialog, text="OK", width=120, command=dialog.destroy).pack(pady=(0, 20))
