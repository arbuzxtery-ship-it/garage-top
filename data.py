from datetime import date

from custom_map import CustomMap
from garage import Garage
from models import Car, OilChange, Refuel, Repair, User


class TestData:
    """Начальные данные, чтобы при запуске таблица не была пустой"""

    @staticmethod
    def get_users():
        users = CustomMap()
        for user in [User("admin", "admin", "Администратор"), User("student", "oop2026", "Студент")]:
            users[user.login] = user
        return users

    @staticmethod
    def get_garage():
        garage = Garage("Мой гараж")

        camry = Car("Toyota", "Camry", 2018, "А123ВС777", 80000)
        rio = Car("Kia", "Rio", 2020, "Е456КХ199", 55000)
        vesta = Car("Lada", "Vesta", 2021, "М789ОР750", 30000)
        garage.add_car(camry)
        garage.add_car(rio)
        garage.add_car(vesta)

        records = [
            Repair(camry, date(2026, 7, 2), 80900, "Замена тормозных колодок", "АвтоТех", 7500),
            OilChange(camry, date(2026, 8, 20), 82400, "Mobil 1 5W-30", 4.5, 6800),
            Refuel(camry, date(2026, 9, 12), 83100, "АИ-95", 45, 56.40),
            Refuel(camry, date(2026, 9, 28), 84200, "АИ-95", 50, 56.90, "перед поездкой на дачу"),
            Refuel(camry, date(2026, 10, 5), 84500, "АИ-95", 38.5, 57.10),

            OilChange(rio, date(2026, 5, 1), 52000, "Shell Helix 5W-40", 4, 4900),
            Repair(rio, date(2026, 6, 18), 55300, "Замена аккумулятора", "Bosch Service", 9200),
            Refuel(rio, date(2026, 9, 14), 60400, "АИ-92", 40, 52.30),
            Refuel(rio, date(2026, 10, 7), 61200, "АИ-92", 42, 52.80),

            OilChange(vesta, date(2026, 3, 10), 30100, "Лукойл Genesis 5W-40", 4.4, 3600, 8000),
            Refuel(vesta, date(2026, 9, 22), 38300, "АИ-92", 35, 52.10),
            Repair(vesta, date(2026, 9, 30), 38900, "Замена лампы ближнего света", "Гаражный сервис", 1200),
        ]
        for record in records:
            garage.add_record(record)
        return garage
