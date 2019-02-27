# -*- coding:utf-8 -*-
'''
@Description: 变量细节widget
@Author: lamborghini1993
@Date: 2019-02-27 11:43:42
@UpdateDate: 2019-02-27 17:38:17
'''

import weakref

from PyQt5 import QtWidgets, QtCore, QtGui
from editdata import interface
from signalmgr import GetSignal

from editdata import define as eddefine
from bpdata import define as bddefine


class CVarWidget(QtWidgets.QWidget):
    m_Num = 3

    def __init__(self, varID, parent=None):
        super(CVarWidget, self).__init__(parent)
        self.m_VarID = varID
        self.m_Box = None
        self.m_Type = interface.GetVariableAttr(self.m_VarID, eddefine.VariableAttrName.TYPE)
        self.m_Name = interface.GetVariableAttr(self.m_VarID, eddefine.VariableAttrName.NAME)
        self.m_ValueWidget = None
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        vBox = QtWidgets.QVBoxLayout(self)

        hBox1 = QtWidgets.QHBoxLayout()
        lable1 = QtWidgets.QLabel("变量名称", self)
        self.m_VarName = QtWidgets.QLineEdit(self)
        hBox1.addWidget(lable1)
        hBox1.addWidget(self.m_VarName)

        hBox2 = QtWidgets.QHBoxLayout()
        lable2 = QtWidgets.QLabel("变量类型", self)
        self.m_VarType = QtWidgets.QComboBox(self)
        hBox2.addWidget(lable2)
        hBox2.addWidget(self.m_VarType)

        self.m_Box = hBox3 = QtWidgets.QHBoxLayout()
        lable3 = QtWidgets.QLabel("变量值", self)
        hBox3.addWidget(lable3)

        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)
        item = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        vBox.addItem(item)

        for sType in bddefine.NAME_TYPE:
            self.m_VarType.addItem(sType)

        self.m_VarName.setText(self.m_Name)
        if self.m_Type in bddefine.TYPE_NAME:
            sType = bddefine.TYPE_NAME[self.m_Type]
            self.m_VarType.setCurrentText(sType)
        self._SetValueWidget()

    def _InitSignal(self):
        self.m_VarName.editingFinished.connect(self.S_NameEditingFinished)
        self.m_VarType.currentIndexChanged.connect(self.S_TypeChanged)

    def _SetValueWidget(self):
        self._RemoveValueWidget()
        if self.m_Type in (bddefine.Type.INT, bddefine.Type.STR, bddefine.Type.FLOAT):
            self.m_ValueWidget = CLineEdit(self.m_VarID, self.m_Type)
        elif self.m_Type == bddefine.Type.BOOL:
            self.m_ValueWidget = CCheckBox(self.m_VarID)
        elif self.m_Type == bddefine.Type.LIST:
            self.m_ValueWidget = CList(self.m_VarID)

        if not self.m_ValueWidget:
            return
        self.m_Box.addWidget(self.m_ValueWidget)
        self.adjustSize()

    def _RemoveValueWidget(self):
        if not self.m_ValueWidget:
            return
        self.m_ValueWidget.setParent(None)
        index = self.m_Box.indexOf(self.m_ValueWidget)
        item = self.m_Box.itemAt(index)
        self.m_Box.removeWidget(self.m_ValueWidget)
        self.m_Box.removeItem(item)
        self.m_ValueWidget = None
        self.adjustSize()

    def S_NameEditingFinished(self):
        sName = self.m_VarName.text()
        if sName == self.m_Name:
            return
        GetSignal().UI_VARIABLE_CHANGE_ATTR.emit(self.m_VarID, eddefine.VariableAttrName.NAME, sName)
        self.m_Name = sName

    def S_TypeChanged(self):
        sType = self.m_VarType.currentText()
        iType = bddefine.NAME_TYPE[sType]
        if iType == self.m_Type:
            return
        value = bddefine.GetDefauleValue(iType)
        GetSignal().UI_VARIABLE_CHANGE_ATTR.emit(self.m_VarID, eddefine.VariableAttrName.TYPE, iType)
        interface.SetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE, value)
        self.m_Type = iType
        self._SetValueWidget()


