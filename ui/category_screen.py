import customtkinter as ctk

from config import (
    PRIMARY_COLOR, SECONDARY_COLOR, TEXT_SECONDARY,
    FONT_TITLE, FONT_SUBTITLE, FONT_BODY, FONT_SMALL, FONT_BUTTON,
)


class CategoryScreen(ctk.CTkFrame):
    """Lets the user pick a category before starting a category quiz."""

    def __init__(self, parent: ctk.CTk, app, categories: list[str]):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.categories = categories
        # Map category → question count for display
        self._counts: dict[str, int] = {
            cat: len(self.app.question_manager.get_by_category(cat))
            for cat in categories
        }
        self._build_ui()

    def _build_ui(self) -> None:
        self._build_header()
        self._build_divider()
        self._build_category_list()
        self._build_back_button()

    # ------------------------------------------------------------------

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(40, 0))

        ctk.CTkLabel(header, text="📂 Kategória választó", font=FONT_TITLE).pack()

        ctk.CTkLabel(
            header,
            text="Válassz egy témakört a gyakorláshoz:",
            font=FONT_SUBTITLE,
            text_color=TEXT_SECONDARY,
        ).pack(pady=(6, 0))

        total = sum(self._counts.values())
        ctk.CTkLabel(
            header,
            text=f"Összesen {total} kérdés, {len(self.categories)} kategóriában",
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
        ).pack(pady=(2, 0))

    def _build_divider(self) -> None:
        ctk.CTkFrame(self, height=2, fg_color=PRIMARY_COLOR).pack(
            fill="x", padx=100, pady=20
        )

    def _build_category_list(self) -> None:
        scroll = ctk.CTkScrollableFrame(self, width=540, height=340)
        scroll.pack(padx=40)

        if not self.categories:
            ctk.CTkLabel(
                scroll,
                text="Nincs elérhető kategória.\nElőbb töltsd be a kérdésbankot!",
                font=FONT_BODY,
                text_color=TEXT_SECONDARY,
            ).pack(expand=True, pady=40)
            return

        for cat in self.categories:
            count = self._counts[cat]
            self._build_category_row(scroll, cat, count)

    def _build_category_row(
        self, parent: ctk.CTkScrollableFrame, cat: str, count: int
    ) -> None:
        """One row: category button + question-count badge."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=4)

        btn = ctk.CTkButton(
            row,
            text=cat,
            width=430,
            height=46,
            font=FONT_BUTTON,
            fg_color=PRIMARY_COLOR,
            hover_color="#173f6a",
            corner_radius=8,
            anchor="w",
            command=lambda c=cat: self.app.start_quiz("category_run", category=c),
        )
        btn.pack(side="left")

        badge = ctk.CTkLabel(
            row,
            text=f"{count} kérdés",
            width=80,
            height=46,
            font=FONT_SMALL,
            text_color=TEXT_SECONDARY,
            fg_color=SECONDARY_COLOR,
            corner_radius=8,
        )
        badge.pack(side="left", padx=(6, 0))

    def _build_back_button(self) -> None:
        ctk.CTkButton(
            self,
            text="← Vissza a főmenübe",
            width=220,
            height=40,
            font=FONT_BUTTON,
            fg_color="transparent",
            border_width=2,
            hover_color="#2a2a3a",
            command=self.app.show_home,
        ).pack(pady=24)
