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
        view.btn_report_start_list_pdf.Bind(wx.EVT_BUTTON, self.on_report_sart_list_pdf)
        view.btn_report_start_list_html.Bind(wx.EVT_BUTTON, self.on_report_sart_list_html)
        view.btn_web_forms_files.Bind(wx.EVT_BUTTON, self.on_web_forms_files)
        view.btn_fiarna.Bind(wx.EVT_BUTTON, self.on_fiarna)
        view.btn_classifications.Bind(wx.EVT_BUTTON, self.on_classifications)
        view.btn_punctuations.Bind(wx.EVT_BUTTON, self.on_punctuations)
        view.btn_sessions.Bind(wx.EVT_BUTTON, self.on_sessions)

    def go_back(self, event):
        self.presenter.go_back()

    def on_gen_champ_auto(self, event):
        self.presenter.gen_champ_auto()
    
    def on_report_inscriptions(self, event):
        self.presenter.report_inscriptions()

    def on_report_sart_list_pdf(self, event):
        self.presenter.report_sart_list_pdf()

    def on_report_sart_list_html(self, event):
        self.presenter.report_sart_list_html()

    def on_web_forms_files(self, event):
        self.presenter.gen_web_forms_files()

    def on_fiarna(self, event):
        self.presenter.load_fiarna()

    def on_classifications(self, event):
        self.presenter.load_classifications()

    def on_punctuations(self, event):
        self.presenter.load_punctuations()

    def on_sessions(self, event):
        self.presenter.load_sessions()
