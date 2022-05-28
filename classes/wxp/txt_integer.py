# -*- coding: utf-8 -*-


import wx


class TxtInteger(object):
    '''
    extend wx.TextCtrl 
    '''

    def __init__(self, txt):
        self.txt = txt
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.kill_focus)

    def get_int(self, value):
        if value.isdigit():
            value = int(value)
        else:
            value = 0
        return value

    def kill_focus(self, event):
        self.SetValue(self.txt.GetValue())
        event.Skip()

    def GetValue(self):
        return self.get_int(self.txt.GetValue())

    def SetValue(self, value):
        if isinstance(value, int):
            self.txt.SetValue('{0}'.format(value))
        else:
            self.txt.SetValue('{0}'.format(self.get_int(value)))

