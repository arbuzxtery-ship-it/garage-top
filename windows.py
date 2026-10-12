from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QMainWindow, QVBoxLayout, QWidget,
)

from models import OilChange, Refuel, Repair
from utils import Utils
from widgets import (
    AccentButton, Button, ComboBox, DateEdit, LineEdit, MessageBox, RecordsTable,
    SpinBox, StatusBar, SummaryBox,
)

RECORD_TYPES = ["Заправка", "Ремонт", "Замена масла"]


class LoginWindow(QDialog):

    def __init__(self, users):
        super().__init__()
        self.users = users
        self.user = None

        self.setWindowTitle("Вход")
        self.setFixedWidth(340)

        title = QLabel("Журнал обслуживания авто")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)

        self.login_edit = LineEdit("Логин")
        self.password_edit = LineEdit("Пароль")
        self.password_edit.setEchoMode(LineEdit.Password)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: #e06c6c;")

        login_button = AccentButton("Войти")
        login_button.setDefault(True)
        login_button.clicked.connect(self.check)

        hint = QLabel("Тестовый вход: admin / admin")
        hint.setStyleSheet("color: #9a9a9a;")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form.addRow("Логин:", self.login_edit)
        form.addRow("Пароль:", self.password_edit)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.error_label)
        layout.addWidget(login_button)
        layout.addWidget(hint)

    def check(self):
        login = self.login_edit.text().strip().lower()
        user = self.users.get(login)
        if user is None or not user.check_password(self.password_edit.text()):
            self.error_label.setText("Неверный логин или пароль")
            self.password_edit.clear()
            return
        self.user = user
        self.accept()


class RecordDialog(QDialog):
    """Окно добавления и изменения записи"""

    def __init__(self, car, record=None, parent=None):
        super().__init__(parent)
        self.car = car
        self.record = None

        if record:
            self.setWindowTitle("Изменить запись")
        else:
            self.setWindowTitle("Новая запись")
        self.setMinimumWidth(400)

        self.type_box = ComboBox(RECORD_TYPES)
        self.date_edit = DateEdit()
        self.mileage_edit = SpinBox(2000000, 0, " км")
        self.mileage_edit.setValue(car.mileage)

        # заправка
        self.fuel_box = ComboBox(Refuel.FUELS)
        self.fuel_box.setCurrentText("АИ-95")
        self.liters_edit = SpinBox(500, 2, " л")
        self.price_edit = SpinBox(1000, 2, " ₽")

        # ремонт
        self.work_edit = LineEdit("Что сделали")
        self.service_edit = LineEdit("Название сервиса")

        # замена масла
        self.oil_edit = LineEdit("Например, Mobil 1 5W-30")
        self.volume_edit = SpinBox(20, 1, " л")
        self.interval_edit = SpinBox(50000, 0, " км")
        self.interval_edit.setValue(10000)

        self.cost_edit = SpinBox(10000000, 2, " ₽")
        self.comment_edit = LineEdit("Необязательно")

        self.form = QFormLayout()
        self.form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.form.addRow("Тип:", self.type_box)
        self.form.addRow("Дата:", self.date_edit)
        self.form.addRow("Пробег:", self.mileage_edit)
        self.form.addRow("Топливо:", self.fuel_box)
        self.form.addRow("Литры:", self.liters_edit)
        self.form.addRow("Цена за литр:", self.price_edit)
        self.form.addRow("Работа:", self.work_edit)
        self.form.addRow("Сервис:", self.service_edit)
        self.form.addRow("Масло:", self.oil_edit)
        self.form.addRow("Объём:", self.volume_edit)
        self.form.addRow("Интервал:", self.interval_edit)
        self.form.addRow("Стоимость:", self.cost_edit)
        self.form.addRow("Комментарий:", self.comment_edit)

        cancel_button = Button("Отмена")
        cancel_button.clicked.connect(self.reject)
        save_button = AccentButton("Сохранить")
        save_button.setDefault(True)
        save_button.clicked.connect(self.save)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(cancel_button)
        buttons.addWidget(save_button)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Автомобиль: {car}"))
        layout.addLayout(self.form)
        layout.addLayout(buttons)

        self.type_box.currentTextChanged.connect(self.update_fields)
        if record:
            self.fill(record)
        self.update_fields()

    def update_fields(self):
        """Показывает только поля, которые нужны для выбранного типа"""
        record_type = self.type_box.currentText()
        refuel = record_type == "Заправка"
        repair = record_type == "Ремонт"
        oil = record_type == "Замена масла"

        for widget in [self.fuel_box, self.liters_edit, self.price_edit]:
            self.form.setRowVisible(widget, refuel)
        for widget in [self.work_edit, self.service_edit]:
            self.form.setRowVisible(widget, repair)
        for widget in [self.oil_edit, self.volume_edit, self.interval_edit]:
            self.form.setRowVisible(widget, oil)
        self.form.setRowVisible(self.cost_edit, not refuel)
        self.adjustSize()

    def fill(self, record):
        self.type_box.setCurrentText(record.get_type())
        self.type_box.setEnabled(False)
        self.date_edit.setDate(QDate(record.date.year, record.date.month, record.date.day))
        self.mileage_edit.setValue(record.mileage)
        self.comment_edit.setText(record.comment)

        if isinstance(record, Refuel):
            self.fuel_box.setCurrentText(record.fuel)
            self.liters_edit.setValue(record.liters)
            self.price_edit.setValue(record.price)
        elif isinstance(record, Repair):
            self.work_edit.setText(record.work)
            self.service_edit.setText(record.service)
            self.cost_edit.setValue(record.price)
        elif isinstance(record, OilChange):
            self.oil_edit.setText(record.oil)
            self.volume_edit.setValue(record.volume)
            self.interval_edit.setValue(record.interval)
            self.cost_edit.setValue(record.price)

    def save(self):
        record_type = self.type_box.currentText()
        record_date = self.date_edit.date().toPython()
        mileage = int(self.mileage_edit.value())
        comment = self.comment_edit.text()

        # если что-то введено неправильно, сеттер выбросит ValueError
        try:
            if record_type == "Заправка":
                self.record = Refuel(self.car, record_date, mileage, self.fuel_box.currentText(),
                                     self.liters_edit.value(), self.price_edit.value(), comment)
            elif record_type == "Ремонт":
                self.record = Repair(self.car, record_date, mileage, self.work_edit.text(),
                                     self.service_edit.text(), self.cost_edit.value(), comment)
            else:
                self.record = OilChange(self.car, record_date, mileage, self.oil_edit.text(),
                                        self.volume_edit.value(), self.cost_edit.value(),
                                        int(self.interval_edit.value()), comment)
        except ValueError as error:
            MessageBox.error(self, str(error))
            return
        self.accept()


