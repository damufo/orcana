# -*- coding: utf-8 -*- 


class Gender(object):

    def __init__(self, **kwargs):
        self.genders = kwargs['genders']
        self.gender_id = kwargs['gender_id']
        self.short_name = kwargs['short_name']
        self.long_name = kwargs['long_name']

