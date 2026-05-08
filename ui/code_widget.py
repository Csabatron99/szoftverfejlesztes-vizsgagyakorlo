"""
Syntax-highlighted, read-only code block widget.
Uses a plain tkinter.Text with VS Code Dark+ inspired colours.
"""
import tkinter as tk
import re

# ── VS Code Dark+ palette ───────────────────────────────────────────────────
_BG          = "#1e1e1e"
_FG          = "#d4d4d4"
_CLR_KEYWORD = "#569cd6"   # blue
_CLR_STRING  = "#ce9178"   # orange-brown
_CLR_COMMENT = "#6a9955"   # green
_CLR_NUMBER  = "#b5cea8"   # light sage
_CLR_TYPE    = "#4ec9b0"   # teal  (UpperCase identifiers)
_CLR_ANNOT   = "#c586c0"   # purple (@annotations)
_CLR_BORDER  = "#3c3c3c"
_CODE_FONT   = ("Consolas", 12)

_KEYWORDS = frozenset({
    "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char",
    "class", "const", "continue", "default", "do", "double", "else", "enum",
    "extends", "final", "finally", "float", "for", "goto", "if", "implements",
    "import", "instanceof", "int", "interface", "long", "native", "new",
    "package", "private", "protected", "public", "return", "short", "static",
    "strictfp", "super", "switch", "synchronized", "this", "throw", "throws",
    "transient", "try", "var", "void", "volatile", "while", "yield",
    "sealed", "record", "permits", "null", "true", "false",
    # common generic types treated as keywords for readability
    "String", "Integer", "Long", "Double", "Float", "Boolean", "Object",
    "List", "Map", "Set", "Optional", "Stream", "Collection",
    "ArrayList", "HashMap", "HashSet", "LinkedList",
})


def create_code_block(parent: tk.Misc, code: str) -> tk.Frame:
    """
    Return a framed, syntax-highlighted, read-only code widget.

    Parameters
    ----------
    parent : tkinter parent widget
    code   : raw code string (may contain newlines)
    """
    lines = code.split("\n")
    n_lines = len(lines)
    width_chars = min(max(max((len(l) for l in lines), default=40) + 2, 42), 110)

    outer = tk.Frame(
        parent,
        bg=_BG,
        highlightthickness=1,
        highlightbackground=_CLR_BORDER,
    )

    widget = tk.Text(
        outer,
        font=_CODE_FONT,
        bg=_BG,
        fg=_FG,
        insertbackground=_FG,
        selectbackground="#264f78",
        selectforeground=_FG,
        relief="flat",
        bd=0,
        wrap="none",
        height=n_lines,
        width=width_chars,
        state="normal",
        cursor="arrow",
        padx=12,
        pady=10,
    )
    widget.pack(fill="both", expand=True)

    # Tag styles
    widget.tag_configure("keyword", foreground=_CLR_KEYWORD)
    widget.tag_configure("string",  foreground=_CLR_STRING)
    widget.tag_configure("comment", foreground=_CLR_COMMENT)
    widget.tag_configure("number",  foreground=_CLR_NUMBER)
    widget.tag_configure("type",    foreground=_CLR_TYPE)
    widget.tag_configure("annot",   foreground=_CLR_ANNOT)

    widget.insert("1.0", code)
    _apply_highlighting(widget, code)
    widget.configure(state="disabled")

    return outer


# ── Highlighting engine ─────────────────────────────────────────────────────

def _apply_highlighting(widget: tk.Text, code: str) -> None:
    def mark(tag: str, pattern: str, flags: int = 0) -> None:
        for m in re.finditer(pattern, code, flags):
            widget.tag_add(tag, _idx(code, m.start()), _idx(code, m.end()))

    # Apply in this order; later tag_raise calls set priority
    mark("string",  r'"(?:[^"\\]|\\.)*"')
    mark("string",  r"'(?:[^'\\]|\\.)*'")
    mark("number",  r"\b\d+[LlFfDd]?\b")
    mark("annot",   r"@\w+")
    kw_pat = r"\b(" + "|".join(re.escape(k) for k in sorted(_KEYWORDS)) + r")\b"
    mark("keyword", kw_pat)
    mark("type",    r"\b[A-Z][a-zA-Z0-9]+\b")   # UpperCase identifiers
    mark("comment", r"//[^\n]*")
    mark("comment", r"/\*.*?\*/", re.DOTALL)

    # Comments and strings win over everything else
    widget.tag_raise("comment")
    widget.tag_raise("string")


def _idx(code: str, offset: int) -> str:
    """Convert a character offset to a Tk '1.0'-style line.col index."""
    before = code[:offset]
    line = before.count("\n") + 1
    col  = offset - before.rfind("\n") - 1
    return f"{line}.{col}"
