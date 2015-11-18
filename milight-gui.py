#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine

import mci


class Remote():
    """ Simple app class """

    def __init__(self, win, online=True):
        """ App init """
        self.online = online
        self.last_group = '0'

        for index in range(0, 5):
            name = 'group_'+str(index)
            btn = win.findChild(QObject, name)
            btn.state1.connect(self.switchOn)
            btn.state2.connect(self.switchOff)

        btn = win.findChild(QObject, 'warmth')
        btn.state1.connect(self.increaseWarmth)
        btn.state2.connect(self.decreaseWarmth)

        btn = win.findChild(QObject, 'brightness')
        btn.state1.connect(self.increaseBrightness)
        btn.state2.connect(self.decreaseBrightness)

    def switchOn(self, name):
        """ switchOn signal handler """
        group = name.split('_')[1]
        self.last_group = group
        if self.online:
            lc = mci.WhiteGroup('192.168.0.230', 8899, group_number=int(group))
            lc.on()

    def switchOff(self, name):
        """ switchOff signal handler """
        group = name.split('_')[1]
        self.last_group = group
        if self.online:
            lc = mci.WhiteGroup('192.168.0.230', 8899, group_number=int(group))
            lc.off()

    def increaseBrightness(self, name):
        """ increaseBrightness signal handler """
        if self.online:
            lc = mci.WhiteGroup('192.168.0.230', 8899, group_number=int(self.last_group))
            lc.increase_brightness()

    def decreaseBrightness(self, name):
        """ decreaseBrightness signal handler """
        if self.online:
            lc = mci.WhiteGroup('192.168.0.230', 8899, group_number=int(self.last_group))
            lc.decrease_brightness()

    def increaseWarmth(self, name):
        """ increaseWarmth signal handler """
        if self.online:
            lc = mci.WhiteGroup('192.168.0.230', 8899, group_number=int(self.last_group))
            lc.increase_warmth()

    def decreaseWarmth(self, name):
        """ decreaseWarmth signal handler """
        if self.online:
            lc = mci.WhiteGroup('192.168.0.230', 8899, group_number=int(self.last_group))
            lc.decrease_warmth()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("main", engine)

    engine.load('qml/example.qml')

    win = engine.rootObjects()[0]
    remote = Remote(win)
    win.show()

    sys.exit(app.exec_())
