import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont
from src.ui.main_window import WhatsAppBotWindow     

def main():
    app = QApplication(sys.argv)

    # Configuração Global de Fonte
    app.setFont(QFont("Segoe UI", 9))

    print("="*60)
    print("📱 WHATSAPP BOT - TEXT MESSAGING SYSTEM")
    print("="*60)
    print("Sistema de envio de mensagens de texto")
    print("Logs detalhados aparecerão no terminal")
    print("="*60)
    print()

    window = WhatsAppBotWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
