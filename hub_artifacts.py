import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import config
import nav


class ExitButton(QtWidgets.QPushButton):

    def __init__(self):
        super(ExitButton, self).__init__("Exit")
        self.clicked.connect(self.exit_action)

    def exit_action(self):
        file = open("user_config.txt", 'w')
        for favorite in config.fav:
            file.write("{:s};".format(favorite))
        file.write("\n")
        file.flush()
        for key, value in config.notes.items():
            file.writelines("{:s} {:s};\n".format(key, value))
        file.flush()
        file.close()
        QtCore.QCoreApplication.exit(0)


class RefreshButton(QtWidgets.QPushButton):

    def __init__(self):
        super(RefreshButton, self).__init__("Refresh")
        self.clicked.connect(self.refresh_action)

    def refresh_action(self):
        favs_list = config.stk.widget(0).centralWidget().h3_box.itemAt(2).widget()
        favs_list.update_favs()
        favs_label = config.stk.widget(0).centralWidget().h2_box.itemAt(2).widget()
        if favs_list.isHidden():
            favs_label.hide()
        else:
            favs_label.show()
        notes_selector = config.stk.widget(0).centralWidget().v_box.itemAt(1).widget()
        notes_selector.update_noted_tickers()


class StockListLabel(QtWidgets.QLabel):

    def __init__(self, text):
        super(StockListLabel, self).__init__(text)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop)
        self.setMinimumWidth(175)
        self.setFont(QtGui.QFont("Verdana", 20))


class StockList(QtWidgets.QListWidget):

    def __init__(self, stock_list):
        super(StockList, self).__init__()
        self.setMaximumSize(175, 510)
        self.viewport().setAutoFillBackground(False)
        self.setStyleSheet("StockList{selection-background-color: khaki;}")
        if stock_list == config.fav:
            stock_list = self.fill_favorites()
            config.fav = stock_list
        self.fill_stock_list(stock_list)
        self.itemClicked.connect(self.action)

    def fill_favorites(self):
        file = open("user_config.txt", "r")
        tickers = []
        for ticker in file.readline().split(";"):
            if ticker == '\n':
                break
            tickers.append(ticker)
        file.close()
        return tickers

    def fill_stock_list(self, stock_list):
        for item in stock_list:
            list_widget_item = QtWidgets.QListWidgetItem("{text}".format(text=item))
            align = QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignVCenter
            list_widget_item.setTextAlignment(align)
            list_widget_item.setSizeHint(QtCore.QSize(0, 75))
            self.addItem(list_widget_item)

    def update_favs(self):
        self.clear()
        self.fill_stock_list(config.fav)
        if self.count() == 0:
            self.hide()
        else:
            self.show()

    def action(self):
        self.clearSelection()
        nav.go_inquiry(self.currentItem().text(), 1)


class NotesSelector(QtWidgets.QComboBox):

    def __init__(self):
        super(NotesSelector, self).__init__()
        self.setStyleSheet("background-color: rgba(0,0,0,0); width: 200px;"
                           "border-style: solid; border-width: 1px; border-color: black;")
        self.setMaximumWidth(100)
        self.cache_users_notes()
        self.update_noted_tickers()
        self.notes_editor = None
        self.ticker_select = None
        self.currentIndexChanged.connect(self.open_notes_action)

    def cache_users_notes(self):
        file = open("user_config.txt", "r")

        file.readline()

        for ticker_notes in file.read().split(";\n"):
            if ticker_notes == '\n':
                break
            entry = ticker_notes.split(' ', 1)
            if len(entry) == 2:
                config.notes[entry[0]] = entry[1]

    def update_noted_tickers(self):
        self.clear()
        self.addItem("")
        self.addItems(config.notes.keys())

    def open_notes_action(self):
        if self.currentText() == "":
            return
        self.ticker_select = self.currentText()
        self.notes_editor = QtWidgets.QTextEdit()
        self.notes_editor.setStyleSheet('''QTextEdit{border-image: url(bg.jpg);}''')
        self.notes_editor.closeEvent = self.save_notes_action
        self.notes_editor.setText(config.notes[self.ticker_select])
        self.notes_editor.show()

    def save_notes_action(self, a0: QtGui.QCloseEvent):
        config.notes[self.ticker_select] = self.notes_editor.toPlainText()
