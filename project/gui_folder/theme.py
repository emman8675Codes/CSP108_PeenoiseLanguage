"""
Theme and styling definitions for Peenoise Language IDE.
Provides a comprehensive dual-mode (Light and Dark) theme system
tailored for developer productivity and the vibrant Peenoise aesthetic.
"""

from typing import Optional, Union, Tuple
import customtkinter as ctk


class Theme:
    # ---------------- Application Backgrounds (Light, Dark) ----------------
    BG_MAIN = ("#F1F5F9", "#0D1117")          # Slate 100 / GitHub Dark
    BG_SIDEBAR = ("#E2E8F0", "#161B22")       # Slate 200 / GitHub Sidebar
    BG_PANEL = ("#F8FAFC", "#161B22")         # Slate 50 / GitHub Panel
    BG_CARD = ("#FFFFFF", "#21262D")          # Pure White / Elevated Dark Card
    BG_CARD_HOVER = ("#E2E8F0", "#2A313C")    # Card Hover state
    BORDER_COLOR = ("#CBD5E1", "#30363D")     # Slate 300 / Dark Border
    BORDER_FOCUS = ("#0284C7", "#58A6FF")     # Focus Accent

    # ---------------- Editor Specific ----------------
    EDITOR_BG = ("#FFFFFF", "#0D1117")
    EDITOR_FG = ("#0F172A", "#F0F6FC")
    EDITOR_INSERT = ("#0284C7", "#58A6FF")
    EDITOR_SELECT_BG = ("#BFDBFE", "#264F78")
    GUTTER_BG = ("#F1F5F9", "#161B22")
    GUTTER_FG = ("#64748B", "#6E7681")
    GUTTER_BORDER = ("#E2E8F0", "#21262D")
    ERROR_LINE_BG = ("#FEE2E2", "#4C1D24")

    # ---------------- Terminal Specific ----------------
    TERMINAL_BG = ("#F8FAFC", "#090D12")
    TERMINAL_FG = ("#0F172A", "#E6EDF3")
    TERMINAL_BANNER_BG = ("#E2E8F0", "#131C2E")

    # ---------------- Action Buttons ----------------
    # Patakbuhin (Run) - Teal / Cyan
    BTN_RUN_BG = ("#0D9488", "#00ADB5")
    BTN_RUN_HOVER = ("#0F766E", "#00C4CD")
    BTN_RUN_TEXT = ("#FFFFFF", "#FFFFFF")

    # Bokabularyo (Dictionary) - Deep Slate / Indigo
    BTN_DICT_BG = ("#4F46E5", "#4F46E5")
    BTN_DICT_HOVER = ("#4338CA", "#6366F1")
    BTN_DICT_TEXT = ("#FFFFFF", "#FFFFFF")

    # Muling Itakda (Reset / Clear) - Vibrant Crimson / Rose
    BTN_RESET_BG = ("#E11D48", "#E11D48")
    BTN_RESET_HOVER = ("#BE123C", "#F43F5E")
    BTN_RESET_TEXT = ("#FFFFFF", "#FFFFFF")

    # Secondary action buttons
    BTN_SECONDARY_BG = ("#E2E8F0", "#21262D")
    BTN_SECONDARY_HOVER = ("#CBD5E1", "#30363D")
    BTN_SECONDARY_TEXT = ("#334155", "#C9D1D9")

    # ---------------- Status & Feedback Colors ----------------
    SUCCESS_GREEN = ("#16A34A", "#10B981")
    SUCCESS_BG = ("#DCFCE7", "#064E3B")
    ERROR_RED = ("#DC2626", "#F43F5E")
    ERROR_BG = ("#FEE2E2", "#4C0519")
    WARNING_AMBER = ("#D97706", "#F59E0B")
    INFO_CYAN = ("#0284C7", "#38BDF8")

    # ---------------- Typography / Text Colors ----------------
    TEXT_PRIMARY = ("#0F172A", "#F0F6FC")
    TEXT_SECONDARY = ("#475569", "#8B949E")
    TEXT_MUTED = ("#64748B", "#6E7681")

    # ---------------- Syntax Highlighting Tokens ----------------
    SYNTAX_KEYWORD = ("#D73A49", "#FF7B72")      # kung, kundi, ipakita, pihitan, etc.
    SYNTAX_TYPE = ("#005CC5", "#79C0FF")         # buong_numero, salita, etc.
    SYNTAX_BOOLEAN = ("#B45309", "#FFA657")      # totoo, mali
    SYNTAX_STRING = ("#032F62", "#A5D6FF")       # "...", '...'
    SYNTAX_NUMBER = ("#6F42C1", "#D2A8FF")       # 123, 45.6
    SYNTAX_COMMENT = ("#57606A", "#8B949E")      # //, /* */, #
    SYNTAX_OPERATOR = ("#D97706", "#F0883E")     # +, -, *, /, ==, &&, etc.
    SYNTAX_DELIMITER = ("#24292F", "#C9D1D9")    # ;, {}, ()

    # ---------------- Fonts ----------------
    FONT_FAMILY_CODE = "Consolas"
    FONT_FAMILY_UI = "Segoe UI"

    @classmethod
    def get_color(cls, color_val: Union[str, Tuple[str, str]], mode: Optional[str] = None) -> str:
        """
        Resolves a color value (which can be a single hex string or (light, dark) tuple)
        to a single hex string suitable for standard Tkinter widgets.
        """
        if isinstance(color_val, (tuple, list)):
            if mode is None:
                current_mode = ctk.get_appearance_mode().lower()
            else:
                current_mode = mode.lower()
            return color_val[0] if current_mode == "light" else color_val[1]
        return color_val

    @classmethod
    def get_code_font(cls, size=13):
        return (cls.FONT_FAMILY_CODE, size)

    @classmethod
    def get_ui_font(cls, size=12, weight="normal"):
        return (cls.FONT_FAMILY_UI, size, weight)