class MainWindow(QMainWindow):
    logout = Signal()

    def __init__(self, user, session, garage):
        super().__init__()
        self.user = user
        self.session = session
        self.garage = garage
        self.cars = garage.cars

        self.setWindowTitle("Журнал обслуживания автомобиля")
        self.resize(1050, 680)

        # верхняя строка: выбор машины и пользователь
        self.car_box = ComboBox([str(car) for car in self.cars])
        self.car_box.setMinimumWidth(260)
        logout_button = Button("Выйти")

        top = QHBoxLayout()
        top.addWidget(QLabel("Автомобиль:"))
        top.addWidget(self.car_box)
        top.addStretch()
        top.addWidget(QLabel(f"Пользователь: {user.name}"))
        top.addWidget(logout_button)

        self.summary = SummaryBox()

        # строка с поиском и кнопками
        self.search_edit = LineEdit("Поиск по описанию")
        self.search_edit.setFixedWidth(220)
        self.type_box = ComboBox(["Все записи"] + RECORD_TYPES)
        add_button = AccentButton("Добавить")
        self.edit_button = Button("Изменить")
        self.delete_button = Button("Удалить")

        tools = QHBoxLayout()
        tools.addWidget(self.search_edit)
        tools.addWidget(self.type_box)
        tools.addStretch()
        tools.addWidget(add_button)
        tools.addWidget(self.edit_button)
        tools.addWidget(self.delete_button)

        self.table = RecordsTable()

        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 6)
        layout.setSpacing(10)
        layout.addLayout(top)
        layout.addWidget(self.summary)
        layout.addLayout(tools)
        layout.addWidget(self.table)

        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        self.status = StatusBar(f"Вход: {user.login} в {session.time_in.strftime('%H:%M')}")
        self.setStatusBar(self.status)

        self.car_box.currentIndexChanged.connect(self.update_all)
        self.type_box.currentIndexChanged.connect(self.update_table)
        self.search_edit.textChanged.connect(self.update_table)
        add_button.clicked.connect(self.add_record)
        self.edit_button.clicked.connect(self.edit_record)
        self.delete_button.clicked.connect(self.delete_record)
        self.table.doubleClicked.connect(self.edit_record)
        self.table.delete_pressed.connect(self.delete_record)
        self.table.itemSelectionChanged.connect(self.update_buttons)
        logout_button.clicked.connect(self.logout.emit)

        self.update_all()

    def current_car(self):
        return self.cars[self.car_box.currentIndex()]

    def update_all(self):
        self.update_table()
        self.update_summary()

    def update_table(self):
        record_type = self.type_box.currentText()
        if record_type == "Все записи":
            record_type = ""
        records = self.garage.get_records(self.current_car(), record_type, self.search_edit.text())
        self.table.show_records(records)
        self.update_buttons()

    def update_summary(self):
        car = self.current_car()
        totals = self.garage.get_totals_by_type(car)

        next_change = self.garage.next_oil_change(car)
        if next_change is None:
            oil_text = "нет данных"
        elif next_change > car.mileage:
            oil_text = f"{Utils.km(next_change)} (осталось {Utils.km(next_change - car.mileage)})"
        else:
            oil_text = f"просрочена на {Utils.km(car.mileage - next_change)}"

        self.summary.set_values([
            Utils.money(self.garage.get_total(car)),
            Utils.money(totals.get("Заправка", 0)),
            Utils.money(totals.get("Ремонт", 0)),
            Utils.money(totals.get("Замена масла", 0)),
            oil_text,
        ])

    def update_buttons(self):
        selected = self.table.selected_record() is not None
        self.edit_button.setEnabled(selected)
        self.delete_button.setEnabled(selected)

    def add_record(self):
        dialog = RecordDialog(self.current_car(), parent=self)
        if dialog.exec():
            self.garage.add_record(dialog.record)
            self.update_all()
            self.status.show_message("Запись добавлена")

    def edit_record(self):
        record = self.table.selected_record()
        if record is None:
            return
        dialog = RecordDialog(self.current_car(), record, self)
        if dialog.exec():
            self.garage.replace_record(record, dialog.record)
            self.update_all()
            self.status.show_message("Запись изменена")

    def delete_record(self):
        record = self.table.selected_record()
        if record is None:
            return
        if MessageBox.ask(self, "Удаление", f"Удалить запись?\n{record}"):
            self.garage.remove_record(record)
            self.update_all()
            self.status.show_message("Запись удалена")

    def closeEvent(self, event):
        # при закрытии окна отмечаем время выхода пользователя
        self.session.close()
        event.accept()
