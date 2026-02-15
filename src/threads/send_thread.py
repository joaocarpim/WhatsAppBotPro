import time
from PySide6.QtCore import QThread, Signal


class SendThread(QThread):
    log_signal = Signal(str, str)
    progress_signal = Signal(int, int, int, int)
    finished_signal = Signal()

    def __init__(self, bot, mensagem, contatos):
        super().__init__()
        self.bot = bot
        self.mensagem = mensagem
        self.contatos = contatos
        self.success = 0
        self.failed = 0
        self.skipped = 0

    def run(self):
        total = len(self.contatos)
        self.log_signal.emit("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "system")
        self.log_signal.emit(f"▸ INICIANDO DISPARO MASSIVO", "system")
        self.log_signal.emit(f"▸ Alvos identificados: {total}", "info")
        self.log_signal.emit("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "system")

        for i, contato in enumerate(self.contatos, 1):
            self.log_signal.emit(
                f"▸ [{i}/{total}] Processando alvo: {contato}", "processing")

            numero_formatado, status = self.bot.formatar_numero(contato)
            if not numero_formatado:
                self.skipped += 1
                self.log_signal.emit(
                    f"⊘ Ignorado | {contato} | {status}", "skip")
                self.progress_signal.emit(
                    self.success, self.failed, self.skipped, total)
                continue

            ok, res = self.bot.enviar(contato, self.mensagem)

            if ok:
                self.success += 1
                self.log_signal.emit(f"✓ Executado | {contato}", "success")
            elif "não cadastrado" in res.lower() or "inválido" in res.lower():
                self.skipped += 1
                self.log_signal.emit(f"⊘ Alvo inválido | {contato}", "skip")
            else:
                self.failed += 1
                self.log_signal.emit(f"✗ Falha | {contato} | {res}", "error")

            self.progress_signal.emit(
                self.success, self.failed, self.skipped, total)

            if i < total:
                self.log_signal.emit("▸ Intervalo de segurança: 8s", "warning")
                time.sleep(8)

        rate = (self.success / (self.success + self.failed) *
                100) if (self.success + self.failed) > 0 else 0

        self.log_signal.emit("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "system")
        self.log_signal.emit("✓ OPERAÇÃO CONCLUÍDA", "success")
        self.log_signal.emit(f"▸ Executados: {self.success}", "success")
        self.log_signal.emit(
            f"▸ Falhas: {self.failed}", "error" if self.failed > 0 else "info")
        self.log_signal.emit(f"▸ Taxa de êxito: {rate:.1f}%", "success")
        self.log_signal.emit("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", "system")

        self.finished_signal.emit()
