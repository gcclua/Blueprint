# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-09 09:55:45
@Desc:
"""

import weakref

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QTransform, QCursor
from PyQt5.QtCore import Qt
from . import chartui, slotui
from .bluechartmgr import GetBlueChartMgr


class CBlueprintScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CBlueprintScene, self).__init__(parent)
        self.m_ChartInfo = {}
        self.m_SlotInfo = {}
        self.m_Pos = None   # 创建图表的位置,已换算成对于场景的位置
        self.m_LeftBtnStartPos = None
        self.m_IsDrawLine = False
        self.m_TempPinLine = None  # 临时引脚线
        self.m_View = weakref.ref(parent)
        self.Init()
        self.InitSignal()

    def Init(self):
        self.setSceneRect(-10000, -10000, 20000, 20000)  # 场景大小，传入item里面

    def InitSignal(self):
        pass

    # def mousePressEvent(self, event):
    #     # super(CBlueprintScene, self).mousePressEvent(event)
    #     # if event.isAccepted():
    #     #     return
    #     sPos = event.scenePos()
    #     item = self.itemAt(sPos, QTransform())
    #     if isinstance(item, slotui.CPinLine):
    #         item = None
    #     print("item:", item)
    #     # if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
    #     #     GetBlueChartMgr().ClearSelect()
    #     if event.button() == Qt.LeftButton:
    #         self.m_LeftBtnStartPos = sPos
    #         if self.m_TempPinLine:
    #             self.MyEndConnect(item)

    #     if not self.m_IsDrawLine:
    #         super(CBlueprintScene, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(CBlueprintScene, self).mouseMoveEvent(event)
        if self.m_TempPinLine:
            self.m_TempPinLine.UpdatePosition()
        if not self.m_LeftBtnStartPos:
            return

    def mouseReleaseEvent(self, event):
        super(CBlueprintScene, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        super(CBlueprintScene, self).wheelEvent(event)
        # 吞噬信号，不再将信号返回父窗口，禁止父窗口滑动条操作
        event.accept()

    def SetPos(self, pos):
        self.m_Pos = pos

    def AddChartWidget(self, idChart, sName):
        oBlueChart = GetBlueChartMgr().GetChart(idChart)
        oWidget = chartui.CBlueChartUI(oBlueChart, sName, self)
        self.m_ChartInfo[idChart] = oWidget
        self.addItem(oWidget)
        x, y = oBlueChart.GetPos()
        oWidget.setPos(x, y)
        # oWidget.setPos(self.m_Pos.x(), self.m_Pos.y())

    def BeginConnect(self, oSlotUI):
        self.m_IsDrawLine = True
        self.m_TempPinLine = slotui.CPinLine()
        self.addItem(self.m_TempPinLine)
        self.m_TempPinLine.SetStartReceiver(oSlotUI)


    def EndConnect(self, event):
        sPos = event.scenePos()
        endSlotUI = self.itemAt(sPos, QTransform())
        if isinstance(endSlotUI, slotui.CSlotUI):    # 如果不是slotui
            startSlotUI = self.m_TempPinLine.GetStartSlotUI()
            if startSlotUI.CanConnect(endSlotUI) and endSlotUI.CanConnect(startSlotUI):
                # 断开原有连线
                if startSlotUI.GetPinLine():
                    self.BreakConnect(startSlotUI)
                if endSlotUI.GetPinLine():
                    self.BreakConnect(endSlotUI)
                if startSlotUI.IsInputSlotUI():
                    inputSlotUI, outputSlotUI = startSlotUI, endSlotUI
                else:
                    inputSlotUI, outputSlotUI = endSlotUI, startSlotUI
                self.AddConnect(inputSlotUI, outputSlotUI)

        self.removeItem(self.m_TempPinLine)
        self.m_TempPinLine = None
        self.m_IsDrawLine = False

    def BreakConnect(self, oSlotUI):
        pass

    def AddConnect(self, inputSlotUI, outputSlotUI):
        """真正执行添加连接线"""
        line = slotui.CPinLine()
        self.addItem(line)  # 这个顺序不能变
        line.SetStartReceiver(inputSlotUI)
        line.SetEndReceiver(outputSlotUI)
        inputSlotUI.SetPinLine(line)
        outputSlotUI.SetPinLine(line)

    def GetMouseScenePos(self):
        view = self.views()[0]
        viewPos = view.mapFromGlobal(QCursor.pos())
        scenePos = view.mapToScene(viewPos)
        return scenePos
