#-*-coding:utf-8-*-

import os, sys

from PySide import QtCore, QtGui

class TrayMenu(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        filePath = os.path.abspath(__file__+"/../")
        self.setIcon(QtGui.QIcon("%s/icon/trayMenuIcon.png"%filePath))
        self.trayMenuItem = TrayMenuItem()
        self.setContextMenu(self.trayMenuItem)

        self.activated.connect(self.leftClick)

    def leftClick(self, value):
        if value == self.Trigger:
            self.trayMenuItem.exec_(QtGui.QCursor.pos())

class TrayMenuItem(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, parent)

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
