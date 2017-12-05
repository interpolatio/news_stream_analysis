from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSplitter, QListView)
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

class GraphWidget(QWidget):
    def __init__(self):
        super(GraphWidget, self).__init__()


        self.view = view(self)
        self.timerId = 0

        # self.scene = QtWidgets.QGraphicsScene(self.view)
        # self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        # self.scene.setSceneRect(-400, -400, 800, 800)
        # self.view.setScene(self.scene)

        df = process.get_dataframe()
        
        for i, node in df.iloc[0:, :].iterrows():
            ooo = Node(node['text_class'], node['x'], node['y'], node['title'], node['not_prep'])
            self.view.scene.addItem(ooo)

        #node1 = Node(1, -50, -50)
        #self.view.scene.addItem(node1)
        #
        #node2 = Node(5, 10, 10)
        #self.view.scene.addItem(node2)
        #
        #node3 = Node(6, -50, 10)
        #self.view.scene.addItem(node3)

        self.view.setMinimumSize(600, 600)

        self.okButton = QPushButton("Process")
        self.cancelButton = QPushButton("Cancel")
        self.text = QListView()


        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.text)
        self.hbox.addWidget(self.okButton)
        self.hbox.addWidget(self.cancelButton)


        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.view)
        self.vbox.addLayout(self.hbox)
        self.setLayout(self.vbox)

        self.view.scene.mouseMoveEvent = lambda event: self.ListViewUpdate()
        self.view.scene.mousePressEvent= lambda event: self.ListViewUpdate()

    def ListViewUpdate(self):
        model = QtGui.QStandardItemModel()
        for node in self.view.scene.selectedItems():
            item = QtGui.QStandardItem(node.title)
            model.appendRow(item)
        self.text.setModel(model)