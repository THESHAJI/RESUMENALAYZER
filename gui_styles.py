"""Premium dark-theme stylesheet for PyQt5 GUI."""

MAIN_STYLESHEET = """
QMainWindow {
    background-color: #0a0a14;
}
QWidget {
    background-color: #0a0a14;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLabel {
    color: #e0e0e0;
    background: transparent;
}
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00d4ff, stop:1 #7c3aed);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-size: 14px;
    font-weight: bold;
    min-height: 20px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #33dfff, stop:1 #9b5de5);
}
QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #0099cc, stop:1 #5b21b6);
}
QPushButton#secondaryBtn {
    background: transparent;
    border: 2px solid #7c3aed;
    color: #7c3aed;
}
QPushButton#secondaryBtn:hover {
    background: #7c3aed22;
}
QTextEdit {
    background-color: #12122a;
    border: 2px solid #252545;
    border-radius: 10px;
    padding: 12px;
    font-size: 13px;
    color: #d0d0d0;
    selection-background-color: #7c3aed;
}
QTextEdit:focus {
    border-color: #00d4ff;
}
QProgressBar {
    background-color: #1a1a2e;
    border: none;
    border-radius: 8px;
    text-align: center;
    color: white;
    font-weight: bold;
    min-height: 22px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00d4ff, stop:1 #7c3aed);
    border-radius: 8px;
}
QTabWidget::pane {
    background: #0f0f1a;
    border: 1px solid #252545;
    border-radius: 8px;
}
QTabBar::tab {
    background: #1a1a2e;
    color: #888;
    padding: 10px 20px;
    margin: 2px;
    border-radius: 6px 6px 0 0;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #252545;
    color: #00d4ff;
}
QTabBar::tab:hover {
    color: #ffffff;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: #0f0f1a;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #333355;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #7c3aed;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""

CARD_STYLE = """
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a1a2e, stop:1 #151528);
    border: 1px solid #252545;
    border-radius: 12px;
    padding: 20px;
"""

SCORE_CARD_STYLE = """
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #0d1b2a, stop:1 #1b2838);
    border: 1px solid #00d4ff44;
    border-radius: 16px;
    padding: 16px;
"""

HEADER_STYLE = """
    font-size: 28px;
    font-weight: bold;
    color: #00d4ff;
    background: transparent;
"""

SUBHEADER_STYLE = """
    font-size: 16px;
    color: #888;
    background: transparent;
"""

SKILL_PILL_PRESENT = """
    background-color: #10b98133;
    color: #10b981;
    border: 1px solid #10b98155;
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: bold;
"""

SKILL_PILL_MISSING = """
    background-color: #ef444433;
    color: #ef4444;
    border: 1px solid #ef444455;
    border-radius: 12px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: bold;
"""
