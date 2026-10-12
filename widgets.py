from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QAbstractItemView, QComboBox, QDateEdit, QDoubleSpinBox, QGridLayout, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QMessageBox, QPushButton, QStatusBar,
    QTableWidget, QTableWidgetItem,
)

from utils import Utils


class Button(QPushButton):

    def __init__(self, text):
        super().__init__(text)
        self.setCursor(Qt.PointingHandCursor)


class AccentButton(Button):
    """Синяя кнопка для главного действия"""

    def __init__(self, text):
        super().__init__(text)
        self.setObjectName("accent")


class LineEdit(QLineEdit):

    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)


class ComboBox(QComboBox):

    def __init__(self, items=None):
        super().__init__()
        if items:
            self.addItems(items)
        self.setFocusPolicy(Qt.StrongFocus)

    # чтобы значение не менялось случайно при прокрутке окна колёсиком
    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class SpinBox(QDoubleSpinBox):

    def __init__(self, maximum, decimals=2, suffix=""):
        super().__init__()
        self.setRange(0, maximum)
        self.setDecimals(decimals)
        self.setSuffix(suffix)
        self.setGroupSeparatorShown(True)
        self.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        if self.hasFocus():
            super().wheelEvent(event)
        else:
            event.ignore()


class DateEdit(QDateEdit):

    def __init__(self):
        super().__init__()
        self.setCalendarPopup(True)
        self.setDisplayFormat("dd.MM.yyyy")
        self.setMaximumDate(QDate.currentDate())
        self.setDate(QDate.currentDate())


class TableItem(QTableWidgetItem):
    """Ячейка, которая сортируется по числу, а не по тексту"""

    def __init__(self, text, sort_value=None):
        super().__init__(text)
        self.sort_value = sort_value if sort_value is not None else text

    def __lt__(self, other):
        return self.sort_value < other.sort_value


class RecordsTable(QTableWidget):
    COLUMNS = ["Дата", "Тип", "Пробег", "Описание", "Стоимость"]

    delete_pressed = Signal()

    def __init__(self):
        super().__init__(0, len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSortIndicator(0, Qt.DescendingOrder)

    def show_records(self, records):
        # во время заполнения сортировку выключаем, иначе строки перемешаются
        self.setSortingEnabled(False)
        self.setRowCount(len(records))
        for row, record in enumerate(records):
            items = [
                TableItem(Utils.date_to_str(record.date), record.date),
                TableItem(record.get_type()),
                TableItem(Utils.km(record.mileage), record.mileage),
                TableItem(record.info()),
                TableItem(Utils.money(record.get_cost()), record.get_cost()),
            ]
            items[0].setData(Qt.UserRole, record)
            items[2].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            items[4].setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            for column, item in enumerate(items):
                self.setItem(row, column, item)
        self.setSortingEnabled(True)

    def selected_record(self):
        row = self.currentRow()
        if row < 0 or not self.selectedItems():
            return None
        return self.item(row, 0).data(Qt.UserRole)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self.delete_pressed.emit()
        else:
            super().keyPressEvent(event)


class SummaryBox(QGroupBox):
    """Блок с итогами по выбранной машине"""

    TITLES = ["Всего потрачено", "Топливо", "Ремонт", "Замена масла", "Следующая замена масла"]

    def __init__(self):
        super().__init__("Сводка")
        layout = QGridLayout(self)
        layout.setHorizontalSpacing(30)

        bold = QFont()
        bold.setPointSize(15)
        bold.setBold(True)

        self.values = []
        for column, title in enumerate(self.TITLES):
            caption = QLabel(title)
            caption.setStyleSheet("color: #9a9a9a;")
            value = QLabel("-")
            value.setFont(bold)
            layout.addWidget(caption, 0, column)
            layout.addWidget(value, 1, column)
            self.values.append(value)

    def set_values(self, values):
        for label, text in zip(self.values, values):
            label.setText(text)


class StatusBar(QStatusBar):

    def __init__(self, text):
        super().__init__()
        self.addPermanentWidget(QLabel(text))

    def show_message(self, text):
        self.showMessage(text, 4000)


class MessageBox(QMessageBox):
    """Окна сообщений с русскими кнопками"""

    @staticmethod
    def ask(parent, title, text):
        box = MessageBox(parent)
        box.setWindowTitle(title)
        box.setText(text)
        yes = box.addButton("Да", QMessageBox.YesRole)
        box.addButton("Нет", QMessageBox.NoRole)
        box.exec()
        return box.clickedButton() == yes

    @staticmethod
    def error(parent, text):
        box = MessageBox(parent)
        box.setWindowTitle("Ошибка")
        box.setIcon(QMessageBox.Warning)
        box.setText(text)
        box.addButton("OK", QMessageBox.AcceptRole)
        box.exec()
