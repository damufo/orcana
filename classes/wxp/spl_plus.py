# -*- coding: utf-8 -*-


import wx


class SplPlus(object):
    '''
    extend wx.SplitterWindow
    '''
    prefs = None

    def __init__(self, spl, view, values=None):
        self.spl = spl  # listcontrol
        self.view = view  # view for messages
        self.values = values  # object type list with function list_fields
        self.sashpos = None

        # self.lsc.Bind(wx.EVT_RIGHT_DOWN, self.menu_contextual)
        # self.lsc.Bind(wx.EVT_LIST_COL_CLICK, self.on_header_click)

    def load_custom_sashpos(self):
        sashpos = self.prefs.get_value(
            '{}.{}.sashpos'.format(self.view.Name, self.spl.Name))
        if sashpos:
            self.sashpos = int(sashpos)
            self.spl.SetSashPosition(int(sashpos))
        else:
            self.sashpos = self.spl.GetSashPosition()
        print("load splitter: ", self.spl.GetSashPosition())

    # def reload_custom_sashpos(self):
    #     sashpos = self.prefs.get_value(
    #         '{}.{}.sashpos'.format(self.view.Name, self.spl.Name))
    #     if sashpos:
    #         self.spl.SetSashPosition(int(sashpos))

    def save_custom_sashpos(self):
        sashpos = str(self.spl.GetSashPosition())
        if sashpos:
            self.prefs.set_value(
                '{}.{}.sashpos'.format(self.view.Name, self.spl.Name),
                sashpos)
        self.prefs.save()

    # def load_header(self, custom_column_widths=False):
    #     # lsc = self.lsc
    #     # lsc.ClearAll()
    #     # values = self.values
    #     # NAME, ALIGN, WIDTH = range(3)
    #     # # Load header
    #     # for i, j in enumerate(values.list_fields):
    #     #     if j[ALIGN] == 'L':
    #     #         wx_align = wx.LIST_FORMAT_LEFT
    #     #     elif j[ALIGN] == 'C':
    #     #         wx_align = wx.LIST_FORMAT_CENTER
    #     #     elif j[ALIGN] == 'R':
    #     #         wx_align = wx.LIST_FORMAT_RIGHT

    #     #     if self.column_widths_custom:
    #     #         width = self.column_widths_custom[i]
    #     #     else:
    #     #         width = j[WIDTH]

    #     #     if i == 0:
    #     #         lsc.InsertColumn(i, j[NAME], width=width)
    #     #         fila_cero = wx.ListItem()
    #     #         fila_cero.SetAlign(wx_align)
    #     #         lsc.SetColumn(i, fila_cero)
    #     #     else:
    #     #         lsc.InsertColumn(i, j[NAME], wx_align, width=width)

    #     if custom_column_widths:
    #         self.load_custom_column_width()
    #     lsc = self.lsc
    #     lsc.ClearAll()
    #     list_fields = self.values.list_fields
    #     NAME, ALIGN, WIDTH = range(3)
    #     # Load header
    #     for i, j in enumerate(list_fields):
    #         if j[ALIGN] == 'L':
    #             wx_align = wx.LIST_FORMAT_LEFT
    #         elif j[ALIGN] == 'C':
    #             wx_align = wx.LIST_FORMAT_CENTER
    #         elif j[ALIGN] == 'R':
    #             wx_align = wx.LIST_FORMAT_RIGHT
    #         # try:
    #         if self.column_widths_custom:
    #             width = self.column_widths_custom[i]
    #         else:
    #         # except:
    #             width = j[WIDTH]
    #         if i == 0:
    #             lsc.InsertColumn(i, j[NAME], width=width)
    #             fila_cero = wx.ListItem()
    #             fila_cero.SetAlign(wx_align)
    #             lsc.SetColumn(i, fila_cero)
    #         else:
    #             lsc.InsertColumn(i, j[NAME], wx_align, width=width)
        


    # def load(self, pos_ini=None, warning_much_items=True, custom_column_widths=False):
        
    #     if pos_ini is None:
    #         pos_ini = self.get_sel_pos_item()
    #     self.load_header(custom_column_widths=custom_column_widths)
    #     values = self.values
    #     if values:
    #         limit_to_show = -1
    #         if warning_much_items and self.view and len(values) > 500:
    #             message = (
    #                 _("This search return %s items, do you like\n"
    #                   "show only first 500 items?") % len(values))
    #             if self.view.msg.question(message=message):
    #                 limit_to_show = 500
    #         # Load values
    #         for i, j in enumerate(values.list_values):
    #             if i == limit_to_show:
    #                 break
    #             for k, line in enumerate(j):
    #                 if not isinstance(line, str):
    #                     if isinstance(line, (int, float)):
    #                         line = str(line)
    #                     else:
    #                         # when value is None or False
    #                         line = ''
    #                 # first column
    #                 if k == 0:
    #                     pos = self.lsc.InsertItem(i, line or '')
    #                 else:
    #                     self.lsc.SetItem(pos, k, line or '')
    #         if pos_ini != -1 and pos_ini is not None:
    #             self.set_sel_pos_item(pos=pos_ini)

    # def add_last_item(self):
    #     lsc = self.lsc
    #     values = self.values
    #     if len(values) != lsc.GetItemCount():
    #         #  Suponse que o novo é o último
    #         i = len(values.list_values)-1
    #         j = values.list_values[i]
    #         pos_ini = i
    #         for k, line in enumerate(j):
    #             if not isinstance(line, str):
    #                 if isinstance(line, int):
    #                     line = str(line)
    #                 elif isinstance(line, float):
    #                     pass
    #                 else:
    #                     line = ''
    #             # first column
    #             if k == 0: 
    #                 pos = lsc.InsertItem(i, line or '')
    #             else:
    #                 lsc.SetItem(pos, k, line or '')
    #         if pos_ini != -1 and pos_ini is not None:
    #             self.set_sel_pos_item(pos=pos_ini)

    # def update_item(self, idx):
    #     '''
    #     Set values for item list
    #     '''
    #     values = self.values.list_values[idx]
    #     for k, line in enumerate(values):
    #         if not isinstance(line, str):
    #             if isinstance(line, int):
    #                 line = str(line)
    #             elif isinstance(line, float):
    #                 line = str(line)
    #             else:
    #                 line = ''
    #         self.lsc.SetItem(idx, k, line or '')

    # def update_items(self, idxs):
    #     '''
    #     Set values for items list
    #     '''
    #     for i in idxs:
    #         self.update_item(i)

    # def delete_item(self, idx):
    #     """
    #     Delete a item of position (integer)
    #     """
    #     self.lsc.DeleteItem(idx)

    # def delete_items(self, idxs):
    #     """
    #     Delete items of positions (iterable with integers)
    #     """
    #     for i in sorted(idxs, reverse=True):
    #         self.delete_item(i)

    # def set_sel_pos_item(self, pos):
    #     """
    #     Set select a position (integer)
    #     """
    #     self.lsc.Freeze()
    #     for i in range(self.lsc.GetItemCount()):
    #         self.lsc.Select(i, on=0)

    #     if self.lsc.GetItemCount() > 0 and self.lsc.GetItemCount() > pos:
    #         self.lsc.Select(pos)
    #         self.lsc.Focus(pos)
    #         print('focus: {}'.format(pos))
    #         self.lsc.EnsureVisible(pos)
    #     self.lsc.Thaw()

    # def set_sel_pos_item_last(self):
    #     """
    #     Set select a position (integer)
    #     """
    #     self.set_sel_pos_item(self.lsc.GetItemCount()-1)

    # def set_sel_pos_items(self, pos):
    #     '''
    #     Pos is a list of positions
    #     '''
    #     pass

    # def get_sel_pos_item(self):
    #     """
    #     Return integer select a list position
    #     """
    #     value = None
    #     if self.lsc.GetFirstSelected() != -1:  # GetFocusedItem not work fine
    #         value = self.lsc.GetFirstSelected()
    #     return value

    # def get_sel_pos_items(self, reverse=False):
    #     '''
    #     Return a list of selected positions (integer)
    #     '''
    #     idxs = []
    #     for i in range(self.lsc.GetItemCount()):
    #         if self.lsc.IsSelected(i):
    #             idxs.append(i)
    #     if reverse:
    #         idxs = sorted(idxs, reverse=True)
    #     return idxs

    # def export(self, event, all_items=True, encoding='utf-8-sig'):
    #     '''
    #     Export rows
    #     '''
    #     lines = []
    #     if self.values and self.values.list_values:
    #         list_values = self.values.list_values
    #         for i in range(self.lsc.GetItemCount()):
    #             if all_items or (not all_items and self.lsc.IsSelected(i)):
    #                 line = list_values[i]
    #                 value = []
    #                 for j in line:
    #                     if not j:
    #                         value_field = ""
    #                     elif isinstance(j, str):
    #                         value_field = j
    #                     else:
    #                         value_field = str(j)
    #                     value.append(value_field)
    #                 lines.append('#'.join(value))
    #         file_path = self.view.msg.save_file(filter_='csv')
    #         if file_path:
    #             file_path = file_path[0]
    #             file_export = open(file_path, 'w', encoding=encoding)
    #             for i in lines:
    #                 file_export.write('%s\n' % i)
    #             file_export.close()
    #     event.Skip()

    # def menu_contextual(self, event):
    #     popup = wx.Menu()
    #     all_items = wx.MenuItem(popup, wx.NewId(), _('Export all items'))
    #     selected_items = wx.MenuItem(
    #         popup, wx.NewId(), _('Export selected items'))
    #     popup.Append(all_items)
    #     popup.Append(selected_items)
    #     popup.Bind(wx.EVT_MENU, lambda event: self.export(
    #         event=event, all_items=True), id=all_items.GetId())
    #     popup.Bind(wx.EVT_MENU, lambda event: self.export(
    #         event=event, all_items=False), id=selected_items.GetId())
    #     self.lsc.PopupMenu(popup, event.GetPosition())
    #     event.Skip()
