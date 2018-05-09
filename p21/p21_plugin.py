# -*- coding: utf-8 -*-

from qgis.core import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from p21widget import P21DockWidget

import resource

import os

class P21:
    icon_dir = ':/plugins/p21/icon.png'
    text = u''
    add_to_toolbar = True
    add_to_menu = True
    enabled = True
    status_tip = None 
    whats_this = None
    
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.parent = self.iface.mainWindow()
        self.callback=self.run
 
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'p21_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&P21')
        
        self.toolbar = self.iface.addToolBar(u'p21')
        self.toolbar.setObjectName(u'p21')       

        self.pluginIsActive = False
        self.dockwidget = None

    def initGui(self):
        icon = QIcon(self.icon_dir)
               
        action = QAction(icon, self.tr(self.text), self.parent)
        action.triggered.connect(self.callback)
        action.setEnabled(self.enabled)                

        if self.status_tip is not None:
            action.setStatusTip(self.status_tip)
        if self.whats_this is not None:
            action.setWhatsThis(self.whats_this)       

        if self.add_to_toolbar:
            self.toolbar.addAction(action)
        if self.add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)
        self.actions.append(action)      

    def unload(self):
        for action in self.actions:
            self.iface.removePluginVectorMenu(self.tr(u'&P21'), action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def run(self):
        if not self.pluginIsActive:
            self.pluginIsActive = True
            if self.dockwidget is None:
                self.dockwidget = P21DockWidget()
            self.dockwidget.closingPlugin.connect(self.onClose)

            self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

    def onClose(self):
        self.dockwidget.closingPlugin.disconnect(self.onClose)
        self.pluginIsActive = False

    def tr(self, message):        
        return QCoreApplication.translate('p21', message)

    def showMessage(self, title, message):
        widget  = iface.messageBar().createMessage(title, message)
       
    def logInfo(self, title, message):
        QgisMessageLog.logMessage(title, message, QgsMessageLog.INFO)

    def logWarning(self, title, message):
        QgisMessageLog.logMessage(title, message, QgsMessageLog.WARNING)

    def logCritical(self, title, message):
        QgisMessageLog.logMessage(title, message, QgsMessageLog.CRITICAL)

    def getVectorLayersNames(self):
        layers = self.iface.legendInterface().layers()
        result = []
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer:
                result.append(layer.name())
        return result

    def getAreaFromPolygon(self, layer):
        features = layer.getFeatures()
        geometry = feature.geometry()
        if geometry.wkbType() == QgsWkbTypes.Polygon:
            return geometry.area()
        else:
            return None

    def getLineLength(self, layer):
        features = layer.getFeatures()
        result = 0.
        for feature in features:
            geometry = feature.geometry()
            result += geometry.length()
        return result
