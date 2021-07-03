# -*- coding: utf-8 -*-


from .m_resize import Model
from .v_resize import View
from .i_resize import Interactor


def create(parent, picture):
    return Presenter(
            Model(picture=picture),
            View(parent.view),
            Interactor())

class Presenter(object):

    def __init__(self, model, view, interactor):
        self.model = model
        self.view = view
        interactor.install(self, view)
        self.view.picture = self.model.picture
        self.view.set_values()
        self.view.view_plus.start(modal=True)

    def acept(self):
        picture = self.model.picture
        width, height = self.view.get_values()
        if width == 0 or height == 0:
            self.view.msg.error(message=_("Error in values, set more than 0."))
        elif picture.width == width and picture.height == height:
            self.view.msg.error(message=_("Same values as the current ones."))
        else:
            picture.resize(width, height)
            picture.resized = True
            self.view.view_plus.stop()

    def close(self):
        self.view.view_plus.stop()
