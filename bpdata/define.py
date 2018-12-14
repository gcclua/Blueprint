# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:10:02
@Desc:  蓝图定义
"""


PIN_INPUT_TYPE = 0
PIN_OUTPUT_TYPE = 1


class Type:
    INT = 1
    FLOAT = 2
    STR = 3


NAME_TYPE = {
    "int": Type.INT,
    "float": Type.FLOAT,
    "str": Type.STR,
}

TYPE_NAME = {
    Type.INT: "int",
    Type.FLOAT: "float",
    Type.STR: "str",
}


def GetDefauleValue(iType):
    if iType in (Type.INT, Type.FLOAT):
        return 0
    if iType in (Type.STR,):
        return ""


def ForceTransValue(iType, sValue):
    value, bSuc = None, False
    if iType == Type.FLOAT:
        try:
            value = float(sValue)
            bSuc = True
        except:
            pass

    if iType == Type.INT:
        try:
            value = int(sValue)
            bSuc = True
        except:
            pass

    if iType == Type.STR:
        value = sValue
        bSuc = True
    return value, bSuc


class NodeName:
    ADD = "加法节点"
    MIUNS = "减法节点"
    MULTIPLY = "乘法节点"
    DIVIDE = "除法节点"
    PRINT = "打印节点"


PIN_ATTR_NAME_PREFIX = "pin_attr_name:"


class PinAttrName:
    ID = PIN_ATTR_NAME_PREFIX + "id"
    NAME = PIN_ATTR_NAME_PREFIX + "name"
    PIN_TYPE = PIN_ATTR_NAME_PREFIX + "pin_type"
    DATA_TYPE = PIN_ATTR_NAME_PREFIX + "data_type"
