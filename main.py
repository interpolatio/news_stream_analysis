#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import GraphWidget

if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = GraphWidget()
    #w = QWidget()
    w.resize(600, 600)
    # w.move(300, 300)
    # w.setWindowTitle('Simple')
    w.show()

    sys.exit(app.exec_())