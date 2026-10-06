"""
Theme and styling definitions for Peenoise Language IDE.
Provides a modern dark theme inspired by contemporary developer environments,
customized with vibrant accent colors matching the Peenoise aesthetic.
"""

class Theme:
    # Application background colors
    BG_MAIN = "#0D1117"
    BG_SIDEBAR = "#161B22"
    BG_PANEL = "#161B22"
    BG_CARD = "#21262D"
    BG_CARD_HOVER = "#2A313C"
    BORDER_COLOR = "#30363D"
    BORDER_FOCUS = "#58A6FF"

    # Editor specific
    EDITOR_BG = "#0D1117"
    EDITOR_FG = "#F0F6FC"
    EDITOR_INSERT = "#58A6FF"
    EDITOR_SELECT_BG = "#264F78"
    GUTTER_BG = "#161B22"
    GUTTER_FG = "#6E7681"
    GUTTER_BORDER = "#21262D"
    ERROR_LINE_BG = "#4C1D24"

    # Terminal specific
    TERMINAL_BG = "#090D12"
    TERMINAL_FG = "#E6EDF3"
    TERMINAL_BANNER_BG = "#131C2E"

    # Action Buttons (Matching User Wireframe with modern vibrant aesthetics)
    # Patakbuhin (Run) - Cyan / Electric Teal
    BTN_RUN_BG = "#00ADB5"
    BTN_RUN_HOVER = "#00C4CD"
    BTN_RUN_TEXT = "#FFFFFF"

    # Bokabularyo (Dictionary) - Deep Slate / Indigo
    BTN_DICT_BG = "#4F46E5"
    BTN_DICT_HOVER = "#6366F1"
    BTN_DICT_TEXT = "#FFFFFF"

    # Muling Itakda (Reset / Clear) - Vibrant Crimson / Rose
    BTN_RESET_BG = "#E11D48"
    BTN_RESET_HOVER = "#F43F5E"
    BTN_RESET_TEXT = "#FFFFFF"

    # Secondary action buttons
    BTN_SECONDARY_BG = "#21262D"
    BTN_SECONDARY_HOVER = "#30363D"
    BTN_SECONDARY_TEXT = "#C9D1D9"

    # Status & Feedback Colors
    SUCCESS_GREEN = "#10B981"
    SUCCESS_BG = "#064E3B"
    ERROR_RED = "#F43F5E"
    ERROR_BG = "#4C0519"
    WARNING_AMBER = "#F59E0B"
    INFO_CYAN = "#38BDF8"

    # Text Colors
    TEXT_PRIMARY = "#F0F6FC"
    TEXT_SECONDARY = "#8B949E"
    TEXT_MUTED = "#6E7681"

    # Syntax Highlighting Tokens
    SYNTAX_KEYWORD = "#FF7B72"      # kung, kundi, ipakita, pihitan, etc.
    SYNTAX_TYPE = "#79C0FF"         # buong_numero, salita, etc.
    SYNTAX_BOOLEAN = "#FFA657"      # totoo, mali
    SYNTAX_STRING = "#A5D6FF"       # "...", '...'
    SYNTAX_NUMBER = "#D2A8FF"       # 123, 45.6
    SYNTAX_COMMENT = "#8B949E"      # //, /* */, #
    SYNTAX_OPERATOR = "#F0883E"     # +, -, *, /, ==, &&, etc.
    SYNTAX_DELIMITER = "#C9D1D9"    # ;, {}, ()

    # Fonts
    FONT_FAMILY_CODE = "Consolas"
    FONT_FAMILY_UI = "Segoe UI"
    
    @classmethod
    def get_code_font(cls, size=13):
        return (cls.FONT_FAMILY_CODE, size)

    @classmethod
    def get_ui_font(cls, size=12, weight="normal"):
        return (cls.FONT_FAMILY_UI, size, weight)
