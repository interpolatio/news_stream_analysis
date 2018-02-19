from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QToolButton, QSlider)
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore

class view(QGraphicsView):
    moved = QtCore.pyqtSignal(QtGui.QMouseEvent)
    def wheelEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ControlModifier):
            if (event.angleDelta().y() > 0):
                self.zoomIn(10)
            else:
                self.zoomOut(10)
        else:
            super(view, self).wheelEvent(event)

    def mouseMoveEvent(self, event):

        self.moved.emit(event)
        super(view, self).mouseMoveEvent(event)

    def __init__(self, owner):
        super(QGraphicsView, self).__init__(owner)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setCacheMode(QtWidgets.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.scene.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        #self.scene.setSceneRect(-400, -400, 800, 800)
        self.setScene(self.scene)

        self.zoomInIcon = QToolButton(self)
        self.zoomOutIcon = QToolButton(self)
        self.zoomSlider = QSlider(self)
        self.zoomSlider.setMinimum(0)
        self.zoomSlider.setMaximum(500)
        self.zoomSlider.setValue(250)
        self.zoomSliderLayout = QVBoxLayout(self)
        self.zoomSliderLayout.addWidget(self.zoomInIcon)
        self.zoomSliderLayout.addWidget(self.zoomSlider)
        self.zoomSliderLayout.addWidget(self.zoomOutIcon)
        self.zoomSlider.valueChanged.connect(self.setupMatrix)

    def setupMatrix(self):

        scale = pow(2, (self.zoomSlider.value() - 250) / 50.)
        k = QtGui.QTransform()
        k.scale(scale, scale)
        print(scale)
        self.setTransform(k)

    def zoomIn(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() + level)

    def zoomOut(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() - level)
