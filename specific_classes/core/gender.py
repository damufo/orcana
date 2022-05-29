# -*- coding: utf-8 -*- 


class Gender(object):

    def __init__(self, **kwargs):
        self.genders = kwargs['genders']
        self.gender_id = kwargs['gender_id']
        self.name = kwargs['name']

