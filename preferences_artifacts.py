import config
import csv
import nav

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class FullHelpButton(QPushButton):

    def __init__(self):
        super(FullHelpButton, self).__init__("Help")
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.help_dialog = QTextEdit()
        self.help_dialog.setStyleSheet('''QTextEdit{border-image: url(bg.jpg);}''')
        self.help_dialog.setMinimumWidth(700)
        self.help_dialog.setReadOnly(True)
        text = "Hub:\t-Click ticker in a list to open its inquiry.\n\t-Customize your favorites per preference.\n\n\n"
        text += "Inquiry:\t-Use slide to manipulate chart to different periods (1w, 1m, ytd, 1y, a-t) real time.\n"
        text += "\t-Use knob to change axis & line dimension to different parameters (open, volume, close) real time.\n"
        text += "\t-Use button to toggle candle-lights representations for days (allowed for all periods except a-t).\n"
        text += "\t-Hover over candle-light w/ mouse for expressions (the appropriate Date, Open, Close, High, Low).\n"
        text += "\t-Calculations on stock (Low-High, Avg.Price, Avg.Volume, RSI, Dividends) will modify accordingly.\n"
        text += "\t-Use mouse wheel (up/down) to zoom (in/out) respectively & right-click on graph to reset the zoom.\n"
        text += "\t-Favorite/Unfavorite button can be clicked to add/remove the stock from user's favorite list.\n\n\n"
        text += "Explore:\t-Type in bar & get suggestions from cache of exact tickers & press ENTER key for analysis.\n"
        text += "\t-Filter w/ combination of explore parameters (Sector, Country, Market Cap Min.) for stocks query.\n"
        text += "\t-Use explore button to execute query conforming to selected parameters.\n"
        text += "\t-Note that ENTER key opens analysis on typed ticker in bar whereas explore button executes query.\n"
        text += "\t-If no stocks can be found for filtered parameters, a message will be displayed.\n"
        text += "\t-For best explore queries, enter American stocks as 80%+ of companies on NASDAQ based in US.\n\n\n"
        self.help_dialog.setText(text)
        self.clicked.connect(self.show_help_dialog)

    def show_help_dialog(self):
        self.help_dialog.show()


class ResetButton(QPushButton):

    def __init__(self):
        super(ResetButton, self).__init__("Reset")
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.clicked.connect(self.reset_action)

    def reset_action(self):
        yes_or_no = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        details = "This will erase everything to default.\nRemoving favorite tickers and wiping notes."
        pick = QMessageBox.question(self, "Confirm", "Reset to default preferences?\n" + details, yes_or_no)
        if pick == QMessageBox.StandardButton.Yes:
            config.fav = ['TSLA']
            config.notes = {'TSLA': 'Good nice.  It should go up.'}
            config.notes['AMZN'] = 'RSI(7): 51.01\nNot so favorable 7/5/2021\nProjected 5 point growth 3Q.\n'
            nav.refresh_home()






