
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from color_constan import color

class Node(QtWidgets.QGraphicsItem):
    Type = QtWidgets.QGraphicsItem.UserType + 1

    def __init__(self, nclass: int, x: int, y: int, title: str, text: str):
        super(Node, self).__init__()

        #self.graph = graphWidget
        self.edgeList = []
        self.newPos = QtCore.QPointF()
        self.nodeclass = nclass
        self.setPos(x,y)
        self.title = title
        self.text = text

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QtWidgets.QGraphicsItem.DeviceCoordinateCache)
        # self.setZValue(1)

    # def type(self):
    #     return Node.Type
    #
    # def advance(self):
    #     if self.newPos == self.pos():
    #         return False
    #
    #     self.setPos(self.newPos)
    #     return True
    #
    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10 - adjust, -10 - adjust, 23 + adjust,
                             23 + adjust)
    #
    # def shape(self):
    #     path = QtGui.QPainterPath()
    #     path.addEllipse(-10, -10, 20, 20)
    #     return path

    def paint(self, painter, option, widget):
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtCore.Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20) #отрисовка тени шара

        lod = option.levelOfDetailFromTransform(painter.worldTransform())
        colornode = color[self.nodeclass]
        gradient = QtGui.QRadialGradient(-3, -3, 10)
        if option.state & QtWidgets.QStyle.State_Selected:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, colornode.lighter(120))
            gradient.setColorAt(0, colornode.darker(200).lighter(150))
        else:
            gradient.setColorAt(0, colornode)
            gradient.setColorAt(1, colornode.darker(200))

        painter.setBrush(QtGui.QBrush(gradient))
        if lod > 0.4:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20) # отрисовка шара
