#-*-coding:utf-8-*-

import os, sys, re
import ConfigParser
from PySide import QtCore, QtGui

trayConfig=ConfigParser.ConfigParser()

class TrayMenu(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.filePath = os.path.abspath(__file__+"/../")
        self.setIcon(QtGui.QIcon("%s/icon/trayMenuIcon.png"%self.filePath))
        # self.setContextMenu(self.trayMenuItem) # init context menu-right

        self.activated.connect(self.showMenu)

    def showMenu(self, value):

        global trayConfig
        trayConfig.read("%s/config.ini"%self.filePath)

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

        trayMenuDic, trayMenuKeys = self.getConfig("menu")

        for nameV in trayMenuKeys:
            menuCmd = trayMenuDic[nameV]
            menuName = "_".join(nameV.split("_")[1:])

            # create sub menu
            if menuName == "submenu":
                traySubMenuDic, traySubMenuKeys = self.getConfig(menuCmd)
                for subnameV in traySubMenuKeys:
                    submenuCmd = traySubMenuDic[subnameV]
                    submenuName = "_".join(subnameV.split("_")[1:])
                    self.createSubMenu(nameV, submenuName, submenuCmd)
            # create menu
            else:
                self.createMenu(menuName, menuCmd)

    def getConfig(self, sectionV):
        global trayConfig
        trayMenuDic = dict(trayConfig.items(sectionV))
        trayMenuKeys = trayMenuDic.keys()
        trayMenuKeys.sort()
        return trayMenuDic, trayMenuKeys

    def createMenu(self, menuName, menuCmd):
        act = QtGui.QAction(menuName, self)
        act.triggered.connect(lambda:self.runCmd(menuCmd))
        self.addAction(act)


    def createSubMenu(self, nameV, menuName, menuCmd):
        subMenu = QtGui.QMenu(nameV, self)
        act = QtGui.QAction(menuName, self)
        act.triggered.connect(lambda:self.runCmd(menuCmd))
        subMenu.addAction(act)

    def runCmd(self, menuCmd):
        os.system("%s &"%menuCmd)
        print menuCmd

if __name__=="__main__":
    trayMenuApp = QtGui.QApplication(sys.argv)

    tray = TrayMenu()
    tray.show()

    trayMenuApp.exec_()
