"""
Terminal and diagnostics output panel for Peenoise Language IDE.
Features:
- Header title: 'Kinalabasan'
- Dynamic execution status badge (Handa / Tumatakbo / Tagumpay / May Error)
- Tabview:
  1. Kinalabasan (Console Output & formatted error diagnostics)
  2. Mga Token (Lexical token inspection)
  3. Puno ng Sintaks (Hierarchical AST tree)
  4. Mga Baryabol (Runtime variables inspection)
"""

import tkinter as tk
import customtkinter as ctk
from typing import Optional, List, Dict, Any

from gui_folder.theme import Theme
from gui_folder.compiler_runner import ExecutionResult, TokenInfo


class Terminal(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color=Theme.BG_PANEL, corner_radius=10, **kwargs)
        self._font_size = 12

        self._build_header()
        self._build_tabs()
        self.set_ready_status()

    def _build_header(self):
        """Constructs the top bar with title 'Kinalabasan' and status badges."""
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=8,
            height=38
        )
        self.header_frame.pack(fill="x", padx=6, pady=(6, 4))
        self.header_frame.pack_propagate(False)

        # Title: 'Kinalabasan' (matching user layout requirement)
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Kinalabasan",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=13, weight="bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        self.title_label.pack(side="left", padx=(12, 8))

        # Status Badge Pill
        self.status_badge = ctk.CTkLabel(
            self.header_frame,
            text="⚪ Handa",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11, weight="bold"),
            fg_color="#1E293B",
            text_color="#94A3B8",
            corner_radius=6,
            padx=8,
            pady=2
        )
        self.status_badge.pack(side="left", padx=4)

        # Execution time label
        self.time_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_MUTED
        )
        self.time_label.pack(side="left", padx=6)

        # Action buttons on right
        self.btn_clear = ctk.CTkButton(
            self.header_frame,
            text="Linisin",
            width=65,
            height=26,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=Theme.BTN_SECONDARY_BG,
            hover_color=Theme.BTN_SECONDARY_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            corner_radius=6,
            command=self.clear_all
        )
        self.btn_clear.pack(side="right", padx=(4, 10))

        self.btn_copy = ctk.CTkButton(
            self.header_frame,
            text="Kopyahin",
            width=70,
            height=26,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=Theme.BTN_SECONDARY_BG,
            hover_color=Theme.BTN_SECONDARY_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            corner_radius=6,
            command=self.copy_current_tab
        )
        self.btn_copy.pack(side="right", padx=4)

    def _build_tabs(self):
        """Builds tabbed views for Console, Tokens, AST, and Variables."""
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=Theme.TERMINAL_BG,
            segmented_button_fg_color=Theme.BG_CARD,
            segmented_button_selected_color=Theme.BTN_RUN_BG,
            segmented_button_selected_hover_color=Theme.BTN_RUN_HOVER,
            segmented_button_unselected_color=Theme.BG_CARD,
            segmented_button_unselected_hover_color=Theme.BG_CARD_HOVER,
            text_color=Theme.TEXT_PRIMARY,
            corner_radius=8
        )
        self.tabview.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Add tabs
        self.tab_console = self.tabview.add("Kinalabasan")
        self.tab_tokens = self.tabview.add("Mga Token")
        self.tab_ast = self.tabview.add("Puno ng Sintaks (AST)")
        self.tab_vars = self.tabview.add("Mga Baryabol")

        # 1. Console Textbox
        self.console_text = ctk.CTkTextbox(
            self.tab_console,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size),
            fg_color=Theme.TERMINAL_BG,
            text_color=Theme.TERMINAL_FG,
            corner_radius=6,
            wrap="none"
        )
        self.console_text.pack(fill="both", expand=True, padx=2, pady=2)
        self._setup_console_tags()

        # 2. Tokens Textbox
        self.tokens_text = ctk.CTkTextbox(
            self.tab_tokens,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size),
            fg_color=Theme.TERMINAL_BG,
            text_color=Theme.TERMINAL_FG,
            corner_radius=6,
            wrap="none"
        )
        self.tokens_text.pack(fill="both", expand=True, padx=2, pady=2)

        # 3. AST Textbox
        self.ast_text = ctk.CTkTextbox(
            self.tab_ast,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size),
            fg_color=Theme.TERMINAL_BG,
            text_color=Theme.TERMINAL_FG,
            corner_radius=6,
            wrap="none"
        )
        self.ast_text.pack(fill="both", expand=True, padx=2, pady=2)

        # 4. Variables Textbox
        self.vars_text = ctk.CTkTextbox(
            self.tab_vars,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size),
            fg_color=Theme.TERMINAL_BG,
            text_color=Theme.TERMINAL_FG,
            corner_radius=6,
            wrap="none"
        )
        self.vars_text.pack(fill="both", expand=True, padx=2, pady=2)

    def _setup_console_tags(self):
        """Sets up colored tags for the console output."""
        inner = self.console_text._textbox
        inner.tag_configure("success_banner", foreground=Theme.SUCCESS_GREEN, font=(Theme.FONT_FAMILY_CODE, self._font_size, "bold"))
        inner.tag_configure("error_badge", foreground="#FFFFFF", background="#991B1B", font=(Theme.FONT_FAMILY_CODE, self._font_size, "bold"))
        inner.tag_configure("error_msg", foreground="#F87171", font=(Theme.FONT_FAMILY_CODE, self._font_size, "bold"))
        inner.tag_configure("error_loc", foreground="#FCD34D", font=(Theme.FONT_FAMILY_CODE, self._font_size))
        inner.tag_configure("error_snippet", foreground="#E2E8F0", font=(Theme.FONT_FAMILY_CODE, self._font_size))
        inner.tag_configure("info_text", foreground=Theme.INFO_CYAN, font=(Theme.FONT_FAMILY_CODE, self._font_size))
        inner.tag_configure("normal_output", foreground="#F1F5F9", font=(Theme.FONT_FAMILY_CODE, self._font_size))
        inner.tag_configure("dim_text", foreground=Theme.TEXT_MUTED, font=(Theme.FONT_FAMILY_CODE, self._font_size))

    # ---------------- Display Methods ----------------

    def set_running_status(self):
        """Displays running state."""
        self.status_badge.configure(
            text="🟡 Tumatakbo...",
            fg_color="#78350F",
            text_color="#FDE68A"
        )
        self.time_label.configure(text="")

    def set_ready_status(self):
        """Displays ready state."""
        self.status_badge.configure(
            text="⚪ Handa",
            fg_color="#1E293B",
            text_color="#94A3B8"
        )
        self.time_label.configure(text="")

    def display_result(self, result: ExecutionResult):
        """Renders the execution results across all tabs."""
        # Update header badge
        if result.success:
            self.status_badge.configure(
                text="🟢 Tagumpay",
                fg_color="#064E3B",
                text_color="#A7F3D0"
            )
            self.time_label.configure(text=f"Oras: {result.execution_time_ms:.2f} ms")
        else:
            loc_str = f"L{result.error_line}:K{result.error_column}" if result.error_line else ""
            self.status_badge.configure(
                text=f"🔴 May Error {loc_str}".strip(),
                fg_color="#7F1D1D",
                text_color="#FECACA"
            )
            self.time_label.configure(text=f"Oras: {result.execution_time_ms:.2f} ms")

        # 1. Populate Console Output Tab
        self._render_console(result)

        # 2. Populate Tokens Tab
        self._render_tokens(result.tokens)

        # 3. Populate AST Tab
        self._render_ast(result.ast_tree)

        # 4. Populate Variables Tab
        self._render_variables(result.variables)

        # Ensure we switch to console tab
        self.tabview.set("Kinalabasan")

    def _render_console(self, result: ExecutionResult):
        """Populates the console tab with styled output or diagnostics."""
        tk_text = self.console_text._textbox
        tk_text.configure(state="normal")
        tk_text.delete("1.0", "end")

        if result.success:
            if result.output.strip():
                # Print program output
                for line in result.output.splitlines():
                    tk_text.insert("end", line + "\n", "normal_output")
            else:
                tk_text.insert("end", "(Walang output na ipinakita ang programa.)\n", "dim_text")

            # Success footer
            tk_text.insert("end", "\n----------------------------------------\n", "dim_text")
            tk_text.insert("end", f"✔ Matagumpay na natapos sa loob ng {result.execution_time_ms:.2f} ms\n", "success_banner")

        else:
            # Formatted Error Diagnostic Card
            tk_text.insert("end", f" ❌ {result.phase.upper()} \n", "error_badge")
            tk_text.insert("end", "\n")
            tk_text.insert("end", f"Uri ng Error : {result.error_type}\n", "error_msg")

            if result.error_line:
                tk_text.insert("end", f"Lokasyon     : Linya {result.error_line}, Kolum {result.error_column}\n", "error_loc")

            tk_text.insert("end", f"Paliwanag    : {result.error_message}\n\n", "error_msg")

            if result.error_snippet:
                tk_text.insert("end", "Tingnan ang kodigo sa bahaging ito:\n", "info_text")
                tk_text.insert("end", result.error_snippet + "\n\n", "error_snippet")

            tk_text.insert("end", "💡 Payo: Suriin ang tamang baybay, tuldok-kuwit (;), at uri ng datos sa 'Bokabularyo'.\n", "dim_text")

        tk_text.configure(state="disabled")

    def _render_tokens(self, tokens: List[TokenInfo]):
        """Renders lexical tokens in a clean tabular view."""
        tk_text = self.tokens_text._textbox
        tk_text.configure(state="normal")
        tk_text.delete("1.0", "end")

        if not tokens:
            tk_text.insert("end", "(Walang mga token na naitala.)\n")
            tk_text.configure(state="disabled")
            return

        header = f"{'#':<4} {'POSISYON':<14} {'URI NG TOKEN':<24} {'TEKSTO (LEXEME)':<22} {'LITERAL':<15}\n"
        separator = "=" * 80 + "\n"
        tk_text.insert("end", header)
        tk_text.insert("end", separator)

        for idx, tok in enumerate(tokens, start=1):
            pos_str = f"L{tok.line}:K{tok.column}"
            lit_str = str(tok.literal) if tok.literal is not None else "-"
            lexeme_display = repr(tok.lexeme) if len(tok.lexeme) > 0 else "EOF"
            row = f"{idx:<4} {pos_str:<14} {tok.token_type:<24} {lexeme_display:<22} {lit_str:<15}\n"
            tk_text.insert("end", row)

        tk_text.configure(state="disabled")

    def _render_ast(self, ast_tree: str):
        """Displays AST tree."""
        tk_text = self.ast_text._textbox
        tk_text.configure(state="normal")
        tk_text.delete("1.0", "end")

        if ast_tree.strip():
            tk_text.insert("end", ast_tree + "\n")
        else:
            tk_text.insert("end", "(Walang AST tree. Posibleng may error sa Parser o walang kodigo.)\n")

        tk_text.configure(state="disabled")

    def _render_variables(self, variables: Dict[str, Any]):
        """Displays runtime variables."""
        tk_text = self.vars_text._textbox
        tk_text.configure(state="normal")
        tk_text.delete("1.0", "end")

        if not variables:
            tk_text.insert("end", "(Walang aktibong baryabol o hindi natapos ang pagpapatupad.)\n")
            tk_text.configure(state="disabled")
            return

        header = f"{'PANGALAN NG BARYABOL':<28} {'URI (PYTHON TYPE)':<20} {'KASALUKUYANG HALAGA':<25}\n"
        separator = "=" * 75 + "\n"
        tk_text.insert("end", header)
        tk_text.insert("end", separator)

        for var_name, val in variables.items():
            type_name = type(val).__name__
            val_display = repr(val)
            row = f"{var_name:<28} {type_name:<20} {val_display:<25}\n"
            tk_text.insert("end", row)

        tk_text.configure(state="disabled")

    def clear_all(self):
        """Clears all terminal and inspector tabs."""
        for text_widget in [self.console_text, self.tokens_text, self.ast_text, self.vars_text]:
            inner = text_widget._textbox
            inner.configure(state="normal")
            inner.delete("1.0", "end")
            inner.configure(state="disabled")
        self.set_ready_status()

    def copy_current_tab(self):
        """Copies content of the active tab to clipboard."""
        current_tab_name = self.tabview.get()
        mapping = {
            "Kinalabasan": self.console_text,
            "Mga Token": self.tokens_text,
            "Puno ng Sintaks (AST)": self.ast_text,
            "Mga Baryabol": self.vars_text,
        }
        target = mapping.get(current_tab_name, self.console_text)
        content = target._textbox.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(content)

    def set_font_size(self, size: int):
        """Changes font size for all terminal tabs."""
        self._font_size = max(9, min(24, size))
        new_font = ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size)
        for tw in [self.console_text, self.tokens_text, self.ast_text, self.vars_text]:
            tw.configure(font=new_font)
        self._setup_console_tags()
