# -*- coding: utf-8 -*-


from .m_properties import Model
from .v_properties import View
from .i_properties import Interactor


def create(parent, champ):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(champ=champ),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(champ=self.model.champ)
        # self.view.view_plus.start(modal=True)

    def gen_champ_auto(self):
        message = _('This action reset all results, delete relay members...'
            'Only current inscriptions will be considered to redo all.')
        self.view.msg.warning(message=message)
        self.model.champ.gen_heats()

    def report_inscriptions(self):
        self.model.champ.report_inscriptions_by_club()
        self.model.champ.report_inscriptions_by_event()
        self.model.champ.report_sumary_participants()

    def report_sart_list_pdf(self):
        self.model.champ.report_start_list_pdf()

    def report_sart_list_html(self):
        self.model.champ.report_start_list_html()

    def gen_web_forms_files(self):
        self.model.champ.gen_web_forms_files()

    def load_classifications(self):
        # Check if changes in fields
        print('Check if changes in fields')
        # if changes:
        #     question if save changes
        from modules.classifications import p_classifications
        p_classifications.create(parent=self, classifications=self.model.champ.classifications)

    def load_punctuations(self):
        msg = self.save_params()
        if not msg:
            from modules.punctuations import p_punctuations
            p_punctuations.create(parent=self, punctuations=self.model.champ.punctuations)

    def load_sessions(self):
        msg = self.save_params()
        if not msg:
            from modules.sessions import p_sessions
            p_sessions.create(parent=self, sessions=self.model.champ.sessions)

    def load_fiarna(self):
        from modules.fiarna import p_fiarna
        p_fiarna.create(parent=self, champ=self.model.champ)

    def save_params(self):
        values = self.view.get_values()
        msg = None
        champ = self.model.champ
        pool_lanes_sort_validated = champ.validade_pool_lanes_sort(values['champ_pool_lanes_sort'])
        if not values['champ_name']:
            msg = 'Set a champ name.'
            self.view.txt_champ_name.SetFocus()
        elif not values['champ_pool_length']:
            msg = 'Set a pool length.'
            self.view.cho_pool_length.SetFocus()
        elif not pool_lanes_sort_validated:
            msg = 'Set a valid pool lanes sort.'
            self.view.txt_pool_lanes_sort.SetFocus()
        elif not values['champ_chrono_type']:
            msg = 'Set a chrono type.'
            self.view.cho_chrono_type.SetFocus()
        elif not values['champ_estament_id']:
            msg = 'Set a estament.'
            self.view.cho_estament_id.SetFocus()
        elif not values['champ_date_age_calculation']:
            msg = 'Set a date age calculation.'
            self.view.txt_date_age_calculation.SetFocus()
        elif not values['champ_venue']:
            msg = 'Set a venue.'
            self.view.txt_venue.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            champ.params.set_value('champ_name', values['champ_name'])
            champ.params.set_value('champ_pool_length', values['champ_pool_length'])
            champ.params.set_value('champ_pool_lanes_sort', pool_lanes_sort_validated)
            champ.params.set_value('champ_chrono_type', values['champ_chrono_type'])
            champ.params.set_value('champ_estament_id', values['champ_estament_id'])
            champ.params.set_value('champ_date_age_calculation', values['champ_date_age_calculation'])
            champ.params.set_value('champ_venue', values['champ_venue'])
            # if 'champ_pool_lanes_sort' in champ.params.changed:
            #     message = _("Do you want to establish this lanes sort for all phases?")
            #     if self.view.msg.question(message=message):
            #         champ.phases.set_champ_pool_lanes_sort()
            champ.params.save()
        print("Atras")
        return msg

    def set_sort_to_phases(self):
        champ = self.model.champ
        if champ.params['champ_pool_lanes_sort']:
            message = _("Do you want to establish this lanes sort for all phases?")
            if self.view.msg.question(message=message):
                champ.phases.set_champ_pool_lanes_sort()
        else:
            message = _("No lanes sort is set.")
            self.view.msg.warning(message)

    def set_pool_lanes_sort(self):
        champ = self.model.champ
        txt_champ_pool_lanes_sort = self.view.txt_pool_lanes_sort.GetValue().strip()
        pool_lanes_sort_validated = self.model.champ.validade_pool_lanes_sort(
                txt_champ_pool_lanes_sort)
        if pool_lanes_sort_validated !=  champ.params['champ_pool_lanes_sort']:
            champ.params.set_value('champ_pool_lanes_sort', pool_lanes_sort_validated)
        self.view.txt_pool_lanes_sort.SetValue(pool_lanes_sort_validated)

    # def set_pool_lanes_sort(self):
    #     txt_champ_pool_lanes_sort = self.view.txt_pool_lanes_sort.GetValue().strip()
    #     msg = None
    #     pool_lanes_sort_validated = self.model.champ.validade_pool_lanes_sort(
    #             txt_champ_pool_lanes_sort)
    #     if not pool_lanes_sort_validated:
    #         msg = 'Set a valid pool lanes sort.'
    #         # self.view.txt_pool_lanes_sort.SetFocus()
    #         self.view.msg.warning(msg)
    #         # self.view.txt_pool_lanes_sort.ChangeValue(self.model.champ.params['champ_pool_lanes_sort'])
    #     else:
    #         self.view.txt_pool_lanes_sort.ChangeValue(pool_lanes_sort_validated)
    #         if pool_lanes_sort_validated != self.model.champ.params['champ_pool_lanes_sort']:
    #             message = _("Do you want to establish this lanes sort for all phases?")
    #             self.model.champ.params.set_value('champ_pool_lanes_sort', pool_lanes_sort_validated)
    #             self.model.champ.params.save()
    #             if self.view.msg.question(message=message):
    #                 self.model.champ.phases.set_champ_pool_lanes_sort()

    def go_back(self):
        msg = self.save_params()
        if not msg:
            self.parent.load_me()
