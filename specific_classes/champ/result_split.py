# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import conversion
# from specific_functions import normalize


class ResultSplit(object):

    def __init__(self, **kwargs):
        self.result_splits = kwargs['result_splits']
        self.config = self.result_splits.config
        self.result_split_id = int(kwargs['result_split_id'])
        self.distance = int(kwargs['distance'])
        self.mark_hundredth = kwargs['mark_hundredth']
        self.result_split_code = kwargs['result_split_code']
        self.official = kwargs['official']
        
    @property
    def style_id(self):
        style_id = self.result_split_code[len(self.result_split_code)-1]
        return style_id

    # def set_type_id(self, type_id):
    #     self.type_id = type_id
    #     if self.type_id == 'S':
    #         self.insc_members = InscMembers(inscription=self)
    #     else:
    #         self.insc_members = []

    # @property
    # def champ(self):
    #     return self.inscriptions.champ




    # def _get_mark_hundredth(self):
    #     return self._mark_hundredth

    # def _set_mark_hundredth(self, mark_hundredth):
    #     self._mark_hundredth = mark_hundredth

    # mark_hundredth = property(_get_mark_hundredth, _set_mark_hundredth)

    # @property
    # def equated_hundredth(self):
    #     champ_pool_length = self.champ.pool_length
    #     champ_chrono_type = self.champ.chrono_type

    #     equated_hundredth = conversion.conv_to_pool_chrono(
    #         mark_hundredth=self.mark_hundredth,
    #         event_id=self.event.code,
    #         gender_id=self.person.gender_id,
    #         chrono_type=self.chrono_type,
    #         pool_length=self.pool_length,
    #         to_pool_length=champ_pool_length,
    #         to_chrono_type=champ_chrono_type)
    #     return equated_hundredth

    def _get_mark_time(self):
        mark_time = marks.hun2mark(value=self.mark_hundredth)
        return mark_time

    def _set_mark_time(self, mark_time):  
        self.mark_hundredth = marks.validate(value=mark_time)

    mark_time = property(_get_mark_time, _set_mark_time)

    # @property
    # def equated_time(self):
    #     return marks.hun2mark(value=self.equated_hundredth)

    # @property
    # def year(self):
    #     return self.birth_date[:4]

    def save(self):
        sql = (
            'update results_splits set distance=?, mark_hundredth=?, '
            'result_split_code=?, official=? where result_split_id=? ')
        values = ((self.distance, self.mark_hundredth, self.result_split_code,
            self.official, self.result_split_id),)
        self.config.dbs.exec_sql(sql=sql, values=values)
