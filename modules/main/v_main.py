# -*- coding: utf-8 -*-


import wx
from wx import adv
from wx.lib.wordwrap import wordwrap
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages
from classes.wxp.list_ctrl_plus import ListCtrlPlus
from classes.wxp.spl_plus import SplPlus
from modules.main.w_main import Main


        
# class MainFrame(MainFrame):
#     def __init__(self):
#         MainFrame.__init__(self, parent=None)
#         self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
#         self.Centre( wx.BOTH )
#         self.main_sizer = None
#         self.view_plus = ViewPlus(self)
#         self.msg = Messages(self)
#         self.panel = None

class MainFrame(wx.Frame):

    def __init__( self):
        wx.Frame.__init__ (self, parent=None, id = wx.ID_ANY, title = _(u"Orcana - (Organizador de campionatos de Natación)"),
                           pos = wx.DefaultPosition, size = wx.Size( 816,490 ),
                           style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.Centre( wx.BOTH )
        self.main_sizer = None
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self)
        self.panel = None
        # self.panels = {}

    def load_panel(self, panel):
        if self.panel:
            self.panel.Destroy()
        # if self.main_sizer:
        #     self.main_sizer.Destroy()
        self.main_sizer = wx.BoxSizer( wx.VERTICAL )
        self.panel = panel
        self.main_sizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
        self.SetSizer(self.main_sizer)
        # self.Refresh()       
        self.Layout()


    def load_panel_intento_recuperar_anterior(self, panel, retrieve_previous=False):
        """
        por se o intento novamente, dicir que habería que xestionar a creación 
        das vistas para evitar crear unha nova e cargar a anterior
        """
        load_previous = False
        if self.panel:
            self.panels[self.panel.Name] = self.panel
            self.panel.Visible(False)
            if panel.Name:
                if panel.Name in self.panels and retrieve_previous:
                    panel = self.panels[panel.Name]
                    panel.Visible(True)
                    load_previous = True
            else:
                print("o panel parece non ter nome")
            # self.panel.Destroy()
        # if self.main_sizer:
        #     self.main_sizer.Destroy()
        self.main_sizer = wx.BoxSizer( wx.VERTICAL )
        self.panel = panel
        self.main_sizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
        self.SetSizer(self.main_sizer)
        # self.Refresh()       
        self.Layout()
        return load_previous
    


    def get_lsc_plus(self, lsc, parent=None):
        if not parent:
            parent = self
        return ListCtrlPlus(lsc=lsc, view=parent)

    def get_spl_plus(self, spl, parent=None):
        if not parent:
            parent = self
        return SplPlus(spl=spl, view=parent)

class View(Main):
    def __init__(self, parent):
        Main.__init__(self, parent=parent)
        self.parent = parent
        self.SetName('main')
        self.parent.load_panel(panel=self)
        self.parent.SetMinSize(wx.Size( 976,718))
        self.msg = Messages(self.parent)
        # self.Centre( wx.BOTH )

        # self.menu = Menu()
        # self.SetMenuBar(self.menu)
        # import os
        # print(os.getcwd())
        image_path = './images/logo/app_logo.png'
        self.btm_logo.SetBitmap(wx.Bitmap(image_path, wx.BITMAP_TYPE_ANY))

        button_image = (
            # (self.btn_move_down, 'move_down.png'),
            # (self.btn_move_up, 'move_up.png'),
            # (self.btn_delete, 'delete.png'),
            # (self.btn_edit, 'edit.png'),
            # (self.btn_add, 'add.png'),
            # (self.btn_import, 'import.png'),
            # (self.btn_close, 'close.png'),
            )
        self.parent.view_plus.set_button_image(button_image)

        
        # button_image = (
        #     (self.btm_logo, 'items.png'),
        #     (self.btn_clone, 'clone.png'),
        #     (self.btn_gen_results, 'results.png'),
        #     (self.btn_toggle_published, 'cloud.png'),
        #     (self.btn_gen_package, 'package_export.png'),
        #     (self.btn_delete, 'delete.png'),
        #     (self.btn_edit, 'edit.png'),
        #     (self.btn_add, 'add.png'),
        #     (self.btn_close, 'close.png'),
        #     )
        # self.view_plus.set_button_image(button_image)

    def set_buttons(self, has_champ):
        if has_champ:
            self.btn_properties.Enable(True)
            self.btn_entities.Enable(True)
            self.btn_categories.Enable(True)
            self.btn_events.Enable(True)
            self.btn_phases.Enable(True)
            self.btn_persons.Enable(True)
            self.btn_relays.Enable(True)
            self.btn_inscriptions.Enable(True)
            self.btn_heats.Enable(True)
            self.btn_results.Enable(True)
        else:
            self.btn_properties.Enable(False)
            self.btn_entities.Enable(False)
            self.btn_categories.Enable(False)
            self.btn_events.Enable(False)
            self.btn_phases.Enable(False)
            self.btn_persons.Enable(False)
            self.btn_relays.Enable(False)
            self.btn_inscriptions.Enable(False)
            self.btn_heats.Enable(False)
            self.btn_results.Enable(False)

    def open_db(self, champ):
        import os
        msg = self.msg
        config = champ.config
        fol_reports = config.prefs.get_value('general.fol_reports')

        if not fol_reports or not os.path.exists(fol_reports):
            fol_reports = str(config.app_path_folder)
            # fol_reports = os.path.join(config.app_path_folder.parts)

        file_path = msg.open_file(default_dir=fol_reports, suffixes=[".sqlite"])

        if not file_path:
            msg.error(_("No file was selected."))
        else:
            if os.path.isfile(file_path):
                # try:
                champ.load_dbs(file_path)
                if not config.prefs['last_path_dbs']:
                    msg.error(_("The file is not a valid orcana dbs."))
                # except:
                    # msg.error(_("The file is not a valid orcana dbs."))
                

    def show_main(self):
        self.pn_properties.Hide()
        self.pn_events.Hide()
        self.pn_main.Show()

    def show_properties(self):
        self.pn_main.Hide()
        self.pn_events.Hide()
        self.pn_properties.Show()

    def show_events(self):
        self.pn_main.Hide()
        self.pn_properties.Hide()
        self.pn_events.Show()

    def about(self, config):
        info = adv.AboutDialogInfo()
        info.SetName(config.app_name)
        info.SetVersion(config.app_version)
        info.SetDescription(
            wordwrap(
                config.app_description,
                800,
                dc=wx.ClientDC(self), breakLongWords=False))
        info.SetCopyright(config.app_copyright)
        info.SetWebSite(
            config.app_web_site,
            _("{} website".format(config.app_name)))
        info.AddDeveloper(config.app_developer)
        info.AddTranslator(config.app_developer)
        info.License = wordwrap(config.app_license, 800,
                                wx.ClientDC(self))

        info.SetIcon(self.parent.view_plus.app_icon)
        adv.AboutBox(info=info, parent=self.parent)
