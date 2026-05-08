import customtkinter as ctk

from config import (
    PRIMARY_COLOR, SECONDARY_COLOR,
    SUCCESS_COLOR, ERROR_COLOR, WARNING_COLOR,
    TEXT_SECONDARY,
    FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_SMALL, FONT_BUTTON,
)


class HomeScreen(ctk.CTkFrame):
    """Main menu screen with quiz mode selection."""

    def __init__(self, parent: ctk.CTk, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        self._build_header()
        self._build_divider()
        self._build_mode_buttons()
        self._build_stats_preview()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(50, 0))

        ctk.CTkLabel(
            header,
            text="📚 Szoftverfejlesztés",
            font=FONT_TITLE,
        ).pack()

        ctk.CTkLabel(
            header,
            text="Vizsgagyakorló Alkalmazás",
            font=FONT_SUBTITLE,
            text_color=TEXT_SECONDARY,
        ).pack(pady=(4, 0))

        ctk.CTkLabel(
            header,
            text="2. ZH felkészülés",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
        ).pack(pady=(2, 0))

    def _build_divider(self) -> None:
        ctk.CTkFrame(self, height=2, fg_color=PRIMARY_COLOR).pack(
            fill="x", padx=100, pady=28
        )

    def _build_mode_buttons(self) -> None:
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack()

        ctk.CTkLabel(
            container,
            text="Válassz tesztmódot:",
            font=FONT_SUBTITLE,
        ).pack(pady=(0, 18))

        mode_defs = [
            ("⚡  Gyors teszt  (10 kérdés)",       "quick",    SUCCESS_COLOR,   "#236b3c"),
            ("📝  Normál teszt  (25 kérdés)",       "normal",   PRIMARY_COLOR,   "#173f6a"),
            ("🎯  Teljes ZH szimuláció  (50 kérdés)", "full",   ERROR_COLOR,     "#922b21"),
            ("📂  Kategória alapú teszt",            "category", SECONDARY_COLOR, "#1e5480"),
            ("❌  Hibás kérdések gyakorlása",        "mistakes", WARNING_COLOR,   "#a0690c"),
        ]

        for label, mode, color, hover in mode_defs:
            ctk.CTkButton(
                container,
                text=label,
                width=370,
                height=50,
                font=FONT_BUTTON,
                fg_color=color,
                hover_color=hover,
                corner_radius=10,
                command=lambda m=mode: self.app.start_quiz(m),
            ).pack(pady=5)

    def _build_stats_preview(self) -> None:
        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(pady=28, padx=60, fill="x")

        stats = self.app.stats_manager.stats
        total = stats.get("total_tests", 0)
        best  = stats.get("best_score", 0)
        avg   = stats.get("avg_percent", 0.0)

        if total == 0:
            text = "📊  Még nem töltöttél ki tesztet. Kezdj el egyet!"
        else:
            last_date = stats.get("last_test_date")
            date_part = f"   |   Utolsó: {last_date}" if last_date else ""
            text = (
                f"📊  Kitöltött tesztek: {total}   |   "
                f"Legjobb: {best}%   |   "
                f"Átlag: {avg:.1f}%{date_part}"
            )

        ctk.CTkLabel(
            card,
            text=text,
            font=FONT_BODY,
            text_color=TEXT_SECONDARY,
        ).pack(pady=18, padx=20)
