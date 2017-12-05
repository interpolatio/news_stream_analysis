from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QToolButton, QSlider)
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtGui
from PyQt5 import QtCore

class view(QGraphicsView):
    def wheelEvent(self, event):
        if (event.modifiers() == QtCore.Qt.ControlModifier):
            if (event.angleDelta().y() > 0):
                self.zoomIn(10)
            else:
                self.zoomOut(10)
        else:
            super(view, self).wheelEvent(event)

    def mouseMoveEvent(self, event):
        #print("sdf")
        #print(self.scene.selectedItems())
        super(view, self).mouseMoveEvent(event)

    def __init__(self, owner):
        #self.view = QGraphicsView(self)
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
        #QtCore.QObject.connect(self.zoomSlider, QtCore.SIGNAL('valueChanged(int)'), self.setupMatrix())
        #self.zoomSlider.valueChanged(int)#.connect(self.setupMatrix())
        #self.zoomSlider.valueChanged.connect(self.setupMatrix)

    def setupMatrix(self):
        #qreal scale = qPow(qreal(2), (zoomSlider->value() - 250) / qreal(50));
        #scale = QtCore.QMath.qPow(2.2)
        z = QtCore.QPointF(33, 12)
        scale = pow(2, (self.zoomSlider.value() - 250) / 50.)
        k = QtGui.QTransform()
        k.scale(scale, scale)
        print(scale)
        self.setTransform(k)

    #connect(zoomSlider, SIGNAL(valueChanged(int)), this, SLOT(setupMatrix()));


    def zoomIn(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() + level)

    def zoomOut(self, level: int):
        self.zoomSlider.setValue(self.zoomSlider.value() - level)
