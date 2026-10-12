import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication, QDialog

from data import TestData
from report import Report, Session
from style import Style
from windows import LoginWindow, MainWindow

REPORT_FILE = Path(__file__).parent / "report.txt"


class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        Style.apply(self.app)

        self.users = TestData.get_users()
        self.garage = TestData.get_garage()
        self.report = Report(REPORT_FILE)
        self.window = None

        # при выходе из программы сохраняем отчет
        self.app.aboutToQuit.connect(self.report.save)

    def login(self):
        dialog = LoginWindow(self.users)
        if dialog.exec() != QDialog.Accepted:
            return False

        session = Session(dialog.user.login)
        self.report.add_session(session)

        self.window = MainWindow(dialog.user, session, self.garage)
        self.window.logout.connect(self.logout)
        self.window.show()
        return True

    def logout(self):
        self.window.session.close()
        self.window.hide()
        if not self.login():
            self.app.quit()

    def run(self):
        if not self.login():
            return 0
        return self.app.exec()


if __name__ == "__main__":
    app = Application()
    sys.exit(app.run())
