# -*- coding: utf-8 -*-


# from specific_classes.pictures import Pictures
# from specific_classes.champ.champ import Champ

class Model(object):

    def __init__(self, champ):
        self.config = champ.config
        self.champ = champ
