from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import (QDockWidget, QMainWindow, QAction, qApp, QFileDialog, QListWidget, QTextEdit, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QSplitter, QListView, QGroupBox,QCheckBox, QGraphicsItemGroup)
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QSplitter
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from PyQt5 import QtGui
import process
import pandas as pd
import os
import pickle
import operator

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
        self.listClassUpdate(owner)
        self.listVisibleClassUpdate()


    def listClassUpdate(self,owner):
        for classBoxChild in self.ClassBox.children():
            if type(classBoxChild) == QCheckBox:
                classBoxChild.setParent(None)
        if not (owner.df.empty):
            #print(self.listClass)
            self.listClass = list(owner.df.groupby('text_class')['text_class'].groups.keys())
            self.listVisibleClassUpdate()

    def listVisibleClassUpdate(self):
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
        self.df = pd.DataFrame()

        # self.df = process.get_dataframe()


        dirAction = QAction("&Open dir", self);
        dirAction.setShortcut('Ctrl+O')
        dirAction.triggered.connect(self.openFileNameDialog)

        datAction = QAction("Open &dat", self);
        datAction.setShortcut('Ctrl+D')
        datAction.triggered.connect(self.openDataNameDialog)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        layout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("&File")
        file.addAction(dirAction)
        file.addAction(datAction)
        file.addAction("Save")
        file.addAction(exitAction)
        file1 = bar.addMenu("asd")
        file1.addAction("123 dir")
        file1.addAction("d")
        file1.addAction("Quit")

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

        # for i, df_node in self.df.iloc[:10, :].iterrows():
        #     node = Node(df_node['text_class'], df_node['x'], df_node['y'], df_node['title'], df_node['not_prep'])
        #     self.view.scene.addItem(node)

        # self.class_rotate()

        self.view.moved.connect(self.ListViewUpdate)
        self.class_compression.zoomSlider.valueChanged.connect(self.compression)
        self.compression()
        # self.compression()
        self.classVisible.list_visible_class_update_signal.connect(self.list_visible_update)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        directory = QFileDialog.getExistingDirectory(self, "Find Files"
                                                     , options=options)
        # directory = 'C:/Users/user/PycharmProjects/russian_text'
        if directory:
            print(directory)
            print(os.listdir(directory))
            text_buf = process.init_text(directory)
            print(len(text_buf))
            text_not_prep = process.filter_symbol(text_buf)
            text_stem = process.stemming(text_not_prep)
            texts_without_stopwords = process.filter_stop_words(text_stem)
            print("stemming ok")
            path = 'C:\\Users\\user\\PycharmProjects\\russian_text'
            with open(path + '\\etalon_model.dat', 'rb') as f:
                print("_")
                etalon_model = pickle.load(f)
            print("etalon ok")
            with open(path + '//dictionary_all.dat', 'rb') as f:
                dictionary_all = pickle.load(f)
            print("dictionary ok")
            corpus = [dictionary_all.doc2bow(text_buf) for text in texts_without_stopwords]
            print("corpus ok")
            pos = process.MDS_text_main(texts_without_stopwords)
            print("MDS ok")
            df_update = pd.DataFrame(
                dict(x=pos[:, 0], y=pos[:, 1], not_prep=text_not_prep, without_stopwords=texts_without_stopwords,
                     title=os.listdir(directory)))
            df_update['text_class'] = df_update.apply(lambda row: max(etalon_model[dictionary_all.doc2bow(row['without_stopwords'])],
                                                        key=operator.itemgetter(1))[0], axis=1)
            self.df = pd.concat([self.df, df_update])
            print("classifitation ok")
            for i, df_node in df_update.iloc[:, :].iterrows():
                node = Node(df_node['text_class'], df_node['x'], df_node['y'], df_node['title'], df_node['not_prep'])
                self.view.scene.addItem(node)
            print(" node ok")
            self.classVisible.listClassUpdate(self)

    def openDataNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Data Files (*.dat);;All Files (*)", options=options)
        if fileName:
            print(fileName)
            df_update = process.get_dataframe(fileName)
            self.df = pd.concat([self.df, df_update])
            for i, df_node in df_update.iloc[:, :].iterrows():
                node = Node(df_node['text_class'], df_node['x'], df_node['y'], df_node['title'], df_node['not_prep'])
                self.view.scene.addItem(node)
            self.classVisible.listClassUpdate(self)

    def compression(self):
        delta_value = abs(self.class_compression.zoomSlider.value() - self.class_compression.old_value)
        # self.class_compression.old_value = self.class_compression.zoomSlider.value()
        scale = pow(2, (self.class_compression.zoomSlider.value() - 250) / 50.)

        # scale = 0.2
        class_node = self.classVisible.listClass[0]
        self.node_group = QGraphicsItemGroup()
        self.node = self.view.scene.items()
        # print(self.node[0],self.node[0].transform().isScaling() )
        # print(scale)
        # print(delta_value)
        # print(pow(2, (self.class_compression.zoomSlider.value() - 250) / 50.))

        for node in self.view.scene.items():
            if (type(node) is Node ):
                #print(node.nodeclass == class_node)
                if (node.nodeclass == class_node):
                    # node.setScale(scale)
                    self.node_group.addToGroup(node)
        self.view.scene.addItem(self.node_group)
        # print(self.node_group)
        # # self.node_group.setScale(scale)
        # print(self.node[0], self.node[0].transform().isScaling() )
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