import math

from PyQt5 import QtCore
from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config
import nav
import yfinance as yf


class ReturnButton(QPushButton):

    def __init__(self):
        super(ReturnButton, self).__init__("Return")
        self.clicked.connect(self.return_home)

    def return_home(self):
        nav.return_home()


class TickerHeader(QLabel):

    def __init__(self, ticker):
        super(TickerHeader, self).__init__(ticker)
        self.setFont(QFont("Verdana", 20, QFont.Bold))


class FavoriteButton(QPushButton):

    def __init__(self, ticker):
        super(FavoriteButton, self).__init__()
        self.ticker = ticker
        self.setCheckable(True)
        if self.ticker in config.fav:
            self.setChecked(True)
            self.setText("Unfavorite")
        else:
            self.setChecked(False)
            self.setText("Favorite")
        self.clicked.connect(self.add_remove_favorite)

    def add_remove_favorite(self):
        if not self.isChecked():
            config.fav.remove(self.ticker)
            self.setText("Favorite")
        else:
            if self.ticker not in config.fav:
                config.fav.append(self.ticker)
                self.setText("Unfavorite")


class StockChartView(QChartView):

    def __init__(self, chart):
        super(StockChartView, self).__init__(chart)


class StockChart(QChart):

    def __init__(self, ticker, period='7d', axis='Close'):
        super(StockChart, self).__init__()
        self.header = ticker
        self.ticker = yf.Ticker(ticker)
        self.period = period
        self.axis = axis
        self.candle_status = False
        self.create_chart(period)
        self.legend().hide()
        self.setTitle("{:s} chart of {:s}".format(period.upper(), ticker))

    def create_chart(self, period):
        stock_history = self.ticker.history(period=period)[self.axis]

        prices = stock_history.tolist()
        dates = stock_history.index.tolist()

        series = QLineSeries()

        for date, price in zip(dates, prices):
            series.append((date.timestamp() + 86400) * 1000, price)

        x_date_axis = QDateTimeAxis()
        x_date_axis.setFormat("MM/dd/yyyy")
        x_date_axis.setLabelsAngle(-45)
        series_size = len(series)
        if series_size < 16:
            x_date_axis.setTickCount(series_size)
        else:
            x_date_axis.setTickCount(16)

        y_value_axis = QValueAxis()
        if self.axis != 'Volume':
            y_value_axis.setLabelFormat("$%.2f")
        else:
            y_value_axis.setLabelFormat("%.0f")

        self.addSeries(series)

        self.setAxisX(x_date_axis, series)
        self.setAxisY(y_value_axis, series)

        if self.candle_status:
            self.toggle_candle_series(True)

    def update_chart(self, period, axis):
        self.period = period
        self.axis = axis
        self.setTitle("{:s} chart of {:s}".format(period.upper(), self.header))
        self.removeAllSeries()
        self.removeAxis(self.axisX())
        self.removeAxis(self.axisY())
        self.create_chart(period)

    def toggle_candle_series(self, status):
        if status is True:
            self.candle_status = status
            entries = self.ticker.history(self.period)

            dates = []
            series = CandleStickDay()

            for i in range(len(entries)):
                candle_set = QCandlestickSet()
                candle_set.setLow(entries['Low'][i])
                candle_set.setHigh(entries['High'][i])
                candle_set.setOpen(entries['Open'][i])
                candle_set.setClose(entries['Close'][i])
                candle_set.setTimestamp((entries.index[i].timestamp()))
                series.append(candle_set)
                date = QDateTime.fromMSecsSinceEpoch(((entries.index[i].timestamp() + 86400) * 1000)).toString(
                    "MM/dd/yyyy")
                dates.append(date)

            self.addSeries(series)

            x_bar_axis = QBarCategoryAxis()
            x_bar_axis.setCategories(dates)

            y_value_axis = QValueAxis(series)
            if self.axis != 'Volume':
                y_value_axis.setLabelFormat("$%.2f")
            else:
                y_value_axis.setLabelFormat("%.0f")

            self.setAxisX(x_bar_axis, series)
            self.setAxisY(y_value_axis, series)
            self.removeAxis(self.axisY())
            self.removeAxis(self.axisX())
        else:
            self.candle_status = status
            self.update_chart(self.period, self.axis)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        button_clicked = event.button()
        tick_count = self.axisX().tickCount()

        if button_clicked == 1:
            self.zoom(1.05)
        elif button_clicked == 2:
            self.zoomReset()


