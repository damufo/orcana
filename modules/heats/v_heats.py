# -*- coding: utf-8 -*-


import re
import wx
from wx.core import Colour

from .w_heats import Heats
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages

from .custom_grid import CustomColLabelRenderer
from operator import itemgetter, attrgetter



class View(Heats):
    def __init__(self, parent):
        Heats.__init__(self, parent=parent)
        self.SetName('heats')
        self.parent = parent
        self.parent.load_panel(panel=self)
        self.lsc_heats_plus = self.parent.get_lsc_plus(
            lsc=self.lsc_heats, parent=self)
        self.lsc_heats.SetName('heats')
        self.view_plus = ViewPlus(self)
        self.msg = Messages(self.parent)
        self.first_split_col = 7

    def load_heat_grid(self, heat):

        if heat.ind_rel == 'I':
            print('Individual heat')
            num_col_fixe = 7
            col_arrival_mark = 3
            col_arrival_pos = 4
            col_issue_id = 5
            col_issue_split = 6
        elif heat.ind_rel == 'R':
            print('Relay heat')
            num_col_fixe = 8
            col_members = 3
            col_arrival_mark = 4
            col_arrival_pos = 5
            col_issue_id = 6
            col_issue_split = 7        
        
        self.first_split_col = num_col_fixe

        self.grd_results.SetGridLineColour(Colour(wx.WHITE))
        self.grd_results.SetGridLineColour(Colour(wx.LIGHT_GREY))
        self.grd_results.SetSelectionMode(wx.grid.Grid.SelectRows)  # By line
        self.grd_results.DisableDragRowSize()  # prevent row resize in height

        results = heat.results
        total_lanes = self.grd_results.GetNumberRows()
        pool_lanes = heat.phase.pool_lanes
        if total_lanes > pool_lanes:
            self.grd_results.DeleteRows(0, total_lanes - pool_lanes)
        elif total_lanes < pool_lanes:
            self.grd_results.InsertRows(0, pool_lanes - total_lanes)
        # header splits
        count_splits = len(results[0].result_splits)

        current_cols = self.grd_results.GetNumberCols()
        required_cols = num_col_fixe + count_splits
        
        if current_cols > required_cols:
            self.grd_results.DeleteCols(num_col_fixe -1, current_cols - required_cols)
        elif current_cols < required_cols:
            self.grd_results.InsertCols(current_cols - 1, required_cols - current_cols)
        for i, split in enumerate(results[0].result_splits):
            col = num_col_fixe + i
            self.grd_results.SetColLabelValue(col, str(split.distance))
            self.grd_results.SetColSize(col, 100)
        self.grd_results.ClearGrid()
        if pool_lanes != 10:
            pool_lane_adjust = 1
        else:
            pool_lane_adjust = 0
        # Header
        self.grd_results.SetColLabelValue(0, 'Full name')
        self.grd_results.SetColSize(0, 400)
        self.grd_results.SetColLabelValue(1, 'Entity')
        self.grd_results.SetColSize(1, 200)
        self.grd_results.SetColLabelValue(2, 'Category')
        self.grd_results.SetColSize(2, 100)
        if heat.ind_rel == 'R':
            self.grd_results.SetColLabelValue(col_members, 'Members')
            self.grd_results.SetColSize(col_members, 100)
        self.grd_results.SetColLabelValue(col_arrival_mark, 'Mark')
        self.grd_results.SetColSize(col_arrival_mark, 100)
        self.grd_results.SetColLabelValue(col_arrival_pos, 'Pos.')
        self.grd_results.SetColSize(col_arrival_pos, 80)
        self.grd_results.SetColLabelValue(col_issue_id, 'Issue')
        self.grd_results.SetColSize(col_issue_id, 150)
        self.grd_results.SetColLabelValue(col_issue_split, 'I. S.') # Issue split
        self.grd_results.SetColSize(col_issue_split, 80)
        results_dict = {}
        for i in results:
            results_dict[i.lane] = i
        for lane in range(0, pool_lanes):
            lane_adjusted = (lane + pool_lane_adjust)
            if lane_adjusted in results_dict:
                result = results_dict[lane_adjusted]
                choices_list = heat.config.issues.choices()
                choice_editor = wx.grid.GridCellChoiceEditor(choices_list, allowOthers=False) 
                self.grd_results.SetCellEditor(lane, col_issue_id, choice_editor)
                if result.person:
                    self.grd_results.SetCellValue(lane, 0, result.person.full_name)
                    self.grd_results.SetCellValue(lane, 1, str(result.person.entity.short_name))
                elif result.relay:
                    self.grd_results.SetCellValue(lane, 0, result.relay.name)
                    self.grd_results.SetCellValue(lane, 1, str(result.relay.entity.short_name))
                    if result.result_members.has_set_members:
                        has_set_members = '√'
                    else:
                        has_set_members = ''
                    self.grd_results.SetCellValue(lane, col_members, has_set_members)
                    self.grd_results.SetCellAlignment(lane, col_members, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grd_results.SetCellAlignment(lane, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grd_results.SetCellValue(lane, 2, str(result.category.name))
                self.grd_results.SetCellAlignment(lane, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                if result.arrival_pos:
                    self.grd_results.SetCellValue(lane, col_arrival_pos, str(result.arrival_pos))
                else:
                    self.grd_results.SetCellValue(lane, col_arrival_pos, '')
                self.grd_results.SetCellAlignment(lane, col_arrival_pos, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grd_results.SetCellAlignment(lane, col_arrival_mark, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
                self.grd_results.SetCellValue(lane, col_issue_id, str(result.issue_id))
                self.grd_results.SetCellAlignment(lane, col_issue_id, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                if result.issue_id:
                    self.grd_results.SetCellValue(lane, col_issue_split, str(result.issue_split))
                else:
                    self.grd_results.SetCellValue(lane, col_issue_split, '')
                self.grd_results.SetCellAlignment(lane, col_issue_split, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grd_results.SetReadOnly(lane, 0)  # Name
                self.grd_results.SetReadOnly(lane, 1)  # Entity
                self.grd_results.SetReadOnly(lane, col_arrival_pos, False)
                self.grd_results.SetReadOnly(lane, col_arrival_mark, False)
                self.grd_results.SetReadOnly(lane, col_issue_id, False)
                self.grd_results.SetReadOnly(lane, col_issue_split, False)
                for i in range(count_splits):
                    split = result.result_splits[i]
                    col = num_col_fixe + i
                    self.grd_results.SetReadOnly(lane, col, False)
                    self.grd_results.SetCellAlignment(lane, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
                    self.grd_results.SetCellValue(lane, col, split.mark_time)
                # isto vai aquí porque colle o valor do último parcial para poñelo en arrival_time
                self.grd_results.SetCellValue(lane, col_arrival_mark, split.mark_time)
            else:
                for i in range(self.grd_results.GetNumberCols()):
                    self.grd_results.SetReadOnly(lane, i, True)
        self.load_arrival_order(results=results)

    def update_result_lane(self, row, result):
        # row = self.grd_results.GetGridCursorRow()
        if not result.result_id:
            # clear line
            print('clear line')
            current_cols = self.grd_results.GetNumberCols()
            for col in range(current_cols):
                self.grd_results.SetCellValue(row, col, '')
                self.grd_results.SetReadOnly(row, col, True)
        else:
            heat = result.heat
            if heat.ind_rel == 'I':
                print('Individual heat')
                num_col_fixe = 7
                col_arrival_mark = 3
                col_arrival_pos = 4
                col_issue_id = 5
                col_issue_split = 6
            elif heat.ind_rel == 'R':
                print('Relay heat')
                num_col_fixe = 8
                col_members = 3
                col_arrival_mark = 4
                col_arrival_pos = 5
                col_issue_id = 6
                col_issue_split = 7
            self.first_split_col = num_col_fixe
            count_splits = len(result.result_splits)
            
            # choices_list = ("", "BAI", "NPR", "RET", "DVI", "DNI", "DSA")
            choices_list = heat.config.issues.choices()
            choice_editor = wx.grid.GridCellChoiceEditor(choices_list, allowOthers=False) 
            self.grd_results.SetCellEditor(row, col_issue_id, choice_editor)
            if result.person:
                self.grd_results.SetCellValue(row, 0, result.person.full_name)
                self.grd_results.SetCellValue(row, 1, str(result.person.entity.short_name))
            elif result.relay:
                self.grd_results.SetCellValue(row, 0, result.relay.name)
                self.grd_results.SetCellValue(row, 1, str(result.relay.entity.short_name))
                if result.result_members.has_set_members:
                    has_set_members = '√'
                else:
                    has_set_members = ''
                self.grd_results.SetCellValue(row, col_members, has_set_members)
                self.grd_results.SetCellAlignment(row, col_members, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grd_results.SetCellAlignment(row, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grd_results.SetCellValue(row, 2, str(result.category.name))
            self.grd_results.SetCellAlignment(row, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            if result.arrival_pos:
                self.grd_results.SetCellValue(row, col_arrival_pos, str(result.arrival_pos))
            else:
                self.grd_results.SetCellValue(row, col_arrival_pos, '')
            self.grd_results.SetCellAlignment(row, col_arrival_pos, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grd_results.SetCellAlignment(row, col_arrival_mark, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
            self.grd_results.SetCellValue(row, col_issue_id, str(result.issue_id))
            self.grd_results.SetCellAlignment(row, col_issue_id, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            if result.issue_id:
                self.grd_results.SetCellValue(row, col_issue_split, str(result.issue_split))
            else:
                self.grd_results.SetCellValue(row, col_issue_split, '')
            self.grd_results.SetCellAlignment(row, col_issue_split, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            self.grd_results.SetReadOnly(row, 0)  # Name
            self.grd_results.SetReadOnly(row, 1)  # Entity
            self.grd_results.SetReadOnly(row, col_arrival_pos, False)
            self.grd_results.SetReadOnly(row, col_arrival_mark, False)
            self.grd_results.SetReadOnly(row, col_issue_id, False)
            self.grd_results.SetReadOnly(row, col_issue_split, False)
            # for i in range(start=1, stop=count_splits):
            for i in range(count_splits):
                split = result.result_splits[i]
                col = num_col_fixe + i
                self.grd_results.SetReadOnly(row, col, False)
                self.grd_results.SetCellAlignment(row, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
                self.grd_results.SetCellValue(row, col, split.mark_time)
            # isto vai aquí porque colle o valor do último parcial para poñelo en arrival_time
            self.grd_results.SetCellValue(row, col_arrival_mark, split.mark_time)

    # def load_heat_rel_grid____(self, heat):
    #     # self.grd_results.SetLabelBackgroundColour(Colour(wx.WHITE))
    #     self.grd_results.SetGridLineColour(Colour(wx.WHITE))
    #     self.grd_results.SetGridLineColour(Colour(wx.LIGHT_GREY))
    #     self.grd_results.SetSelectionMode(wx.grid.Grid.SelectRows)  # By line

    #     # self.grd_results.colLabels = ['a', 'b', 'c', 'd', 'e']
    #     # self.grd_results.rowLabels = ['a', 'b', 'c', 'd', 'e']
    #     # self.grd_results.SetRowLabelSize(0)
    #     # self.grd_results.SetColLabelSize(0)
    #     # self.grd_results.SetMargins(0,0)
    #     # self.grd_results.AutoSizeColumns(False)
        
    #     num_col_fixe = 6
    #     self.grd_results.InsertCols(0, num_col_fixe)
        
    #     total_lanes = self.grd_results.GetNumberRows()
    #     total_cols = self.grd_results.GetNumberCols()
        
    #     first_col_splits = num_col_fixe
    #     if total_cols > first_col_splits:
    #         self.grd_results.DeleteCols(first_col_splits, total_cols-first_col_splits)
    #     # self.grd_results.DeleteRows(0, total_lanes - 1)
        
    #     results = heat.results
    #     pool_lanes = 6
    #     if total_lanes > pool_lanes:
    #         self.grd_results.DeleteRows(0, total_lanes - pool_lanes)
    #     elif total_lanes < pool_lanes:
    #         self.grd_results.InsertRows(0, pool_lanes - total_lanes)
        
    #     # Load splits
    #     # for i in results:
    #     #     i.splits.load_items_from_dbs()
    #     # header splits
    #     count_splits = len(results[0].result_splits)
    #     self.grd_results.InsertCols(0, count_splits)
    #     for i, split in enumerate(results[0].result_splits):
    #         col = first_col_splits + i
    #         self.grd_results.SetColLabelValue(col, str(split.distance))
    #         self.grd_results.SetColSize(col, 100)
    #     self.grd_results.ClearGrid()
    #     # return
    #     # self.grd_results.EnableEditing(False)
    #     if pool_lanes != 10:
    #         pool_lane_adjust = 1
    #     else:
    #         pool_lane_adjust = 0
    #     # Header
    #     self.grd_results.SetColLabelValue(0, 'Full name')
    #     self.grd_results.SetColLabelValue(1, 'Entity')
    #     self.grd_results.SetColLabelValue(2, 'Category')
    #     self.grd_results.SetColLabelValue(3, 'Mark')
    #     self.grd_results.SetColLabelValue(4, 'Pos.')
    #     self.grd_results.SetColLabelValue(5, 'Issue')
    #     self.grd_results.SetColLabelValue(6, 'I. S.') # Issue split
    #     self.grd_results.SetColSize(0, 400)
    #     self.grd_results.SetColSize(1, 200)
    #     self.grd_results.SetColSize(2, 100)
    #     self.grd_results.SetColSize(3, 100)
    #     self.grd_results.SetColSize(4, 80)
    #     self.grd_results.SetColSize(5, 150)
    #     self.grd_results.SetColSize(6, 80)
    #     # self.grd_results.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
    #     # Colour(colour)
    #     results_dict = {}
    #     for i in results:
    #         results_dict[i.lane] = i

    #     for lane in range(0, pool_lanes):
    #         lane_adjusted = (lane + pool_lane_adjust)
    #         if lane_adjusted in results_dict:
    #             result = results_dict[lane_adjusted]
    #             # choices_list = ("", "BAI", "NPR", "RET", "DVI", "DNI", "DSA")
    #             choices_list = heat.config.issues.choices()
    #             # self.grd_results.SetCellValue(lane, 3, "")
    #             choice_editor = wx.grid.GridCellChoiceEditor(choices_list, False) 


    #             self.grd_results.SetCellEditor(lane, 5, choice_editor)


    #             # tChoiceEditor = wx.grid.GridCellChoiceEditor([], allowOthers=True)
    #             # self.grd_results.SetCellEditor(lane, 3, tChoiceEditor)
    #             # self.grd_results.list = [('spam', 42), ('eggs', 69)]
    #             # self.grd_results.SetCellValue(lane, 3, self.grd_results.list[0][0])

    #             # self.grd_results.SetCellValue(1, 1, 'A')
    #             # dict = {'A':'A    Description_of_A', 'B':'B    Description_of_B'}
    #             # self.grd_results.SetCellEditor(1, 1, CustomCellChoiceEditor(dict, true))


    #             if result.person:
    #                 self.grd_results.SetCellValue(lane, 0, result.person.full_name)
    #                 self.grd_results.SetCellValue(lane, 1, str(result.person.entity.short_name))
    #             elif result.relay:
    #                 self.grd_results.SetCellValue(lane, 0, result.relay.name)
    #                 self.grd_results.SetCellValue(lane, 1, str(result.relay.entity.short_name))
    #             self.grd_results.SetCellValue(lane, 2, str(result.category.name))
    #             if result.arrival_pos:
    #                 self.grd_results.SetCellValue(lane, 4, str(result.arrival_pos))
    #             else:
    #                 self.grd_results.SetCellValue(lane, 4, '')                    
    #             self.grd_results.SetCellValue(lane, 5, str(result.issue_id))
    #             if result.issue_id:
    #                 self.grd_results.SetCellValue(lane, 6, str(result.issue_split))
    #             else:
    #                 self.grd_results.SetCellValue(lane, 6, '')
    #             self.grd_results.SetCellAlignment(lane, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 3, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 4, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 5, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 6, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetReadOnly(lane, 0)  # Name
    #             self.grd_results.SetReadOnly(lane, 1)  # Entity
    #             for i in range(count_splits):
    #                 split = result.result_splits[i]
    #                 col = first_col_splits + i
    #                 self.grd_results.SetReadOnly(lane, col, False)
    #                 self.grd_results.SetCellAlignment(lane, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
    #                 # self.grd_results.SetCellBackgroundColour(lane, col, Colour(wx.WHITE))
    #                 self.grd_results.SetCellValue(lane, col, split.mark_time)
    #             # isto vai aquí porque colle o valor o último parcial para poñelo en arrival_time
    #             self.grd_results.SetCellValue(lane, 3, split.mark_time)


    #             # self.grd_results.SetCellValue(lane, 4, str(result.arrival_pos))
    #         else:
    #             for i in range(self.grd_results.GetNumberCols()):
    #                 self.grd_results.SetReadOnly(lane, i, True)
    #                 # self.grd_results.SetCellBackgroundColour(lane, i, wx.Colour(225, 225, 225 ))
            


    #     # self.grd_results.FreezeTo(2, 2)
    #     # self.grd_results.FreezeTo(0, 3)
    #     # self.grd_results.EnableEditing(True)
    #     print("dd")
    #     # gc_attr = wx.grid.GridCellAttr()
    #     # gc_attr.SetAlignment(wx.ALIGN_RIGHT, wx.
    #     # ALIGN_CENTRE)
    #     # self.grd_results.SetColAttr(2, gc_attr)
    #     bg = self.grd_results.GetLabelBackgroundColour()

    #     # col_render = CustomColLabelRenderer(bg)
    #     # self.grd_results.SetDefaultColLabelRenderer(col_render)

    #     self.load_arrival_order(results=results)
    #     # attr = wx.grid.GridCellAttr()
    #     # attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
    #     # self.grd_results.SetColAttr(2, attr)
    #     self.btn_members.Enable(False)

    # def load_heat_ind_rel_grid(self, heat):
    #     # self.grd_results.SetLabelBackgroundColour(Colour(wx.WHITE))
    #     self.grd_results.SetGridLineColour(Colour(wx.WHITE))
    #     self.grd_results.SetGridLineColour(Colour(wx.LIGHT_GREY))
    #     self.grd_results.SetSelectionMode(wx.grid.Grid.SelectRows)  # By line

    #     # self.grd_results.colLabels = ['a', 'b', 'c', 'd', 'e']
    #     # self.grd_results.rowLabels = ['a', 'b', 'c', 'd', 'e']
    #     # self.grd_results.SetRowLabelSize(0)
    #     # self.grd_results.SetColLabelSize(0)
    #     # self.grd_results.SetMargins(0,0)
    #     # self.grd_results.AutoSizeColumns(False)
        
    #     num_col_fixe = 6
    #     self.grd_results.InsertCols(0, num_col_fixe)
        
    #     total_lanes = self.grd_results.GetNumberRows()
    #     total_cols = self.grd_results.GetNumberCols()
        
    #     first_col_splits = num_col_fixe
    #     if total_cols > first_col_splits:
    #         self.grd_results.DeleteCols(first_col_splits, total_cols-first_col_splits)
    #     # self.grd_results.DeleteRows(0, total_lanes - 1)
        
    #     results = heat.results
    #     pool_lanes = 6
    #     if total_lanes > pool_lanes:
    #         self.grd_results.DeleteRows(0, total_lanes - pool_lanes)
    #     elif total_lanes < pool_lanes:
    #         self.grd_results.InsertRows(0, pool_lanes - total_lanes)
        
    #     # Load splits
    #     # for i in results:
    #     #     i.splits.load_items_from_dbs()
    #     # header splits
    #     count_splits = len(results[0].result_splits)
    #     self.grd_results.InsertCols(0, count_splits)
    #     for i, split in enumerate(results[0].result_splits):
    #         col = first_col_splits + i
    #         self.grd_results.SetColLabelValue(col, str(split.distance))
    #         self.grd_results.SetColSize(col, 100)
    #     self.grd_results.ClearGrid()
    #     # return
    #     # self.grd_results.EnableEditing(False)
    #     if pool_lanes != 10:
    #         pool_lane_adjust = 1
    #     else:
    #         pool_lane_adjust = 0
    #     # Header
    #     self.grd_results.SetColLabelValue(0, 'Full name')
    #     self.grd_results.SetColLabelValue(1, 'Entity')
    #     self.grd_results.SetColLabelValue(2, 'Category')
    #     self.grd_results.SetColLabelValue(3, 'Mark')
    #     self.grd_results.SetColLabelValue(4, 'Pos.')
    #     self.grd_results.SetColLabelValue(5, 'Issue')
    #     self.grd_results.SetColLabelValue(6, 'I. S.') # Issue split
    #     self.grd_results.SetColSize(0, 400)
    #     self.grd_results.SetColSize(1, 200)
    #     self.grd_results.SetColSize(2, 100)
    #     self.grd_results.SetColSize(3, 100)
    #     self.grd_results.SetColSize(4, 80)
    #     self.grd_results.SetColSize(5, 150)
    #     self.grd_results.SetColSize(6, 80)
    #     # self.grd_results.SetColLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
    #     # Colour(colour)
    #     results_dict = {}
    #     for i in results:
    #         results_dict[i.lane] = i

    #     for lane in range(0, pool_lanes):
    #         lane_adjusted = (lane + pool_lane_adjust)
    #         if lane_adjusted in results_dict:
    #             result = results_dict[lane_adjusted]
    #             # choices_list = ("", "BAI", "NPR", "RET", "DVI", "DNI", "DSA")
    #             choices_list = heat.config.issues.choices()
    #             # self.grd_results.SetCellValue(lane, 3, "")
    #             choice_editor = wx.grid.GridCellChoiceEditor(choices_list, False) 


    #             self.grd_results.SetCellEditor(lane, 5, choice_editor)


    #             # tChoiceEditor = wx.grid.GridCellChoiceEditor([], allowOthers=True)
    #             # self.grd_results.SetCellEditor(lane, 3, tChoiceEditor)
    #             # self.grd_results.list = [('spam', 42), ('eggs', 69)]
    #             # self.grd_results.SetCellValue(lane, 3, self.grd_results.list[0][0])

    #             # self.grd_results.SetCellValue(1, 1, 'A')
    #             # dict = {'A':'A    Description_of_A', 'B':'B    Description_of_B'}
    #             # self.grd_results.SetCellEditor(1, 1, CustomCellChoiceEditor(dict, true))


    #             if result.person:
    #                 self.grd_results.SetCellValue(lane, 0, result.person.full_name)
    #                 self.grd_results.SetCellValue(lane, 1, str(result.person.entity.short_name))
    #             elif result.relay:
    #                 self.grd_results.SetCellValue(lane, 0, result.relay.name)
    #                 self.grd_results.SetCellValue(lane, 1, str(result.relay.entity.short_name))
    #             self.grd_results.SetCellValue(lane, 2, str(result.category.name))
    #             if result.arrival_pos:
    #                 self.grd_results.SetCellValue(lane, 4, str(result.arrival_pos))
    #             else:
    #                 self.grd_results.SetCellValue(lane, 4, '')                    
    #             self.grd_results.SetCellValue(lane, 5, str(result.issue_id))
    #             if result.issue_id:
    #                 self.grd_results.SetCellValue(lane, 6, str(result.issue_split))
    #             else:
    #                 self.grd_results.SetCellValue(lane, 6, '')
    #             self.grd_results.SetCellAlignment(lane, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 2, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 3, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 4, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 5, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetCellAlignment(lane, 6, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
    #             self.grd_results.SetReadOnly(lane, 0)  # Name
    #             self.grd_results.SetReadOnly(lane, 1)  # Entity
    #             for i in range(count_splits):
    #                 split = result.result_splits[i]
    #                 col = first_col_splits + i
    #                 self.grd_results.SetReadOnly(lane, col, False)
    #                 self.grd_results.SetCellAlignment(lane, col, wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
    #                 # self.grd_results.SetCellBackgroundColour(lane, col, Colour(wx.WHITE))
    #                 self.grd_results.SetCellValue(lane, col, split.mark_time)
    #             # isto vai aquí porque colle o valor o último parcial para poñelo en arrival_time
    #             self.grd_results.SetCellValue(lane, 3, split.mark_time)


    #             # self.grd_results.SetCellValue(lane, 4, str(result.arrival_pos))
    #         else:
    #             for i in range(self.grd_results.GetNumberCols()):
    #                 self.grd_results.SetReadOnly(lane, i, True)
    #                 # self.grd_results.SetCellBackgroundColour(lane, i, wx.Colour(225, 225, 225 ))
            


    #     # self.grd_results.FreezeTo(2, 2)
    #     # self.grd_results.FreezeTo(0, 3)
    #     # self.grd_results.EnableEditing(True)
    #     print("dd")
    #     # gc_attr = wx.grid.GridCellAttr()
    #     # gc_attr.SetAlignment(wx.ALIGN_RIGHT, wx.
    #     # ALIGN_CENTRE)
    #     # self.grd_results.SetColAttr(2, gc_attr)
    #     bg = self.grd_results.GetLabelBackgroundColour()

    #     # col_render = CustomColLabelRenderer(bg)
    #     # self.grd_results.SetDefaultColLabelRenderer(col_render)

    #     self.load_arrival_order(results=results)
    #     # attr = wx.grid.GridCellAttr()
    #     # attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
    #     # self.grd_results.SetColAttr(2, attr)
    #     self.btn_members.Enable(False)


    def load_arrival_order(self, results):
        arrival_order = ''
        arrival_pos_sorted = sorted(results, key=attrgetter('arrival_pos'), reverse=False)
        for i in arrival_pos_sorted:
            if i.arrival_pos:
                arrival_order += ' {}'.format(i.lane)
        self.lbl_arrival_order.SetLabel(arrival_order)

    def update_arrival_pos(self, results):
        arrival_order = ''
        results_dict = {}
        for i in results:
            results_dict[i.lane] = i
        arrival_time_sorted = sorted(results, key=attrgetter('arrival_hundredth'), reverse=False)
        pos = 0
        last_arrival_hundredth = 0
        equated = 0
        # for i in [i for i in arrival_time_sorted if not i.issue_id]:
        for i in arrival_time_sorted:
            print("lane {} arrival_hundredth {}".format(i.lane, i.arrival_hundredth))
            save_result =  False
            if not i.arrival_hundredth or i.issue_id:
                results_dict[i.lane].arrival_pos = 0
                self.grd_results.SetCellValue(i.lane-1, 4, '')
            else:
                if i.arrival_hundredth != last_arrival_hundredth:
                    pos += 1 + equated
                    if results_dict[i.lane].arrival_pos != pos:
                        save_result =  True
                    results_dict[i.lane].arrival_pos = pos
                    last_arrival_hundredth = i.arrival_hundredth
                    equated = 0
                else:
                    if results_dict[i.lane].arrival_pos != pos:
                        save_result =  True
                    results_dict[i.lane].arrival_pos = pos
                    equated += 1
                arrival_order += ' {}'.format(i.lane) 
                self.grd_results.SetCellValue(i.lane-1, 4, str(pos))
            if save_result:
                results_dict[i.lane].save()
        self.lbl_arrival_order.SetLabel(arrival_order)
        print("lbl arival positions")

    def close(self):
        self.lsc_heats_plus.save_custom_column_width()
        # self.lsc_results_plus.save_custom_column_width()
        # self.lsc_splits_plus.save_custom_column_width()
