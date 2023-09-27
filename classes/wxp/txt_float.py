# -*- coding: utf-8 -*-


import wx
from specific_functions import floats

class TxtFloat(object):
    '''
    extend wx.TextCtrl
    '''

    def __init__(self, txt, decimals=2):
        self.txt = txt
        self.decimals = decimals
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.kill_focus)

    def kill_focus(self, event):
        self.SetValue(self.txt.GetValue())
        event.Skip()

    def GetValue(self):
        return floats.get_float(self.txt.GetValue())

    def SetValue(self, value):
        value = floats.get_float(value)
        self.txt.SetValue(floats.get_str(value))
