from PyQt5.QtWidgets import QWidget, QGraphicsPolygonItem, QGraphicsPathItem, QGraphicsItem
from PyQt5.QtCore import Qt, QPointF, QRectF
from PyQt5.QtGui import QColor, QBrush, QPen, QPainterPath, QPainter, QPolygonF

import weakref

from .slotmgr import GetSlotMgr
from . import define


class CWidget(QWidget):
    def __init__(self, parent=None):
        super(CWidget, self).__init__(parent)
        self.m_Stype = {}
        self.setCursor(Qt.SizeAllCursor)

    def mousePressEvent(self, event):
        event.accept()

    def GetStyle(self):
        style = self.styleSheet()
        self.m_Stype["Widget"] = ""
        self.m_Stype["Press"] = ""
        sWidgetStyle = "QWidget#outline{background:transparent;}"
        sWidgetPressStr = "QWidget#outline{"
        sWidgetPressStyle = ""
        iIndex = style.find(sWidgetPressStr)
        if iIndex != -1:
            tmpStyle = style[iIndex:]
            iEnd = tmpStyle.find("}") + 1
            sWidgetPressStyle = tmpStyle[:iEnd]
            style = style.replace(sWidgetPressStyle, "")
        self.m_Stype["Widget"] = style + sWidgetStyle
        self.m_Stype["Press"] = style + sWidgetPressStyle

    def SetStyle(self, state):
        self.setStyleSheet(self.m_Stype.get(state, ""))


class CSlotUI(QGraphicsPolygonItem):
    def __init__(self, uid, oSlot, parent=None):
        super(CSlotUI, self).__init__(parent)
        self.m_Uid = uid
        self.m_Slot = weakref.ref(oSlot)
        self.m_LintItem = None
        self.m_IsLineMoving = False  # 是否在划线
        self.m_DownPosition = None   # 划线的起始坐标（相对于场景）
        self.m_CurPos = None         # 划线当前的坐标（相对于场景）
        self.m_PinLine = None
        self.InitUI()

    def InitUI(self):
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setZValue(4)
        self.setAcceptHoverEvents(True)

        size = self.m_Slot().GetSize()
        self.m_PF = QRectF(0, 0, size[0], size[1])
        self.setPolygon(QPolygonF(self.m_PF))
        self.setCursor(Qt.CrossCursor)

    def IsInputSlotUI(self):
        iType = self.m_Slot().GetType()
        return iType == define.INPUT_BTN_TYPE

    def GetConnectPoint(self):
        return self.m_Slot().m_Center

    def mousePressEvent(self, event):
        print("slotui-mousePressEvent", self.scene())
        super(CSlotUI, self).mousePressEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton:
            self.scene().BeginConnect(self)
            # self.m_DownPosition = event.buttonDownScenePos(Qt.LeftButton)

    def mouseMoveEvent(self, event):
        super(CSlotUI, self).mouseMoveEvent(event)
        event.accept()
        if event.button() == Qt.LeftButton and self.m_DownPosition:
            self.m_IsLineMoving = True
            self.m_CurPos = event.scenePos()
            self.update()

            lastuid = GetSlotMgr().GetLastSelect()
            if not lastuid:
                GetSlotMgr().SetLastSelect(self.m_Uid)

    def mouseReleaseEvent(self, event):
        print("slotui-mouseReleaseEvent")
        event.accept()
        super(CSlotUI, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.scene().EndConnect(event)
            self.m_IsLineMoving = False
            self.m_DownPosition = None
            self.m_CurPos = None

    def CanConnect(self, oSlotUI):
        """判断self是否可以和oSlotUI连接"""
        return True

    def SetPinLine(self, oPinLine):
        self.m_PinLine = weakref.ref(oPinLine)

    def GetPinLine(self):
        if self.m_PinLine:
            return self.m_PinLine()
        return None


class CPinLine(QGraphicsItem):
    """引脚连线"""

    def __init__(self, parent=None):
        super(CPinLine, self).__init__(parent)
        self.m_StartSlotUI = None
        self.m_EndSlotUI = None
        self.setZValue(-1000)
        self.m_StartPoint = None
        self.m_EndPoint = None
        self.m_Path = None
        self.m_Rect = None
        self.RecalculateShapeAndBount()

    def RecalculateShapeAndBount(self):
        if self.m_StartPoint is None or self.m_EndPoint is None:
            self.m_Path = QPainterPath()
            self.m_Path.addRect(0, 0, 0, 0)
            self.m_Rect = self.m_Path.boundingRect()
            return
        if self.m_StartPoint.x() < self.m_EndPoint.x():
            centerY = (self.m_StartPoint.y() + self.m_EndPoint.y()) // 2
            c1 = QPointF(self.m_StartPoint.x(), centerY)
            c2 = QPointF(self.m_EndPoint.x(), centerY)
        else:
            centerX = (self.m_StartPoint.x() + self.m_EndPoint.x()) // 2
            c1 = QPointF(centerX, self.m_StartPoint.y())
            c2 = QPointF(centerX, self.m_EndPoint.y())
        self.m_Path = QPainterPath()
        self.m_Path.moveTo(self.m_StartPoint)
        self.m_Path.cubicTo(c1, c2, self.m_EndPoint)
        self.m_Path.addEllipse(self.m_StartPoint, 4, 4)
        self.m_Path.addEllipse(self.m_EndPoint, 4, 4)
        self.m_Rect = self.m_Path.boundingRect()

    def SetStartReceiver(self, oSlotUI):
        self.m_StartSlotUI = weakref.ref(oSlotUI)
        # self.m_StartPoint = self.mapFromItem(oSlotUI, *oSlotUI.GetConnectPoint())
        print("StartPoint", self.m_StartPoint)
        self.UpdatePosition()

    def GetStartSlotUI(self):
        if self.m_StartSlotUI:
            return self.m_StartSlotUI()
        return None

    def SetEndReceiver(self, oSlotUI):
        self.m_EndSlotUI = weakref.ref(oSlotUI)
        # self.m_EndPoint = self.mapFromItem(oSlotUI, *oSlotUI.GetConnectPoint())
        print("EndPoint", self.m_EndPoint)
        self.UpdatePosition()

    def GetEndSlotUI(self):
        if self.m_EndSlotUI:
            return self.m_EndSlotUI()
        return None

    def UpdatePosition(self):
        startSlotUI = self.GetStartSlotUI()
        if startSlotUI:
            self.m_StartPoint = self.mapFromItem(startSlotUI, *startSlotUI.GetConnectPoint())
        endSlotUI = self.GetEndSlotUI()
        if endSlotUI:
            self.m_EndPoint = self.mapFromItem(endSlotUI, *endSlotUI.GetConnectPoint())
        else:
            self.m_EndPoint = self.mapFromScene(self.scene().GetMouseScenePos())
        self.prepareGeometryChange()
        self.RecalculateShapeAndBount()

    def paint(self, painter, _, __):
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setPen(Qt.white)
        painter.drawPath(self.m_Path)
