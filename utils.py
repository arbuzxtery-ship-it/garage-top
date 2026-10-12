class Utils:
    """Вспомогательные функции для вывода чисел и дат"""

    @staticmethod
    def money(value):
        # 1234.5 -> "1 234,50 ₽"
        text = f"{value:,.2f}".replace(",", " ").replace(".", ",")
        return text + " ₽"

    @staticmethod
    def km(value):
        return f"{value:,}".replace(",", " ") + " км"

    @staticmethod
    def date_to_str(value):
        return value.strftime("%d.%m.%Y")
