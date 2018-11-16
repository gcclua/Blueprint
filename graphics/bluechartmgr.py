
import miscqt
from PyQt5.QtCore import pyqtSignal, QObject

g_BlueChartMgr = None


def GetBlueChartMgr():
    global g_BlueChartMgr
    if not g_BlueChartMgr:
        g_BlueChartMgr = CBlueChartMgr()
    return g_BlueChartMgr


class CBlueChartMgr(QObject):
    SIG_ADD_CHART = pyqtSignal(str)

    def __init__(self):
        super(CBlueChartMgr, self).__init__()
        self.m_ActionItem = {}

    def NewChart(self, sName, tPos):
        idChart = miscqt.NewUuid()
        oAction = CBlueChart(idChart, sName, tPos)
        self.m_ActionItem[idChart] = oAction
        return idChart

    def GetChart(self, iID):
        if iID in self.m_ActionItem:
            return self.m_ActionItem[iID]
        return None


class CBlueChart:
    def __init__(self, id, sName, tPos):
        self.m_ID = id
        self.m_Name = sName
        self.m_Pos = tPos   # 相对于场景的位置

    def GetName(self):
        return self.m_Name

    def SetName(self, sName):
        self.m_Name = sName

    def GetID(self):
        return self.m_ID

    def GetPos(self):
        return self.m_Pos
