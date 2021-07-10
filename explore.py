from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import explore_artifacts as explore_gui


class ExploreQuery(QFrame):

    def __init__(self, sector='', country='', marketcap=0):
        super(ExploreQuery, self).__init__()
        self.setStyleSheet('''ExploreQuery{border-image: url(bg.jpg);}''')
        self.build_query(sector, country, marketcap)

    def build_query(self, sector, country, marketcap):
        v_box = QVBoxLayout()
        v_box.setAlignment(Qt.AlignmentFlag.AlignTop)

        h_box = QHBoxLayout()
        h_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        h_box.addWidget(explore_gui.BackButton())

        v_box.addLayout(h_box)

        v_box.addWidget(explore_gui.QueryResults(sector, country, marketcap))

        self.setLayout(v_box)
