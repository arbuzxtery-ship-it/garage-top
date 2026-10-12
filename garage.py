from custom_map import CustomMap
from models import Entity


class Garage(Entity):
    """Хранит машины и все записи по ним"""

    def __init__(self, name):
        self.name = name
        self._cars = []
        self._records = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.strip()

    @property
    def cars(self):
        return sorted(self._cars)

    @property
    def records(self):
        return list(self._records)

    def add_car(self, car):
        if car in self._cars:
            raise ValueError("Такая машина уже есть")
        self._cars.append(car)

    def add_record(self, record):
        self._records.append(record)
        self._update_mileage(record)

    def remove_record(self, record):
        self._records.remove(record)

    def replace_record(self, old, new):
        index = self._records.index(old)
        self._records[index] = new
        self._update_mileage(new)

    def _update_mileage(self, record):
        # пробег машины берём из самой свежей записи
        if record.mileage > record.car.mileage:
            record.car.mileage = record.mileage

    def get_records(self, car, record_type="", text=""):
        result = []
        for record in self._records:
            if record.car != car:
                continue
            if record_type and record.get_type() != record_type:
                continue
            if text and text.lower() not in record.info().lower():
                continue
            result.append(record)
        result.sort(reverse=True)
        return result

    def get_total(self, car, record_type=""):
        total = 0
        for record in self.get_records(car, record_type):
            total += record.get_cost()
        return total

    def get_totals_by_type(self, car):
        totals = CustomMap()
        for record in self.get_records(car):
            totals[record.get_type()] = totals.get(record.get_type(), 0) + record.get_cost()
        return totals

    def next_oil_change(self, car):
        changes = self.get_records(car, "Замена масла")
        if not changes:
            return None
        return changes[0].next_change()

    def info(self):
        return f"{self.name}: машин {len(self._cars)}, записей {len(self._records)}"

    def __len__(self):
        return len(self._records)

    def __contains__(self, item):
        return item in self._cars or item in self._records

    def __eq__(self, other):
        return isinstance(other, Garage) and self.name == other.name

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Garage('{self.name}')"

    def __str__(self):
        return self.info()
