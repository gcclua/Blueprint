# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-10 21:32:24
@Desc: 管理pin
"""

import copy
import misc
from . import basemgr

g_PinMgr = None


def GetPinMgr():
    global g_PinMgr
    if not g_PinMgr:
        g_PinMgr = CPinMgr()
    return g_PinMgr


class CPinMgr(basemgr.CBaseMgr):

    def NewPin(self, oDefinePin):
        oPin = copy.deepcopy(oDefinePin)
        pinID = misc.uuid()
        oPin.SetID(pinID)
        self.m_ItemInfo[pinID] = oPin
        return pinID

    def NewObj(self, ID):
        from bpdata import pin
        oPin = pin.CPin(ID)
        return oPin
