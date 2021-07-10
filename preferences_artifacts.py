import config
import csv
import nav

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ResetButton(QPushButton):

    def __init__(self):
        super(ResetButton, self).__init__("Reset")
        self.clicked.connect(self.reset_action)

    def reset_action(self):
        yes_or_no = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        pick = QMessageBox.question(self, "Confirm", "Reset to default preferences?", yes_or_no)
        if pick == QMessageBox.StandardButton.Yes:
            config.fav = ['TSLA']
            nav.refresh_home()
