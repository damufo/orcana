# -*- coding: utf-8 -*-


import wx

from .w_persons import Persons
# from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages


class View(Persons):
    def __init__(self, parent):
        Persons.__init__(self, parent=parent)
        self.SetName('persons')
        self.parent = parent
        self.parent.load_panel(self)
        self.msg = Messages(self.parent)
        self.lsc_persons.SetName('persons')
        self.lsc_persons_plus = self.parent.get_lsc_plus(lsc=self.lsc_persons, parent=self)
        self.lsc_inscriptions_ind.SetName('inscriptions_ind')
        self.lsc_inscriptions_ind_plus = self.parent.get_lsc_plus(lsc=self.lsc_inscriptions_ind, parent=self)
        self.spl_persons.SetName('spl_persons')
        self.spl_persons_plus = self.parent.get_spl_plus(spl=self.spl_persons, parent=self)
        # self.spl_persons_plus.load_custom_sashpos()
        # load_custom_sashpos execútase 300 milisegundos despois de iniciarse
        # Do contrario non funciona
        wx.CallLater (500, self.spl_persons_plus.load_custom_sashpos)
        print("split invisible: ", self.spl_persons.IsSashInvisible())
        print("split size: ", self.spl_persons.GetSashSize())

    def close(self):
        self.lsc_persons_plus.save_custom_column_width()
        self.lsc_inscriptions_ind_plus.save_custom_column_width()
        print("save splitter: ", self.spl_persons.GetSashPosition())
        self.spl_persons_plus.save_custom_sashpos()

        
