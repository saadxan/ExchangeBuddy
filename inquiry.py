from PyQt5.QtCore import *

import config
from inquiry_artifacts import *


class InquiryCard(QWidget):

    def __init__(self, ticker, period='7d'):
        super(InquiryCard, self).__init__()
        self.ticker = ticker
        self.period = period
        self.chart = StockChart(self.ticker)
        self.info = InfoPiece(self.ticker)
        self.make_inquiry_card()

    def make_inquiry_card(self):
        v_box = QVBoxLayout()
        v_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        h_box = QHBoxLayout()
        h_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        h_box.addWidget(ReturnButton())
        h_box.addWidget(TickerHeader(self.ticker))
        h_box.insertSpacing(2, 1000)
        h_box.addWidget(FavoriteButton(self.ticker))

        v_box.addLayout(h_box)
        v_box.addWidget(QChartView(self.chart))

        h2_box = QHBoxLayout()
        h2_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        h2_box.setSpacing(10)
        h2_box.addWidget(self.info)

        v2_box = QVBoxLayout()
        v2_box.setSpacing(5)
        v2_box.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        v2_box.addWidget(QLabel("a-t\tytd\t1y\t1m\t1w"))
        v2_box.addWidget(PeriodSlider())
        v2_box.insertSpacing(2, 30)
        v2_box.addWidget(QLabel("\t\tVolume\t\t"))
        v2_box.addWidget(AxisDial())
        v2_box.addWidget(QLabel("\tClose\t\tOpen"))
        v2_box.insertSpacing(6, 30)
        v2_box.addWidget(CandlestickToggle())

        h2_box.addLayout(v2_box)

        v_box.addLayout(h2_box)

        self.setLayout(v_box)
