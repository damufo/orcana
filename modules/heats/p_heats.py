# -*- coding: utf-8 -*-


from wx.core import NO
from .m_heats import Model
from .v_heats import View
from .i_heats import Interactor


def create(parent, heats):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(heats=heats),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.model.heats.load_items_from_dbs()
        self.view.lsc_heats_plus.values = self.model.heats
        self.view.lsc_heats_plus.load(custom_column_widths=True)
        if 'heats' in self.model.heats.config.views:
            heat_pos = self.model.heats.config.views['heats']['heat_pos']
            result_cell_row = self.model.heats.config.views['heats']['result_cell_row']
            result_cell_col = self.model.heats.config.views['heats']['result_cell_col']
            self.view.lsc_heats_plus.set_sel_pos_item(heat_pos)
            self.view.grd_results.SetGridCursor(row=result_cell_row, col=result_cell_col)
            self.view.grd_results.SelectRow(row=result_cell_row)
            self.view.grd_results.SetFocus()
        else:
            self.view.lsc_heats_plus.set_sel_pos_item(0)
        # self.view_refresh()

    def load_members(self):
        heat_view = {}
        heat_view['heat_pos'] = self.view.lsc_heats_plus.get_sel_pos_item()
        heat_view['result_cell_row'] = self.view.grd_results.GetGridCursorRow()
        heat_view['result_cell_col'] = self.view.grd_results.GetGridCursorCol()
        self.model.heats.config.views['heats'] = heat_view
        self.view.lsc_heats_plus.save_custom_column_width()
        from modules.result_members import p_result_members
        p_result_members.create(parent=self, result_members=self.model.result.result_members)


    def view_refresh(self):
        event_id = self.view.get_event_id()

    def toggle_members_button__(self, row):
        # row = self.view.grd_results.GetGridCursorRow()
        # print('row presenter {}'.format(row))
        self.view.btn_members.Enable(False)
        # self.model.result = None
        if row != -1:
            heat = self.model.heat
            if heat.ind_rel == 'R':
                if not heat.official:
                    lane = int(self.view.grd_results.GetRowLabelValue(row))
                    print('lane {}'.format(lane))
                    result = heat.results.get_result(lane=lane)
                    if result:
                        self.model.result = result
                        self.view.btn_members.Enable(True)
                    else:
                        self.model.result = None
                        print('non hai resultado')
                else:
                    print('isto non debería producirse')
        else:
            print('isto nunca debería pasar')

    def select_lane(self, row):
        self.view.btn_members.Enable(False)
        self.view.btn_change_participant.Enable(False)
        heat = self.model.heat
        if not heat.official and row != -1:
            lane = int(self.view.grd_results.GetRowLabelValue(row))
            result = heat.results.get_result(lane=lane)
            print('lane: {}'.format(lane))
            self.view.btn_change_participant.Enable(True)
            if result:
                self.model.result = result
                if result.ind_rel == 'R':
                    self.view.btn_members.Enable(True)
            else:
                self.model.result = None
        self.view.grd_results.SelectRow(row=row)


        

    def go_back(self):
        if 'heats' in self.model.heats.config.views:
            del self.model.heats.config.views['heats']
        self.view.close()
        self.parent.load_me()

    def get_heat(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        heat = None
        if pos is not None:
            heat = self.model.heats[pos]
        return heat

    def select_heat(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            heat = self.model.heats[pos]
            self.model.heat = heat
            self.model.results = heat.results
            heat.results.load_items_from_dbs()
            
            # for i in heat.results:
            #     i.result_splits.load_items_from_dbs()

            row = self.view.grd_results.GetGridCursorRow()
            print('select_heat, results cusor row: {}'.format(row))
            sel_rows = self.view.grd_results.GetSelectedRows()
            print('select_heat, results selected rows: {}'.format(sel_rows))

            self.view.load_heat_grid(heat)
            row = self.view.grd_results.GetGridCursorRow()
            # self.view.grd_results.SelectRow(row)
            self.select_lane(row=row)

            if heat.official:
                self.view.grd_results.EnableEditing(False)
                self.view.btn_members.Enable(False)
            else:
                self.view.grd_results.EnableEditing(True)
                # self.toggle_members_button(row=row)
        else:
            self.model.results = None


    # def fhase_is_official____(self):
    #     # aproveitar de aquí para imprimir o resultado, a parte de comprobar se todos está oficial
    #     pos = self.view.lsc_heats_plus.get_sel_pos_item()
    #     if pos is not None:
    #         heat = self.model.heats[pos]
    #         if heat.official:
    #             heat.official = 0
    #             self.view.lsc_heats_plus.update_item(pos)
    #         else:
    #             phase_id = heat.phase.phase_id
    #             pending_heats = True
    #             for i in heat.heats:
    #                 if i.phase.phase_id == phase_id:
    #                     for j in i.results:
    #                         if not j.mark_hundredth and not j.issue_id:
    #                             pending_heats = True
    #                             break
    #                     if pending_heats:
    #                         break
    #             if pending_heats:
    #                 self.view.msg.error(message=_("There are heats pending completion."))
    #             else:
    #                 heat.official = 1
    #                 self.view.lsc_heats_plus.update_item(pos)

    def gen_results_report(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            phase = self.model.heats[pos].phase
            if phase.official:
                print('is official')
                phase.gen_results_pdf()
            else:
                self.view.msg.error(message=_("Heats must be in official status."))

    def gen_clasifications_report(self):
        champ = self.model.heats.champ
        champ.gen_clasifications_pdf()

    def go_next_heat(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        self.view.lsc_heats_plus.set_sel_pos_item(pos+1)

    def toggle_official(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            heat = self.model.heats[pos]
            if heat.official:
                heat.official = 0
                self.view.lsc_heats_plus.update_item(pos)
                self.view.grd_results.EnableEditing(True)
                heat.save()
                row = self.view.grd_results.GetGridCursorRow()
                # self.view.grd_results.SelectRow(row)
                # self.toggle_members_button(row=row)
                self.select_lane(row=row)
                heat.phase.delete_results_phase_categories()
            else:
                results = heat.results
                pending_results = False
                for i in results:
                    if not i.mark_hundredth and not i.issue_id:
                        pending_results = True
                        break
                if pending_results:
                    self.view.msg.error(message=_("There are results pending completion."))
                    self.view.grd_results.EnableEditing(True)
                else:
                    heat.official = 1
                    heat.save()
                    self.view.lsc_heats_plus.update_item(pos)
                    self.view.grd_results.EnableEditing(False)
                    self.view.btn_members.Enable(False)
                    self.view.btn_change_participant.Enable(False)
                    if heat.phase.official:
                        heat.phase.calculate_results()

    def update_result(self, col, row):
        heat = self.get_heat()
        lane = int(self.view.grd_results.GetRowLabelValue(row))
        result = heat.results.get_result(lane=lane)
        if heat and result:
            # self.model.result = result
            if result.ind_rel == 'I':
                print('Individual result')
                num_col_fixe = self.view.cols["ind_num_col_fixe"]
                col_arrival_mark = self.view.cols["ind_col_arrival_mark"]
                col_arrival_pos = self.view.cols["ind_col_arrival_pos"]
                col_issue_id = self.view.cols["ind_col_issue_id"]
                col_issue_split = self.view.cols["ind_col_issue_split"]
            elif result.ind_rel == 'R':
                print('Relay result')
                num_col_fixe = self.view.cols["rel_num_col_fixe"]
                # rel_col_members = self.view.cols["rel_col_members"]
                col_arrival_mark = self.view.cols["rel_col_arrival_mark"]
                col_arrival_pos = self.view.cols["rel_col_arrival_pos"]
                col_issue_id = self.view.cols["rel_col_issue_id"]
                col_issue_split = self.view.cols["rel_col_issue_split"]
            value = self.view.grd_results.GetCellValue(row, col).strip()
            print("value: {}".format(value))
            if col == col_arrival_mark or col >= num_col_fixe:  # Is split mark time
                count_splits = len(result.result_splits)
                col_last_split = num_col_fixe + count_splits -1
                if col == col_arrival_mark or col == col_last_split:  # final mark time
                    # distance = count_splits * 50  
                    split = result.result_splits[-1]
                    split.mark_time = value  
                    self.view.grd_results.SetCellValue(row, col_arrival_mark, split.mark_time)
                    self.view.grd_results.SetCellValue(row, col_last_split , split.mark_time)
                    self.view.update_arrival_pos(result.results)
                    # result.save()
                else:
                    # distance = (col - num_col_fixe) * 50
                    split = result.result_splits[(col - num_col_fixe)]
                    split.mark_time = value
                    # split = result.result_splits.set_value(value=value, distance=distance)
                    # distance = split.distance
                    self.view.grd_results.SetCellValue(row, col, split.mark_time)
                split.save()
            elif col == col_arrival_pos:  # Set arrive_pos
                if value.isdigit():
                    result.arrival_pos = int(value)
                else:
                    result.arrival_pos = 0
                if not result.arrival_pos:
                    self.view.grd_results.SetCellValue(row, col_arrival_pos , "")
                else:
                    self.view.grd_results.SetCellValue(row, col_arrival_pos , str(result.arrival_pos))
                result.save()
            elif col == col_issue_id:  # Set issue id
                result.issue_id = value
                if not result.issue_id:
                    result.issue_split = 0
                    self.view.grd_results.SetCellValue(row, col_issue_split , "")
                if result.issue_id and not result.issue_split:
                    result.issue_split = 1
                    self.view.grd_results.SetCellValue(row, col_issue_split , str(1))
                self.view.update_arrival_pos(result.results)
                result.save()
            elif col == col_issue_split:  # Set issue split
                if result.issue_id:
                    value = int(value)
                    if value > 0 and value <= len(result.result_splits):
                        result.issue_split = value
                        self.view.grd_results.SetCellValue(row, col_issue_split , str(value))
                    else:
                        result.issue_split = 1
                        self.view.grd_results.SetCellValue(row, col_issue_split , "1")
                else:
                    result.issue_split = 0
                    self.view.grd_results.SetCellValue(row, col_issue_split , "")
                result.save()
        else:
            print('non se atopou o resultado')
        print("fin update result")

    def res_change(self):
        row = self.view.grd_results.GetGridCursorRow()
        # print('row presenter {}'.format(row))
        heat = self.get_heat()
        lane = int(self.view.grd_results.GetRowLabelValue(row))
        result = heat.results.get_result(lane=lane)
        result_index = -1           
        if not result:
            result = heat.results.item_blank
            result.lane = lane
            if result.ind_rel == 'R':
                result.relay = result.champ.relays.item_blank
        else:
            result_index = heat.results.index(result)
        if self.model.heat.ind_rel == 'I':
            from modules.res_ind_add_edit import p_res_ind_add_edit
            p_res_ind_add_edit.create(parent=self, result=result)
            self.view.update_result_lane(row=row, result=result)
            self.view.update_arrival_pos(heat.results)
        elif self.model.heat.ind_rel == 'R':
            from modules.res_rel_add_edit import p_res_rel_add_edit
            p_res_rel_add_edit.create(parent=self, result=result)
            self.view.update_result_lane(row=row, result=result)
            self.view.update_arrival_pos(heat.results)
        # Isto é porque o obxexto result cambia o id ó ir ó formulario res_rel_add_edit
        if result.result_id and result_index != -1 and result != heat.results[result_index]:
            heat.results[result_index] = result
        self.select_lane(row=row)

