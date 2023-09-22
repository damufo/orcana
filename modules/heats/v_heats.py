# -*- coding: utf-8 -*-


import re
import wx
from wx.core import Colour

from .w_heats import Heats
from classes.wxp.view_plus import ViewPlus
from classes.wxp.messages import Messages

from .custom_grid import CustomColLabelRenderer
from .custom_grid import CustomGrid
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
        # set cols
        self.cols = {}
        self.cols["ind_num_col_fixe"] = 7
        self.cols["ind_col_arrival_mark"] = 3
        self.cols["ind_col_arrival_pos"] = 4
        self.cols["ind_col_issue_id"] = 5
        self.cols["ind_col_issue_split"] = 6
        self.cols["rel_num_col_fixe"] = 8
        self.cols["rel_col_members"] = 3
        self.cols["rel_col_arrival_mark"] = 4
        self.cols["rel_col_arrival_pos"] = 5
        self.cols["rel_col_issue_id"] = 6
        self.cols["rel_col_issue_split"] = 7

        self.first_split_col = 0
        self.col_arrival_mark = 0

        self.spl_heats.SetName('spl_heats')
        self.spl_heats_plus = self.parent.get_spl_plus(spl=self.spl_heats, parent=self)
        # self.spl_persons_plus.load_custom_sashpos()
        # load_custom_sashpos execútase 300 milisegundos despois de iniciarse
        # Do contrario non funciona
        wx.CallLater (500, self.spl_heats_plus.load_custom_sashpos)

    def load_heat_grid(self, heat):
        self.heat = heat
        ind_rel = heat.ind_rel
        if ind_rel == 'I':
            print('Individual heat')
            num_col_fixe = self.cols["ind_num_col_fixe"]
            col_arrival_mark = self.cols["ind_col_arrival_mark"]
            col_arrival_pos = self.cols["ind_col_arrival_pos"]
            col_issue_id = self.cols["ind_col_issue_id"]
            col_issue_split = self.cols["ind_col_issue_split"]
        elif ind_rel == 'R':
            print('Relay heat')
            num_col_fixe = self.cols["rel_num_col_fixe"]
            col_members = self.cols["rel_col_members"]
            col_arrival_mark = self.cols["rel_col_arrival_mark"]
            col_arrival_pos = self.cols["rel_col_arrival_pos"]
            col_issue_id = self.cols["rel_col_issue_id"]
            col_issue_split = self.cols["rel_col_issue_split"]        
        
        # Estas liñas de abaixo úsanse no interactor en OnKeyDown
        self.first_split_col = num_col_fixe
        self.col_arrival_mark = col_arrival_mark

        self.grd_results.SetGridLineColour(Colour(wx.WHITE))
        self.grd_results.SetGridLineColour(Colour(wx.LIGHT_GREY))
        self.grd_results.SetSelectionMode(wx.grid.Grid.SelectRows)  # By line
        self.grd_results.DisableDragRowSize()  # prevent row resize in height

        results = heat.results
        # if not len(results):
        #     self.grd_results.Hide()
        #     self.msg.warning(_("No exists results in this heat."))
            
        # else:
        # self.grd_results.Show()
        total_lanes = self.grd_results.GetNumberRows()
        pool_lanes_count = heat.phase.pool_lanes_count
        if total_lanes > pool_lanes_count:
            self.grd_results.DeleteRows(0, total_lanes - pool_lanes_count)
        elif total_lanes < pool_lanes_count:
            self.grd_results.InsertRows(0, pool_lanes_count - total_lanes)
        # header splits
        
        # count_splits = len(results[0].result_splits)
        event_splits = heat.event.splits
        count_splits = len(event_splits)

        current_cols = self.grd_results.GetNumberCols()
        required_cols = num_col_fixe + count_splits
        
        if current_cols > required_cols:
            self.grd_results.DeleteCols(num_col_fixe -1, current_cols - required_cols)
        elif current_cols < required_cols:
            self.grd_results.InsertCols(current_cols - 1, required_cols - current_cols)
        (DISTANCE, SPLIT_CODE, OFFICIAL) = range(3)
        for i, event_split in enumerate(event_splits):
            col = num_col_fixe + i
            self.grd_results.SetColLabelValue(col, str(event_split[DISTANCE]))
            self.grd_results.SetColSize(col, 100)
        self.grd_results.ClearGrid()
        if pool_lanes_count != 10:
            pool_lane_adjust = 1
        else:
            pool_lane_adjust = 0
        # Header
        self.grd_results.SetColLabelValue(0, _('Full name'))
        self.grd_results.SetColSize(0, 400)
        self.grd_results.SetColLabelValue(1, _('Entity'))
        self.grd_results.SetColSize(1, 200)
        self.grd_results.SetColLabelValue(2, _('Category'))
        self.grd_results.SetColSize(2, 100)
        if ind_rel == 'R':
            self.grd_results.SetColLabelValue(col_members, _('Members'))
            self.grd_results.SetColSize(col_members, 100)
        self.grd_results.SetColLabelValue(col_arrival_mark, _('Mark'))
        self.grd_results.SetColSize(col_arrival_mark, 100)
        self.grd_results.SetColLabelValue(col_arrival_pos, _('Pos.'))
        self.grd_results.SetColSize(col_arrival_pos, 80)
        self.grd_results.SetColLabelValue(col_issue_id, _('Issue'))
        self.grd_results.SetColSize(col_issue_id, 150)
        self.grd_results.SetColLabelValue(col_issue_split, _('I. S.')) # Issue split
        self.grd_results.SetColSize(col_issue_split, 80)
        results_dict = {}
        for i in results:
            results_dict[i.lane] = i
        for lane in range(0, pool_lanes_count):
            lane_adjusted = (lane + pool_lane_adjust)
            if lane_adjusted in results_dict:
                result = results_dict[lane_adjusted]
                choices_list = heat.config.issues.choices()
                choice_editor = wx.grid.GridCellChoiceEditor(choices_list, allowOthers=False) 
                self.grd_results.SetCellEditor(lane, col_issue_id, choice_editor)
                if ind_rel == 'I':
                    self.grd_results.SetCellValue(lane, 0, result.person.full_name)
                    self.grd_results.SetCellValue(lane, 1, str(result.person.entity.short_name))
                elif ind_rel == 'R':
                    self.grd_results.SetCellValue(lane, 0, result.relay.name)
                    self.grd_results.SetCellValue(lane, 1, str(result.relay.entity.short_name))
                    if result.relay.has_set_members:
                        has_set_members = '√'  # square root
                    else:
                        has_set_members = ''
                    self.grd_results.SetCellValue(lane, col_members, has_set_members)
                    self.grd_results.SetCellAlignment(lane, col_members, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grd_results.SetCellAlignment(lane, 1, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grd_results.SetCellValue(lane, 2, str(result.category_code))
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
                self.grd_results.SetReadOnly(lane, 2)  # Category code
                if ind_rel == 'R':
                    self.grd_results.SetReadOnly(lane, col_members)  # members
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
        if results and self.chb_go_to_first.GetValue():
            row = self.grd_results.GetGridCursorRow()
            col = self.grd_results.GetGridCursorCol()
            if col != col_arrival_mark:
                col = num_col_fixe # first_split_col
            self.grd_results.SetGridCursor(results[0].lane - pool_lane_adjust, col)
        
        # ALIÑADO PERSONALIZADO PARA COLUMNA
        # ADAPTA O ALIÑAMENTO INDIVIDUAL/REMUDA
        bg = self.grd_results.GetLabelBackgroundColour()
        col_render = CustomColLabelRenderer(color=bg, ind_rel=ind_rel)
        self.grd_results.SetDefaultColLabelRenderer(col_render)

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
            ind_rel = heat.ind_rel
            if ind_rel == 'I':
                print('Individual heat')
                num_col_fixe = self.cols["ind_num_col_fixe"]
                col_arrival_mark = self.cols["ind_col_arrival_mark"]
                col_arrival_pos = self.cols["ind_col_arrival_pos"]
                col_issue_id = self.cols["ind_col_issue_id"]
                col_issue_split = self.cols["ind_col_issue_split"]
            elif ind_rel == 'R':
                print('Relay heat')
                num_col_fixe = self.cols["rel_num_col_fixe"]
                col_members = self.cols["rel_col_members"]
                col_arrival_mark = self.cols["rel_col_arrival_mark"]
                col_arrival_pos = self.cols["rel_col_arrival_pos"]
                col_issue_id = self.cols["rel_col_issue_id"]
                col_issue_split = self.cols["rel_col_issue_split"] 
            self.first_split_col = num_col_fixe
            count_splits = len(result.result_splits)
            
            # choices_list = ("", "BAI", "NPR", "RET", "DVI", "DNI", "DSA")
            choices_list = heat.config.issues.choices()
            choice_editor = wx.grid.GridCellChoiceEditor(choices_list, allowOthers=False) 
            self.grd_results.SetCellEditor(row, col_issue_id, choice_editor)
            if ind_rel == 'I':
                self.grd_results.SetCellValue(row, 0, result.person.full_name)
                self.grd_results.SetCellValue(row, 1, str(result.person.entity.short_name))
            elif ind_rel == 'R':
                self.grd_results.SetCellValue(row, 0, result.relay.name)
                self.grd_results.SetCellValue(row, 1, str(result.relay.entity.short_name))
                if result.relay.relay_members.has_set_members:
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

    def load_arrival_order(self, results):
        arrival_order = ''
        arrival_pos_sorted = sorted(results, key=attrgetter('arrival_pos'), reverse=False)
        for i in arrival_pos_sorted:
            if i.arrival_pos:
                arrival_order += ' {}'.format(i.lane)
        self.lbl_arrival_order.SetLabel(arrival_order)

    def update_arrival_pos(self, heat):
        results = heat.results
        
        ind_rel = heat.ind_rel

        if ind_rel == 'I':
            print('Individual heat')
            num_col_fixe = self.cols["ind_num_col_fixe"]
            col_arrival_mark = self.cols["ind_col_arrival_mark"]
            col_arrival_pos = self.cols["ind_col_arrival_pos"]
            col_issue_id = self.cols["ind_col_issue_id"]
            col_issue_split = self.cols["ind_col_issue_split"]
        elif ind_rel == 'R':
            print('Relay heat')
            num_col_fixe = self.cols["rel_num_col_fixe"]
            col_members = self.cols["rel_col_members"]
            col_arrival_mark = self.cols["rel_col_arrival_mark"]
            col_arrival_pos = self.cols["rel_col_arrival_pos"]
            col_issue_id = self.cols["rel_col_issue_id"]
            col_issue_split = self.cols["rel_col_issue_split"] 
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
                self.grd_results.SetCellValue(i.lane-1, col_arrival_pos, '')
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
                self.grd_results.SetCellValue(i.lane-1, col_arrival_pos, str(pos))
            if save_result:
                results_dict[i.lane].save()
        self.lbl_arrival_order.SetLabel(arrival_order)
        print("lbl arival positions")

    def close(self):
        self.lsc_heats_plus.save_custom_column_width()
        print("save splitter: ", self.spl_heats.GetSashPosition())
        self.spl_heats_plus.save_custom_sashpos()
