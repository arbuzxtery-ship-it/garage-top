from abc import ABC, abstractmethod
from datetime import date

from utils import Utils


class Entity(ABC):
    """Абстрактный класс, от него наследуются все классы программы"""

    @abstractmethod
    def info(self):
        pass


class Car(Entity):
    def __init__(self, brand, model, year, number, mileage):
        self.brand = brand
        self.model = model
        self.year = year
        self.number = number
        self.mileage = mileage

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value):
        if not value.strip():
            raise ValueError("Марка не может быть пустой")
        self._brand = value.strip()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if not value.strip():
            raise ValueError("Модель не может быть пустой")
        self._model = value.strip()

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if value < 1950 or value > date.today().year:
            raise ValueError("Неправильный год выпуска")
        self._year = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not value.strip():
            raise ValueError("Госномер не может быть пустым")
        self._number = value.strip().upper()

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        if value < 0:
            raise ValueError("Пробег не может быть отрицательным")
        self._mileage = int(value)

    def info(self):
        return f"{self.year} г., {self.number}, пробег {Utils.km(self.mileage)}"

    def __eq__(self, other):
        return isinstance(other, Car) and self.number == other.number

    def __lt__(self, other):
        return (self.brand, self.model) < (other.brand, other.model)

    def __gt__(self, other):
        return (self.brand, self.model) > (other.brand, other.model)

    def __hash__(self):
        return hash(self.number)

    def __repr__(self):
        return f"Car('{self.brand}', '{self.model}', {self.year}, '{self.number}', {self.mileage})"

    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"


class ServiceRecord(Entity):
    """Общий класс для записей (заправка, ремонт, замена масла)"""

    def __init__(self, car, record_date, mileage, comment=""):
        self.car = car
        self.date = record_date
        self.mileage = mileage
        self.comment = comment

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, value):
        if not isinstance(value, Car):
            raise ValueError("Не выбран автомобиль")
        self._car = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if value > date.today():
            raise ValueError("Дата не может быть в будущем")
        self._date = value

    @property
    def mileage(self):
        return self._mileage

    @mileage.setter
    def mileage(self, value):
        if value <= 0:
            raise ValueError("Укажите пробег")
        self._mileage = int(value)

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value):
        self._comment = value.strip()

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_cost(self):
        pass

    @abstractmethod
    def get_details(self):
        pass

    def info(self):
        if self.comment:
            return f"{self.get_details()} ({self.comment})"
        return self.get_details()

    def _key(self):
        return (self.date, self.mileage, self.get_type(), self.get_cost(), self.car.number)

    def __eq__(self, other):
        return isinstance(other, ServiceRecord) and self._key() == other._key()

    # сначала по дате, потом по пробегу
    def __lt__(self, other):
        return (self.date, self.mileage) < (other.date, other.mileage)

    def __gt__(self, other):
        return (self.date, self.mileage) > (other.date, other.mileage)

    def __hash__(self):
        return hash(self._key())

    def __str__(self):
        return f"{Utils.date_to_str(self.date)} {self.get_type()} {Utils.money(self.get_cost())}"


class Refuel(ServiceRecord):
    FUELS = ["АИ-92", "АИ-95", "АИ-98", "ДТ"]

    def __init__(self, car, record_date, mileage, fuel, liters, price, comment=""):
        super().__init__(car, record_date, mileage, comment)
        self.fuel = fuel
        self.liters = liters
        self.price = price

    @property
    def fuel(self):
        return self._fuel

    @fuel.setter
    def fuel(self, value):
        if value not in Refuel.FUELS:
            raise ValueError("Неизвестный вид топлива")
        self._fuel = value

    @property
    def liters(self):
        return self._liters

    @liters.setter
    def liters(self, value):
        if value <= 0:
            raise ValueError("Количество литров должно быть больше нуля")
        self._liters = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Цена за литр должна быть больше нуля")
        self._price = value

    def get_type(self):
        return "Заправка"

    def get_cost(self):
        return round(self.liters * self.price, 2)

    def get_details(self):
        liters = f"{self.liters:g}".replace(".", ",")
        return f"{self.fuel}, {liters} л по {Utils.money(self.price)}"

    def __repr__(self):
        return f"Refuel('{self.car.number}', '{self.date}', {self.mileage}, '{self.fuel}', {self.liters}, {self.price})"


class Repair(ServiceRecord):
    def __init__(self, car, record_date, mileage, work, service, price, comment=""):
        super().__init__(car, record_date, mileage, comment)
        self.work = work
        self.service = service
        self.price = price

    @property
    def work(self):
        return self._work

    @work.setter
    def work(self, value):
        if not value.strip():
            raise ValueError("Напишите, что было сделано")
        self._work = value.strip()

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        if not value.strip():
            raise ValueError("Укажите сервис")
        self._service = value.strip()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Стоимость должна быть больше нуля")
        self._price = value

    def get_type(self):
        return "Ремонт"

    def get_cost(self):
        return self.price

    def get_details(self):
        return f"{self.work}, {self.service}"

    def __repr__(self):
        return f"Repair('{self.car.number}', '{self.date}', {self.mileage}, '{self.work}', {self.price})"


class OilChange(ServiceRecord):
    def __init__(self, car, record_date, mileage, oil, volume, price, interval=10000, comment=""):
        super().__init__(car, record_date, mileage, comment)
        self.oil = oil
        self.volume = volume
        self.price = price
        self.interval = interval

    @property
    def oil(self):
        return self._oil

    @oil.setter
    def oil(self, value):
        if not value.strip():
            raise ValueError("Укажите масло")
        self._oil = value.strip()

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        if value <= 0:
            raise ValueError("Объём масла должен быть больше нуля")
        self._volume = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Стоимость должна быть больше нуля")
        self._price = value

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        if value < 1000:
            raise ValueError("Интервал замены не может быть меньше 1000 км")
        self._interval = int(value)

    def next_change(self):
        return self.mileage + self.interval

    def get_type(self):
        return "Замена масла"

    def get_cost(self):
        return self.price

    def get_details(self):
        volume = f"{self.volume:g}".replace(".", ",")
        return f"{self.oil}, {volume} л, следующая на {Utils.km(self.next_change())}"

    def __repr__(self):
        return f"OilChange('{self.car.number}', '{self.date}', {self.mileage}, '{self.oil}', {self.price})"


class User(Entity):
    def __init__(self, login, password, name):
        self.login = login
        self.password = password
        self.name = name

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        if not value.strip():
            raise ValueError("Логин не может быть пустым")
        self._login = value.strip().lower()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if len(value) < 4:
            raise ValueError("Пароль должен быть не короче 4 символов")
        self._password = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip()

    def check_password(self, password):
        return self.password == password

    def info(self):
        return f"{self.name} ({self.login})"

    def __eq__(self, other):
        return isinstance(other, User) and self.login == other.login

    def __lt__(self, other):
        return self.login < other.login

    def __gt__(self, other):
        return self.login > other.login

    def __hash__(self):
        return hash(self.login)

    def __repr__(self):
        return f"User('{self.login}', '{self.name}')"

    def __str__(self):
        return self.name
