# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2019-01-10 20:59:14
@Desc: 蓝图文件树
"""

import os

from PyQt5.QtWidgets import QTreeView, QFileSystemModel
from PyQt5.QtCore import QDir

from signalmgr import GetSignal


class CFileTree(QTreeView):
    def __init__(self, parent=None):
        super(CFileTree, self).__init__(parent)
        self.m_FileSystem = CFileSystem(self)
        self._InitUI()

    def _InitUI(self):
        path = os.path.join(os.getcwd(), "bpfile")
        index = self.m_FileSystem.setRootPath(path)
        self.header().hide()
        self.setModel(self.m_FileSystem)
        self.setRootIndex(index)

    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        sFile = self.m_FileSystem.filePath(index)
        if os.path.isfile(sFile):
            GetSignal().UI_OPEN_BLUEPRINT.emit(sFile)


class CFileSystem(QFileSystemModel):
    def __init__(self, parent=None):
        super(CFileSystem, self).__init__(parent)
        self.setFilter(QDir.Files | QDir.AllDirs | QDir.NoDotAndDotDot)
        self.setNameFilters([".xh"])
        self.setNameFilterDisables(False)

    def columnCount(self):
        return 1
