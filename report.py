from datetime import datetime

from models import Entity

TIME_FORMAT = "%d.%m.%Y %H:%M:%S"


class Session(Entity):
    """Один вход пользователя в программу"""

    def __init__(self, login):
        self.login = login
        self._time_in = datetime.now()
        self._time_out = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        if value < self.time_in:
            raise ValueError("Время выхода раньше времени входа")
        self._time_out = value

    def is_open(self):
        return self.time_out is None

    def close(self):
        if self.is_open():
            self.time_out = datetime.now()

    def info(self):
        return f"{self.login}: {self.time_in.strftime(TIME_FORMAT)}"

    def to_row(self):
        time_out = self.time_out.strftime(TIME_FORMAT) if self.time_out else "-"
        return [self.login, self.time_in.strftime(TIME_FORMAT), time_out]

    def __eq__(self, other):
        return isinstance(other, Session) and self.to_row() == other.to_row()

    def __lt__(self, other):
        return self.time_in < other.time_in

    def __gt__(self, other):
        return self.time_in > other.time_in

    def __hash__(self):
        return hash((self.login, self.time_in))

    def __repr__(self):
        return f"Session('{self.login}', {self.time_in!r})"

    def __str__(self):
        return " | ".join(self.to_row())


class Report(Entity):
    """Отчёт о работе программы, сохраняется в файл при закрытии"""

    HEADER = ["login", "time_in", "time_out"]

    def __init__(self, filename):
        self.filename = filename
        self._sessions = []

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def add_session(self, session):
        self._sessions.append(session)

    @staticmethod
    def make_table(rows):
        # ширина каждой колонки по самому длинному значению
        widths = []
        for i in range(len(Report.HEADER)):
            column = [Report.HEADER[i]] + [row[i] for row in rows]
            widths.append(max(len(text) for text in column))

        header = "| " + " | ".join(Report.HEADER[i].center(widths[i]) for i in range(len(widths))) + " |"
        line = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
        border = "+" + "-" * (len(header) - 2) + "+"

        lines = [border, header, line]
        for row in rows:
            lines.append("| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(widths))) + " |")
        lines.append(border)
        return "\n".join(lines) + "\n"

    def save(self):
        if not self._sessions:
            return
        for session in self._sessions:
            session.close()
        rows = [session.to_row() for session in sorted(self._sessions)]
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(Report.make_table(rows))

    def info(self):
        return f"Отчёт {self.filename}, сессий: {len(self)}"

    def __len__(self):
        return len(self._sessions)

    def __eq__(self, other):
        return isinstance(other, Report) and self.filename == other.filename

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __hash__(self):
        return hash(self.filename)

    def __repr__(self):
        return f"Report('{self.filename}')"

    def __str__(self):
        return self.info()
