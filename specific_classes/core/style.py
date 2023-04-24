# -*- coding: utf-8 -*- 


class Style(object):

    def __init__(self, **kwargs):
        self.styles = kwargs['styles']
        self.style_id = kwargs['style_id']
        self.short_name = kwargs['short_name']
        self.long_name = kwargs['long_name']

