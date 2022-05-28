# -*- coding: utf-8 -*-


# Version: 20200604


from pathlib import Path
import wx
from wx import adv


class Messages:
    """
    Class messages as box dialog
    """

    def __init__(self, view):
        self.view = view

    def entry(self, message, caption=None, value=''): 
        if not caption:
            caption = self.view.GetTitle()
        dlg = wx.TextEntryDialog(
            parent=self.view,
            message=message,
            caption=caption,
            value=value,
            # style=TextEntryDialogStyle,
            # pos=DefaultPosition
            )
        if dlg.ShowModal() == wx.ID_OK:
            value = dlg.GetValue()
        else:
            value = False
        dlg.Destroy()
        return value

    def error(self, message, caption=None):
        '''Show a error message dialog'''
        self._message_dialog(
            message=message,
            caption=caption,
            style=wx.ICON_ERROR | wx.OK)

    def information(self, message, caption=None):
        '''Show a information message dialog'''
        self._message_dialog(
            message=message,
            caption=caption,
            style=wx.ICON_INFORMATION | wx.OK)

    def warning(self, message, caption=None):
        '''Show a warning message dialog'''
        self._message_dialog(
            message=message,
            caption=caption,
            style=wx.ICON_WARNING | wx.OK)

    def choice(self, title, question, values):
        """
        choide dialog
        """
        dlg = wx.SingleChoiceDialog(self.view, question, self.view.GetTitle(),
                                    values, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            value = (dlg.GetSelection(),  dlg.GetStringSelection())
        else:
            value = None
        dlg.Destroy()
        self.view.SetFocus()
        print(self.view.GetName())
        return value

    def question(self, message, caption=None):
        '''Show a question message dialog
        
        If YES, return True'''
        result = self._message_dialog(
            message=message,
            caption=caption,
            style=wx.ICON_QUESTION | wx.YES_NO)
        return result
            
    def _message_dialog(self, message, caption=None, style=None):
        '''Show a message dialog'''
        if not caption:
            caption = self.view.GetTitle()
        mns = wx.MessageDialog(
            parent=self.view, 
            message=message,
            caption=caption,
            style=style)
        if mns.ShowModal() == wx.ID_YES:
            value = True
        else:
            value = False
        mns.Destroy()
        return value

    def open_file(self, message=None, default_dir=".", default_file="", suffixes=[".*"]):
        '''
        suffixes is a list of suffixes example: ('.jpg', '.png') 
        '''
        if not message:
            message = _("Browse...")

        file_path = self._file_dialog(
            message=message,
            default_dir=default_dir,
            default_file=default_file,
            suffixes=suffixes,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        return file_path

    def save_file(self, message=None, default_dir=".", default_file="", suffixes=[".*"]):
        if not message:
            message = _("Save as...")
        file_path = self._file_dialog(
            message=message,
            default_dir=default_dir,
            default_file=default_file,
            suffixes=suffixes,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        return file_path

    def _file_dialog(self, message, default_dir, default_file, suffixes, style):
        '''
        wildcard format, tuple(text, suffix)
        '''
        # FIXME: wildcard for Mac OS X https://docs.wxpython.org/wx.FileDialog.html
        # wildcard = "File (*.jpeg,*.png)|*.jpeg;*.png"
        # wildcard = "BMP and GIF files (*.bmp;*.gif)|*.bmp;*.gif|PNG files (*.png)|*.png"
        suffixes = ['*{}'.format(i) for i in suffixes]
        wildcard = "Files ({})|{}".format(','.join(suffixes), ';'.join(suffixes))
        dlg = wx.FileDialog(
            self.view,
            message=message,
            defaultDir=default_dir,
            defaultFile=default_file,
            wildcard=wildcard,
            style=style)
        if dlg.ShowModal() == wx.ID_OK:
            file_path = Path(dlg.GetPath())
        else:
            file_path = None
        dlg.Destroy()
        return file_path
