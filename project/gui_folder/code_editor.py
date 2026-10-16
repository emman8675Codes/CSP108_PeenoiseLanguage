"""
Code Editor component for Peenoise Language IDE.
Provides a modern code editing surface with:
- Title banner: 'Mga tagubilin o iskrip'
- Synchronized line numbers gutter
- Tagalog syntax highlighting for keywords, types, booleans, literals, and comments
- Real-time cursor coordinates and statistics
- Error line highlight with jump-to-error
- Smart Tab (4 spaces) and auto-indentation on Enter
"""

import re
import tkinter as tk
import customtkinter as ctk
from typing import Callable, Optional

from gui_folder.theme import Theme


class CodeEditor(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        on_cursor_move: Optional[Callable[[int, int], None]] = None,
        on_change: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(parent, fg_color=Theme.BG_PANEL, corner_radius=10, **kwargs)
        self.on_cursor_move = on_cursor_move
        self.on_change = on_change

        self._font_size = 13
        self._highlight_job = None
        self._error_line = None

        self._build_header()
        self._build_editor_area()
        self._setup_syntax_tags()
        self._bind_events()

    def _build_header(self):
        """Builds the top bar with title, stats badge, and editor actions."""
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=Theme.BG_CARD,
            corner_radius=8,
            height=38
        )
        self.header_frame.pack(fill="x", padx=6, pady=(6, 4))
        self.header_frame.pack_propagate(False)

        # Title: 'Mga tagubilin o iskrip' (as per user design requirement)
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Mga tagubilin o iskrip",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=13, weight="bold"),
            text_color=Theme.TEXT_PRIMARY
        )
        self.title_label.pack(side="left", padx=(12, 8))

        # Tag badge
        self.lang_badge = ctk.CTkLabel(
            self.header_frame,
            text="🇵🇭 Peenoise Script",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=("#E2E8F0", "#1E293B"),
            text_color=Theme.INFO_CYAN,
            corner_radius=6,
            padx=8,
            pady=2
        )
        self.lang_badge.pack(side="left", padx=4)

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
            command=self.clear
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
            command=self.copy_to_clipboard
        )
        self.btn_copy.pack(side="right", padx=4)

        self.btn_format = ctk.CTkButton(
            self.header_frame,
            text="Ayusin (Format)",
            width=90,
            height=26,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            fg_color=Theme.BTN_SECONDARY_BG,
            hover_color=Theme.BTN_SECONDARY_HOVER,
            text_color=Theme.TEXT_SECONDARY,
            corner_radius=6,
            command=self.format_code
        )
        self.btn_format.pack(side="right", padx=4)

        # Line and char stats
        self.stats_label = ctk.CTkLabel(
            self.header_frame,
            text="Linya: 1 | Karakter: 0",
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_UI, size=11),
            text_color=Theme.TEXT_MUTED
        )
        self.stats_label.pack(side="right", padx=(8, 12))

    def _build_editor_area(self):
        """Constructs the gutter and text widget container."""
        self.editor_container = ctk.CTkFrame(
            self,
            fg_color=Theme.EDITOR_BG,
            border_width=1,
            border_color=Theme.BORDER_COLOR,
            corner_radius=8
        )
        self.editor_container.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        # Line numbers gutter (standard Tk Text widget for precise alignment)
        self.gutter = tk.Text(
            self.editor_container,
            width=4,
            bg=Theme.get_color(Theme.GUTTER_BG),
            fg=Theme.get_color(Theme.GUTTER_FG),
            font=(Theme.FONT_FAMILY_CODE, self._font_size),
            bd=0,
            highlightthickness=0,
            relief="flat",
            state="disabled",
            cursor="arrow",
            padx=4,
            pady=6,
            spacing1=1,
            spacing3=1,
            takefocus=0
        )
        self.gutter.pack(side="left", fill="y", padx=(0, 1), pady=1)

        # Main Code Textbox
        self.textbox = ctk.CTkTextbox(
            self.editor_container,
            font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size),
            fg_color=Theme.EDITOR_BG,
            text_color=Theme.EDITOR_FG,
            border_width=0,
            corner_radius=0,
            undo=True,
            wrap="none"
        )
        self.textbox.pack(side="left", fill="both", expand=True, pady=1, padx=(0, 1))

        # Configure inner tk.Text properties for clean alignment
        inner_tk = self.textbox._textbox
        inner_tk.configure(
            spacing1=1,
            spacing3=1,
            insertbackground=Theme.get_color(Theme.EDITOR_INSERT),
            selectbackground=Theme.get_color(Theme.EDITOR_SELECT_BG),
            selectforeground="#FFFFFF",
            padx=8,
            pady=6
        )

        # Synchronize gutter scrolling with textbox scrolling
        orig_y_scroll = inner_tk.cget("yscrollcommand")
        def _on_scroll(*args):
            self.gutter.yview_moveto(args[0])
            if hasattr(self.textbox, "_vsb") and self.textbox._vsb:
                self.textbox._vsb.set(*args)
        inner_tk.configure(yscrollcommand=_on_scroll)

        # Synchronize mouse wheel
        def _on_gutter_mousewheel(event):
            inner_tk.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
        self.gutter.bind("<MouseWheel>", _on_gutter_mousewheel)

    def _setup_syntax_tags(self, mode: Optional[str] = None):
        """Configures color tags for Peenoise language syntax highlighting."""
        current_mode = mode or ctk.get_appearance_mode()
        tk_text = self.textbox._textbox
        code_font = (Theme.FONT_FAMILY_CODE, self._font_size)
        bold_font = (Theme.FONT_FAMILY_CODE, self._font_size, "bold")
        italic_font = (Theme.FONT_FAMILY_CODE, self._font_size, "italic")

        tk_text.tag_configure("kw_type", foreground=Theme.get_color(Theme.SYNTAX_TYPE, current_mode), font=bold_font)
        tk_text.tag_configure("kw_stmt", foreground=Theme.get_color(Theme.SYNTAX_KEYWORD, current_mode), font=bold_font)
        tk_text.tag_configure("kw_bool", foreground=Theme.get_color(Theme.SYNTAX_BOOLEAN, current_mode), font=bold_font)
        tk_text.tag_configure("lit_str", foreground=Theme.get_color(Theme.SYNTAX_STRING, current_mode), font=code_font)
        tk_text.tag_configure("lit_num", foreground=Theme.get_color(Theme.SYNTAX_NUMBER, current_mode), font=code_font)
        tk_text.tag_configure("comment", foreground=Theme.get_color(Theme.SYNTAX_COMMENT, current_mode), font=italic_font)
        tk_text.tag_configure("operator", foreground=Theme.get_color(Theme.SYNTAX_OPERATOR, current_mode), font=code_font)
        tk_text.tag_configure("error_line", background=Theme.get_color(Theme.ERROR_LINE_BG, current_mode))

    def update_theme(self, mode: Optional[str] = None):
        """Updates native Tkinter gutter, insert cursor, and syntax highlight tags."""
        current_mode = mode or ctk.get_appearance_mode()
        self.gutter.configure(
            bg=Theme.get_color(Theme.GUTTER_BG, current_mode),
            fg=Theme.get_color(Theme.GUTTER_FG, current_mode)
        )
        inner_tk = self.textbox._textbox
        inner_tk.configure(
            insertbackground=Theme.get_color(Theme.EDITOR_INSERT, current_mode),
            selectbackground=Theme.get_color(Theme.EDITOR_SELECT_BG, current_mode)
        )
        self._setup_syntax_tags(current_mode)
        if self._error_line is not None:
            self.highlight_error_line(self._error_line)
        self._schedule_highlight()

    def _bind_events(self):
        """Binds typing, keyboard shortcuts, and cursor navigation."""
        tk_text = self.textbox._textbox

        tk_text.bind("<KeyRelease>", self._on_key_release)
        tk_text.bind("<ButtonRelease-1>", self._on_cursor_update)
        tk_text.bind("<Tab>", self._on_tab)
        tk_text.bind("<Return>", self._on_enter)
        tk_text.bind("<Control-a>", self._on_select_all)
        tk_text.bind("<Control-A>", self._on_select_all)

    def _on_key_release(self, event=None):
        """Called when keys are typed or released."""
        self._update_gutter()
        self._update_stats()
        self._on_cursor_update()
        self._schedule_highlight()
        if self.on_change:
            self.on_change()

    def _on_cursor_update(self, event=None):
        """Updates status of cursor coordinates."""
        cursor_pos = self.textbox._textbox.index("insert")
        parts = cursor_pos.split(".")
        line, col = int(parts[0]), int(parts[1]) + 1
        if self.on_cursor_move:
            self.on_cursor_move(line, col)

    def _on_tab(self, event):
        """Inserts 4 spaces instead of shifting GUI widget focus."""
        self.textbox._textbox.insert("insert", "    ")
        self._on_key_release()
        return "break"

    def _on_enter(self, event):
        """Auto-indentation: replicates indentation of the current line, adding 4 spaces after { or :."""
        tk_text = self.textbox._textbox
        line_start = tk_text.index("insert linestart")
        line_text = tk_text.get(line_start, "insert")

        # Determine existing leading spaces
        indent = len(line_text) - len(line_text.lstrip(" "))
        stripped = line_text.strip()
        extra_indent = 4 if stripped.endswith(("{", ":")) else 0

        tk_text.insert("insert", "\n" + " " * (indent + extra_indent))
        self._on_key_release()
        return "break"

    def _on_select_all(self, event):
        """Selects all text on Ctrl+A."""
        self.textbox._textbox.tag_add("sel", "1.0", "end")
        return "break"

    def _update_gutter(self):
        """Regenerates line numbers matching the current line count."""
        tk_text = self.textbox._textbox
        total_lines = int(tk_text.index("end-1c").split(".")[0])
        total_lines = max(1, total_lines)

        # Adjust gutter width if line count expands to 3 or 4 digits
        digits = max(3, len(str(total_lines)) + 1)
        if self.gutter.cget("width") != digits:
            self.gutter.configure(width=digits)

        gutter_content = "\n".join(str(i).rjust(digits - 1) for i in range(1, total_lines + 1))

        self.gutter.configure(state="normal")
        self.gutter.delete("1.0", "end")
        self.gutter.insert("1.0", gutter_content)
        self.gutter.configure(state="disabled")

        # Keep gutter scroll offset matching the editor
        self.gutter.yview_moveto(tk_text.yview()[0])

    def _update_stats(self):
        """Updates line and character counts in the header badge."""
        content = self.get_code()
        lines = len(content.splitlines()) if content else 0
        chars = len(content)
        self.stats_label.configure(text=f"Linya: {lines} | Karakter: {chars}")

    def _schedule_highlight(self):
        """Debounced syntax highlighting application."""
        if self._highlight_job:
            self.after_cancel(self._highlight_job)
        self._highlight_job = self.after(35, self._apply_syntax_highlighting)

    def _apply_syntax_highlighting(self):
        """Applies regex-driven syntax highlighting for Peenoise tokens."""
        tk_text = self.textbox._textbox
        content = tk_text.get("1.0", "end-1c")
        if not content:
            return

        # Clear existing syntax tags
        for tag in ["kw_type", "kw_stmt", "kw_bool", "lit_str", "lit_num", "comment", "operator"]:
            tk_text.tag_remove(tag, "1.0", "end")

        # 1. Comments (highest priority)
        comment_ranges = []
        for m in re.finditer(r"(//[^\n]*)|(#[^\n]*)|(/\*[\s\S]*?\*/)", content):
            start = f"1.0 + {m.start()}c"
            end = f"1.0 + {m.end()}c"
            tk_text.tag_add("comment", start, end)
            comment_ranges.append((m.start(), m.end()))

        # Helper to avoid highlighting within comments or strings
        def is_in_ranges(idx, ranges):
            return any(s <= idx < e for s, e in ranges)

        # 2. Strings & Characters
        string_ranges = []
        for m in re.finditer(r'("[^"\\]*(?:\\.[^"\\]*)*")|(\'[^\'\\]*(?:\\.[^\'\\]*)*\')', content):
            if is_in_ranges(m.start(), comment_ranges):
                continue
            start = f"1.0 + {m.start()}c"
            end = f"1.0 + {m.end()}c"
            tk_text.tag_add("lit_str", start, end)
            string_ranges.append((m.start(), m.end()))

        excluded_ranges = comment_ranges + string_ranges

        # 3. Data Types
        for m in re.finditer(r"\b(buong_numero|lutang_numero|salita|titik_uri|katotohanan)\b", content):
            if not is_in_ranges(m.start(), excluded_ranges):
                tk_text.tag_add("kw_type", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")

        # 4. Statements / Keywords
        for m in re.finditer(r"\b(itakda|ipakita|kung|kundi_kung|kundi|pihitan|kaso|hinto|likas)\b", content):
            if not is_in_ranges(m.start(), excluded_ranges):
                tk_text.tag_add("kw_stmt", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")

        # 5. Booleans
        for m in re.finditer(r"\b(totoo|mali)\b", content):
            if not is_in_ranges(m.start(), excluded_ranges):
                tk_text.tag_add("kw_bool", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")

        # 6. Numbers
        for m in re.finditer(r"\b\d+(\.\d+)?\b", content):
            if not is_in_ranges(m.start(), excluded_ranges):
                tk_text.tag_add("lit_num", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")

        # 7. Operators
        for m in re.finditer(r"(==|!=|<=|>=|&&|\|\||[+\-*/%<>=!])", content):
            if not is_in_ranges(m.start(), excluded_ranges):
                tk_text.tag_add("operator", f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")

    # ---------------- Public API Methods ----------------

    def get_code(self) -> str:
        """Returns the complete script content."""
        return self.textbox._textbox.get("1.0", "end-1c")

    def set_code(self, code: str):
        """Replaces current script with new code."""
        tk_text = self.textbox._textbox
        tk_text.delete("1.0", "end")
        tk_text.insert("1.0", code)
        self.clear_error_highlight()
        self._update_gutter()
        self._update_stats()
        self._schedule_highlight()
        if self.on_change:
            self.on_change()

    def insert_snippet(self, snippet: str):
        """Inserts a snippet at the cursor or end of the script."""
        tk_text = self.textbox._textbox
        if not snippet.endswith("\n"):
            snippet += "\n"
        tk_text.insert("insert", snippet)
        self._update_gutter()
        self._update_stats()
        self._schedule_highlight()
        tk_text.see("insert")

    def clear(self):
        """Clears the code editor."""
        self.set_code("")

    def highlight_error_line(self, line_num: Optional[int]):
        """Highlights the specific error line in red and scrolls to it."""
        self.clear_error_highlight()
        if not line_num or line_num < 1:
            return

        tk_text = self.textbox._textbox
        self._error_line = line_num
        start_idx = f"{line_num}.0"
        end_idx = f"{line_num}.end + 1c"

        tk_text.tag_add("error_line", start_idx, end_idx)
        tk_text.see(start_idx)

    def clear_error_highlight(self):
        """Removes error line background styling."""
        if self._error_line:
            self.textbox._textbox.tag_remove("error_line", "1.0", "end")
            self._error_line = None

    def copy_to_clipboard(self):
        """Copies code to clipboard."""
        code = self.get_code()
        self.clipboard_clear()
        self.clipboard_append(code)

    def format_code(self):
        """Cleans up indentation based on curly braces and statement structure."""
        code = self.get_code()
        if not code.strip():
            return

        lines = code.splitlines()
        formatted_lines = []
        indent_level = 0
        indent_str = "    "

        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append("")
                continue

            # Check if line closes block
            if stripped.startswith("}") or stripped.startswith(")") or stripped.startswith("likas") or stripped.startswith("kaso"):
                cur_indent = max(0, indent_level - 1)
            else:
                cur_indent = indent_level

            formatted_lines.append((indent_str * cur_indent) + stripped)

            # Adjust indent level for subsequent lines
            opens = stripped.count("{")
            closes = stripped.count("}")
            indent_level = max(0, indent_level + (opens - closes))

        formatted_code = "\n".join(formatted_lines)
        self.set_code(formatted_code)

    def set_font_size(self, size: int):
        """Changes editor and gutter font sizes dynamically."""
        self._font_size = max(9, min(24, size))
        font_tuple = (Theme.FONT_FAMILY_CODE, self._font_size)
        self.gutter.configure(font=font_tuple)
        self.textbox.configure(font=ctk.CTkFont(family=Theme.FONT_FAMILY_CODE, size=self._font_size))
        self._setup_syntax_tags()
        self._schedule_highlight()
