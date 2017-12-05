from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QDockWidget, QMainWindow, QListWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSplitter, QListView)
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QSplitter
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import process
import pandas as pd

from node import Node
from view import view

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.view = view(self)
        self.timerId = 0

        df = process.get_dataframe()

        for i, node in df.iloc[:, :].iterrows():
            ooo = Node(node['text_class'], node['x'], node['y'], node['title'], node['not_prep'])
            self.view.scene.addItem(ooo)

        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("save")
        file.addAction("quit")

        self.items = QDockWidget("Title file", self)
        self.textWidget = QListView()
        #self.listWidget = QListWidget()
        #self.listWidget.addItem("item1")
        #self.listWidget.addItem("item2")
        #self.listWidget.addItem("item3")

        self.items.setWidget(self.textWidget)
        self.items.setFloating(False)
        self.setCentralWidget(self.view)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.items)
        self.setLayout(layout)
        self.setWindowTitle("Text Visualization")

        self.view.scene.mouseMoveEvent = lambda event: self.ListViewUpdate()


    def ListViewUpdate(self):
        model = QtGui.QStandardItemModel()
        for node in self.view.scene.selectedItems():
            item = QtGui.QStandardItem(node.title)
            model.appendRow(item)
        self.textWidget.setModel(model)