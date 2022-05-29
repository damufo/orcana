# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import conversion
# from specific_functions import normalize
from specific_classes.champ.results import Results


class Heat(object):

    def __init__(self, **kwargs):
        self.heats = kwargs['heats']
        self.config = self.heats.config
        self.heat_id = int(kwargs['heat_id'])
        self.phase = kwargs['phase']
        self.pos = kwargs['pos']
        self.official = kwargs['official']
        self.start_time = kwargs['start_time']
        self.results = Results(heat=self)


    # def set_type_id(self, type_id):
    #     self.type_id = type_id
    #     if self.type_id == 'S':
    #         self.insc_members = InscMembers(inscription=self)
    #     else:
    #         self.insc_members = []

    @property
    def champ(self):
        return self.heats.champ

    @property
    def event(self):
        return self.phase.event

    @property
    def ind_rel(self):
        '''
        return I: individual, R: relay
        '''
        return self.phase.event.ind_rel

    # def _get_mark_hundredth(self):
    #     return self._mark_hundredth

    # def _set_mark_hundredth(self, mark_hundredth):
    #     self._mark_hundredth = mark_hundredth

    # mark_hundredth = property(_get_mark_hundredth, _set_mark_hundredth)

    @property
    def equated_hundredth(self):
        champ_pool_length = self.champ.pool_length
        champ_chrono_type = self.champ.chrono_type

        equated_hundredth = conversion.conv_to_pool_chrono(
            mark_hundredth=self.mark_hundredth,
            event_id=self.event.code,
            gender_id=self.person.gender_id,
            chrono_type=self.chrono_type,
            pool_length=self.pool_length,
            to_pool_length=champ_pool_length,
            to_chrono_type=champ_chrono_type)
        return equated_hundredth

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
    def year(self):
        return self.birth_date[:4]

    def save(self):
        sql = ('update heats set official=?, start_time=? where heat_id=? ')
        values = ((self.official, self.start_time, self.heat_id),)
        self.config.dbs.exec_sql(sql=sql, values=values)
