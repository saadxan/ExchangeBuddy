from PyQt5.QtChart import *
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import config
import nav
import yfinance as yf


class ReturnButton(QtWidgets.QPushButton):

    def __init__(self):
        super(ReturnButton, self).__init__("Return")
        self.clicked.connect(self.return_home)

    def return_home(self):
        nav.return_home()


class TickerHeader(QtWidgets.QLabel):

    def __init__(self, ticker):
        super(TickerHeader, self).__init__(ticker)
        self.setFont(QtGui.QFont("Verdana", 20, QtGui.QFont.Bold))


class HelpButton(QtWidgets.QPushButton):

    def __init__(self):
        super(HelpButton, self).__init__("Help")
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.help_dialog = QtWidgets.QTextEdit()
        self.help_dialog.setStyleSheet('''QTextEdit{border-image: url(bg.jpg);}''')
        self.help_dialog.setMinimumWidth(700)
        self.help_dialog.setReadOnly(True)
        text = "Inquiry:\t-Use slide to manipulate chart to different periods (1w, 1m, ytd, 1y, a-t) real time.\n"
        text += "\t-Use knob to change axis & line dimension to different parameters (open, volume, close) real time.\n"
        text += "\t-Use button to toggle candle-lights representations for days (allowed for all periods except a-t).\n"
        text += "\t-Hover over candle-light w/ mouse for expressions (the appropriate Date, Open, Close, High, Low).\n"
        text += "\t-Calculations on stock (Low-High, Avg.Price, Avg.Volume, RSI, Dividends) will modify accordingly.\n"
        text += "\t-Use mouse wheel (up/down) to zoom (in/out) respectively & right-click on graph to reset the zoom.\n"
        text += "\t-Favorite/Unfavorite button can be clicked to add/remove the stock from user's favorite list.\n"
        self.help_dialog.setText(text)
        self.clicked.connect(self.show_help_dialog)

    def show_help_dialog(self):
        self.help_dialog.show()


class NotesButton(QtWidgets.QPushButton):

    def __init__(self, ticker):
        super(NotesButton, self).__init__("Notes")
        self.ticker = ticker
        self.notes_editor = QtWidgets.QTextEdit()
        self.notes_editor.setStyleSheet('''QTextEdit{border-image: url(bg.jpg);}''')
        self.notes_editor.closeEvent = self.save_notes_action
        self.clicked.connect(self.open_notes_action)

    def open_notes_action(self):
        if self.ticker in config.notes.keys():
            self.notes_editor.setText(config.notes[self.ticker])
        self.notes_editor.show()

    def save_notes_action(self, a0: QtGui.QCloseEvent):
        notes = self.notes_editor.toPlainText()
        if notes != "":
            config.notes[self.ticker] = notes
        nav.refresh_home()


class FavoriteButton(QtWidgets.QPushButton):

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

    def validate_move(self):
        min_val = self.chart().axisX().min()
        true_min = self.chart().initial_range[0]
        if min_val < true_min:
            self.chart().axisX().setMin(true_min)
            return False

        max_val = self.chart().axisX().max()
        true_max = self.chart().initial_range[1]

        if max_val > true_max:
            self.chart().axisX().setMax(true_max)
            return False

        return True

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if a0.angleDelta().y() > 0:
            if self.validate_move() is True:
                self.zoom_action(1.01, a0.pos().x() - self.chart().plotArea().x())

        elif a0.angleDelta().y() < 0 and type(self.chart().axisX().min()) is not str:
            if self.validate_move() is True:
                self.zoom_action(0.99, a0.pos().x() - self.chart().plotArea().x())

    def zoom_action(self, matrix, midpoint):
        plot_area = self.chart().plotArea()

        width = plot_area.width()
        plot_area.setWidth(float(width / matrix))
        mid_matrix = float(midpoint / width)

        left_move_factor = midpoint - (plot_area.width() * mid_matrix)
        plot_area.moveLeft(plot_area.x() + left_move_factor)
        self.chart().zoomIn(plot_area)

    def mousePressEvent(self, event):
        if event.button() == 2:
            self.chart().zoomReset()
            self.validate_move()


