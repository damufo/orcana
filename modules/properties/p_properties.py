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
        self.model.champ.auto_gen_heats()

    def report_inscriptions(self):
        self.model.champ.report_inscriptions_by_club()
        self.model.champ.report_inscriptions_by_event()
        self.model.champ.report_sumary_participants()

    def report_heats_pdf(self):
        self.model.champ.report_start_list_pdf()

    def report_heats_html(self):
        self.model.champ.report_start_list_html()

    def fiarna(self):
        from modules.fiarna import p_fiarna
        p_fiarna.create(parent=self, config=self.model.champ.config)

    def go_back(self):
        self.view.get_values(champ=self.model.champ)
        self.model.champ.save()
        self.parent.load_me()
