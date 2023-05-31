# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import utils


class Inscription(object):

    def __init__(self, **kwargs):
        self.inscriptions = kwargs['inscriptions']
        self.config = self.inscriptions.config
        self.inscription_id = int(kwargs['inscription_id'])
        self.mark_hundredth = int(kwargs['mark_hundredth'])
        self.event = kwargs['event']
        if 'pool_length' in list(kwargs.keys()):
            self.pool_length = int(kwargs['pool_length'])
        else:
            self.pool_length = 0
        if 'chrono_type' in list(kwargs.keys()):
            self.chrono_type = kwargs['chrono_type']
        else:
            self.chrono_type = ''
        if 'date' in list(kwargs.keys()):
            self.date = kwargs['date']
        else:
            self.date = ''
        if 'venue' in list(kwargs.keys()):
            self.venue = kwargs['venue']
        else:
            self.venue = None

    @property
    def champ(self):
        return self.inscriptions.champ

    def _get_mark_time(self):
        mark_time = marks.hun2mark(value=self.mark_hundredth)
        return mark_time

    def _set_mark_time(self, mark_time):  
        if not isinstance(mark_time, str) and not isinstance(mark_time, str):
            mark_time = 0
        self.mark_hundredth = marks.mark2hun(value=mark_time)

    mark_time = property(_get_mark_time, _set_mark_time)

    @property
    def equated_time(self):
        return marks.hun2mark(value=self.equated_hundredth)

    @property
    def venue_normalized(self):
        return utils.normalize(self.venue)