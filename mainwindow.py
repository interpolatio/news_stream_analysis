from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QDockWidget, QMainWindow, QListWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSplitter, QListView, QGroupBox,QCheckBox, QGraphicsItemGroup)
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
from compression_dockwidget import compression_widget

# class Communicate(QtCore.QObject):
#     closeApp = pyqtSignal()

class VisibleWidget(QDockWidget):
    listClass = ['no_class']
    listVisibleClass = ['no_class']
    list_visible_class_update_signal = QtCore.pyqtSignal()
    def __init__(self, owner):
        super(VisibleWidget, self).__init__()
        self.setWindowTitle("Tracing Parameters")
        self.ClassBox = QGroupBox(self)
        self.ClassBox.classVisibleBoxLayout = QVBoxLayout()
        # self.ClassBox.setTitle("")
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
        for checkbox in self.findChildren(QCheckBox)[1:]:
            checkbox.setChecked(flagCheckAll)

    def toggleGroupBox(self, event):
        flag_check = True
        self.listVisibleClass = []
        for checkbox, className in zip(self.ClassBox.findChildren(QCheckBox)[1:], self.listClass[0:]):
            if not checkbox.isChecked():
                flag_check = False
            else:
                self.listVisibleClass.append(className)
        self.list_visible_class_update_signal.emit()
        self.ClassBox.findChildren(QCheckBox)[0].setChecked(flag_check)


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.view = view(self)
        self.timerId = 0
        #self.c = Communicate()


        self.df = process.get_dataframe()


        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")
        file.addAction("save")
        file.addAction("quit")

        self.items = QDockWidget("Title file", self)
        self.classVisible = VisibleWidget(self)
        self.class_compression = compression_widget(self)

        self.textWidget = QListView()
        self.items.setWidget(self.textWidget)
        self.items.setFloating(False)


        self.setCentralWidget(self.view)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.items)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.classVisible)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.class_compression)

        self.setLayout(layout)
        self.setWindowTitle("Text Visualization")

        for i, df_node in self.df.iloc[:, :].iterrows():
            node = Node(df_node['text_class'], df_node['x'], df_node['y'], df_node['title'], df_node['not_prep'])
            self.view.scene.addItem(node)

        # self.class_rotate()

        self.view.moved.connect(self.ListViewUpdate)
        self.class_compression.zoomSlider.valueChanged.connect(self.compression)
        self.compression()
        # self.compression()
        self.classVisible.list_visible_class_update_signal.connect(self.list_visible_update)

    def compression(self):
        delta_value = abs(self.class_compression.zoomSlider.value() - self.class_compression.old_value)
        # self.class_compression.old_value = self.class_compression.zoomSlider.value()
        scale = pow(2, (self.class_compression.zoomSlider.value() - 250) / 50.)

        # scale = 0.2
        class_node = self.classVisible.listClass[0]
        self.node_group = QGraphicsItemGroup()
        self.node = self.view.scene.items()
        print(self.node[0],self.node[0].transform().isScaling() )
        print(scale)
        print(delta_value)
        print(pow(2, (self.class_compression.zoomSlider.value() - 250) / 50.))

        for node in self.view.scene.items():
            if (type(node) is Node ):
                #print(node.nodeclass == class_node)
                if (node.nodeclass == class_node):
                    # node.setScale(scale)
                    self.node_group.addToGroup(node)
        self.view.scene.addItem(self.node_group)
        print(self.node_group)
        # self.node_group.setScale(scale)
        print(self.node[0], self.node[0].transform().isScaling() )
        # self.node_group.setRotation(90)
        self.view.scene.destroyItemGroup(self.node_group)

    def ListViewUpdate(self):
        model = QtGui.QStandardItemModel()
        for node in self.view.scene.selectedItems():
            item = QtGui.QStandardItem(node.title)
            model.appendRow(item)
        self.textWidget.setModel(model)

    def list_visible_update(self):

        for node in self.view.scene.items():
            if not(node.nodeclass in self.classVisible.listVisibleClass):
                node.hide()
            else:
                node.show()