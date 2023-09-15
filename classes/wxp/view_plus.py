# -*- coding: utf-8 -*-

import wx

class ViewPlus(object):
    '''
    prefs is a prefs file
    '''
    prefs = None
    app_icon = None
    image_path = None

    def __init__(self, view):
        self.view = view
    
    def set_value(self, key, value):
        '''
        overload prefs set_value
        save the value addin to key the view name
        '''
        key = '{}.{}'.format(self.view.Name, key)
        self.prefs.set_value(key, value)

    def get_value(self, key):
        '''
        overload prefs get_value
        get the value for key of the view name
        '''
        key = '{}.{}'.format(self.view.Name, key)
        return self.prefs.get_value(key)

    def view_get_pos_size(self):
        name = self.view.Name
#        position
        pos_x = self.view.GetPosition()[0]
        pos_y = self.view.GetPosition()[1]
        self.set_value('pos_x', pos_x)
        self.set_value('pos_y', pos_y)
#        size
        width = self.view.Size.width
        height = self.view.Size.height
        self.set_value('width', width)
        self.set_value('height', height)

    def view_set_pos_size(self):
        name = self.view.Name

#        size
        width = self.get_value('width')
        height = self.get_value('height')
        if width and height:
            self.view.SetSize(wx.Size(width, height))
#        position
        pos_x = self.get_value('pos_x')
        pos_y = self.get_value('pos_y')
        if pos_y and pos_y:
            scr_width, scr_height = self.get_display_size()
            if (pos_x + width) <= scr_width and (pos_y + height) <= scr_height:
                self.view.SetPosition(wx.Point(pos_x, pos_y))
        else:
            self.view.CenterOnScreen()
#        icon
        self.view.SetIcon(self.app_icon)

    def get_display_size(self):
            width, height = wx.GetDisplaySize() 
            return (width, height)

    def cho_get(self, choice):
        '''
        Get choice client data
        '''
        value = None
        if len(choice.Items):
            if choice.GetSelection() != -1:  # add for wxpython < 2.8
                value = choice.GetClientData(choice.GetSelection())  # wx 2.8
        return value

    def cho_set(self, choice, value):
        '''
        set values when same client data
        '''
        for i in range(choice.GetCount()):
            if str(choice.GetClientData(i)) == str(value):
                choice.Select(i)
                break

    def cho_load(self, choice, values, default=None):
        '''
        for wxchoice
        set a choice with client data value
        '''
        choice.Clear()
        for i in values:
            choice.Append(item=i[0], clientData=i[1])
        if default is not None:
            self.cho_set(choice, default)

    def clb_load(self, choice, values, default=[]):
        '''
        For wxchecklistbox
        set a choices with client data value
        default, list
        '''
        choice.Clear()
        for i in values:
            choice.Append(item=i[0], clientData=i[1])
        if default is not None:
            for j in default:
                self.clb_set(choice, j)
        
    def clb_set(self, choice, value):
        '''
        For wxchecklistbox
        set value when same client data
        value is a clientData id
        '''
        for i in range(choice.GetCount()):
            if str(choice.GetClientData(i)) == str(value):
                choice.Check(i)
                break

    def clb_get(self, choice):
        '''
        For wxchecklistbox
        Get list with choice client data
        '''
        values = []
        if len(choice.Items):
            if choice.GetCheckedItems() != -1:  # add for wxpython < 2.8
                for i in choice.GetCheckedItems():
                    values.append(choice.GetClientData(i))  # wx 2.8
        return values


    def start(self, modal=False):
        self.view_set_pos_size()
        if modal:
            self.view.ShowModal()
        else:
            self.view.Show()

    def stop(self):
        self.view_get_pos_size()
        self.prefs.save()
        self.view.Destroy()

    def set_button_image(self, button_image):
        for button, image in button_image:
            button_image_path = str(self.image_path / image)
            button.SetBitmap(wx.Bitmap(button_image_path, wx.BITMAP_TYPE_ANY))
