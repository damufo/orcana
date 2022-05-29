# -*- coding: utf-8 -*-


import wx
from specific_functions import dates


class TxtDate(object):
    '''
    extend wx.TextCtrl
    set_value: from aaaammdd to aaaa/mm/dd
    get_value: from aaaa/mm/dd to aaaammdd
    '''

    def __init__(self, txt):
        self.txt = txt
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.check_date)

    @property
    def date(self):
        return self.txt.GetValue()

    def check_date(self, event):
        self.txt.SetValue(dates.validate(self.date))
        event.Skip()

    def GetValue(self):
        return self.date.replace("/", "")

    def SetValue(self, value):
        self.txt.SetValue(dates.validate(value))

class TxtDateIso(object):
    '''
    TxtDateIso
    extend wx.TextCtrl
    set_value: from aaaa-mm-dd to aaaa/mm/dd
    get_value: from aaaa/mm/dd to aaaa-mm-dd
    '''

    def __init__(self, txt):
        self.txt = txt
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.on_kill_focus)

    def on_kill_focus(self, event):
        self.SetValue(self.txt.GetValue())
        event.Skip()  # activado, se inactivo fallan as datas en convocatorias arbitrais, comportamento extraño, quedan os campos seleccionados...

    def GetValue(self):
        self.SetValue(self.txt.GetValue())
        return self.txt.GetValue()

    def SetValue(self, value):
        self.txt.SetValue(dates.validate(value))
