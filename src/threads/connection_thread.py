from PySide6.QtCore import QThread, Signal


class ConnectionThread(QThread):
    log_signal = Signal(str, str)
    status_signal = Signal(bool)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def run(self):
        self.log_signal.emit("▸ INICIANDO SISTEMA...", "system")

        if self.bot.iniciar(headless=False):
            self.log_signal.emit(
                "✓ Navegador aberto. Verificando sessão...", "info")
            if self.bot.aguardar_login():
                self.log_signal.emit("✓✓✓ CONECTADO! ✓✓✓", "success")
                self.log_signal.emit("▸ Sessão salva.", "success")
                self.status_signal.emit(True)
            else:
                self.log_signal.emit("✗ Timeout: QR Code não lido.", "error")
                self.bot.fechar()
                self.status_signal.emit(False)
        else:
            self.log_signal.emit("✗ Erro crítico ao abrir navegador.", "error")
            self.status_signal.emit(False)
