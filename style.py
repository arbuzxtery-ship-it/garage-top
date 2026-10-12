from pathlib import Path

from PySide6.QtGui import QColor, QPalette


class Style:
    """Тёмная тема для всего приложения"""

    ACCENT = "#3d7be0"

    QSS = """
    QPushButton {
        padding: 6px 14px;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
        background: #353535;
    }
    QPushButton:hover { background: #404040; }
    QPushButton:disabled { color: #777777; }
    QPushButton#accent {
        background: #3d7be0;
        border-color: #3d7be0;
        color: white;
    }
    QPushButton#accent:hover { background: #4a88ee; }

    QLineEdit, QComboBox, QDoubleSpinBox, QDateEdit {
        padding: 4px 6px;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
        background: #1f1f1f;
        min-height: 22px;
    }
    QLineEdit:focus, QComboBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
        border-color: #3d7be0;
    }
    QComboBox::drop-down, QDateEdit::drop-down {
        border: none;
        width: 22px;
    }
    QComboBox::down-arrow, QDateEdit::down-arrow {
        image: url(ARROW_PATH);
        width: 10px;
        height: 6px;
    }

    QGroupBox {
        border: 1px solid #4a4a4a;
        border-radius: 6px;
        margin-top: 10px;
        padding-top: 8px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
    }

    QTableWidget {
        border: 1px solid #4a4a4a;
        gridline-color: #333333;
    }
    QHeaderView::section {
        background: #2b2b2b;
        border: none;
        border-bottom: 1px solid #4a4a4a;
        padding: 6px;
    }
    """

    @staticmethod
    def apply(app):
        app.setStyle("Fusion")

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#2b2b2b"))
        palette.setColor(QPalette.WindowText, QColor("#e6e6e6"))
        palette.setColor(QPalette.Base, QColor("#1f1f1f"))
        palette.setColor(QPalette.AlternateBase, QColor("#262626"))
        palette.setColor(QPalette.Text, QColor("#e6e6e6"))
        palette.setColor(QPalette.Button, QColor("#353535"))
        palette.setColor(QPalette.ButtonText, QColor("#e6e6e6"))
        palette.setColor(QPalette.Highlight, QColor(Style.ACCENT))
        palette.setColor(QPalette.HighlightedText, QColor("white"))
        palette.setColor(QPalette.ToolTipBase, QColor("#353535"))
        palette.setColor(QPalette.ToolTipText, QColor("#e6e6e6"))
        palette.setColor(QPalette.PlaceholderText, QColor("#808080"))
        palette.setColor(QPalette.Disabled, QPalette.Text, QColor("#777777"))
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor("#777777"))
        app.setPalette(palette)

        # путь к картинке стрелки для выпадающих списков
        arrow = Path(__file__).parent / "arrow.svg"
        app.setStyleSheet(Style.QSS.replace("ARROW_PATH", arrow.as_posix()))
