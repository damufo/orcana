# -*- coding: utf-8 -*-


import wx
from specific_functions import marks


class TxtMark(object):
    '''
    extend wx.TextCtrl
    set_value: from numeric
    get_value: return a float
    '''

    def __init__(self, txt):
        self.txt = txt
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.kill_focus)

    def kill_focus(self, event):
        self.txt.SetValue(marks.hun2mark(marks.validate(self.txt.GetValue())))
        event.Skip()

    def GetValue(self):
        return marks.validate(self.txt.GetValue())

    def SetValue(self, value):
        hundredths = marks.validate(value)
        self.txt.SetValue(marks.hun2mark(hundredths))
