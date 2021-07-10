from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from inquiry import *

import config


class ExitButton(QPushButton):

    def __init__(self):
        super(ExitButton, self).__init__("Exit")
        self.clicked.connect(self.exit_action)

    def exit_action(self):
        QCoreApplication.exit(0)


class RefreshButton(QPushButton):

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


class StockListLabel(QLabel):

    def __init__(self, text):
        super(StockListLabel, self).__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        self.setMinimumWidth(175)
        self.setFont(QFont("Verdana", 20))


class StockList(QListWidget):

    def __init__(self, list):
        super(StockList, self).__init__()
        self.setMaximumSize(175, 510)
        self.fill_stock_list(list)
        self.itemClicked.connect(self.action)

    def fill_stock_list(self, list):
        for item in list:
            list_widget_item = QListWidgetItem("{text}".format(text=item))
            list_widget_item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            list_widget_item.setSizeHint(QSize(0, 75))
            self.addItem(list_widget_item)

    def update_favs(self):
        self.clear()
        self.fill_stock_list(config.fav)
        if self.count() == 0:
            self.hide()
        else:
            self.show()

    def action(self, item):
        self.clearSelection()
        config.stk.insertWidget(1, InquiryCard(item.text()))
        config.stk.setCurrentIndex(1)
