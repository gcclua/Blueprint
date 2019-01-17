# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-12-07 17:10:02
@Desc:  蓝图定义
"""


PIN_INPUT_DATA_TYPE = 0
PIN_OUTPUT_DATA_TYPE = 1
PIN_INPUT_FLOW_TYPE = 2
PIN_OUTPUT_FLOW_TYPE = 3


NODE_TYPE_NORMAL = 0    # 正常节点
NODE_TYPE_EVENT = 1     # 事件节点
NODE_TYPE_VARIABLE = 2  # 变量节点


class Type:
    INT = 1
    FLOAT = 2
    STR = 3
    BOOL = 4


NAME_TYPE = {
    "int": Type.INT,
    "float": Type.FLOAT,
    "str": Type.STR,
    "bool": Type.BOOL,
}

TYPE_NAME = {
    Type.INT: "int",
    Type.FLOAT: "float",
    Type.STR: "str",
    Type.BOOL: "bool",
}


def PinIsFlow(iPinType):
    if iPinType in (PIN_INPUT_FLOW_TYPE, PIN_OUTPUT_FLOW_TYPE):
        return True
    return False


def PinIsInput(iPinType):
    if iPinType in (PIN_INPUT_FLOW_TYPE, PIN_INPUT_DATA_TYPE):
        return True
    return False


def GetDefauleValue(iType):
    if iType in (Type.INT, Type.FLOAT):
        return 0
    if iType in (Type.STR,):
        return ""
    return None


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
    ADD = "加法"
    MIUNS = "减法"
    MULTIPLY = "乘法"
    DIVIDE = "除法"
    PRINT = "打印"
    IF = "if分支"

    GET_VARIABLE = "Get变量"
    SET_VARIABLE = "Set变量"

    START = "开始事件"



# ----------------------Node-------------------------------
NODE_ATTR_NAME_PREFIX = "node_attr_name:"


class NodeAttrName:
    ID = NODE_ATTR_NAME_PREFIX + "id"
    NAME = NODE_ATTR_NAME_PREFIX + "name"
    DISPLAYNAME = NODE_ATTR_NAME_PREFIX + "display_name"
    POSITION = NODE_ATTR_NAME_PREFIX + "postion"
    PINIDLIST = NODE_ATTR_NAME_PREFIX + "pin_list"
    TYPE = NODE_ATTR_NAME_PREFIX + "type"
    VARIABLE_ID = NODE_ATTR_NAME_PREFIX + "variable_id"


# ----------------------pin-------------------------------
PIN_ATTR_NAME_PREFIX = "pin_attr_name:"


class PinAttrName:
    ID = PIN_ATTR_NAME_PREFIX + "id"
    NAME = PIN_ATTR_NAME_PREFIX + "name"
    DISPLAYNAME = PIN_ATTR_NAME_PREFIX + "display_name"
    PIN_TYPE = PIN_ATTR_NAME_PREFIX + "pin_type"    # 引脚类型
    DATA_TYPE = PIN_ATTR_NAME_PREFIX + "data_type"
    VALUE = PIN_ATTR_NAME_PREFIX + "data_value"
