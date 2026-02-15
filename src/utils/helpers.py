from datetime import datetime


def get_timestamp():
    """Retorna hora formatada para logs"""
    return datetime.now().strftime('%H:%M:%S')


def format_log_html(msg, tipo="info"):
    """Formata a mensagem para o terminal HTML"""
    colors = {
        "info": "#00D9FF",
        "success": "#00FF9C",
        "error": "#FF3B5C",
        "warning": "#FFB84D",
        "processing": "#7A5CFF",
        "skip": "#6B6B7A",
        "system": "#00FF9C"
    }
    timestamp = get_timestamp()
    color = colors.get(tipo, colors["info"])

    html = f'<span style="color: #4A4A5A;">[{timestamp}]</span> '
    html += f'<span style="color: {color};">{msg}</span><br>'
    return html
