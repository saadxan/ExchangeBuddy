import config
import csv
import nav

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ExploreBar(QLineEdit):

    def __init__(self, explore_type):
        super(ExploreBar, self).__init__()
        self.setPlaceholderText("Type & Press Enter")
        self.setCompleter(TickerCompleter(explore_type))
        self.textEdited.connect(self.to_uppercase)
        self.returnPressed.connect(self.execute_explore)

    def to_uppercase(self):
        self.setText(self.text().upper())

    def execute_explore(self):
        nav.go_inquiry(self.text())
        self.clear()


class ExploreDataSet():

    def __init__(self):
        self.data = []
        self.cols = {}
        self.make_data_set()
        self.basic_info = (self.cols['Symbol'], self.cols['Name'], self.cols['Market Cap'])
        self.advanced_info = self.basic_info + (self.cols['Country'], self.cols['Sector'], self.cols['Industry'])

    def make_data_set(self):
        with open('tickers_dataset.csv', 'rU') as f:
            dict_reader = csv.DictReader(f)
            self.data = list(dict_reader)
            f.seek(0)

            for read_row in dict_reader:
                for column_head, column_info in read_row.items():
                    try:
                        if column_head != column_info:
                            self.cols[column_head].append(column_info)
                    except KeyError:
                        self.cols[column_head] = [column_info]


class TickerCompleter(QCompleter):

    def __init__(self, model_type=0):
        super(TickerCompleter, self).__init__()
        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.set_model_type(model_type)
        self.highlighted.connect(self.test)

    def set_model_type(self, model_type):
        self.setModel(QStringListModel(EXPLORE_DATA_SET.advanced_info[model_type]))

    def test(self):
        print("testing")


class ExploreApparatus():

    def __init__(self):
        self.country_combo = TypeComboBox(3)
        self.sector_combo = TypeComboBox(4)
        self.cap_buttons = CapFilterButtons()


class TypeComboBox(QComboBox):

    def __init__(self, type_combos=4):
        super(TypeComboBox, self).__init__()
        self.addItems(set(EXPLORE_DATA_SET.advanced_info[type_combos]))
        self.setCurrentText('')
        self.selected_value = ''
        self.currentIndexChanged.connect(self.change_explore_type)

    def change_explore_type(self):
        self.selected_value = self.currentText()


class CapFilterButtons(QButtonGroup):

    def __init__(self):
        super(CapFilterButtons, self).__init__()
        self.cap_filter = 0
        self.b_none = QRadioButton("None")
        self.b_1B = QRadioButton("1B")
        self.b_10B = QRadioButton("10B")
        self.b_100B = QRadioButton("100B")
        self.addButton(self.b_none, 0)
        self.addButton(self.b_1B, 1)
        self.addButton(self.b_10B, 2)
        self.addButton(self.b_100B, 3)
        self.buttonClicked.connect(self.set_cap_filter)

    def set_cap_filter(self):
        id = self.checkedId()

        if id == 0:
            self.cap_filter = 0
        elif id == 1:
            self.cap_filter = 1000000000
        elif id == 2:
            self.cap_filter = 10000000000
        elif id == 3:
            self.cap_filter = 100000000000


class ExploreButton(QPushButton):

    def __init__(self):
        super(ExploreButton, self).__init__("Explore")
        self.clicked.connect(self.explore_action)

    def explore_action(self):
        sector_value = config.stk.widget(0).centralWidget().explore_form.itemAt(4).widget().selected_value
        country_value = config.stk.widget(0).centralWidget().explore_form.itemAt(6).widget().selected_value
        marketcap_value = config.stk.widget(0).centralWidget().explore_form.children()[0].cap_filter
        nav.go_explore(sector_value, country_value, marketcap_value)


class BackButton(QPushButton):

    def __init__(self):
        super(BackButton, self).__init__("Back")
        self.clicked.connect(self.return_action)

    def return_action(self):
        nav.return_home()


class QueryResults(QTableWidget):

    def __init__(self, sector='', country='', marketcap=''):
        super(QueryResults, self).__init__()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results = []
        self.query(sector, country, marketcap)
        self.make_query_table()
        self.itemClicked.connect(self.selected_inquiry)

    def query(self, sector, country, marketcap):
        for ds in EXPLORE_DATA_SET.data:
            if sector in (ds['Sector'], '') and country in (ds['Country'], '') and marketcap <= float(ds['Market Cap']):
                self.results.append(ds)

    def make_query_table(self):
        if len(self.results) == 0:
            return

        self.setColumnCount(6)
        self.setRowCount(len(self.results))

        for i, header in enumerate(self.results[0].keys()):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(header))

        for i, result in enumerate(self.results):
            for j, result_val in enumerate(result):
                if result_val != 'Market Cap':
                    self.setItem(i, j, QTableWidgetItem(result[result_val]))
                else:
                    self.setItem(i, j, QTableWidgetItem("{:,.0f}M".format(float(result[result_val]) / 1000000)))

        self.setColumnWidth(0, 75)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(3, 125)
        self.setColumnWidth(4, 150)
        self.setColumnWidth(5, 300)

    def selected_inquiry(self):
        nav.go_inquiry(self.selectedItems()[0].text(), 2)
        self.clearSelection()


EXPLORE_DATA_SET = ExploreDataSet()
