# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class P21Dialog(QDialog):
    def __init__(self):
        QDialog.__init__(self):
        self.bar = QgsMessageBar()
        self.bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.setLayout(QGsGridLayout())
        self.layout().setContentMargins(0,0,0,0)
        self.buttonbox = QDialogButtonBox(QDialogButtonBox.Ok)
        self.buttonbox.accepted.connect(self.show)
        self.layout().addWidget(self.buttonbox, 0,0, 2,1)
        self.layout().addWidget(self.bar, 0,0,1,1)

    def show(self, title, message):
        self.bar.pushMessage(title, message, level=QgsMessageBar.INFO)