class CandleStickDay(QCandlestickSeries):

    def __init__(self):
        super(CandleStickDay, self).__init__()
        self.setIncreasingColor(QColor(0, 200, 0))
        self.setDecreasingColor(QColor(200, 0, 0))
        self.parent_chart = get_this('chart')
        self.hovered.connect(self.action)

    def action(self, hovered, cs):
        if hovered is True:
            date = QDateTime.fromMSecsSinceEpoch((cs.timestamp() + 86400) * 1000).toString("MM/dd/yyyy")
            tool = "{:s}:\nOpen:${:.2f}\nClose:${:.2f}".format(date, cs.open(), cs.close())
            tool += "\nLow:${:.2f}\nHigh:${:.2f}".format(cs.low(), cs.high())
            self.parent_chart.setToolTip(tool)
        else:
            self.parent_chart.setToolTip("")


class InfoPiece(QTableWidget):

    def __init__(self, ticker, period='7d'):
        super(InfoPiece, self).__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ticker = yf.Ticker(ticker)
        self.period = period
        self.info_table = []
        self.update_info(self.period)

    def update_info(self, period):
        self.period = period

        stock_history = self.ticker.history(period=period)

        last = len(stock_history)
        prev_close_price = stock_history.iloc[last - 2]['Close']
        today_open_price = stock_history.iloc[last - 1]['Open']

        low_price = stock_history['Low'].min()
        high_price = stock_history['High'].max()
        avg_price = (stock_history['Open'].mean() + stock_history['Close'].mean()) / 2
        avg_volume = stock_history['Volume'].mean()
        dividends = stock_history['Dividends'].sum()
        dollar_volume = stock_history.iloc[last - 1]['Volume'] * today_open_price
        avg_move = stock_history['Close'].sum() - stock_history['Open'].sum()
        rsi = 100 - (100 / (1 + avg_move))

        self.info_table.append(("Previous Close:", "${:,.2f}".format(prev_close_price)))
        self.info_table.append(("Low - High:", "${:.2f} - ${:,.2f}".format(low_price, high_price)))
        self.info_table.append(("Open:", "${:,.2f}".format(today_open_price)))
        self.info_table.append(("Average Price:", "${:,.2f}".format(avg_price)))
        self.info_table.append(("Dollar Volume:", "${:,.0f}".format(dollar_volume)))
        self.info_table.append(("Average Volume:", "{:,.0f}".format(avg_volume)))
        self.info_table.append(("Dividends:", "{:.2f}".format(dividends)))
        self.info_table.append(("RSI:", "{:.2f}".format(rsi)))

        self.build_table()

    def build_table(self):
        self.horizontalScrollBar().setDisabled(True)
        self.setRowCount(len(self.info_table))
        self.setColumnCount(2)
        self.setColumnWidth(0, 125)
        self.setColumnWidth(1, 175)
        self.setMaximumWidth(300)

        for i in range(self.rowCount()):
            title_value = self.info_table.pop(0)
            self.setItem(i, 0, QTableWidgetItem(title_value[0]))
            self.setItem(i, 1, QTableWidgetItem(title_value[1]))


class PeriodSlider(QSlider):

    def __init__(self):
        super(PeriodSlider, self).__init__(Qt.Orientation.Horizontal)
        self.setFixedSize(230, 30)
        self.setRange(0, 4)
        self.setTickInterval(1)
        self.setValue(4)
        self.valueChanged.connect(self.change_period)

    def change_period(self):
        stock_chart = get_this('chart')
        info_piece = get_this('info')

        cur_value = self.value()
        period = ''
        if cur_value == 0:
            period = 'max'
        elif cur_value == 1:
            period = 'ytd'
        elif cur_value == 2:
            period = '1y'
        elif cur_value == 3:
            period = '30d'
        elif cur_value == 4:
            period = '7d'

        stock_chart.update_chart(period, stock_chart.axis)
        info_piece.update_info(period)


class AxisDial(QDial):

    def __init__(self):
        super(AxisDial, self).__init__()
        self.setFixedSize(QSize(250, 75))
        self.setRange(0, 2)
        self.setNotchesVisible(True)
        self.valueChanged.connect(self.change_axis)

    def change_axis(self):
        stock_chart = get_this('chart')

        cur_value = self.value()
        axis = ''
        if cur_value == 0:
            axis = 'Close'
        elif cur_value == 1:
            axis = 'Volume'
        elif cur_value == 2:
            axis = 'Open'

        stock_chart.update_chart(stock_chart.period, axis)


class CandlestickToggle(QPushButton):

    def __init__(self):
        super(CandlestickToggle, self).__init__("Show Candlesticks")
        self.setFixedSize(QSize(250, 50))
        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(self.toggle_candles)

    def toggle_candles(self):
        stock_chart = get_this('chart')

        if self.isChecked():
            stock_chart.toggle_candle_series(True)
            self.setText("Hide Candlesticks")
        else:
            stock_chart.toggle_candle_series(False)
            self.setText("Show Candlesticks")


def get_this(item='chart' or 'info'):
    if hasattr(config.stk.widget(1), item):
        return getattr(config.stk.widget(1), item)
    else:
        return getattr(config.stk.widget(2), item)
