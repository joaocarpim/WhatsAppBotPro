import time
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QFrame, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont

# Imports Modularizados
from src.bot.whatsapp_bot import WhatsAppBot
from src.ui.widgets import GlowButton, StatusIndicator, BiohackerCard, SystemMetric
from src.ui.styles import *
from src.threads.connection_thread import ConnectionThread
from src.threads.send_thread import SendThread
from src.utils.helpers import format_log_html


class WhatsAppBotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bot = WhatsAppBot()
        self.connected = False
        self.start_time = None
        self.stats = {"sent": 0, "success": 0, "failed": 0, "skipped": 0}
        self.is_sending = False
        self.setup_ui()
        self.apply_styles()
        self.start_timer()

    def setup_ui(self):
        self.setWindowTitle("WhatsApp Bot // Professional Edition 2.0")
        self.setGeometry(100, 80, 950, 600)
        self.setMinimumSize(950, 600)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.addWidget(self.create_header())

        content = QHBoxLayout()
        content.setSpacing(15)
        content.addWidget(self.create_left_column(), 3)
        content.addWidget(self.create_right_column(), 2)
        main_layout.addLayout(content)

    def create_header(self):
        header = QFrame()
        header.setFixedHeight(75)
        header.setStyleSheet("background: transparent; border: none;")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)

        tc = QFrame()
        tc.setStyleSheet("background: transparent; border: none;")
        tl = QHBoxLayout(tc)
        tl.setContentsMargins(0, 0, 0, 0)
        tl.setSpacing(12)

        logo = QLabel("⚡")
        logo.setFont(QFont("Segoe UI", 32))
        logo.setStyleSheet("color: #00FF9C; background: transparent;")
        tl.addWidget(logo)

        tb = QFrame()
        tb.setStyleSheet("background: transparent; border: none;")
        txl = QVBoxLayout(tb)
        txl.setContentsMargins(0, 0, 0, 0)
        txl.setSpacing(2)

        t = QLabel("WHATSAPP BOT")
        t.setFont(QFont("Segoe UI", 20, QFont.Bold))
        t.setStyleSheet(
            "color: #FFFFFF; background: transparent; letter-spacing: 2px;")
        txl.addWidget(t)
        sub = QLabel("TEXT MESSAGING SYSTEM")
        sub.setFont(QFont("Consolas", 8))
        sub.setStyleSheet(
            "color: #00FF9C; background: transparent; letter-spacing: 1px;")
        txl.addWidget(sub)
        tl.addWidget(tb)
        layout.addWidget(tc)
        layout.addStretch()

        sc = QFrame()
        sc.setStyleSheet(
            "background: rgba(26, 26, 35, 0.8); border: 1px solid rgba(255, 59, 92, 0.3); border-radius: 18px; padding: 10px 20px;")
        sl = QHBoxLayout(sc)
        sl.setContentsMargins(20, 10, 20, 10)
        sl.setSpacing(10)
        self.status_indicator = StatusIndicator()
        sl.addWidget(self.status_indicator)
        self.status_label = QLabel("DESCONECTADO")
        self.status_label.setFont(QFont("Consolas", 10, QFont.Bold))
        self.status_label.setStyleSheet(
            "color: #FF3B5C; background: transparent; border: none; letter-spacing: 1px;")
        sl.addWidget(self.status_label)
        layout.addWidget(sc)
        return header

    def create_left_column(self):
        left = QFrame()
        left.setStyleSheet("background: transparent; border: none;")
        layout = QVBoxLayout(left)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        self.btn_connect = GlowButton("CONECTAR", "◉", "#00FF9C")
        self.btn_connect.clicked.connect(self.conectar)
        self.btn_connect.setStyleSheet(GLOW_BTN_STYLE)
        btn_layout.addWidget(self.btn_connect)
        self.btn_send = GlowButton("EXECUTAR", "▸", "#7A5CFF")
        self.btn_send.clicked.connect(self.disparar)
        self.btn_send.setEnabled(False)
        self.btn_send.setStyleSheet(EXEC_BTN_STYLE)
        btn_layout.addWidget(self.btn_send)
        layout.addLayout(btn_layout)

        msg_card = BiohackerCard("MENSAGEM", "◈")
        self.txt_msg = QTextEdit()
        self.txt_msg.setPlaceholderText(
            "Digite a mensagem que será enviada...")
        self.txt_msg.setStyleSheet(TEXT_EDIT_STYLE)
        msg_card.main_layout.addWidget(self.txt_msg)
        layout.addWidget(msg_card)

        contacts_card = BiohackerCard("ALVOS // CONTATOS", "◎")
        self.txt_contacts = QTextEdit()
        self.txt_contacts.setPlaceholderText("11987654321\n11912345678...")
        self.txt_contacts.setStyleSheet(
            TEXT_EDIT_STYLE.replace("Segoe UI", "Consolas"))
        contacts_card.main_layout.addWidget(self.txt_contacts)
        layout.addWidget(contacts_card)
        return left

    def create_right_column(self):
        right = QFrame()
        right.setStyleSheet("background: transparent; border: none;")
        right.setFixedWidth(340)
        layout = QVBoxLayout(right)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        metrics_card = BiohackerCard("MÉTRICAS DO SISTEMA", "◉")
        self.metric_time = SystemMetric("⧗", "TEMPO ATIVO", "00:00:00")
        self.metric_sent = SystemMetric("◈", "EXECUTADOS", "0")
        self.metric_rate = SystemMetric("◎", "TAXA DE ÊXITO", "0%")
        metrics_card.main_layout.addWidget(self.metric_time)
        metrics_card.main_layout.addWidget(self.metric_sent)
        metrics_card.main_layout.addWidget(self.metric_rate)

        info_frame = QFrame()
        info_frame.setStyleSheet(
            "background: rgba(0, 255, 156, 0.05); border: 1px solid rgba(0, 255, 156, 0.15); border-radius: 12px; padding: 12px;")
        il = QVBoxLayout(info_frame)
        il.setSpacing(6)
        it = QLabel("◉ SISTEMA DE MENSAGENS")
        it.setFont(QFont("Consolas", 9, QFont.Bold))
        it.setStyleSheet(
            "color: #00FF9C; background: transparent; border: none;")
        il.addWidget(it)

        for p in ["▸ Envio de mensagens de texto", "▸ Logs detalhados no terminal", "▸ Intervalo de segurança: 8s"]:
            pl = QLabel(p)
            pl.setFont(QFont("Segoe UI", 8))
            pl.setStyleSheet(
                "color: #8B8B9A; background: transparent; border: none;")
            il.addWidget(pl)
        metrics_card.main_layout.addWidget(info_frame)
        metrics_card.main_layout.addStretch()
        layout.addWidget(metrics_card)

        logs_card = BiohackerCard("TERMINAL // LOGS", "◈")
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setFont(QFont("Consolas", 8))
        self.log_view.setStyleSheet(LOG_STYLE)
        logs_card.main_layout.addWidget(self.log_view)
        layout.addWidget(logs_card)
        return right

    def apply_styles(self):
        self.setStyleSheet(MAIN_WINDOW_STYLE)

    def log(self, msg, tipo="info"):
        self.log_view.insertHtml(format_log_html(msg, tipo))
        self.log_view.verticalScrollBar().setValue(
            self.log_view.verticalScrollBar().maximum())

    def conectar(self):
        self.btn_connect.setEnabled(False)
        self.connection_thread = ConnectionThread(self.bot)
        self.connection_thread.log_signal.connect(self.log)
        self.connection_thread.status_signal.connect(self.on_connection_result)
        self.connection_thread.start()

    def on_connection_result(self, success):
        if success:
            self.connected = True
            self.start_time = time.time()
            self.status_label.setText("CONECTADO")
            self.status_label.setStyleSheet(
                "color: #00FF9C; background: transparent; border: none;")
            self.status_indicator.set_color("#00FF9C")
            self.status_indicator.start_pulse()
            self.btn_send.setEnabled(True)
        else:
            self.btn_connect.setEnabled(True)
            QMessageBox.critical(
                self, "✗ FALHA", "Não foi possível estabelecer conexão")

    def disparar(self):
        if self.is_sending:
            QMessageBox.warning(self, "⚠ ATENÇÃO", "Aguarde a operação atual")
            return
        msg = self.txt_msg.toPlainText().strip()
        contatos = [c.strip()
                    for c in self.txt_contacts.toPlainText().split('\n') if c.strip()]
        if not msg or not contatos:
            QMessageBox.warning(self, "⚠ DADOS INSUFICIENTES",
                                "Preencha a mensagem e os alvos")
            return

        reply = QMessageBox.question(
            self, "◉ CONFIRMAR EXECUÇÃO", f"Executar para {len(contatos)} alvos?", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        self.is_sending = True
        self.btn_send.setEnabled(False)
        self.btn_connect.setEnabled(False)
        self.send_thread = SendThread(self.bot, msg, contatos)
        self.send_thread.log_signal.connect(self.log)
        self.send_thread.progress_signal.connect(self.update_stats)
        self.send_thread.finished_signal.connect(self.on_send_finished)
        self.send_thread.start()

    def update_stats(self, success, failed, skipped, total):
        self.stats = {"success": success, "failed": failed, "skipped": skipped}
        sent = success + failed
        rate = (success / sent * 100) if sent > 0 else 0
        self.metric_sent.set_value(str(sent))
        self.metric_rate.set_value(f"{rate:.1f}%")

    def on_send_finished(self):
        self.btn_send.setEnabled(True)
        self.btn_connect.setEnabled(False)
        self.is_sending = False
        total = self.stats['success'] + self.stats['failed']
        rate = (self.stats['success'] / total * 100) if total > 0 else 0
        QMessageBox.information(self, "✓ OPERAÇÃO CONCLUÍDA",
                                f"Executados: {self.stats['success']}\nFalhas: {self.stats['failed']}\nIgnorados: {self.stats['skipped']}\nTaxa: {rate:.1f}%")

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def update_time(self):
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            h, m, s = elapsed // 3600, (elapsed % 3600) // 60, elapsed % 60
            self.metric_time.set_value(f"{h:02d}:{m:02d}:{s:02d}")

    def closeEvent(self, event):
        if self.bot.driver:
            self.bot.fechar()
        event.accept()