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
        self.name = "heats"
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
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
        self.view.load_splitter()

    def load_members(self):
        heat_view = {}
        heat_view['heat_pos'] = self.view.lsc_heats_plus.get_sel_pos_item()
        heat_view['result_cell_row'] = self.view.grd_results.GetGridCursorRow()
        heat_view['result_cell_col'] = self.view.grd_results.GetGridCursorCol()
        self.model.heats.config.views['heats'] = heat_view
        self.view.lsc_heats_plus.save_custom_column_width()
        from modules.relay_members import p_relay_members
        p_relay_members.create(parent=self, relay_members=self.model.result.relay.relay_members)

    def view_refresh(self):
        event_id = self.view.get_event_id()

    def select_lane(self, row):
        self.view.btn_members.Enable(False)
        self.view.btn_change_participant.Enable(False)
        heat = self.model.heat
        if row != -1:
            if not heat.official:
                self.view.btn_change_participant.Enable(True)
            lane = int(self.view.grd_results.GetRowLabelValue(row))
            result = heat.get_result(lane=lane)
            # print('lane: {}'.format(lane))
            if result:
                self.model.result = result
                if result.ind_rel == 'R':
                    self.view.btn_members.Enable(True)
            else:
                self.model.result = None
        self.view.grd_results.SelectRow(row=row)

    def select_members(self):
        row = self.view.grd_results.GetGridCursorRow()
        # self.view.btn_members.Enable(False)
        # self.view.btn_change_participant.Enable(False)
        heat = self.model.heat
        if not heat.official and row != -1:
            lane = int(self.view.grd_results.GetRowLabelValue(row))
            result = heat.get_result(lane=lane)
            if self.view.btn_members.IsEnabled():
                self.load_members()

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

            row = self.view.grd_results.GetGridCursorRow()
            # print('select_heat, results cusor row: {}'.format(row))
            sel_rows = self.view.grd_results.GetSelectedRows()
            # print('select_heat, results selected rows: {}'.format(sel_rows))

            self.view.load_heat_grid(heat)
            row = self.view.grd_results.GetGridCursorRow()
            # self.view.grd_results.SelectRow(row)
            self.select_lane(row=row)

            if heat.official:
                self.view.grd_results.EnableEditing(False)
                # self.view.btn_members.Enable(False)
            else:
                self.view.grd_results.EnableEditing(True)
                # self.toggle_members_button(row=row)
        else:
            self.model.results = None

    def gen_results_report(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            phase = self.model.heats[pos].phase
            if phase.official:
                # print('is official')
                phase.gen_results_report()
            else:
                self.view.msg.error(message=_("Heats must be in official status."))

    def gen_medals_report(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            phase = self.model.heats[pos].phase
            selections = self.view.select_phase_medals(phase=phase)
            # print(selections)
            if selections:
                process = True
                official_selections = []
                for i in selections:
                    if not phase.phases[i].official:
                        message=_("Ignoring not official phases.")
                    else:
                        official_selections.append(i)
                if message:
                    self.view.msg.error(message=message)
                if official_selections:
                    phase.champ.gen_medals_report(selections)

    def gen_start_list_report(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            phase = self.model.heats[pos].phase
            phase.report_start_list_pdf()

    def phase_category_results(self):
        pos = self.view.lsc_heats_plus.get_sel_pos_item()
        if pos is not None:
            phase = self.model.heats[pos].phase
            if phase.official:
                # print('is official')
                # Garda a siguación do formulario actual (heats)
                heats_view = {}
                heats_view['heat_pos'] = self.view.lsc_heats_plus.get_sel_pos_item()
                heats_view['result_cell_row'] = self.view.grd_results.GetGridCursorRow()
                heats_view['result_cell_col'] = self.view.grd_results.GetGridCursorCol()
                self.model.heats.config.views['heats'] = heats_view
                self.view.lsc_heats_plus.save_custom_column_width()
                # Fin garda a siguación do formulario actual (heats)
                phase_category_result_view = {}
                phase_category_result_view['phase_id'] = phase.phase_id
                phase_category_result_view['phase_category_id'] = phase.phase_categories[0].phase_category_id
                self.model.heats.config.views['phase_category_results'] = phase_category_result_view
                from modules.phase_category_results import p_phase_category_results
                p_phase_category_results.create(parent=self, champ=phase.champ)
            else:
                self.view.msg.error(message=_("Only available for official phases."))

    def gen_classifications_report(self):
        champ = self.model.heats.champ
        champ.gen_classifications_pdf()

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
                ind_rel = heat.phase.ind_rel
                empty_members_relay = False
                pending_results = False
                for i in results:
                    if not i.mark_hundredth and not i.issue_id:
                        pending_results = True
                        break
                    if ind_rel == 'R' and not i.issue_id and not i.relay.has_set_members:
                        empty_members_relay = True
                        break
                if pending_results:
                    self.view.msg.error(
                        message=_("There are results pending completion."))
                    self.view.grd_results.EnableEditing(True)
                elif empty_members_relay:
                    self.view.msg.warning(
                        message=_("No be able set official without add all relay members."))
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
        result = heat.get_result(lane=lane)
        if heat and result:
            # self.model.result = result
            if result.ind_rel == 'I':
                # print('Individual result')
                num_col_fixe = self.view.cols["ind_num_col_fixe"]
                col_arrival_mark = self.view.cols["ind_col_arrival_mark"]
                col_arrival_pos = self.view.cols["ind_col_arrival_pos"]
                col_issue_id = self.view.cols["ind_col_issue_id"]
                col_issue_split = self.view.cols["ind_col_issue_split"]
            elif result.ind_rel == 'R':
                # print('Relay result')
                num_col_fixe = self.view.cols["rel_num_col_fixe"]
                # rel_col_members = self.view.cols["rel_col_members"]
                col_arrival_mark = self.view.cols["rel_col_arrival_mark"]
                col_arrival_pos = self.view.cols["rel_col_arrival_pos"]
                col_issue_id = self.view.cols["rel_col_issue_id"]
                col_issue_split = self.view.cols["rel_col_issue_split"]
            value = self.view.grd_results.GetCellValue(row, col).strip()
            # print("value: {}".format(value))
            if col == col_arrival_mark or col >= num_col_fixe:  # Is split mark time
                count_splits = len(result.result_splits)
                col_last_split = num_col_fixe + count_splits -1
                if col == col_arrival_mark or col == col_last_split:  # final mark time
                    # distance = count_splits * 50  
                    split = result.result_splits[-1]
                    split.mark_time = value  
                    self.view.grd_results.SetCellValue(row, col_arrival_mark, split.mark_time)
                    self.view.grd_results.SetCellValue(row, col_last_split , split.mark_time)
                    self.view.update_arrival_pos(heat)
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
                self.view.update_arrival_pos(heat)
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
            # print('non se atopou o resultado')
            pass
        # print("fin update result")

    def res_change(self):
        row = self.view.grd_results.GetSelectedRows()[0]
        # print('row presenter {}'.format(row))
        heat = self.get_heat()
        lane = int(self.view.grd_results.GetRowLabelValue(row))
        result = heat.get_result(lane=lane)
        result_index = -1           
        if self.model.heat.ind_rel == 'I':
            from modules.res_ind_add_edit import p_res_ind_add_edit
            p_res_ind_add_edit.create(parent=self, heat=heat, lane=lane, result=result)
            self.select_heat()
            # self.view.update_result_lane(row=row, result=result)
            self.view.update_arrival_pos(heat)
        elif self.model.heat.ind_rel == 'R':
            from modules.res_rel_add_edit import p_res_rel_add_edit
            p_res_rel_add_edit.create(parent=self, heat=heat, lane=lane, result=result)
            # FIXME: o de abaixo ten que actualizar igual que nas individuais
            # o motivo é que o cambio pode implicar outra estaxe da mesma serie
            self.select_heat()
            # self.view.update_result_lane(row=row, result=result)
            self.view.update_arrival_pos(heat)
        # Isto é porque o obxexto result cambia o id ó ir ó formulario res_rel_add_edit
        print('En teoría o de abaixo xa non fai falta')
        # if result.result_id and result_index != -1 and result != heat.results[result_index]:
        #     heat.results[result_index] = result
        self.select_lane(row=row)