class CLineEdit(QtWidgets.QLineEdit):
    def __init__(self, varID, iDataType, parent=None):
        super(CLineEdit, self).__init__(parent)
        self.m_DataType = iDataType
        self.m_VarID = varID
        self.m_LastValue = None
        self._InitUI()
        self._InitSignal()

    def _InitUI(self):
        if self.m_DataType == bddefine.Type.INT:
            self.setValidator(QtGui.QIntValidator())
            self.setText("0")
        elif self.m_DataType == bddefine.Type.FLOAT:
            self.setValidator(QtGui.QDoubleValidator())
            self.setText("0.0")

        value = interface.GetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE)
        self.setText(str(value))
        self.m_LastValue = value

    def _InitSignal(self):
        self.editingFinished.connect(self.S_EditingFinished)

    def S_EditingFinished(self):
        text = self.text()
        if not text and self.m_DataType in (bddefine.Type.INT, bddefine.Type.FLOAT):
            text = "0"
        value, bSuc = bddefine.ForceTransValue(self.m_DataType, text)
        if not bSuc:
            self.setText(str(self.m_LastValue))
            return
        if value == self.m_LastValue:
            return
        interface.SetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE, value)
        self.m_LastValue = value
        self.setText(str(value))
        self.clearFocus()


class CCheckBox(QtWidgets.QCheckBox):
    def __init__(self, varID, parent=None):
        super(CCheckBox, self).__init__(parent)
        self.m_VarID = varID
        self.m_LastValue = None
        self._InitUI()
        self._InitSignal()
        self._InitData()

    def _InitUI(self):
        size = QtCore.QSize(20, 20)
        self.setMinimumSize(size)
        self.setMaximumSize(size)

    def _InitSignal(self):
        self.toggled.connect(self.S_CheckedChanged)

    def _InitData(self):
        value = interface.GetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE)
        if value:
            self.setCheckState(QtCore.Qt.Checked)
        else:
            self.setCheckState(QtCore.Qt.Unchecked)
        self.m_LastValue = value

    def S_CheckedChanged(self, value):
        if value == self.m_LastValue:
            return
        interface.SetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE, value)
        self.m_LastValue = value


class CList(QtWidgets.QWidget):
    m_Num = 2
    m_TypeList = [bddefine.SType.INT, bddefine.SType.FLOAT, bddefine.SType.STR]

    def __init__(self, varID, parent=None):
        super(CList, self).__init__(parent)
        self.m_VarID = varID
        self.m_Box = None
        self.m_Type = None
        self.m_ID = 0
        self.m_ListWidget = []
        self.m_LastValue = interface.GetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE)
        if not isinstance(self.m_LastValue, list):
            self.m_LastValue = []
        self._GetType()
        self._InitUI()
        self._InitData()

    def _GetType(self):
        if not self.m_LastValue:
            self.m_Type = bddefine.Type.INT
            return
        temp = self.m_LastValue[0]
        if isinstance(temp, bool):
            self.m_Type = bddefine.Type.BOOL
            return
        if isinstance(temp, int):
            self.m_Type = bddefine.Type.INT
            return
        if isinstance(temp, float):
            self.m_Type = bddefine.Type.FLOAT
            return
        self.m_Type = bddefine.Type.STR

    def _InitUI(self):
        self.m_Box = vBox = QtWidgets.QVBoxLayout(self)
        self.m_Box.setSpacing(0)

        hBox1 = QtWidgets.QHBoxLayout()
        lable1 = QtWidgets.QLabel("值类型", self)
        self.m_ComBoxValueType = QtWidgets.QComboBox(self)
        hBox1.addWidget(lable1)
        hBox1.addWidget(self.m_ComBoxValueType)

        hBox2 = QtWidgets.QHBoxLayout()
        self.m_LableInfo = QtWidgets.QLabel(self)
        btnAdd = QtWidgets.QPushButton("+", self)
        btnClear = QtWidgets.QPushButton("x", self)
        btnAdd.setToolTip("插入新的一行")
        btnClear.setToolTip("清除所有行")
        size = QtCore.QSize(20, 20)
        btnAdd.setMaximumSize(size)
        btnClear.setMaximumSize(size)
        hBox2.addWidget(self.m_LableInfo)
        hBox2.addWidget(btnAdd)
        hBox2.addWidget(btnClear)

        vBox.addLayout(hBox1)
        vBox.addLayout(hBox2)

        self.m_ComBoxValueType.addItems(self.m_TypeList)
        self.m_ComBoxValueType.currentTextChanged.connect(self.S_ValueTypeChange)
        sType = bddefine.TYPE_NAME[self.m_Type]
        self.m_ComBoxValueType.setCurrentText(sType)
        self._SetLableInfo()
        btnAdd.clicked.connect(self.S_ListAdd)
        btnClear.clicked.connect(self.S_ListClear)

        vBox.setContentsMargins(0, 0, 0, 0)
        vBox.setSpacing(1)

    def _InitData(self):
        for value in self.m_LastValue:
            oWidget = CSubList(self.m_Type, self)
            self.m_ListWidget.append(oWidget)
            self.m_Box.addWidget(oWidget)
            oWidget.SetValue(value)
        self._RefreshID()

    def _SetLableInfo(self):
        self.m_LableInfo.setText("数组长度:%s" % len(self.m_LastValue))

    def _RefreshID(self):
        lst = []
        for ID, oWidget in enumerate(self.m_ListWidget):
            oWidget.SetID(ID)
            lst.append(oWidget.GetValue())
        interface.SetVariableAttr(self.m_VarID, eddefine.VariableAttrName.VALUE, lst)

    def S_ValueTypeChange(self, sType):
        iType = bddefine.NAME_TYPE[sType]
        if self.m_Type == iType:
            return
        self.m_Type = iType
        self.S_ListClear()

    def S_ListAdd(self, ID):
        oWidget = CSubList(self.m_Type, self)
        if isinstance(ID, bool):
            self.m_ListWidget.append(oWidget)
            self.m_Box.addWidget(oWidget)
        else:
            self.m_ListWidget.insert(ID, oWidget)
            self.m_Box.insertWidget(ID + self.m_Num, oWidget)
        self._RefreshID()

    def S_ListClear(self):
        for oWidget in self.m_ListWidget:
            self._RemoveWidget(oWidget)
        self.m_ListWidget = []
        self._RefreshID()

    def ListDel(self, ID):
        oWidget = self.m_ListWidget[ID]
        del self.m_ListWidget[ID]
        self._RemoveWidget(oWidget)
        self._RefreshID()

    def _RemoveWidget(self, oWidget):
        oWidget.setParent(None)
        index = self.m_Box.indexOf(oWidget)
        item = self.m_Box.itemAt(index)
        self.m_Box.removeWidget(oWidget)
        self.m_Box.removeItem(item)
        oWidget = None
        self.adjustSize()


