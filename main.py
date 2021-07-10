import config
import sys

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

import explore_artifacts as explore_gui
import hub_artifacts as hub_gui
import preferences_artifacts as preferences_gui


class StackDriver(QtWidgets.QStackedWidget):

    def __init__(self):
        super(StackDriver, self).__init__()
        self.setWindowTitle("ExchangeBuddy")
        self.setFixedSize(1280, 720)


class MainTab(QtWidgets.QTabWidget):

    def __init__(self):
        super(MainTab, self).__init__()
        self.hub_tab = QtWidgets.QWidget()
        self.explore_tab = QtWidgets.QWidget()
        self.preferences_tab = QtWidgets.QWidget()
        self.hub_box = QtWidgets.QVBoxLayout()
        self.h_box = QtWidgets.QHBoxLayout()
        self.h2_box = QtWidgets.QHBoxLayout()
        self.h3_box = QtWidgets.QHBoxLayout()
        self.v_box = QtWidgets.QVBoxLayout()
        self.create_hub_tab()
        self.explore_form = QtWidgets.QFormLayout()
        self.create_explore_tab()
        self.preferences_form = QtWidgets.QFormLayout()
        self.create_preferences_tab()

    def create_hub_tab(self):
        self.hub_box.setSpacing(10)

        self.h_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.h_box.addWidget(hub_gui.ExitButton())
        self.h_box.addWidget(hub_gui.RefreshButton())

        self.h2_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.h2_box.setSpacing(20)
        self.h2_box.addWidget(hub_gui.StockListLabel("Market Indices"))
        self.h2_box.addWidget(hub_gui.StockListLabel("Tech"))
        self.h2_box.addWidget(hub_gui.StockListLabel("Favorites"))

        self.h3_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self.h3_box.setSpacing(20)
        self.h3_box.addWidget(hub_gui.StockList(['^DJI', '^GSPC', '^IXIC', '^RUT']))
        self.h3_box.addWidget(hub_gui.StockList(['IBM', 'AMZN', 'INTC', 'AMD', 'CRM', 'CSCO', 'ADBE', 'PLTR']))
        self.h3_box.addWidget(hub_gui.StockList(config.fav))

        self.v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignRight)
        self.v_box.setSpacing(10)
        self.v_box.addWidget(QtWidgets.QLabel("Access Notes:"))
        self.v_box.addWidget(hub_gui.NotesSelector())

        self.h3_box.addLayout(self.v_box)
        self.hub_box.addLayout(self.h_box)
        self.hub_box.addLayout(self.h2_box)
        self.hub_box.addLayout(self.h3_box)

        self.hub_tab.setLayout(self.hub_box)
        self.addTab(self.hub_tab, "Hub")

    def create_explore_tab(self):
        self.explore_form.addWidget(QtWidgets.QLabel("Explore By Ticker:"))
        self.explore_form.addWidget(explore_gui.ExploreBar(0))
        self.explore_form.addWidget(QtWidgets.QLabel("\n\n\n"))

        explore_apparatus = explore_gui.ExploreApparatus()

        self.explore_form.addWidget(QtWidgets.QLabel("Filter Sector:"))
        self.explore_form.addWidget(explore_apparatus.sector_combo)
        self.explore_form.addWidget(QtWidgets.QLabel("Filter Country:"))
        self.explore_form.addWidget(explore_apparatus.country_combo)
        self.explore_form.addWidget(QtWidgets.QLabel("Filter Min Market Cap:"))
        explore_apparatus.cap_buttons.setParent(self.explore_form)
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(0))
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(1))
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(2))
        self.explore_form.addWidget(explore_apparatus.cap_buttons.button(3))

        self.explore_form.addWidget(explore_gui.ExploreButton())

        self.explore_tab.setLayout(self.explore_form)
        self.addTab(self.explore_tab, "Explore")

    def create_preferences_tab(self):
        self.preferences_form.addWidget(preferences_gui.FullHelpButton())
        self.preferences_form.addWidget(QtWidgets.QLabel("\n\n\n"))
        self.preferences_form.addWidget(preferences_gui.ResetButton())

        self.preferences_tab.setLayout(self.preferences_form)
        self.addTab(self.preferences_tab, "Preferences")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    win.setStyleSheet('''QMainWindow{border-image: url(bg.jpg);}''')
    win.setCentralWidget(MainTab())
    config.stk = StackDriver()
    config.stk.insertWidget(0, win)
    config.stk.setCurrentIndex(0)
    config.stk.show()
    sys.exit(app.exec_())
