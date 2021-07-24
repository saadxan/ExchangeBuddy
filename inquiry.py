import random

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

import inquiry_artifacts as inquiry_gui


class InquiryCard(QtWidgets.QFrame):

    def __init__(self, ticker, period='7d'):
        super(InquiryCard, self).__init__()
        image = "images/mesh" + str(random.randint(1, 5)) + ".jpg"
        style = "InquiryCard{" + "border-image: url({:s});".format(image) + "}"
        self.setStyleSheet(style)
        self.ticker = ticker
        self.period = period
        self.chart = inquiry_gui.StockChart(self.ticker)
        self.info = inquiry_gui.InfoPiece(self.ticker)
        self.make_inquiry_card()

    def make_inquiry_card(self):
        v_box = QtWidgets.QVBoxLayout()
        v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        h_box = QtWidgets.QHBoxLayout()
        h_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        h_box.addWidget(inquiry_gui.ReturnButton())
        h_box.addWidget(inquiry_gui.TickerHeader(self.ticker))
        h_box.insertSpacing(2, 1000)
        h_box.addWidget(inquiry_gui.HelpButton())
        h_box.addWidget(inquiry_gui.NotesButton(self.ticker))
        h_box.addWidget(inquiry_gui.FavoriteButton(self.ticker))

        v_box.addLayout(h_box)
        v_box.addWidget(inquiry_gui.StockChartView(self.chart))

        h2_box = QtWidgets.QHBoxLayout()
        h2_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignLeft)
        h2_box.setSpacing(10)
        h2_box.addWidget(self.info)

        v2_box = QtWidgets.QVBoxLayout()
        v2_box.setSpacing(0)
        v2_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
        v2_box.addWidget(QtWidgets.QLabel("a-t\tytd\t1y\t1m\t1w"))
        v2_box.addWidget(inquiry_gui.PeriodSlider())
        v2_box.insertSpacing(2, 30)
        v2_box.addWidget(QtWidgets.QLabel("\t\tVolume\t\t"))
        v2_box.addWidget(inquiry_gui.AxisDial())
        v2_box.addWidget(QtWidgets.QLabel("\tClose\t\tOpen"))
        v2_box.insertSpacing(6, 30)
        v2_box.addWidget(inquiry_gui.CandlestickToggle())

        h2_box.addLayout(v2_box)

        v_box.addLayout(h2_box)

        self.setLayout(v_box)