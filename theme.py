DARK_STYLESHEET = """
/* ── Application base ─────────────────────────────────────────────────────── */
QWidget {
    color: #DCE4EE;
    font-family: "Roboto", "Segoe UI", sans-serif;
}
QMainWindow, QMainWindow > QWidget {
    background-color: #242424;
}
/* ── Panels / Frames ──────────────────────────────────────────────────────── */
QFrame#leftPanel {
    background-color: #2B2B2B;
}
QFrame#rightOuter {
    background-color: #1D1E1E;
}
QFrame#rightInner {
    background-color: #2B2B2B;
    border-radius: 6px;
}
/* ── Labels ───────────────────────────────────────────────────────────────── */
QLabel {
    background-color: transparent;
    color: #DCE4EE;
}
QLabel#terminal {
    background-color: #1F1E1E;
    color: #DCE4EE;
    border-radius: 6px;
    padding: 10px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
}
/* ── Buttons ──────────────────────────────────────────────────────────────── */
QPushButton {
    background-color: #FF8000;
    color: #DCE4EE;
    border: none;
    border-radius: 6px;
    padding: 6px 16px;
}
QPushButton:hover {
    background-color: #FF9E17;
}
QPushButton:pressed {
    background-color: #E07000;
}
QPushButton:disabled {
    background-color: #4A4D50;
    color: #808080;
}
/* ── Toggle switch track states ───────────────────────────────────────────── */
QPushButton#toggleOff {
    background-color: #4A4D50;
    border-radius: 14px;
    border: 3px solid #4A4D50;
    padding: 0px;
}
QPushButton#toggleOn {
    background-color: #FFBA88;
    border-radius: 14px;
    border: 3px solid #FFBA88;
    padding: 0px;
}
/* ── Drag & drop boxes ────────────────────────────────────────────────────── */
QFrame#dropBox {
    border: 2px dashed #555555;
    border-radius: 6px;
    background-color: #2B2B2B;
}
QFrame#dropBoxActive {
    border: 2px dashed #4A90D9;
    border-radius: 6px;
    background-color: #303A45;
}
QLabel#dropBoxPath {
    color: #777777;
}
/* ── Scrollbars ───────────────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #696969;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #878787;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""

LIGHT_STYLESHEET = """
/* ── Application base ─────────────────────────────────────────────────────── */
QWidget {
    color: #2E2E2E;
    font-family: "Roboto", "Segoe UI", sans-serif;
}
QMainWindow, QMainWindow > QWidget {
    background-color: #F2F0ED;
}
/* ── Panels / Frames ──────────────────────────────────────────────────────── */
QFrame#leftPanel {
    background-color: #E9E6E1;
}
QFrame#rightOuter {
    background-color: #EDEAE5;
}
QFrame#rightInner {
    background-color: #FBFAF8;
    border-radius: 6px;
}
/* ── Labels ───────────────────────────────────────────────────────────────── */
QLabel {
    background-color: transparent;
    color: #2E2E2E;
}
QLabel#terminal {
    background-color: #E3E0DA;
    color: #3A3A3A;
    border-radius: 6px;
    padding: 10px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
    border: 1px solid #DDD9D2;
}
/* ── Buttons ──────────────────────────────────────────────────────────────── */
QPushButton {
    background-color: #E07B00;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    padding: 6px 16px;
}
QPushButton:hover {
    background-color: #F08C10;
}
QPushButton:pressed {
    background-color: #C46A00;
}
QPushButton:disabled {
    background-color: #D8D5CF;
    color: #A6A29A;
}
/* ── Toggle switch track states ───────────────────────────────────────────── */
QPushButton#toggleOff {
    background-color: #D3CFC7;
    border-radius: 14px;
    border: 3px solid #D3CFC7;
    padding: 0px;
}
QPushButton#toggleOn {
    background-color: #F3B87E;
    border-radius: 14px;
    border: 3px solid #F3B87E;
    padding: 0px;
}
/* ── Drag & drop boxes ────────────────────────────────────────────────────── */
QFrame#dropBox {
    border: 2px dashed #C7C2B9;
    border-radius: 6px;
    background-color: #EDEAE5;
}
QFrame#dropBoxActive {
    border: 2px dashed #E07B00;
    border-radius: 6px;
    background-color: #F7E7D6;
}
QLabel#dropBoxPath {
    color: #9A968D;
}
/* ── Scrollbars ───────────────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #C2BDB3;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #A8A297;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