class CSubList(QtWidgets.QWidget):
    def __init__(self, iType, parent=None):
        super(CSubList, self).__init__(parent)
        self.m_DataType = iType
        self.m_Parent = weakref.ref(parent)
        self.m_ID = None
        self._InitUI()

    def _InitUI(self):
        hBox = QtWidgets.QHBoxLayout(self)
        self.m_LableID = QtWidgets.QLabel("0", self)
        self.m_LineValue = QtWidgets.QLineEdit(self)
        if self.m_DataType == bddefine.Type.INT:
            self.m_LineValue.setValidator(QtGui.QIntValidator())
            self.m_LineValue.setText("0")
        elif self.m_DataType == bddefine.Type.FLOAT:
            self.m_LineValue.setValidator(QtGui.QDoubleValidator())
            self.m_LineValue.setText("0.0")

        btnAdd = QtWidgets.QPushButton("i", self)
        btnAdd.setToolTip("在本行之前插入")
        btnDel = QtWidgets.QPushButton("-", self)
        btnDel.setToolTip("删除当前行")
        size = QtCore.QSize(20, 20)
        btnAdd.setMaximumSize(size)
        btnDel.setMaximumSize(size)
        hBox.addWidget(self.m_LableID)
        hBox.addWidget(self.m_LineValue)
        hBox.addWidget(btnAdd)
        hBox.addWidget(btnDel)

        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.setSpacing(1)

        btnAdd.clicked.connect(self.S_Add)
        btnDel.clicked.connect(self.S_Del)
        self.m_LineValue.editingFinished.connect(self.S_EditingFinished)

    def SetID(self, ID):
        self.m_ID = ID
        self.m_LableID.setText(str(ID))

    def S_Add(self):
        self.m_Parent().S_ListAdd(self.m_ID)

    def S_Del(self):
        self.m_Parent().ListDel(self.m_ID)

    def S_EditingFinished(self):
        self.m_Parent()._RefreshID()

    def SetValue(self, value):
        self.m_LineValue.setText(str(value))

    def GetValue(self):
        text = self.m_LineValue.text()
        value, bSuc = bddefine.ForceTransValue(self.m_DataType, text)
        if not bSuc:
            return None
        return value
