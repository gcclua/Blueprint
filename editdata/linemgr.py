# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 14:51:59
@Desc: 节点连线管理
"""

import misc

from signalmgr import GetSignal
from .idmgr import GetIDMgr
from . import define, basemgr

g_LineMgr = None


def GetLineMgr():
    global g_LineMgr
    if not g_LineMgr:
        g_LineMgr = CLineMgr()
    return g_LineMgr


class CLineMgr(basemgr.CBaseMgr):

    def NewLine(self, graphicID, oPinID, iPinID):
        # 删除input槽之前的连接
        from .graphicmgr import GetGraphicMgr
        lstLine = GetIDMgr().GetAllLineByPin(iPinID)
        for lineID in lstLine:
            self.DelLine(lineID)
        lineID = misc.uuid()
        oLine = CLine(lineID, oPinID, iPinID)
        self.m_ItemInfo[lineID] = oLine
        GetIDMgr().SetLine2Graphic(graphicID, lineID)           # 记录line对应的graphic
        GetIDMgr().AddLine2Pin(oPinID, iPinID, lineID)          # 记录引脚对应的line
        GetGraphicMgr().AddLine2Graphic(lineID)                 # 添加到graphic属性里面
        return lineID

    def DelLine(self, lineID):
        from .graphicmgr import GetGraphicMgr
        oLine = self.m_ItemInfo[lineID]
        oPinID = oLine.GetAttr(define.LineAttrName.OUTPUT_PINID)
        iPinID = oLine.GetAttr(define.LineAttrName.INPUT_PINID)
        GetIDMgr().DelLine4Pin(oPinID, iPinID, lineID)
        GetGraphicMgr().DelLine4Graphic(lineID)
        del self.m_ItemInfo[lineID]
        graphicID = GetIDMgr().DelLine2Graphic(lineID)
        GetSignal().DEL_LINE.emit(graphicID, lineID)

    def NewObj(self, ID):
        oItem = CLine(ID)
        return oItem


class CLine(basemgr.CBase):
    def __init__(self, uid, oPinID=None, iPinID=None):
        super(CLine, self).__init__(uid)
        self.m_Info = {
            define.LineAttrName.ID: uid,
            define.LineAttrName.OUTPUT_PINID: oPinID,
            define.LineAttrName.INPUT_PINID: iPinID,
        }

    def SetLoadInfo(self, dInfo):
        super(CLine, self).SetLoadInfo(dInfo)
        oPin = self.GetAttr(define.LineAttrName.OUTPUT_PINID)
        iPinID = self.GetAttr(define.LineAttrName.INPUT_PINID)
        GetIDMgr().AddLine2Pin(oPin, iPinID, self.m_ID)
