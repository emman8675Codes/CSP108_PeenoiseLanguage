"""
Peenoise Language IDE - Main Application Window.
OOP architecture coordinating:
- Sidebar (action buttons, samples, settings)
- Resizable Split Pane
- Code Editor ('Mga tagubilin o iskrip')
- Terminal & Compiler Diagnostics ('Kinalabasan')
- Syntax Dictionary ('Bokabularyo')
- Bottom status bar and hotkeys
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# Ensure parent directory is in sys.path when run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from gui_folder.theme import Theme
from gui_folder.sidebar import Sidebar
from gui_folder.resizable_pane import ResizableSplitView
from gui_folder.code_editor import CodeEditor
from gui_folder.terminal import Terminal
from gui_folder.dictionary_window import DictionaryWindow
from gui_folder.compiler_runner import CompilerRunner
from gui_folder.sample_codes import SAMPLE_CODES


class PeenoiseApp(ctk.CTk):
    """Main Application Window for Peenoise Language IDE."""

    def __init__(self):
        super().__init__()

        # Window Title as explicitly requested by user
        self.title("Peenoise Language")
        self.geometry("1260x800")
        self.minsize(960, 620)
        self.configure(fg_color=Theme.BG_MAIN)

        self._dictionary_window = None

        self._build_layout()
        self._bind_global_shortcuts()
        self._load_initial_code()
        self._center_window()

    def _build_layout(self):
        """Builds sidebar, resizable editor/terminal split, and status bar."""
        # Main horizontal container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        # 1. Left Sidebar
        self.sidebar = Sidebar(
            self.main_container,
            on_run=self.run_code,
            on_dictionary=self.open_dictionary,
            on_reset=self.reset_code,
            on_load_sample=self.load_sample,
            on_clear_terminal=self.clear_terminal,
            on_zoom_change=self.change_font_size
        )
        self.sidebar.pack(side="left", fill="y")

        # 2. Resizable Split View (Center & Right)
        self.split_view = ResizableSplitView(self.main_container, initial_left_ratio=0.52)
        self.split_view.pack(side="left", fill="both", expand=True)

        # Code Editor in Left Pane
        self.editor = CodeEditor(
            self.split_view.left_pane,
            on_cursor_move=self._update_cursor_status,
            on_change=self._on_code_modified
        )
        self.editor.pack(fill="both", expand=True)

        # Terminal in Right Pane
        self.terminal = Terminal(self.split_view.right_pane)
        self.terminal.pack(fill="both", expand=True)

        # 3. Bottom Status Bar
        self._build_status_bar()

    def _build_status_bar(self):
        """Constructs bottom status bar."""
        self.status_bar = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            height=26,
            corner_radius=0
        )
        self.status_bar.pack(side="bottom", fill="x")
        self.status_bar.pack_propagate(False)

        # Left status text
        self.status_lbl = ctk.CTkLabel(
            self.status_bar,
            text="● Handa na magpatakbo ng kodigo",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color="#38BDF8"
        )
        self.status_lbl.pack(side="left", padx=12)

        # Right items
        lang_lbl = ctk.CTkLabel(
            self.status_bar,
            text="🇵🇭 Wikang Peenoise",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11, weight="bold"),
            text_color=Theme.TEXT_SECONDARY
        )
        lang_lbl.pack(side="right", padx=12)

        enc_lbl = ctk.CTkLabel(
            self.status_bar,
            text="UTF-8",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_MUTED
        )
        enc_lbl.pack(side="right", padx=10)

        self.cursor_lbl = ctk.CTkLabel(
            self.status_bar,
            text="Linya: 1, Kolum: 1",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_MUTED
        )
        self.cursor_lbl.pack(side="right", padx=10)

    def _bind_global_shortcuts(self):
        """Binds global hotkeys for run, dictionary, clear, and reset."""
        # F5 or Ctrl+Enter to Run
        self.bind("<F5>", lambda event: self.run_code())
        self.bind("<Control-Return>", lambda event: self.run_code())

        # Ctrl+B for Dictionary
        self.bind("<Control-b>", lambda event: self.open_dictionary())
        self.bind("<Control-B>", lambda event: self.open_dictionary())

        # Ctrl+R for Reset
        self.bind("<Control-r>", lambda event: self.reset_code())
        self.bind("<Control-R>", lambda event: self.reset_code())

        # Ctrl+L for Clear Terminal
        self.bind("<Control-l>", lambda event: self.clear_terminal())
        self.bind("<Control-L>", lambda event: self.clear_terminal())

    def _load_initial_code(self):
        """Loads default starter program."""
        default_code = SAMPLE_CODES.get("Pangunahing Pagsubok (Main Demo)", "")
        self.editor.set_code(default_code)

    def _center_window(self):
        """Centers window on user screen."""
        self.update_idletasks()
        w = 1260
        h = 800
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - h) // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    # ---------------- Application Actions ----------------

    def run_code(self):
        """Compiles and runs the current editor code through all 4 compiler phases."""
        code = self.editor.get_code()

        # Update UI to running state
        self.editor.clear_error_highlight()
        self.terminal.set_running_status()
        self.status_lbl.configure(text="● Tumatakbo ang compiler...", text_color="#FBBF24")
        self.update_idletasks()

        # Execute compiler runner
        result = CompilerRunner.run(code)

        # Display results in Terminal tabs
        self.terminal.display_result(result)

        # Update Status Bar & highlight error line if any
        if result.success:
            self.status_lbl.configure(
                text=f"✔ Matagumpay na natapos sa loob ng {result.execution_time_ms:.2f} ms",
                text_color=Theme.SUCCESS_GREEN
            )
            self.editor.clear_error_highlight()
        else:
            loc_str = f"sa Linya {result.error_line}" if result.error_line else ""
            self.status_lbl.configure(
                text=f"✖ {result.error_type} {loc_str}: {result.error_message}",
                text_color=Theme.ERROR_RED
            )
            if result.error_line:
                self.editor.highlight_error_line(result.error_line)

    def open_dictionary(self):
        """Opens or brings to front the 'Bokabularyo' window."""
        if self._dictionary_window is None or not self._dictionary_window.winfo_exists():
            self._dictionary_window = DictionaryWindow(
                self,
                on_insert_snippet=self.insert_snippet_from_dict
            )
        else:
            self._dictionary_window.lift()
            self._dictionary_window.focus_force()

    def insert_snippet_from_dict(self, snippet: str):
        """Inserts snippet from dictionary directly into code editor."""
        self.editor.insert_snippet(snippet)
        self.status_lbl.configure(
            text="✔ Naipasok ang sintaks sa editor.",
            text_color="#38BDF8"
        )
        self.lift()

    def reset_code(self):
        """Resets editor with confirmation to prevent accidental loss."""
        default_code = SAMPLE_CODES.get("Pangunahing Pagsubok (Main Demo)", "")
        self.editor.set_code(default_code)
        self.terminal.clear_all()
        self.status_lbl.configure(
            text="● Naibalik ang editor sa batayang halimbawa.",
            text_color="#38BDF8"
        )

    def load_sample(self, sample_code: str):
        """Loads a specific sample code snippet into editor."""
        self.editor.set_code(sample_code)
        self.terminal.clear_all()
        self.status_lbl.configure(
            text="● Na-load ang halimbawang programa.",
            text_color="#38BDF8"
        )

    def clear_terminal(self):
        """Clears terminal output."""
        self.terminal.clear_all()
        self.status_lbl.configure(
            text="● Nalinisan ang terminal.",
            text_color="#94A3B8"
        )

    def change_font_size(self, size: int):
        """Scales font sizes in both editor and terminal."""
        self.editor.set_font_size(size)
        self.terminal.set_font_size(size)

    def _update_cursor_status(self, line: int, col: int):
        """Updates cursor coordinate display in status bar."""
        self.cursor_lbl.configure(text=f"Linya: {line}, Kolum: {col}")

    def _on_code_modified(self):
        """Clears previous error line highlight when user types."""
        self.editor.clear_error_highlight()


def main():
    """Application entry point."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = PeenoiseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
