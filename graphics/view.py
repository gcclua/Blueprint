# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-11-08 16:44:23
@Desc: 蓝图view
"""
import misc

from . import scene, config
from .bluechartmgr import GetBlueChartMgr

from PyQt5.QtWidgets import QGraphicsView, QMenu, QAction
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt


class CBlueprintView(QGraphicsView):
    def __init__(self, parent=None):
        super(CBlueprintView, self).__init__(parent)
        self.m_Scale = 1
        self.m_StartPos = None
        self.m_Scene = scene.CBlueprintScene(self)
        self.Init()

    def Init(self):
        self.setWindowTitle("蓝图")
        self.setScene(self.m_Scene)
        self.setGeometry(300, 150, 1200, 800)
        self.setBackgroundBrush(QBrush(QColor(103, 103, 103), Qt.SolidPattern))
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        # 隐藏滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def mousePressEvent(self, event):
        super(CBlueprintView, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        else:
            self.setDragMode(QGraphicsView.NoDrag)

        if event.button() == Qt.MidButton:
            self.setTransformationAnchor(QGraphicsView.NoAnchor)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.m_StartPos = event.pos()

    def mouseMoveEvent(self, event):
        super(CBlueprintView, self).mouseMoveEvent(event)
        if not self.m_StartPos:
            return
        pos = event.pos()
        offsetX, offsetY = pos.x() - self.m_StartPos.x(), pos.y()-self.m_StartPos.y()
        offsetX /= self.m_Scale
        offsetY /= self.m_Scale
        self.translate(offsetX, offsetY)
        self.m_StartPos = pos

    def mouseReleaseEvent(self, event):
        super(CBlueprintView, self).mouseReleaseEvent(event)
        if event.button() == Qt.MidButton:
            self.m_StartPos = None
        self.setDragMode(QGraphicsView.RubberBandDrag)

    def wheelEvent(self, event):
        """ctrl+滑轮滚动缩放"""
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.modifiers() == Qt.ControlModifier:
            fAngleDelta = event.angleDelta().y()
            factor = 1.41 ** (fAngleDelta / 240.0)
            minScale, maxScale = 0.1, 2.0   # 控制缩放的值
            fNewScale = self.m_Scale * factor
            if fNewScale > maxScale:
                fNewScale = maxScale
            elif fNewScale < minScale:
                fNewScale = minScale
            fScale = fNewScale / self.m_Scale
            self.scale(fScale, fScale)
            self.m_Scale = fNewScale
            return
        # 没有缩放信号传递给下层
        super(CBlueprintView, self).wheelEvent(event)
        event.ignore()

    def contextMenuEvent(self, event):
        """右键上下文事件"""
        super(CBlueprintView, self).contextMenuEvent(event)
        if event.isAccepted():
            return
        lPos = event.pos()
        gPos = self.mapToGlobal(lPos)
        sPos = self.mapToScene(lPos)
        tPos = sPos.x(), sPos.y()
        menu = QMenu(self)
        for sName in config.CHART_DATA:
            func = misc.Functor(self.S_OnCreateAction, sName, tPos)
            action = QAction(sName, self)
            action.triggered.connect(func)
            menu.addAction(action)
        menu.exec_(gPos)

    def S_OnCreateAction(self, sName, tPos, _):
        idChart = GetBlueChartMgr().NewChart(sName, tPos)
        self.m_Scene.AddChartWidget(idChart, sName)
