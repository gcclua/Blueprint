# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-01 16:32:54
@Desc: 变量
"""

import random
import copy
import misc

from . import define, basemgr
from bpdata import define as bddefine

g_VariableMgr = None


def GetVariableMgr():
    global g_VariableMgr
    if not g_VariableMgr:
        g_VariableMgr = CVariableMgr()
    return g_VariableMgr


class CVariableMgr(basemgr.CBaseMgr):
    def __init__(self):
        super(CVariableMgr, self).__init__()
        self.InitTestData()

    def NewVariable(self):
        iType = bddefine.Type.INT
        sName = "NewVar%s" % self.NewID()
        varID = misc.uuid()
        self.m_ItemInfo[varID] = CVariable(varID, sName, iType, 0)
        return varID

    def InitTestData(self):
        for i in range(10):
            sName = "Test%s" % i
            iType = random.randint(1, 3)
            value = random.randint(-999999, 999999)
            varID = misc.uuid()
            self.m_ItemInfo[varID] = CVariable(varID, sName, iType, value)

    def GetAllVarInfo(self):
        return copy.deepcopy(self.m_ItemInfo)


class CVariable(basemgr.CBase):
    def __init__(self, varID, sName=None, iType=None, value=None):
        super(CVariable, self).__init__(varID)
        self.m_Info = {
            define.VariableAttrName.ID: varID,
            define.VariableAttrName.NAME: sName,
            define.VariableAttrName.TYPE: iType,
            define.VariableAttrName.VALUE: value
        }
