from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import csv, config

from inquiry import *


class ExploreBar(QLineEdit):

    def __init__(self):
        super(ExploreBar, self).__init__()
        self.setPlaceholderText("Type & Press Enter")
        rec = TickerCompleter()
        self.setCompleter(rec)
        self.textEdited.connect(self.to_uppercase)
        self.returnPressed.connect(self.execute_explore)


    def to_uppercase(self):
        self.setText(self.text().upper())

    def execute_explore(self):
        try:
            ticker_inquiry = InquiryCard(self.text())
        except IndexError:
            bad_ticker_message = QErrorMessage()
            bad_ticker_message.showMessage("Ticker {:s} does not exist.".format(self.text()))
            bad_ticker_message.exec_()
            self.clear()
            return

        self.clear()

        config.stk.insertWidget(1, ticker_inquiry)
        config.stk.setCurrentIndex(1)



class TickerCompleter(QCompleter):

    def __init__(self):
        super(TickerCompleter, self).__init__()
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.set_type()

    def set_type(self):
        with open('tickers_dataset.csv', 'rU') as f:
            reader = csv.DictReader(f)
            data = {}

            for row in reader:
                for head, info in row.items():
                    try:
                        data[head].append(info)
                    except KeyError:
                        data[head] = [info]

        self.setModel(QStringListModel(data['Symbol']))


