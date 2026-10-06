"""
Dictionary window ('Bokabularyo') for Peenoise Language IDE.
Presents a modern, searchable cheat sheet of all Peenoise language syntaxes,
data types, keywords, operators, and snippets with quick copy and insert buttons.
"""

import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional, List

from gui_folder.theme import Theme
from gui_folder.dictionary_data import DICTIONARY_ENTRIES, CATEGORIES, DictionaryEntry


class DictionaryWindow(ctk.CTkToplevel):
    def __init__(self, parent, on_insert_snippet: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        self.on_insert_snippet = on_insert_snippet

        self.title("Bokabularyo ng Peenoise Language")
        self.geometry("860x650")
        self.minsize(700, 500)
        self.configure(fg_color=Theme.BG_MAIN)

        self._active_category = "Lahat"
        self._search_query = ""

        # Make it appear above parent
        self.transient(parent)
        self.after(50, self.lift)

        self._build_header()
        self._build_filters()
        self._build_content_area()
        self._render_entries()

    def _build_header(self):
        """Builds search bar and title banner."""
        self.header_frame = ctk.CTkFrame(self, fg_color=Theme.BG_PANEL, corner_radius=10)
        self.header_frame.pack(fill="x", padx=14, pady=(14, 8))

        top_row = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        top_row.pack(fill="x", padx=16, pady=(12, 6))

        # Title and subtitle
        title_box = ctk.CTkFrame(top_row, fg_color="transparent")
        title_box.pack(side="left")

        title_lbl = ctk.CTkLabel(
            title_box,
            text="📖 Bokabularyo ng Peenoise",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=18, weight="bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = ctk.CTkLabel(
            title_box,
            text="Talaan ng mga sintaks, uri ng datos, keyword, at operator sa wikang Tagalog",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=12),
            text_color=Theme.TEXT_SECONDARY
        )
        subtitle_lbl.pack(anchor="w")

        # Live Search Entry
        self.search_entry = ctk.CTkEntry(
            self.header_frame,
            placeholder_text="Maghanap ng keyword, operator, o sintaks (hal. 'kung', 'numero', 'print')...",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=13),
            fg_color=Theme.BG_CARD,
            border_color=Theme.BORDER_COLOR,
            text_color=Theme.TEXT_PRIMARY,
            height=38,
            corner_radius=8
        )
        self.search_entry.pack(fill="x", padx=16, pady=(6, 12))
        self.search_entry.bind("<KeyRelease>", self._on_search_change)

    def _build_filters(self):
        """Builds category filter bar."""
        self.filter_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            orientation="horizontal",
            height=46
        )
        self.filter_frame.pack(fill="x", padx=14, pady=(0, 6))

        self.category_buttons: List[ctk.CTkButton] = []
        for cat in CATEGORIES:
            btn = ctk.CTkButton(
                self.filter_frame,
                text=cat,
                font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11, weight="bold"),
                fg_color=Theme.BTN_DICT_BG if cat == "Lahat" else Theme.BG_CARD,
                hover_color=Theme.BTN_DICT_HOVER if cat == "Lahat" else Theme.BG_CARD_HOVER,
                text_color="#FFFFFF" if cat == "Lahat" else Theme.TEXT_SECONDARY,
                height=30,
                corner_radius=15,
                command=lambda c=cat: self._set_category(c)
            )
            btn.pack(side="left", padx=4)
            self.category_buttons.append(btn)

    def _build_content_area(self):
        """Builds scrollable container for dictionary cards."""
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=Theme.BG_MAIN,
            corner_radius=8
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    def _set_category(self, category: str):
        """Switches active category filter."""
        self._active_category = category
        for btn in self.category_buttons:
            if btn.cget("text") == category:
                btn.configure(fg_color=Theme.BTN_DICT_BG, text_color="#FFFFFF")
            else:
                btn.configure(fg_color=Theme.BG_CARD, text_color=Theme.TEXT_SECONDARY)
        self._render_entries()

    def _on_search_change(self, event=None):
        """Filters entries based on user search term."""
        self._search_query = self.search_entry.get().strip().lower()
        self._render_entries()

    def _render_entries(self):
        """Populates scroll area with matching dictionary cards."""
        # Clear existing card widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Filter entries
        filtered: List[DictionaryEntry] = []
        for entry in DICTIONARY_ENTRIES:
            # Check category
            if self._active_category != "Lahat" and entry.category != self._active_category:
                continue

            # Check search query
            if self._search_query:
                searchable = (
                    entry.name.lower()
                    + " " + entry.category.lower()
                    + " " + entry.english_equiv.lower()
                    + " " + entry.syntax.lower()
                    + " " + entry.description.lower()
                    + " " + " ".join(entry.tags)
                )
                if self._search_query not in searchable:
                    continue

            filtered.append(entry)

        if not filtered:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text=f"Walang nahanap para sa '{self._search_query}'. Subukan ang ibang salita.",
                font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=13),
                text_color=Theme.TEXT_MUTED
            )
            empty_lbl.pack(pady=40)
            return

        # Render each dictionary card
        for entry in filtered:
            self._create_entry_card(entry)

    def _create_entry_card(self, entry: DictionaryEntry):
        """Constructs an individual entry card widget."""
        card = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=Theme.BG_PANEL,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            corner_radius=10
        )
        card.pack(fill="x", pady=6, padx=4)

        # Header Row
        head_row = ctk.CTkFrame(card, fg_color="transparent")
        head_row.pack(fill="x", padx=14, pady=(10, 4))

        # Syntax Name
        name_lbl = ctk.CTkLabel(
            head_row,
            text=entry.name,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=15, weight="bold"),
            text_color="#38BDF8"
        )
        name_lbl.pack(side="left")

        # English Equivalent badge
        en_badge = ctk.CTkLabel(
            head_row,
            text=f"Eng: {entry.english_equiv}",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color="#1E293B",
            text_color="#94A3B8",
            corner_radius=6,
            padx=8,
            pady=2
        )
        en_badge.pack(side="left", padx=10)

        # Category pill
        cat_badge = ctk.CTkLabel(
            head_row,
            text=entry.category,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11, weight="bold"),
            fg_color="#312E81",
            text_color="#C7D2FE",
            corner_radius=6,
            padx=8,
            pady=2
        )
        cat_badge.pack(side="right")

        # Syntax Signature Box
        syntax_box = ctk.CTkFrame(card, fg_color=Theme.BG_CARD, corner_radius=6)
        syntax_box.pack(fill="x", padx=14, pady=4)

        syntax_lbl = ctk.CTkLabel(
            syntax_box,
            text=f"Sintaks: {entry.syntax}",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=12),
            text_color="#F1F5F9",
            anchor="w"
        )
        syntax_lbl.pack(fill="x", padx=10, pady=6)

        # Description
        desc_lbl = ctk.CTkLabel(
            card,
            text=entry.description,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=12),
            text_color=Theme.TEXT_SECONDARY,
            anchor="w",
            justify="left",
            wraplength=760
        )
        desc_lbl.pack(fill="x", padx=14, pady=4)

        # Example Code Box
        ex_container = ctk.CTkFrame(card, fg_color="#0F172A", corner_radius=6)
        ex_container.pack(fill="x", padx=14, pady=6)

        ex_lbl = ctk.CTkLabel(
            ex_container,
            text=entry.example,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=12),
            text_color="#A5F3FC",
            anchor="w",
            justify="left"
        )
        ex_lbl.pack(side="left", fill="both", expand=True, padx=10, pady=8)

        # Action buttons for example
        btn_box = ctk.CTkFrame(card, fg_color="transparent")
        btn_box.pack(fill="x", padx=14, pady=(2, 10))

        if self.on_insert_snippet:
            insert_btn = ctk.CTkButton(
                btn_box,
                text="Ipasok sa Editor ➕",
                width=130,
                height=28,
                font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11, weight="bold"),
                fg_color=Theme.BTN_RUN_BG,
                hover_color=Theme.BTN_RUN_HOVER,
                text_color="#FFFFFF",
                corner_radius=6,
                command=lambda ex=entry.example: self._insert_to_editor(ex)
            )
            insert_btn.pack(side="right", padx=(6, 0))

        copy_btn = ctk.CTkButton(
            btn_box,
            text="Kopyahin 📋",
            width=90,
            height=28,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=Theme.BTN_SECONDARY_BG,
            hover_color=Theme.BTN_SECONDARY_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            corner_radius=6,
            command=lambda ex=entry.example: self._copy_snippet(ex)
        )
        copy_btn.pack(side="right")

    def _insert_to_editor(self, code: str):
        """Passes snippet to editor callback and brings parent window to front."""
        if self.on_insert_snippet:
            self.on_insert_snippet(code)

    def _copy_snippet(self, code: str):
        """Copies code snippet to system clipboard."""
        self.clipboard_clear()
        self.clipboard_append(code)
