import config
import sys

from PyQt5.QtWidgets import *

from explore_artifacts import *
from hub_artifacts import *


class StackDriver(QStackedWidget):

    def __init__(self):
        super(StackDriver, self).__init__()
        self.setWindowTitle("ExchangeBuddy")
        self.setFixedSize(1280, 720)


class MainTab(QTabWidget):

    def __init__(self):
        super(MainTab, self).__init__()
        self.hub_tab, self.explore_tab, self.preferences_tab = QWidget(), QWidget(), QWidget()
        self.hub_box, self.h_box, self.h2_box, self.h3_box = QVBoxLayout(), QHBoxLayout(), QHBoxLayout(), QHBoxLayout()
        self.create_hub_tab()
        self.explore_form = QFormLayout()
        self.create_explore_tab()
        self.create_preferences_tab()

    def create_hub_tab(self):
        self.hub_box.setSpacing(10)

        self.h_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.h_box.addWidget(ExitButton())
        self.h_box.addWidget(RefreshButton())

        self.h2_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.h2_box.setSpacing(20)
        self.h2_box.addWidget(StockListLabel("Market Indices"))
        self.h2_box.addWidget(StockListLabel("Tech"))
        self.h2_box.addWidget(StockListLabel("Favorites"))

        self.h3_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.h3_box.setSpacing(20)
        self.h3_box.addWidget(StockList(['^DJI', '^GSPC', '^IXIC', '^RUT']))
        self.h3_box.addWidget(StockList(['MSFT', 'AAPL', 'IBM', 'AMZN', 'INTC', 'AMD', 'CRM', 'CSCO', 'ADBE', 'PLTR']))
        self.h3_box.addWidget(StockList(config.fav))

        self.hub_box.addLayout(self.h_box)
        self.hub_box.addLayout(self.h2_box)
        self.hub_box.addLayout(self.h3_box)

        self.hub_tab.setLayout(self.hub_box)

        self.addTab(self.hub_tab, "Hub")

    def create_explore_tab(self):
        self.explore_form.addWidget(QLabel("Explore By Ticker:"))
        self.explore_form.addWidget(ExploreBar(0))
        self.explore_form.addWidget(QLabel("\n\n\n"))

        explore_apparatus = ExploreApparatus()


        self.explore_form.addWidget(QLabel("Filter Sector:"))
        self.explore_form.addWidget(explore_apparatus.sector_combo)
        self.explore_form.addWidget(QLabel("Filter Country:"))
        self.explore_form.addWidget(explore_apparatus.country_combo)
        self.explore_form.addWidget(QLabel("Filter Min Market Cap:"))
        explore_apparatus.cap_buttons.setParent(self.explore_form)
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(0))
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(1))
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(2))
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(3))

        self.explore_form.addWidget(ExploreButton())

        self.explore_tab.setLayout(self.explore_form)

        self.addTab(self.explore_tab, "Explore")

    def create_preferences_tab(self):
        self.addTab(QWidget(), "Preferences")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setStyleSheet('''QMainWindow{border-image: url(bg.jpg);}''')
    win.setCentralWidget(MainTab())
    config.stk = StackDriver()
    config.stk.insertWidget(0, win)
    config.stk.setCurrentIndex(0)
    config.stk.show()
    sys.exit(app.exec_())
