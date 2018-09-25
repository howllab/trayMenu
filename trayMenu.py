#-*-coding:utf-8-*-

import os, sys
import ConfigParser
from PySide import QtCore, QtGui

class TrayMenu(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)

        self.filePath = os.path.abspath(__file__+"/../")
        self.setIcon(QtGui.QIcon("%s/icon/trayMenuIcon.png"%self.filePath))
        self.leftMenu = QtGui.QMenu()
        self.rightMenu = QtGui.QMenu()

        self.activated.connect(self.showMenu)

    def showMenu(self, value):
        self.leftMenu.clear()
        self.rightMenu.clear()

        # menu exec
        if value == self.Trigger: #left mouse
            self.makeMenu(self.leftMenu)
            self.leftMenu.exec_(QtGui.QCursor.pos())
        if value == self.Context: #right mouse
            self.makeMenu(self.rightMenu)
            self.rightMenu.exec_(QtGui.QCursor.pos())

    def makeMenu(self, menuObj):
        # get config file
        self.trayConfig=ConfigParser.ConfigParser()
        self.trayConfig.read("%s/config.ini"%self.filePath)
        trayMenuDic, trayMenuKeys = self.getConfig("menu")

        # menu loop
        for nameV in trayMenuKeys:
            menuCmd = trayMenuDic[nameV]
            menuName = "_".join(nameV.split("_")[1:])

            # create sub menu
            if menuName == "submenu":
                # menuCmd is submenu section name
                subMenu = QtGui.QMenu(menuName)
                traySubMenuDic, traySubMenuKeys = self.getConfig(menuCmd)
                for subnameV in traySubMenuKeys:
                    submenuCmd = traySubMenuDic[subnameV]
                    submenuName = "_".join(subnameV.split("_")[1:])
                    self.createMenu(subMenu, submenuName, submenuCmd)
                menuObj.addMenu(subMenu)
            # create menu
            else:
                self.createMenu(menuObj, menuName, menuCmd)

    def getConfig(self, sectionV):
        # get item - dic, key
        trayMenuDic = dict(self.trayConfig.items(sectionV))
        trayMenuKeys = trayMenuDic.keys()
        trayMenuKeys.sort()
        return trayMenuDic, trayMenuKeys

    def createMenu(self, typeV, menuName, menuCmd):
        act = QtGui.QAction(menuName, self)
        act.triggered.connect(lambda:self.runCmd(menuCmd))
        typeV.addAction(act)

    def runCmd(self, menuCmd):
        os.system("%s &"%menuCmd)
        print menuCmd

if __name__=="__main__":
    trayMenuApp = QtGui.QApplication(sys.argv)

    tray = TrayMenu()
    tray.show()

    trayMenuApp.exec_()
