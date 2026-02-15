from PySide6.QtWidgets import QPushButton, QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QBrush, QFont


class GlowButton(QPushButton):
    def __init__(self, text, icon="", color="#00FF9C"):
        super().__init__(f"{icon} {text}" if icon else text)
        self.color = color
        self.setFixedHeight(42)
        self.setCursor(Qt.PointingHandCursor)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(25)
        glow.setColor(QColor(color))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)


class StatusIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(12, 12)
        self.color = QColor("#FF3B5C")
        self.pulse_value = 1.0
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.update_pulse)

    def set_color(self, color):
        self.color = QColor(color)
        self.update()

    def start_pulse(self):
        self.pulse_timer.start(50)

    def stop_pulse(self):
        self.pulse_timer.stop()
        self.pulse_value = 1.0
        self.update()

    def update_pulse(self):
        self.pulse_value += 0.05
        if self.pulse_value > 1.5:
            self.pulse_value = 1.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        glow_size = int(6 * self.pulse_value)
        glow_offset = 6 - glow_size // 2
        painter.setBrush(
            QBrush(QColor(self.color.red(), self.color.green(), self.color.blue(), 40)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(glow_offset, glow_offset, glow_size, glow_size)
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(4, 4, 4, 4)


class BiohackerCard(QFrame):
    def __init__(self, title, icon="", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(26, 26, 35, 0.95), stop:1 rgba(15, 15, 20, 0.95));
                border: 1px solid rgba(0, 255, 156, 0.2);
                border-radius: 20px;
            }
        """)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setColor(QColor(0, 255, 156, 30))
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 12, 15, 12)
        self.main_layout.setSpacing(10)

        if title:
            header = QHBoxLayout()
            header.setSpacing(8)
            if icon:
                il = QLabel(icon)
                il.setFont(QFont("Segoe UI", 12))
                il.setStyleSheet(
                    "color: #00FF9C; background: transparent; border: none;")
                header.addWidget(il)
            tl = QLabel(title)
            tl.setFont(QFont("Segoe UI", 11, QFont.Bold))
            tl.setStyleSheet(
                "color: #FFFFFF; background: transparent; border: none; letter-spacing: 1px;")
            header.addWidget(tl)
            header.addStretch()
            self.main_layout.addLayout(header)
            sep = QFrame()
            sep.setFixedHeight(1)
            sep.setStyleSheet(
                "background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.5 rgba(0, 255, 156, 0.5), stop:1 transparent); border: none;")
            self.main_layout.addWidget(sep)


class SystemMetric(QFrame):
    def __init__(self, icon, label, value="---"):
        super().__init__()
        self.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(10)
        il = QLabel(icon)
        il.setFont(QFont("Segoe UI", 12))
        il.setStyleSheet("color: #00FF9C; background: transparent;")
        layout.addWidget(il)
        tl = QLabel(label)
        tl.setFont(QFont("Segoe UI", 9))
        tl.setStyleSheet(
            "color: #8B8B9A; background: transparent; letter-spacing: 0.5px;")
        layout.addWidget(tl)
        layout.addStretch()
        vc = QFrame()
        vc.setStyleSheet(
            "background: rgba(0, 255, 156, 0.08); border: 1px solid rgba(0, 255, 156, 0.2); border-radius: 12px; padding: 4px 12px;")
        vl = QHBoxLayout(vc)
        vl.setContentsMargins(10, 3, 10, 3)
        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("Consolas", 10, QFont.Bold))
        self.value_label.setStyleSheet(
            "color: #00FF9C; background: transparent; border: none;")
        vl.addWidget(self.value_label)
        layout.addWidget(vc)

    def set_value(self, value):
        self.value_label.setText(str(value))