class StockChart(QChart):

    def __init__(self, ticker, period='7d', axis='Close'):
        super(StockChart, self).__init__()
        self.header = ticker
        self.ticker = yf.Ticker(ticker)
        self.period = period
        self.axis = axis
        self.candle_status = False
        self.initial_range = None
        self.entry_amount = 0
        self.create_chart(period)
        self.legend().hide()
        self.setTheme(QChart.ChartThemeBlueCerulean)
        self.setMinimumHeight(375)
        self.setTitle("{:s} chart of {:s}".format(period.upper(), ticker))
        self.axisX().setLabelsFont(QtGui.QFont("Verdana", 10))
        self.axisY().setLabelsFont(QtGui.QFont("Verdana", 10))

    def create_chart(self, period):
        stock_history = self.ticker.history(period=period)[self.axis]

        prices = stock_history.tolist()
        dates = stock_history.index.tolist()

        series = QLineSeries()

        for date, price in zip(dates, prices):
            series.append((date.timestamp() + 86400) * 1000, price)

        self.entry_amount = len(series)

        x_date_axis = QDateTimeAxis()
        x_date_axis.setFormat("MM/dd/yyyy")
        x_date_axis.setLabelsAngle(-45)

        if len(series) < 16:
            x_date_axis.setTickCount(len(series))
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

        self.initial_range = (self.axisX().min(), self.axisX().max())

        if period == 'max':
            self.candle_status = False

        if self.candle_status:
            self.toggle_candle_series(True)

        self.axisX().setLabelsFont(QtGui.QFont("Verdana", 10))
        self.axisY().setLabelsFont(QtGui.QFont("Verdana", 10))

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
                off = 86400
                date = QtCore.QDateTime.fromSecsSinceEpoch((entries.index[i].timestamp() + off)).toString("MM/dd/yyyy")
                dates.append(CandleDayString(date))

            self.entry_amount = len(dates)

            x_bar_axis = QBarCategoryAxis()
            x_bar_axis.setCategories(dates)
            x_bar_axis.setGridLineVisible(False)
            if self.entry_amount < 30:
                x_bar_axis.setLabelsAngle(-45)
            else:
                x_bar_axis.setLabelsAngle(-90)

            y_value_axis = QValueAxis(series)
            if self.axis != 'Volume':
                y_value_axis.setLabelFormat("$%.2f")
            else:
                y_value_axis.setLabelFormat("%.0f")

            self.addSeries(series)
            self.setAxisX(x_bar_axis, series)
            self.setAxisY(y_value_axis, series)
            self.removeAxis(self.axisY())
            self.removeAxis(self.axisX())
            self.initial_range = (self.axisX().min(), self.axisX().max())

            self.axisX().setLabelsFont(QtGui.QFont("Verdana", 10))
            self.axisY().setLabelsFont(QtGui.QFont("Verdana", 10))
        else:
            self.candle_status = status
            self.update_chart(self.period, self.axis)


class CandleDayString(str):

    def __new__(cls, *args, **kwargs):
        return str.__new__(cls, *args, **kwargs)

    def __eq__(self, x: str) -> bool:
        return QtCore.QDateTime.fromString(self, "MM/dd/yyyy") == QtCore.QDateTime.fromString(str(x), "MM/dd/yyyy")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, x: str) -> bool:
        return QtCore.QDateTime.fromString(self, "MM/dd/yyyy") < QtCore.QDateTime.fromString(str(x), "MM/dd/yyyy")

    def __gt__(self, x: str) -> bool:
        return not self.__lt__(x)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)


class CandleStickDay(QCandlestickSeries):

    def __init__(self):
        super(CandleStickDay, self).__init__()
        self.setIncreasingColor(QtGui.QColor(0, 200, 0))
        self.setDecreasingColor(QtGui.QColor(200, 0, 0))
        self.parent_chart = get_this('chart')
        self.hovered.connect(self.action)

    def action(self, hovered, cs):
        if hovered is True:
            date = QtCore.QDateTime.fromMSecsSinceEpoch((cs.timestamp() + 86400) * 1000).toString("MM/dd/yyyy")
            tool = "{:s}:\nOpen:${:.2f}\nClose:${:.2f}".format(date, cs.open(), cs.close())
            tool += "\nLow:${:.2f}\nHigh:${:.2f}".format(cs.low(), cs.high())
            self.parent_chart.setToolTip(tool)
        else:
            self.parent_chart.setToolTip("")


