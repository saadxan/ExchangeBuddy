import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets

import explore_artifacts as explore_gui


class ExploreQuery(QtWidgets.QFrame):

    def __init__(self, sector='', country='', marketcap=0):
        super(ExploreQuery, self).__init__()
        self.setStyleSheet('''ExploreQuery{border-image: url(bg.jpg);}''')
        self.build_query(sector, country, marketcap)

    def build_query(self, sector, country, marketcap):
        v_box = QtWidgets.QVBoxLayout()
        v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        h_box = QtWidgets.QHBoxLayout()
        h_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        h_box.addWidget(explore_gui.BackButton())

        v_box.addLayout(h_box)

        v_box.addWidget(explore_gui.QueryResults(sector, country, marketcap))

        self.setLayout(v_box)
