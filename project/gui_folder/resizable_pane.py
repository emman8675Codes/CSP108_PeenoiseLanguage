"""
Resizable split container for Peenoise Language IDE.
Allows the user to drag the dividing separator to dynamically resize
the Code Editor panel (left) and the Terminal panel (right).
"""

from typing import Optional
import tkinter as tk
import customtkinter as ctk

from gui_folder.theme import Theme


class ResizableSplitView(ctk.CTkFrame):
    def __init__(self, parent, initial_left_ratio: float = 0.52, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)

        self.initial_left_ratio = initial_left_ratio
        self._min_left_width = 300
        self._min_right_width = 300
        self._start_x = 0
        self._start_width = 0
        self._is_dragging = False

        self._build_panes()

    def _build_panes(self):
        """Constructs left pane, splitter divider, and right pane."""
        # Left Panel (Editor container)
        self.left_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.left_pane.pack(side="left", fill="both", expand=False)
        self.left_pane.pack_propagate(False)

        # Splitter divider handle
        self.splitter = tk.Frame(
            self,
            width=8,
            bg=Theme.get_color(Theme.BG_MAIN),
            cursor="sb_h_double_arrow"
        )
        self.splitter.pack(side="left", fill="y", padx=1)

        # Center line visual on the splitter
        self.splitter_line = tk.Frame(
            self.splitter,
            width=2,
            bg=Theme.get_color(Theme.BORDER_COLOR)
        )
        self.splitter_line.place(relx=0.5, rely=0.2, relheight=0.6, anchor="n")

        # Right Panel (Terminal container)
        self.right_pane = ctk.CTkFrame(self, fg_color="transparent")
        self.right_pane.pack(side="left", fill="both", expand=True)

        # Bind dragging and hover events to splitter
        self.splitter.bind("<Button-1>", self._on_drag_start)
        self.splitter.bind("<B1-Motion>", self._on_dragging)
        self.splitter.bind("<ButtonRelease-1>", self._on_drag_end)
        self.splitter.bind("<Enter>", self._on_hover_enter)
        self.splitter.bind("<Leave>", self._on_hover_leave)

        # Configure initial sizing after window geometry settles
        self.bind("<Configure>", self._on_first_configure)

    def _on_first_configure(self, event):
        """Initializes left pane width based on ratio once container size is known."""
        self.unbind("<Configure>")
        total_w = self.winfo_width()
        if total_w > 100:
            initial_w = int(total_w * self.initial_left_ratio)
            self.left_pane.configure(width=initial_w)

    def _on_hover_enter(self, event):
        if not self._is_dragging:
            self.splitter_line.configure(bg=Theme.get_color(Theme.BTN_RUN_BG))

    def _on_hover_leave(self, event):
        if not self._is_dragging:
            self.splitter_line.configure(bg=Theme.get_color(Theme.BORDER_COLOR))

    def _on_drag_start(self, event):
        self._is_dragging = True
        self._start_x = event.x_root
        self._start_width = self.left_pane.winfo_width()
        self.splitter_line.configure(bg=Theme.get_color(Theme.BTN_RUN_BG))

    def _on_dragging(self, event):
        if not self._is_dragging:
            return

        delta_x = event.x_root - self._start_x
        total_width = self.winfo_width()
        max_left = max(self._min_left_width, total_width - self._min_right_width)
        new_width = max(self._min_left_width, min(max_left, self._start_width + delta_x))

        self.left_pane.configure(width=new_width)

    def _on_drag_end(self, event):
        self._is_dragging = False
        self.splitter_line.configure(bg=Theme.get_color(Theme.BORDER_COLOR))

    def update_theme(self, mode: Optional[str] = None):
        """Updates standard Tkinter splitter elements when appearance mode changes."""
        current_mode = mode or ctk.get_appearance_mode()
        self.splitter.configure(bg=Theme.get_color(Theme.BG_MAIN, current_mode))
        self.splitter_line.configure(bg=Theme.get_color(Theme.BORDER_COLOR, current_mode))
