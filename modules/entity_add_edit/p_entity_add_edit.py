# -*- coding: utf-8 -*-


from .m_entity_add_edit import Model
from .v_entity_add_edit import View
from .i_entity_add_edit import Interactor


def create(parent, entity, lock=None):
    '''
    parent is a presenter
    '''
    return Presenter(
            parent=parent,
            model=Model(entity=entity),
            view=View(parent.view),
            interactor=Interactor())

class Presenter(object):

    def __init__(self, parent, model, view, interactor):
        self.parent = parent
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.set_values(entity=self.model.entity)
        self.view.view_plus.start(modal=True)

    def acept(self):
        entity = self.model.entity
        self.view.get_values(entity=entity)
        msg = None
        if entity.already_exists:
            msg = 'Already exists.'
            self.view.txt_entity_code.SetFocus()
        elif len(entity.entity_code) != 5:
            msg = 'Entity code must be 5 characters.'
        elif not entity.short_name:
            msg = 'Set a short name.'
            self.view.txt_short_name.SetFocus()
        elif not entity.medium_name:
            msg = 'Set a medium name.'
            self.view.txt_medium_name.SetFocus()
        elif not entity.long_name:
            msg = 'Set a long name.'
            self.view.txt_long_name.SetFocus()
        if msg:
            self.view.msg.warning(msg)
        else:
            self.model.entity.save()
            # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
            # self.view.close()
            self.view.view_plus.stop()




    def entity_name(self):
        self.model.entity.entity_code = ""
        entity_name = self.view.txt_entity_short_name.GetValue()
        if entity_name:
            entities = self.model.entity.champ.entities
            entities_match = entities.get_entities_with_name(entity_name)
            if len(entities_match) == 1:
                self.view.lbl_entity_code.SetLabel(entities_match[0].entity_code)
                self.view.txt_entity_short_name.SetValue(entities_match[0].short_name)
            elif len(entities_match) > 1:
                choices = []
                for i in entities_match:
                    choices.append(i.medium_name)
                choice = self.view.msg.choice(
                    _('Select entity'),
                    _('Select entity'), 
                    choices
                    )
                if choice is not None:
                    self.view.lbl_entity_code.SetLabel(entities_match[choice[0]].entity_code)
                    self.view.txt_entity_short_name.SetValue(entities_match[choice[0]].short_name)
            else:
                self.view.txt_entity_short_name.SetValue("")
                self.view.lbl_entity_code.SetLabel("")
        else:
            self.view.txt_entity_short_name.SetValue("")
            self.view.lbl_entity_code.SetLabel("")
        # FIXME recuperar foco cando hai varias opcións
        # self.view.txt_entity_short_name.SetFocus()
        # print(self.view.HasFocus())
        # # self.view.Show()
        # self.view.SetFocus()
        # self.view.panel.SetFocus()
        # self.view.panel.SetFocusIgnoringChildren()
        # print(self.view.panel.HasFocus())
        # print('pasou')


    def cancel(self):
        # self.view.view_plus.close()
        # self.model.entity.save()
        # self.parent.parent.parent.load_result_members(parent=self.parent.parent)
        self.view.view_plus.stop()

