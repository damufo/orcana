# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import conversion
# from specific_functions import normalize
# from specific_classes.champ.results import Results


class Heat(object):

    def __init__(self, **kwargs):
        self.heats = kwargs['heats']
        self.config = self.heats.config
        self.heat_id = int(kwargs['heat_id'])
        self.phase = kwargs['phase']
        self.pos = kwargs['pos']
        self.official = kwargs['official']
        self.start_time = kwargs['start_time']
        # self.results = Results(heat=self)

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

    def get_result(self, lane):
        result = None
        for i in self.results:
            if i.lane == lane:
                result = i
                break
        return result

    @property
    def results(self):
        # Return heat results sorted by lane
        list_results = []
        for inscription in self.phase.inscriptions:
            if inscription.result and inscription.result.heat == self:
                list_results.append(inscription.result)
        list_results = sorted(list_results, key=lambda x: x.lane)
        return list_results

    @property
    def equated_hundredth(self):
        champ_pool_length = self.champ.params['champ_pool_length']
        champ_chrono_type = self.champ.params['champ_chrono_type']
        equated_hundredth = conversion.conv_to_pool_chrono(
            mark_hundredth=self.mark_hundredth,
            event_id=self.event.code,
            gender_id=self.person.gender_id,
            chrono_type=self.chrono_type,
            pool_length=self.pool_length,
            to_pool_length=champ_pool_length,
            to_chrono_type=champ_chrono_type)
        return equated_hundredth

    @property
    def mark_time_st(self):  # lenex swim time 
        return marks.hun2mark(value=self.mark_hundredth, force='hours')

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

    def delete(self):
        # asume que se borraron antes todos os phases_categories_results
        print("ATENCIÓN!! Asume que se está a borrar unha fase.")
        # delete all results
        for i in self.results:
            i.delete()
        sql = ''' delete from heats where heat_id={}'''
        sql = sql.format(self.heat_id)
        self.config.dbs.exec_sql(sql=sql)
        self.heats.remove(self)
