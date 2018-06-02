#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MainWindow()
    w.resize(1000, 800)
    #max_width = app.desktop().screenGeometry().width()
    #max_height = app.desktop().screenGeometry().height()
    #w.setMaximumSize(max_width, max_height)
    w.show()

    sys.exit(app.exec_())