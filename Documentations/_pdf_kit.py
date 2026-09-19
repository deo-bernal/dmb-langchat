"""Shared navy/red PDF kit for DMB product documentation."""

from pathlib import Path

from fpdf import FPDF

NAVY = (15, 23, 42)
SLATE = (51, 65, 85)
RED = (185, 28, 28)
RULE = (226, 232, 240)
HEADING = (30, 41, 59)
MUTED = (100, 116, 139)
BOX_FILL = (241, 245, 249)
ACCENT_FILL = (254, 242, 242)
OK_FILL = (236, 253, 245)
OK_BORDER = (5, 150, 105)
WHITE = (255, 255, 255)
INFO_FILL = (239, 246, 255)

LEFT = 16
RIGHT = 194
USABLE = RIGHT - LEFT


def safe(text):
    if text is None:
        return ""
    s = str(text)
    trans = str.maketrans(
        {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2026": "...",
            "\u2192": "->",
            "\u00a0": " ",
            "\u2022": "-",
            "\u20b1": "PHP",
        }
    )
    return s.translate(trans).encode("latin-1", "replace").decode("latin-1")


class DmbDoc(FPDF):
    def __init__(self, header_left, header_right, **kwargs):
        kwargs.setdefault("format", "A4")
        kwargs.setdefault("unit", "mm")
        super().__init__(**kwargs)
        self.header_left = safe(header_left)
        self.header_right = safe(header_right)
        self.set_auto_page_break(auto=True, margin=18)
        self.set_left_margin(LEFT)
        self.set_right_margin(16)

    def header(self):
        if self.page_no() == 1:
            return
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 12, "F")
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "", 8)
        self.set_xy(LEFT, 4)
        self.cell(118, 5, self.header_left, align="L")
        self.cell(0, 5, self.header_right, align="R")
        self.ln(12)
        self.set_text_color(*SLATE)

    def footer(self):
        self.set_y(-14)
        self.set_draw_color(*RULE)
        self.line(LEFT, self.get_y(), RIGHT, self.get_y())
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*MUTED)
        self.set_y(-11)
        self.cell(0, 6, f"Confidential  ·  {self.page_no()}", align="C")

    def cover(self, brand, title, subtitle, meta):
        self.add_page()
        self.set_fill_color(*NAVY)
        self.rect(0, 0, 210, 58, "F")
        self.set_fill_color(*RED)
        self.rect(0, 58, 210, 3, "F")
        self.set_text_color(*WHITE)
        self.set_xy(LEFT, 16)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 6, safe(brand))
        self.set_xy(LEFT, 26)
        self.set_font("Helvetica", "B", 22)
        self.cell(0, 10, safe(title))
        self.set_xy(LEFT, 38)
        self.set_font("Helvetica", "", 12)
        self.cell(0, 7, safe(subtitle))
        self.set_xy(LEFT, 46)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(203, 213, 225)
        self.cell(0, 6, safe(meta))
        self.set_y(70)
        self.set_text_color(*SLATE)

    def ensure_space(self, height):
        if self.get_y() + height > self.page_break_trigger:
            self.add_page()

    def h1(self, text):
        self.ensure_space(22)
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(*HEADING)
        self.cell(0, 9, safe(text), new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*RED)
        self.set_line_width(0.6)
        self.line(LEFT, self.get_y(), 70, self.get_y())
        self.ln(5)
        self.set_text_color(*SLATE)
        self.set_line_width(0.2)

    def h2(self, text):
        self.ensure_space(16)
        self.ln(2)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(*HEADING)
        self.cell(0, 8, safe(text), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*SLATE)

    def h3(self, text):
        self.ensure_space(14)
        self.ln(1)
        self.set_font("Helvetica", "B", 10.5)
        self.set_text_color(*HEADING)
        self.cell(0, 7, safe(text), new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(*SLATE)

    def p(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*SLATE)
        self.multi_cell(0, 5.2, safe(text))
        self.ln(1.5)

    def bullet(self, text):
        x = self.get_x()
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*RED)
        self.cell(6, 5.2, "-")
        self.set_text_color(*SLATE)
        self.multi_cell(0, 5.2, safe(text))
        self.set_x(x)
        self.ln(0.4)

    def numbered(self, n, text):
        x = self.get_x()
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*RED)
        self.cell(8, 5.2, f"{n}.")
        self.set_font("Helvetica", "", 10)
        self.set_text_color(*SLATE)
        self.multi_cell(0, 5.2, safe(text))
        self.set_x(x)
        self.ln(0.4)

    def code(self, text):
        self.set_fill_color(248, 250, 252)
        self.set_font("Courier", "", 8.0)
        self.set_text_color(*HEADING)
        self.multi_cell(0, 4.6, safe(text), fill=True)
        self.ln(2)
        self.set_text_color(*SLATE)

    def note(self, text):
        self.set_fill_color(*ACCENT_FILL)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 5, safe(text), fill=True)
        self.ln(2)
        self.set_text_color(*SLATE)

    def info(self, text):
        self.set_fill_color(*INFO_FILL)
        self.set_font("Helvetica", "", 9.5)
        self.set_text_color(*NAVY)
        self.multi_cell(0, 5, safe(text), fill=True)
        self.ln(2)
        self.set_text_color(*SLATE)

    def business(
        self,
        headline,
        problem,
        customer,
        money,
        loop_rows,
        kpis,
        note=None,
        flow=None,
        flow_caption=None,
    ):
        """Front-of-doc business chapter. loop_rows: [step, real_world, software]."""
        self.h1("Business perspective")
        self.info(headline)
        self.h2("The problem (why this exists at all)")
        self.p(problem)
        self.h2("Who the customer is")
        self.p(customer)
        self.h2("How money is supposed to move")
        self.p(money)
        if flow:
            self.flowchart(flow, caption=flow_caption)
        self.h2("How the business runs day to day")
        self.table(
            ["Step", "In the real world", "What this software is for"],
            loop_rows,
            [28, 75, 75],
        )
        self.h2("What 'winning' looks like (KPIs)")
        for item in kpis:
            self.bullet(item)
        if note:
            self.note(note)

    def caption(self, text):
        self.set_font("Helvetica", "I", 8.5)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 4.5, safe(text))
        self.ln(2)
        self.set_text_color(*SLATE)

    def _wrap_line(self, text, width, font="Helvetica", style="", size=8.2):
        text = safe(text)
        self.set_font(font, style, size)
        if self.get_string_width(text) <= width:
            return [text] if text else [""]
        lines = []
        remaining = text
        while remaining:
            if self.get_string_width(remaining) <= width:
                lines.append(remaining)
                break
            lo, hi = 1, len(remaining)
            fit = 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if self.get_string_width(remaining[:mid]) <= width:
                    fit = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            cut = remaining.rfind(" ", 0, fit)
            if cut < 8:
                cut = fit
            lines.append(remaining[:cut].rstrip())
            remaining = remaining[cut:].lstrip()
        return lines or [""]

    def table(self, headers, rows, col_widths):
        self.ensure_space(16)
        line_h = 4.6
        pad = 1.4
        self.set_font("Helvetica", "B", 8.5)
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        header_lines = [
            self._wrap_line(h, w - 2.4, style="B", size=8.5) for h, w in zip(headers, col_widths)
        ]
        header_h = max(len(lines) for lines in header_lines) * line_h + pad * 2
        x0 = LEFT
        y0 = self.get_y()
        x = x0
        for lines, w in zip(header_lines, col_widths):
            self.set_xy(x, y0)
            self.set_fill_color(*NAVY)
            self.rect(x, y0, w, header_h, "F")
            self.set_text_color(*WHITE)
            self.set_font("Helvetica", "B", 8.5)
            ty = y0 + pad
            for line in lines:
                self.set_xy(x + 1.2, ty)
                self.cell(w - 2.4, line_h, line)
                ty += line_h
            x += w
        self.set_y(y0 + header_h)
        fill = False
        for row in rows:
            wrapped = [
                self._wrap_line(cell, w - 2.4, size=8.0) for cell, w in zip(row, col_widths)
            ]
            row_h = max(len(lines) for lines in wrapped) * line_h + pad * 2
            self.ensure_space(row_h + 2)
            y = self.get_y()
            bg = (241, 245, 249) if fill else WHITE
            x = LEFT
            for lines, w in zip(wrapped, col_widths):
                self.set_fill_color(*bg)
                self.rect(x, y, w, row_h, "F")
                self.set_text_color(*SLATE)
                self.set_font("Helvetica", "", 8.0)
                ty = y + pad
                for line in lines:
                    self.set_xy(x + 1.2, ty)
                    self.cell(w - 2.4, line_h, line)
                    ty += line_h
                x += w
            self.set_y(y + row_h)
            fill = not fill
        self.ln(3)
        self.set_text_color(*SLATE)

    def _box_style(self, kind):
        if kind == "dark":
            return NAVY, WHITE, NAVY
        if kind == "accent":
            return ACCENT_FILL, NAVY, RED
        if kind == "ok":
            return OK_FILL, HEADING, OK_BORDER
        return BOX_FILL, HEADING, NAVY

    def _draw_box(self, x, y, w, h, text, kind="default"):
        fill, fg, border = self._box_style(kind)
        self.set_fill_color(*fill)
        self.set_draw_color(*border)
        self.set_line_width(0.35)
        try:
            self.rounded_rect(x, y, w, h, 1.6, style="DF")
        except Exception:
            self.rect(x, y, w, h, style="DF")
        lines = self._wrap_line(text, w - 4, style="B", size=8.0)
        self.set_text_color(*fg)
        self.set_font("Helvetica", "B", 8.0)
        total = len(lines) * 3.8
        ty = y + max((h - total) / 2, 1.2)
        for line in lines:
            self.set_xy(x + 2, ty)
            self.cell(w - 4, 3.8, line, align="C")
            ty += 3.8
        self.set_line_width(0.2)

    def _arrow_right(self, x, y, length=7):
        self.set_draw_color(*NAVY)
        self.set_fill_color(*NAVY)
        self.set_line_width(0.45)
        self.line(x, y, x + length - 2.2, y)
        self.polygon(
            [(x + length - 2.4, y - 1.4), (x + length, y), (x + length - 2.4, y + 1.4)],
            style="F",
        )
        self.set_line_width(0.2)

    def _arrow_down(self, x, y, length=7):
        self.set_draw_color(*NAVY)
        self.set_fill_color(*NAVY)
        self.set_line_width(0.45)
        self.line(x, y, x, y + length - 2.2)
        self.polygon(
            [(x - 1.4, y + length - 2.4), (x, y + length), (x + 1.4, y + length - 2.4)],
            style="F",
        )
        self.set_line_width(0.2)

    def _parse_flow_row(self, row):
        arrows = True
        raw = row
        if isinstance(row, dict):
            raw = row.get("items") or row.get("nodes") or []
            arrows = bool(row.get("arrows", True))
        items = []
        for item in raw:
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                items.append((safe(item[0]), item[1]))
            else:
                items.append((safe(item), "default"))
        return items, arrows

    def flowchart(self, rows, caption=None, box_h=14, h_arrows=None):
        """rows: list of list of str|(text, kind), or dict {items, arrows}."""
        gap_x = 7
        gap_y = 6
        parsed = [self._parse_flow_row(row) for row in rows]
        n_rows = len(parsed)
        height = n_rows * box_h + max(n_rows - 1, 0) * gap_y + 8
        self.ensure_space(height + (8 if caption else 0))
        for r, (items, row_arrows) in enumerate(parsed):
            draw_h = row_arrows if h_arrows is None else h_arrows
            n = max(len(items), 1)
            box_w = (USABLE - gap_x * (n - 1)) / n
            y = self.get_y()
            total_w = n * box_w + (n - 1) * gap_x
            start_x = LEFT + (USABLE - total_w) / 2
            xs = []
            for i, (text, kind) in enumerate(items):
                x = start_x + i * (box_w + gap_x)
                self._draw_box(x, y, box_w, box_h, text, kind)
                xs.append(x + box_w / 2)
                if i < n - 1 and draw_h:
                    self._arrow_right(x + box_w, y + box_h / 2, gap_x)
            self.set_y(y + box_h)
            if r < n_rows - 1:
                next_items, _ = parsed[r + 1]
                next_n = len(next_items)
                next_w = (USABLE - gap_x * (next_n - 1)) / next_n
                next_total = next_n * next_w + (next_n - 1) * gap_x
                next_start = LEFT + (USABLE - next_total) / 2
                next_centers = [
                    next_start + i * (next_w + gap_x) + next_w / 2 for i in range(next_n)
                ]
                y_line = self.get_y()
                if len(xs) == len(next_centers):
                    for cx, nx in zip(xs, next_centers):
                        if abs(cx - nx) < 0.8:
                            self._arrow_down(cx, y_line, gap_y)
                        else:
                            mid_y = y_line + gap_y / 2
                            self.set_draw_color(*NAVY)
                            self.set_fill_color(*NAVY)
                            self.set_line_width(0.45)
                            self.line(cx, y_line, cx, mid_y)
                            self.line(cx, mid_y, nx, mid_y)
                            self._arrow_down(nx, mid_y, gap_y / 2)
                            self.set_line_width(0.2)
                elif len(xs) == 1 and len(next_centers) > 1:
                    mid_y = y_line + gap_y / 2
                    self.set_draw_color(*NAVY)
                    self.set_line_width(0.45)
                    self.line(xs[0], y_line, xs[0], mid_y)
                    self.line(min(next_centers), mid_y, max(next_centers), mid_y)
                    for nx in next_centers:
                        self._arrow_down(nx, mid_y, gap_y / 2)
                    self.set_line_width(0.2)
                elif len(xs) > 1 and len(next_centers) == 1:
                    mid_y = y_line + gap_y / 2
                    self.set_draw_color(*NAVY)
                    self.set_line_width(0.45)
                    self.line(min(xs), mid_y, max(xs), mid_y)
                    for cx in xs:
                        self.line(cx, y_line, cx, mid_y)
                    self._arrow_down(next_centers[0], mid_y, gap_y / 2)
                    self.set_line_width(0.2)
                else:
                    self._arrow_down(LEFT + USABLE / 2, y_line, gap_y)
                self.set_y(y_line + gap_y)
        self.ln(2)
        if caption:
            self.caption(caption)

    def stack(self, layers, caption=None):
        box_h = 12
        gap = 5
        height = len(layers) * box_h + max(len(layers) - 1, 0) * gap + 4
        self.ensure_space(height + (8 if caption else 0))
        for i, layer in enumerate(layers):
            if isinstance(layer, (tuple, list)) and len(layer) >= 2:
                text, kind = layer[0], layer[1]
            else:
                text, kind = layer, "default" if i not in (0, len(layers) - 1) else ("dark" if i == 0 else "ok")
            y = self.get_y()
            self._draw_box(LEFT, y, USABLE, box_h, text, kind)
            self.set_y(y + box_h)
            if i < len(layers) - 1:
                self._arrow_down(LEFT + USABLE / 2, self.get_y(), gap)
                self.set_y(self.get_y() + gap)
        self.ln(2)
        if caption:
            self.caption(caption)

    def scenario(self, number, title, setup, steps, expected):
        self.ensure_space(36)
        self.set_fill_color(*NAVY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 10)
        self.multi_cell(0, 7, safe(f"Scenario {number}.  {title}"), fill=True)
        self.ln(2)
        self.set_text_color(*SLATE)
        if setup:
            self.h3("Setup")
            for line in setup:
                self.bullet(line)
        self.h3("Steps")
        for i, step in enumerate(steps, 1):
            self.numbered(i, step)
        self.h3("Expected result")
        if isinstance(expected, str):
            self.p(expected)
        else:
            for line in expected:
                self.bullet(line)

    def end_note(self, text):
        self.ln(4)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*MUTED)
        self.multi_cell(0, 5, safe(text))


def new_doc(header_left, header_right):
    return DmbDoc(header_left, header_right)


def write_pdf(pdf, path):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out))
    print(out)
    return out
