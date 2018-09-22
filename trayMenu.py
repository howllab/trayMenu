#-*-coding:utf-8-*-

import os, sys, re
import ConfigParser
from PySide import QtCore, QtGui

trayMenuList = []

class TrayMenu(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.filePath = os.path.abspath(__file__+"/../")
        self.setIcon(QtGui.QIcon("%s/icon/trayMenuIcon.png"%self.filePath))
        # self.setContextMenu(self.trayMenuItem) # init context menu-right

        self.activated.connect(self.showMenu)

    def showMenu(self, value):

        global trayMenuList
        config = ConfigParser.ConfigParser()
        config.read("%s/config.ini"%self.filePath)

        configDic = dict(config.items('menu'))
        trayMenuList =  configDic.keys()
        trayMenuList.sort()

        # menu setting
        if value == self.Trigger: #left mouse
            self.trayMenuItem = TrayMenuItem()
            self.trayMenuItem.exec_(QtGui.QCursor.pos())
        if value == self.Context: #right mouse
            self.trayMenuItem = TrayMenuItem()
            self.trayMenuItem.exec_(QtGui.QCursor.pos())


class TrayMenuItem(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, parent)

        print trayMenuList

        menu1V="http://act1"
        self.act1 = QtGui.QAction("menu1", self)
        self.act1.triggered.connect(lambda :self.menuAct(menu1V))
        self.addAction(self.act1)

        submenu1V="http://subact1"
        self.subMenu =QtGui.QMenu("submenu", self)
        self.subact1 = QtGui.QAction("menu1", self)
        self.subact1.triggered.connect(lambda :self.menuAct(submenu1V))
        self.subMenu.addAction(self.subact1)

        self.addMenu(self.subMenu)

    def menuAct(self, menuV):
        print menuV


if __name__=="__main__":
    trayMenuApp = QtGui.QApplication(sys.argv)

    tray = TrayMenu()
    tray.show()

    trayMenuApp.exec_()
