# -*- coding: utf-8 -*-


import wx


class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        view.btn_generate_champ.Bind(wx.EVT_BUTTON, self.on_gen_champ_auto)
        view.btn_report_inscriptions.Bind(wx.EVT_BUTTON, self.on_report_inscriptions)
        view.btn_report_heats.Bind(wx.EVT_BUTTON, self.on_report_heats)
        view.btn_fiarna.Bind(wx.EVT_BUTTON, self.on_fiarna)

    def go_back(self, event):
        self.presenter.go_back()

    def on_gen_champ_auto(self, event):
        self.presenter.gen_champ_auto()
    
    def on_report_inscriptions(self, event):
        self.presenter.report_inscriptions()

    def on_report_heats(self, event):
        self.presenter.report_heats()

    def on_fiarna(self, event):
        self.presenter.fiarna()


