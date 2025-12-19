import tkinter as tk
import re, keyword

SYNTAX_COLORS = {
    "keyword": ["#bf0000", ("Consolas", 10, "bold")],
    "string": ["#00bf00", ("Consolas", 10)],
    "comment": ["#808080", ("Consolas", 10, "italic")],
    "number": ["#0000bf", ("Consolas", 10)],
    "builtin": ["#bf8000", ("Consolas", 10)],
    "operator": ["#404040", ("Consolas", 10)],
}

def highlight(widget, event=None):
    content = widget.get("1.0", "end-1c")

    for tag in SYNTAX_COLORS:
        widget.tag_remove(tag, "1.0", "end")
        
    def has_tag(index, tag):
        return tag in widget.tag_names(index)

    for m in re.finditer(r"""(?<!["'])#.*""", content):
        widget.tag_add("comment", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    for m in re.finditer(r"(\".*?\"|\'.*?\')", content):
        widget.tag_add("string", f"1.0+{m.start()}c", f"1.0+{m.end()}c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", content):
        start = f"1.0+{m.start()}c"
        if has_tag(start, "string") or has_tag(start, "comment"):
            continue
        widget.tag_add("number", start, f"1.0+{m.end()}c")

    for b in dir(__builtins__):
        for m in re.finditer(rf"\b{b}\b", content):
            start = f"1.0+{m.start()}c"
            if has_tag(start, "string") or has_tag(start, "comment"):
                continue
            widget.tag_add("builtin", start, f"1.0+{m.end()}c")

    for kw in keyword.kwlist:
        for m in re.finditer(rf"\b{kw}\b", content):
            widget.tag_add("keyword", f"1.0+{m.start()}c", f"1.0+{m.end()}c")
    
    operator_pattern = r"""
        (\+=|-=|\*=|/=|%=|//=|\*\*|
         ==|!=|<=|>=|
         =|<|>|
         \+|-|\*|/|%|
         \b(and|or|not)\b)
    """

    for m in re.finditer(operator_pattern, content, re.VERBOSE):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"

        if has_tag(start, "string") or has_tag(start, "comment"):
            continue

        widget.tag_add("operator", start, end)