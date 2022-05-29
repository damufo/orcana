# -*- coding: utf-8 -*-


from .m_entities import Model
from .v_entities import View
from .i_entities import Interactor


def create(parent, entities):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(entities=entities),
            view=View(parent.main_frame),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        # self.model.entities.load_items_from_dbs()
        self.view.lsc_plus.values = self.model.entities
        self.view.lsc_plus.load(custom_column_widths=True)
        # self.view.set_values(prefs=self.model.prefs)
        # self.view.view_plus.start(modal=True)

    # def acept(self):
    #     self.view.get_values(prefs=self.model.prefs)
    #     self.model.prefs.save()
    #     self.view.view_plus.stop()

    def go_back(self):
        self.view.close()
        self.parent.load_me()

    def add(self):
        entities = self.model.entities
        entity = entities.item_blank
        entity.lock = []
        from modules.entity_add_edit import p_entity_add_edit
        p_entity_add_edit.create(parent=self, entity=entity)
        if entity.entity_id:  # foi engadida
            self.view.lsc_plus.add_last_item()
            self.view.lsc.EnsureVisible(len(entities) - 1)

    def edit(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if len(idxs) < 1:
            self.view.msg.warning(message=_("No item selected."))
        elif len(idxs) > 1:
            self.view.msg.warning(message=_("Only one item can be selected."))
        else:
            idx = idxs[0]
            entity = self.model.entities[idx]
            entity.lock = ['entity_code']
            from modules.entity_add_edit import p_entity_add_edit
            p_entity_add_edit.create(parent=self, entity=entity)
            self.view.lsc_plus.update_item(idx)

    def delete(self):
        idxs = self.view.lsc_plus.get_sel_pos_items()
        if idxs:
            message = _("Are you sure that delete selected items?")
            if self.view.msg.question(message=message):
                for i in idxs:
                    if self.model.entities[i].is_in_use:
                        message = '{} {} is in use.\nDelete first all inscriptions and results where it is being used.'.format(
                            self.model.entities[i].short_name,
                            self.model.entities[i].entity_code,
                        )
                        self.view.msg.warning(message=message)
                        break
                else:
                    self.model.entities.delete_items(idxs)
                    self.view.lsc_plus.delete_items(idxs)
        else:
            self.view.msg.warning(message=_("No item selected."))