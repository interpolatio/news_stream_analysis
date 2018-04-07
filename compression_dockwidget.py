from PyQt5.QtWidgets import (QDockWidget, QGroupBox, QHBoxLayout, QComboBox, QPushButton, QCheckBox,QSlider, QGraphicsItemGroup)
from PyQt5 import QtCore
from node import Node

class compression_widget(QDockWidget):
    old_value = 0
    def __init__(self, owner):
        super(compression_widget, self).__init__()
        self.listClass = owner.classVisible.listClass
        self.setWindowTitle("Tracing Parameters")
        self.ClassBox = QGroupBox(self)
        self.ClassBox.classVisibleBoxLayout = QHBoxLayout()
        # self.ClassBox.setTitle("")
        self.setWidget(self.ClassBox)
        self.setFloating(False)


        self.zoomSlider = QSlider(QtCore.Qt.Horizontal, self.ClassBox)
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(500)
        self.zoomSlider.setValue(250)
        self.ClassBox.classVisibleBoxLayout.addWidget(self.zoomSlider)
        self.ClassBox.setLayout(self.ClassBox.classVisibleBoxLayout)
        #self.compression(owner)

    # def compression(self, owner):
    #     # scale = pow(2, (self.zoomSlider.value() - 250) / 50.)
    #     scale = 100
    #     print(scale)
    #     class_node = self.listClass[0]
    #     self.node_group = QGraphicsItemGroup()
    #     print(owner.view.scene.items())
    #     owner.view.scene.addItem(self.node_group)
    #
    #     for node in owner.view.scene.items():
    #         if (type(node) is Node):
    #             # print(node.nodeclass == class_node)
    #             # if (node.nodeclass == class_node):
    #             self.node_group.addToGroup(node)
    #     self.node_group.setScale(scale)
    #     # self.node_group.setRotation(180)
    #     owner.view.scene.destroyItemGroup(self.node_group)