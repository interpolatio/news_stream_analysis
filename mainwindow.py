from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QDockWidget, QMainWindow, QListWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSplitter, QListView, QGroupBox,QCheckBox)
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

class Communicate(QtCore.QObject):
    closeApp = pyqtSignal()

class VisibleWidget(QDockWidget):
    listClass = ['no_class']
    listVisibleClass = ['no_class']
    def __init__(self, owner):
        super(VisibleWidget, self).__init__()
        self.ClassBox = QGroupBox(self)
        self.ClassBox.classVisibleBoxLayout = QVBoxLayout()
        self.ClassBox.setTitle("Tracing Parameters")
        self.setWidget(self.ClassBox)
        self.setFloating(False)
        self.listClass = list(owner.df.groupby('text_class')['text_class'].groups.keys())
        self.listClassUpdate()

    def listClassUpdate(self):
        qChkBx_shot_all = QCheckBox("Class-" + "All", self)

        qChkBx_shot_all.clicked.connect(self.toggleGroupBoxAll)
        qChkBx_shot_all.setChecked(True)
        self.ClassBox.classVisibleBoxLayout.addWidget(qChkBx_shot_all, QtCore.Qt.AlignCenter)
        for class_group in (self.listClass):
            qChkBx_shot = QCheckBox("Class-" + str(class_group), self)
            qChkBx_shot.setChecked(True)
            self.ClassBox.classVisibleBoxLayout.addWidget(qChkBx_shot, QtCore.Qt.AlignCenter)
            qChkBx_shot.stateChanged.connect(self.toggleGroupBox)

        self.ClassBox.setLayout(self.ClassBox.classVisibleBoxLayout)

    def toggleGroupBoxAll(self, event):
        check_all = self.findChildren(QCheckBox)[0]
        flagCheckAll = check_all.isChecked()
        for checkbox in self.findChildren(QCheckBox)[0:]:
            checkbox.setChecked(flagCheckAll)


    def toggleGroupBox   (self, event):
        flagCheck = True
        self.listVisibleClass = []
        for checkbox, className in zip(self.ClassBox.findChildren(QCheckBox)[1:], self.listClass[1:]):
            if not checkbox.isChecked():
                flagCheck = False
            else:
                self.listVisibleClass.append(className)
        self.ClassBox.findChildren(QCheckBox)[0].setChecked(flagCheck)


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.view = view(self)
        self.timerId = 0
        self.c = Communicate()


        self.df = process.get_dataframe()

        for i, node in self.df.iloc[:, :].iterrows():
            ooo = Node(node['text_class'], node['x'], node['y'], node['title'], node['not_prep'])
            self.view.scene.addItem(ooo)

        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("save")
        file.addAction("quit")

        self.items = QDockWidget("Title file", self)
        self.classVisible = VisibleWidget(self)

        self.textWidget = QListView()
        self.items.setWidget(self.textWidget)
        self.items.setFloating(False)


        self.setCentralWidget(self.view)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.items)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.classVisible)

        self.setLayout(layout)
        self.setWindowTitle("Text Visualization")

        self.view.moved.connect(self.ListViewUpdate)

    def ListViewUpdate(self):
        model = QtGui.QStandardItemModel()
        for node in self.view.scene.selectedItems():
            item = QtGui.QStandardItem(node.title)
            model.appendRow(item)
        self.textWidget.setModel(model)

    def classVisibleUpdate(self):
        model = QtGui.QStandardItemModel()
        for node in self.view.scene.selectedItems():
            item = QtGui.QStandardItem(node.title)
            model.appendRow(item)
        self.textWidget.setModel(model)

