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

    def report_heats_pdf(self):
        self.model.champ.report_start_list_pdf()

    def report_heats_html(self):
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

    def load_fiarna(self):
        from modules.fiarna import p_fiarna
        p_fiarna.create(parent=self, champ=self.model.champ)

    def save_params(self):
        values = self.view.get_values()
        msg = None
        pool_lanes_sort_validated = self.model.champ.validade_pool_lanes_sort(values['champ_pool_lanes_sort'])
        if not values['champ_name']:
            msg = 'Set a champ name.'
            self.view.txt_champ_name.SetFocus()
        elif not values['champ_pool_length']:
            msg = 'Set a pool length.'
            self.view.cho_pool_length.SetFocus()
        elif not pool_lanes_sort_validated:
            msg = 'Set a pool lanes sort.'
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
            self.model.champ.params.set_value('champ_name', values['champ_name'])
            self.model.champ.params.set_value('champ_pool_length', values['champ_pool_length'])
            self.model.champ.params.set_value('champ_pool_lanes_sort', pool_lanes_sort_validated)
            self.model.champ.params.set_value('champ_chrono_type', values['champ_chrono_type'])
            self.model.champ.params.set_value('champ_estament_id', values['champ_estament_id'])
            self.model.champ.params.set_value('champ_date_age_calculation', values['champ_date_age_calculation'])
            self.model.champ.params.set_value('champ_venue', values['champ_venue'])

            if 'champ_pool_lanes_sort' in self.model.champ.params.changed:
                message = _("Do you want to establish this ordering of the estates in all phases?")
                if self.view.msg.question(message=message):
                    self.model.champ.phases.set_champ_pool_lanes_sort()
            self.model.champ.params.save()
        return msg

    def go_back(self):
        msg = self.save_params()
        if not msg:
            self.parent.load_me()
