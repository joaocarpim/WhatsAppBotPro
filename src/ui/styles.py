MAIN_WINDOW_STYLE = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0B0B0F, stop:1 #12121A);
    }
    QWidget {
        background: transparent;
        color: #FFFFFF;
    }
"""

GLOW_BTN_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 255, 156, 0.15), stop:1 rgba(0, 255, 156, 0.05));
        color: #00FF9C;
        border: 1px solid rgba(0, 255, 156, 0.3);
        border-radius: 25px;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1px;
        font-family: 'Consolas';
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 255, 156, 0.25), stop:1 rgba(0, 255, 156, 0.15));
    }
"""

EXEC_BTN_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(122, 92, 255, 0.15), stop:1 rgba(122, 92, 255, 0.05));
        color: #7A5CFF;
        border: 1px solid rgba(122, 92, 255, 0.3);
        border-radius: 25px;
        font-size: 13px;
        font-weight: bold;
        letter-spacing: 1px;
        font-family: 'Consolas';
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(122, 92, 255, 0.25), stop:1 rgba(122, 92, 255, 0.15));
    }
    QPushButton:disabled {
        background: rgba(40, 40, 50, 0.3);
        color: #4A4A5A;
        border: 1px solid rgba(74, 74, 90, 0.2);
    }
"""

TEXT_EDIT_STYLE = """
    QTextEdit {
        background: rgba(15, 15, 20, 0.6);
        color: #E0E0E8;
        border: 1px solid rgba(0, 255, 156, 0.15);
        border-radius: 15px;
        padding: 10px;
        font-size: 11px;
        font-family: 'Segoe UI';
    }
    QTextEdit:focus {
        border: 1px solid rgba(0, 255, 156, 0.4);
    }
"""

LOG_STYLE = """
    QTextEdit {
        background: rgba(11, 11, 15, 0.8);
        color: #00FF9C;
        border: 1px solid rgba(0, 255, 156, 0.1);
        border-radius: 12px;
        padding: 10px;
    }
"""
