"""
Sidebar component for Peenoise Language IDE.
Features:
- Main action buttons matching the layout:
  1. Patakbuhin (Run)
  2. Bokabularyo (Dictionary)
  3. Muling Itakda (Reset / Clear)
- Preset sample loader (Pangunahing Pagsubok, Kondisyonal, Pihitan, etc.)
- Quick terminal clear button
- Font zoom adjuster
- Appearance theme switcher
- Keyboard shortcuts cheat sheet
"""

import customtkinter as ctk
from typing import Callable, Optional

from gui_folder.theme import Theme
from gui_folder.sample_codes import SAMPLE_CODES


class Sidebar(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_run: Optional[Callable[[], None]] = None,
        on_dictionary: Optional[Callable[[], None]] = None,
        on_reset: Optional[Callable[[], None]] = None,
        on_load_sample: Optional[Callable[[str], None]] = None,
        on_clear_terminal: Optional[Callable[[], None]] = None,
        on_zoom_change: Optional[Callable[[int], None]] = None,
        **kwargs
    ):
        super().__init__(parent, fg_color=Theme.BG_SIDEBAR, width=240, corner_radius=0, **kwargs)
        self.pack_propagate(False)

        self.on_run = on_run
        self.on_dictionary = on_dictionary
        self.on_reset = on_reset
        self.on_load_sample = on_load_sample
        self.on_clear_terminal = on_clear_terminal
        self.on_zoom_change = on_zoom_change
        self._current_font_size = 13

        self._build_branding()
        self._build_primary_buttons()
        self._build_samples_section()
        self._build_tools_section()
        self._build_shortcuts_footer()

    def _build_branding(self):
        """Constructs logo and project title."""
        brand_frame = ctk.CTkFrame(self, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(16, 12))

        logo_row = ctk.CTkFrame(brand_frame, fg_color="transparent")
        logo_row.pack(anchor="w")

        title_lbl = ctk.CTkLabel(
            logo_row,
            text="🇵🇭 Peenoise",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=20, weight="bold"),
            text_color="#38BDF8"
        )
        title_lbl.pack(side="left")

        version_badge = ctk.CTkLabel(
            logo_row,
            text="v1.0",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10, weight="bold"),
            fg_color="#1E293B",
            text_color="#94A3B8",
            corner_radius=6,
            padx=6,
            pady=1
        )
        version_badge.pack(side="left", padx=6)

        subtitle_lbl = ctk.CTkLabel(
            brand_frame,
            text="Tagalog Mini Compiler IDE",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_MUTED
        )
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # Thin separator line
        sep = ctk.CTkFrame(self, fg_color=Theme.BORDER_COLOR, height=1)
        sep.pack(fill="x", padx=16, pady=(8, 12))

    def _build_primary_buttons(self):
        """Constructs the 3 primary action buttons requested by user."""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=16, pady=4)

        sec_label = ctk.CTkLabel(
            actions_frame,
            text="MGA PANGUNAHING UTOS",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10, weight="bold"),
            text_color=Theme.TEXT_MUTED
        )
        sec_label.pack(anchor="w", pady=(0, 6))

        # 1. Patakbuhin (Run) - Cyan / Electric Teal
        self.btn_run = ctk.CTkButton(
            actions_frame,
            text="▶  Patakbuhin",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=14, weight="bold"),
            fg_color=Theme.BTN_RUN_BG,
            hover_color=Theme.BTN_RUN_HOVER,
            text_color=Theme.BTN_RUN_TEXT,
            height=42,
            corner_radius=8,
            command=self._handle_run
        )
        self.btn_run.pack(fill="x", pady=4)

        # 2. Bokabularyo (Dictionary) - Deep Slate / Indigo
        self.btn_dict = ctk.CTkButton(
            actions_frame,
            text="📖  Bokabularyo",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=13, weight="bold"),
            fg_color=Theme.BTN_DICT_BG,
            hover_color=Theme.BTN_DICT_HOVER,
            text_color=Theme.BTN_DICT_TEXT,
            height=40,
            corner_radius=8,
            command=self._handle_dictionary
        )
        self.btn_dict.pack(fill="x", pady=4)

        # 3. Muling Itakda (Reset / Clear) - Vibrant Crimson / Rose
        self.btn_reset = ctk.CTkButton(
            actions_frame,
            text="↺  Muling Itakda",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=13, weight="bold"),
            fg_color=Theme.BTN_RESET_BG,
            hover_color=Theme.BTN_RESET_HOVER,
            text_color=Theme.BTN_RESET_TEXT,
            height=40,
            corner_radius=8,
            command=self._handle_reset
        )
        self.btn_reset.pack(fill="x", pady=4)

    def _build_samples_section(self):
        """Constructs sample code selector dropdown."""
        samples_frame = ctk.CTkFrame(self, fg_color="transparent")
        samples_frame.pack(fill="x", padx=16, pady=(14, 4))

        sec_label = ctk.CTkLabel(
            samples_frame,
            text="MGA HALIMBAWANG KODIGO",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10, weight="bold"),
            text_color=Theme.TEXT_MUTED
        )
        sec_label.pack(anchor="w", pady=(0, 6))

        sample_names = list(SAMPLE_CODES.keys())
        self.sample_dropdown = ctk.CTkOptionMenu(
            samples_frame,
            values=sample_names,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            dropdown_font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=Theme.BG_CARD,
            button_color=Theme.BG_CARD_HOVER,
            button_hover_color="#374151",
            text_color=Theme.TEXT_PRIMARY,
            height=34,
            corner_radius=6,
            command=self._handle_sample_select
        )
        self.sample_dropdown.pack(fill="x")
        self.sample_dropdown.set(sample_names[0])

    def _build_tools_section(self):
        """Constructs tools for zoom, theme, and terminal clear."""
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.pack(fill="x", padx=16, pady=(14, 4))

        sec_label = ctk.CTkLabel(
            tools_frame,
            text="MGA KAGAMITAN",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10, weight="bold"),
            text_color=Theme.TEXT_MUTED
        )
        sec_label.pack(anchor="w", pady=(0, 6))

        # Clear Terminal Button
        btn_clr_term = ctk.CTkButton(
            tools_frame,
            text="🗑️  Linisin ang Terminal",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=Theme.BG_CARD,
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            height=32,
            corner_radius=6,
            command=self._handle_clear_terminal
        )
        btn_clr_term.pack(fill="x", pady=2)

        # Zoom adjustment (+ / -)
        zoom_row = ctk.CTkFrame(tools_frame, fg_color="transparent")
        zoom_row.pack(fill="x", pady=4)

        zoom_lbl = ctk.CTkLabel(
            zoom_row,
            text="Laki ng Font:",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_SECONDARY
        )
        zoom_lbl.pack(side="left")

        btn_plus = ctk.CTkButton(
            zoom_row,
            text="+",
            width=28,
            height=26,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=12, weight="bold"),
            fg_color=Theme.BG_CARD,
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_PRIMARY,
            command=lambda: self._adjust_font(1)
        )
        btn_plus.pack(side="right", padx=(2, 0))

        self.zoom_display = ctk.CTkLabel(
            zoom_row,
            text=f"{self._current_font_size}px",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_MUTED,
            width=36
        )
        self.zoom_display.pack(side="right")

        btn_minus = ctk.CTkButton(
            zoom_row,
            text="-",
            width=28,
            height=26,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=12, weight="bold"),
            fg_color=Theme.BG_CARD,
            hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_PRIMARY,
            command=lambda: self._adjust_font(-1)
        )
        btn_minus.pack(side="right", padx=(0, 2))

        # Appearance mode menu
        theme_row = ctk.CTkFrame(tools_frame, fg_color="transparent")
        theme_row.pack(fill="x", pady=4)

        theme_lbl = ctk.CTkLabel(
            theme_row,
            text="Tema:",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_SECONDARY
        )
        theme_lbl.pack(side="left")

        self.theme_menu = ctk.CTkOptionMenu(
            theme_row,
            values=["Madilim (Dark)", "Maliwanag (Light)", "Sistema (System)"],
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10),
            dropdown_font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10),
            fg_color=Theme.BG_CARD,
            button_color=Theme.BG_CARD_HOVER,
            width=120,
            height=26,
            corner_radius=6,
            command=self._change_theme
        )
        self.theme_menu.pack(side="right")
        self.theme_menu.set("Madilim (Dark)")

    def _build_shortcuts_footer(self):
        """Constructs bottom shortcuts reference box."""
        card = ctk.CTkFrame(self, fg_color=Theme.BG_CARD, corner_radius=8)
        card.pack(side="bottom", fill="x", padx=16, pady=16)

        title = ctk.CTkLabel(
            card,
            text="⌨️ Mabilisang Pindutan",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11, weight="bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        title.pack(anchor="w", padx=10, pady=(8, 4))

        shortcuts = [
            ("F5 / Ctrl+Enter", "Patakbuhin"),
            ("Ctrl+B", "Bokabularyo"),
            ("Ctrl+R", "Muling Itakda"),
            ("Ctrl+L", "Linisin")
        ]

        for key, desc in shortcuts:
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=1)

            k_lbl = ctk.CTkLabel(
                row,
                text=key,
                font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=10, weight="bold"),
                text_color="#38BDF8"
            )
            k_lbl.pack(side="left")

            d_lbl = ctk.CTkLabel(
                row,
                text=desc,
                font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=10),
                text_color=Theme.TEXT_MUTED
            )
            d_lbl.pack(side="right")

        spacer = ctk.CTkLabel(card, text="", height=4)
        spacer.pack()

    # ---------------- Action Handlers ----------------

    def _handle_run(self):
        if self.on_run:
            self.on_run()

    def _handle_dictionary(self):
        if self.on_dictionary:
            self.on_dictionary()

    def _handle_reset(self):
        if self.on_reset:
            self.on_reset()

    def _handle_sample_select(self, sample_name: str):
        if self.on_load_sample and sample_name in SAMPLE_CODES:
            self.on_load_sample(SAMPLE_CODES[sample_name])

    def _handle_clear_terminal(self):
        if self.on_clear_terminal:
            self.on_clear_terminal()

    def _adjust_font(self, delta: int):
        new_size = max(9, min(24, self._current_font_size + delta))
        if new_size != self._current_font_size:
            self._current_font_size = new_size
            self.zoom_display.configure(text=f"{self._current_font_size}px")
            if self.on_zoom_change:
                self.on_zoom_change(self._current_font_size)

    def _change_theme(self, selection: str):
        if "Madilim" in selection:
            ctk.set_appearance_mode("dark")
        elif "Maliwanag" in selection:
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")
