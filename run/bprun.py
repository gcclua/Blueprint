# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-11 22:29:45
@Desc: 蓝图运行
"""

import copy
import logging

from editdata import interface
from editdata import define as eddefine
from bpdata import define as bddefine
from signalmgr import GetSignal


g_BlueprintRunMgr = None


def GetRunMgr():
    global g_BlueprintRunMgr
    if not g_BlueprintRunMgr:
        g_BlueprintRunMgr = CBlueprintRunMgr()
    return g_BlueprintRunMgr


def GetPinValue(pinID):
    value = GetRunMgr().GetPinValue(pinID)
    return value


class CBlueprintRunMgr:
    def __init__(self):
        self.m_PinValue = {}
        self.m_LineList = []

    def Reset(self):
        self.m_PinValue = {}
        for lineID in self.m_LineList:
            GetSignal().LINE_RUN_STATUE.emit(lineID, False)

    def _GetPinFunc(self, pinID):
        nodeID = interface.GetNodeIDByPinID(pinID)
        pinName = interface.GetPinAttr(pinID, bddefine.PinAttrName.NAME)
        dFunc = interface.GetNodeFuncInfo(nodeID)
        func = dFunc.get(pinName, None)
        return func

    def GetPinValue(self, pinID):
        if interface.IsFlowPin(pinID):
            logging.error("flowpin:%s not value" % pinID)
            return
        if pinID in self.m_PinValue:
            return self.m_PinValue[pinID]

        if interface.IsInputPin(pinID):  # 输入引脚
            lstLine = interface.GetAllLineByPin(pinID)
            if lstLine:  # 有连线
                lineID = lstLine[0]
                outPin = interface.GetLineOtherPin(lineID, pinID)
                outPinValue = GetPinValue(outPin)
                self.m_PinValue[outPin] = outPinValue
                self.m_PinValue[pinID] = outPinValue
                logging.info("pin:%s->%s value:%s type:%s" % (outPin, pinID, outPinValue, type(outPinValue)))
                GetSignal().LINE_RUN_STATUE.emit(lineID, True)
                self.m_LineList.append(lineID)
                return outPinValue

            # 无连线
            inputValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
            self.m_PinValue[pinID] = inputValue
            logging.info("pin:%s value:%s type:%s" % (pinID, inputValue, type(inputValue)))
            return inputValue

        # 输出引脚
        func = self._GetPinFunc(pinID)
        if func:
            outPinValue = func()
            self.m_PinValue[pinID] = outPinValue
            logging.info("pin:%s value:%s type:%s" % (pinID, outPinValue, type(outPinValue)))
            return outPinValue

        outPinValue = interface.GetPinAttr(pinID, bddefine.PinAttrName.VALUE)
        self.m_PinValue[pinID] = outPinValue
        logging.info("pin:%s value:%s type:%s" % (pinID, outPinValue, type(outPinValue)))
        return outPinValue

    def RunOutputFlow(self, outputPin):
        lstline = interface.GetAllLineByPin(outputPin)
        for lineID in lstline:
            inputPin = interface.GetLineOtherPin(lineID, outputPin)
            self.RunInputFlow(inputPin)
            GetSignal().LINE_RUN_STATUE.emit(lineID, True)
            self.m_LineList.append(lineID)

    def RunInputFlow(self, inputPin):
        func = self._GetPinFunc(inputPin)
        if func:
            func()
        nodeID = interface.GetNodeIDByPinID(inputPin)
        lstPin = interface.GetNodeAttr(nodeID, bddefine.NodeAttrName.PINIDLIST)
        for pinID in lstPin:
            if pinID == inputPin:
                continue
            iType = interface.GetPinAttr(pinID, bddefine.PinAttrName.PIN_TYPE)
            if iType != bddefine.PIN_OUTPUT_FLOW_TYPE:
                continue
            self.RunOutputFlow(pinID)


def RunBlueprint(bpID):
    iEventNode = interface.GetBlueprintAttr(bpID, eddefine.BlueprintAttrName.EVENT_NODE)
    if not iEventNode:
        return
    lstPin = interface.GetNodeAttr(iEventNode, bddefine.NodeAttrName.PINIDLIST)
    startPin = lstPin[0]
    obj = GetRunMgr()
    obj.Reset()
    obj.RunOutputFlow(startPin)


def StopBlueprint(bpID):
    obj = GetRunMgr()
    obj.Reset()
