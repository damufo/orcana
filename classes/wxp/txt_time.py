# -*- coding: utf-8 -*-


import wx
from specific_functions import dates

import time

def validate_short(input):
    try:
        if ':' in input:
            validated = time.strptime(input, '%H:%M')
        elif '.' in input:
            validated = time.strptime(input, '%H.%M')
        else:
            validated = time.strptime(input, '%H%M')
        validated = time.strftime('%H:%M', validated)
    except ValueError:
        validated = ''
    return validated

def validate_full(input):
    try:
        validated = time.strptime(input, '%H:%M:%S')
        validated = time.strftime('%H:%M:%S', validated)
    except ValueError:
        validated = ''
    return validated

class TxtTimeShort(object):
    '''
    extend wx.TextCtrl
    set_value: HH:MM
    get_value: HH:MM
    '''

    def __init__(self, txt):
        self.txt = txt
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.check_time)

    @property
    def time(self):
        return self.txt.GetValue()

    def check_time(self, event):
        self.txt.SetValue(validate_short(self.time))
        event.Skip()

    def GetValue(self):
        return self.time

    def SetValue(self, value):
        self.txt.SetValue(validate_short(value))

class TxtTimeIso(object):
    '''
    extend wx.TextCtrl
    set_value: HH:MM:SS.HHH
    get_value: HH:MM:SS.HHH
    non é preciso inserir a parte decimal dos segundos, son opcionais
    '''

    def __init__(self, txt):
        self.txt = txt
        self.txt.Bind(wx.EVT_KILL_FOCUS, self.check_time)

    @property
    def time(self):
        return self.txt.GetValue()

    def check_time(self, event):
        self.txt.SetValue(validate_full(self.time))
        event.Skip()

    def GetValue(self):
        return self.time

    def SetValue(self, value):
        self.txt.SetValue(validate_full(value))