class InfoPiece(QtWidgets.QTableWidget):

    def __init__(self, ticker, period='7d'):
        super(InfoPiece, self).__init__()
        self.setSizeAdjustPolicy(QtWidgets.QTableWidget.AdjustToContentsOnFirstShow)
        self.setStyleSheet('''InfoPiece{background-color: lightsteelblue;}
                            InfoPiece QTableCornerButton::section{background-color: lightsteelblue;}''')
        self.horizontalHeader().setStyleSheet("background-color: lightsteelblue;")
        self.verticalHeader().setStyleSheet("background-color: lightsteelblue;")
        self.setShowGrid(False)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ticker_symbol = ticker
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

        avg_up = []
        avg_down = []
        for entry_close, entry_open in zip(list(stock_history['Close']), list(stock_history['Open'])):
            move = entry_close - entry_open
            if move >= 0:
                avg_up.append(move)
            else:
                avg_down.append(move)
        avg_gain = sum(avg_up) / len(avg_up)
        avg_loss = sum(avg_down) / len(avg_down)
        rsi = 100 - (100 / (1 + (avg_gain / abs(avg_loss))))

        self.info_table.append(("Previous Close:", "${:,.2f}".format(prev_close_price)))
        self.info_table.append(("Low - High:", "${:,.2f} - ${:,.2f}".format(low_price, high_price)))
        self.info_table.append(("Open:", "${:,.2f}".format(today_open_price)))
        self.info_table.append(("Average Price:", "${:,.2f}".format(avg_price)))
        self.info_table.append(("Dollar Volume:", "${:,.0f}".format(dollar_volume)))
        self.info_table.append(("Average Volume:", "{:,.0f}".format(avg_volume)))
        self.info_table.append(("RSI({:d}):".format(last), "{:.2f}".format(rsi)))
        self.info_table.append(("Dividends:", "{:.2f}".format(dividends)))

        self.build_table()

    def build_table(self):
        self.horizontalScrollBar().setDisabled(True)
        self.setRowCount(len(self.info_table))
        self.setColumnCount(1)
        self.setColumnWidth(0, 200)
        self.setMaximumWidth(310)
        self.setMaximumHeight(240)
        self.setHorizontalHeaderLabels(["{:s} Stats".format(self.ticker_symbol)])

        for i in range(self.rowCount()):
            title_value = self.info_table.pop(0)
            self.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(title_value[0]))
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(title_value[1]))


class PeriodSlider(QtWidgets.QSlider):

    def __init__(self):
        super(PeriodSlider, self).__init__(QtCore.Qt.Orientation.Horizontal)
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


class AxisDial(QtWidgets.QDial):

    def __init__(self):
        super(AxisDial, self).__init__()
        self.setFixedSize(QtCore.QSize(250, 75))
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


class CandlestickToggle(QtWidgets.QPushButton):

    def __init__(self):
        super(CandlestickToggle, self).__init__("Show Candlesticks")
        self.setFixedSize(QtCore.QSize(250, 50))
        self.setCheckable(True)
        self.setChecked(False)
        self.clicked.connect(self.toggle_candles)

    def toggle_candles(self):
        stock_chart = get_this('chart')

        if stock_chart.period == 'max':
            self.setChecked(False)

        if not self.isChecked():
            stock_chart.toggle_candle_series(False)
            self.setText("Show Candlesticks")
        elif self.isChecked():
            stock_chart.toggle_candle_series(True)
            self.setText("Hide Candlesticks")


def get_this(item='chart' or 'info'):
    if hasattr(config.stk.widget(1), item):
        return getattr(config.stk.widget(1), item)
    else:
        return getattr(config.stk.widget(2), item)
