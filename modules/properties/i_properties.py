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
        view.btn_report_heats_pdf.Bind(wx.EVT_BUTTON, self.on_report_heats_pdf)
        view.btn_report_heats_html.Bind(wx.EVT_BUTTON, self.on_report_heats_html)
        view.btn_web_forms_files.Bind(wx.EVT_BUTTON, self.on_web_forms_files)
        view.btn_fiarna.Bind(wx.EVT_BUTTON, self.on_fiarna)

    def go_back(self, event):
        self.presenter.go_back()

    def on_gen_champ_auto(self, event):
        self.presenter.gen_champ_auto()
    
    def on_report_inscriptions(self, event):
        self.presenter.report_inscriptions()

    def on_report_heats_pdf(self, event):
        self.presenter.report_heats_pdf()

    def on_report_heats_html(self, event):
        self.presenter.report_heats_html()

    def on_web_forms_files(self, event):
        self.presenter.gen_web_forms_files()

    def on_fiarna(self, event):
        self.presenter.fiarna()


