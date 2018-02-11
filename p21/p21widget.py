# -*- coding: utf-8 -*-

from qgis.core import *
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal

import os

FORM, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__),
        'form.ui'))

class P21DockWidget(QtGui.QDockWidget, FORM):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        super(P21DockWidget, self).__init__(parent)
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

