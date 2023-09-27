# -*- coding: utf-8 -*-


import wx
import wx.grid
from wx.core import Colour

class Interactor(object):

    def install(self, presenter, view):
        self.presenter = presenter
        self.view = view
        view.parent.Bind(wx.EVT_CLOSE, self.go_back)
        view.btn_back.Bind(wx.EVT_BUTTON, self.go_back)
        # view.lsc.Bind(wx.EVT_LEFT_DCLICK, self.on_edit)
        view.btn_members.Bind(wx.EVT_BUTTON, self.load_members)
        view.btn_phase_category_results.Bind(wx.EVT_BUTTON, self.phase_category_results)
        view.btn_results_report.Bind(wx.EVT_BUTTON, self.gen_results_report)
        view.btn_classifications_report.Bind(wx.EVT_BUTTON, self.gen_classifications_report)
        view.btn_official.Bind(wx.EVT_BUTTON, self.toggle_official)
        view.btn_next.Bind(wx.EVT_BUTTON, self.go_next_heat)
        view.lsc_heats.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_select_heat)
        view.lsc_heats.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_select_heat)
        view.lsc_heats.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_select_heat)



        view.grd_results.Bind(wx.EVT_MOTION, self.OnMotion)
        # view.grd_results.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnGrid1GridRangeSelect)
        view.grd_results.Bind(wx.grid.EVT_GRID_RANGE_SELECTING, self.OnGrid1GridRangeSelect)


        view.grd_results.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self.OnGrid1GridEditorHidden)
        view.grd_results.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.on_grid_select_cell)
        view.grd_results.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.on_select_members)
        # view.grd_results.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.on_grid_select_cell)
        view.grd_results.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        view.btn_change_participant.Bind(wx.EVT_BUTTON, self.res_change)

    def res_change(self, event):
        self.presenter.res_change()

    def load_members(self, event):
        self.presenter.load_members()

    def OnKeyDown(self, event):
        first_split_col = self.view.first_split_col
        col_arrival_mark = self.view.col_arrival_mark

        if event.GetKeyCode() != wx.WXK_RETURN:
            event.Skip()
            return

        if event.ControlDown():   # the edit control needs this key
            event.Skip()
            return

        self.view.grd_results.DisableCellEditControl()
        col = self.view.grd_results.GetGridCursorCol()
        if col == col_arrival_mark:
            print("Move down")
            success = self.view.grd_results.MoveCursorDown(event.ShiftDown())
            set_col = col_arrival_mark
        else:
            print("Move first split")
            success = self.view.grd_results.MoveCursorRight(event.ShiftDown())
            set_col = first_split_col

        if not success:
            newRow = self.view.grd_results.GetGridCursorRow() + 1

            if newRow < self.view.grd_results.GetTable().GetNumberRows():
                self.view.grd_results.SetGridCursor(newRow, set_col)
                self.view.grd_results.MakeCellVisible(newRow, set_col)
            else:
                # this would be a good place to add a new row if your app
                # needs to do that
                pass

    def OnGrid1GridRangeSelect(self, event):
        # disable drag selection by mouse
        row = self.view.grd_results.GetGridCursorRow()
        self.view.grd_results.SelectRow(row=row)

    def OnMotion(self, event):
        # just trap this event and prevent it from percolating up the window hierarchy
        pass

    def OnGrid1GridEditorHidden(self, event):
        print("ola caracola")
        row = event.Row
        col = event.Col
        self.presenter.update_result(col, row)
    
    def on_grid_select_cell(self, event):
        print("ola caracola2")
        row = event.Row
        col = event.Col
        print('row interactor {}'.format(row))
        # self.presenter.toggle_members_button(row=row)
        self.presenter.select_lane(row=row)
        
    def on_select_members(self, event):
        # print("ola caracola2")
        # row = event.Row
        col = event.Col
        
        # print('row interactor {}'.format(row))
        # # self.presenter.toggle_members_button(row=row)
        # self.presenter.select_lane(row=row)
        if col < 4:
            self.presenter.select_members()

    # def change_colum_width(self, event):
    #     self.view.lsc_splits_plus.save_custom_column_width()

    def go_next_heat(self, event):
        self.presenter.go_next_heat()

    def gen_results_report(self, event):
        self.presenter.gen_results_report()

    def gen_classifications_report(self, event):
        self.presenter.gen_classifications_report()

    def phase_category_results(self, event):
        self.presenter.phase_category_results()

    def toggle_official(self, event):
        self.presenter.toggle_official()

    def go_back(self, event):
        self.presenter.go_back()
        # if event.CanVeto():
            # event.Veto()
            # return

    def on_select_heat(self, event):
        self.presenter.select_heat()
        # event.Skip()
        # self.view.grd_results.SetFocus()

    # def on_select_result(self, event):
    #     self.presenter.select_result()
    #     event.Skip()

    # def on_select_results(self, event):
    #     pos = self.view.lsc_results.FocusedItem()
    #     print(pos)
    #     color_sel = Colour(wx.LIGHT_GREY)
    #     color_all = Colour(wx.WHITE)
    #     bold_font = wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString )
    #     normal_font = wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString )
    #     for i in range(self.view.lsc_results.GetItemCount()):
    #         self.view.lsc_results.SetItemBackgroundColour(i, color_all)
    #         self.view.lsc_results.SetItemFont(i, normal_font)

    #     if pos:
    #         # self.view.lsc_results.Select(pos, on=0)
    #         print("is selected: {}".format(self.view.lsc_results.IsSelected(pos)))
    #         self.view.lsc_results.Focus(pos)
    #         self.view.lsc_results.SetItemBackgroundColour(pos, color_sel)
    #         self.view.lsc_results.SetItemFont(pos, bold_font)

    #     event.Skip()

    def on_select_results_focused(self, event):
        pos = self.view.lsc_results.FocusedItem
        print(pos)
        color_sel = Colour(wx.LIGHT_GREY)
        color_all = Colour(wx.WHITE)
        bold_font = wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString )
        normal_font = wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString )
        for i in range(self.view.lsc_results.GetItemCount()):
            self.view.lsc_results.SetItemBackgroundColour(i, color_all)
            self.view.lsc_results.SetItemFont(i, normal_font)
            self.view.lsc_results.Select(i, on=0)
        if pos:
            print("is selected: {}".format(self.view.lsc_results.IsSelected(pos)))
            self.view.lsc_results.Focus(pos)
            self.view.lsc_results.SetItemBackgroundColour(pos, color_sel)
            self.view.lsc_results.SetItemFont(pos, bold_font)
        event.Skip()

    def on_refresh(self, event):
        self.presenter.view_refresh()
        event.Skip()

