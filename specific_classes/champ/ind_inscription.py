# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import conversion
# from specific_functions import normalize


class IndInscription(object):

    def __init__(self, **kwargs):
        self.ind_inscriptions = kwargs['ind_inscriptions']
        self.config = self.ind_inscriptions.champ
        self.ind_inscriptions_id = int(kwargs['ind_inscription_id'])

        self.event = kwargs['event']
        self.person = kwargs['person']
        if 'pool_length' in list(kwargs.keys()):
            self.pool_length = int(kwargs['pool_length'])
        else:
            self.pool_length = 0
        if 'chrono_type' in list(kwargs.keys()):
            self.chrono_type = kwargs['chrono_type']
        else:
            self.chrono_type = ''
        # self._mark_hundredth = 0
        self.mark_hundredth = int(kwargs['mark_hundredth'])
        if 'date_time' in list(kwargs.keys()):
            self.date_time = kwargs['date_time']
        else:
            self.date_time = ''
        if 'venue' in list(kwargs.keys()):
            self.venue = kwargs['venue']
        else:
            self.venue = None


    # def set_type_id(self, type_id):
    #     self.type_id = type_id
    #     if self.type_id == 'S':
    #         self.insc_members = InscMembers(inscription=self)
    #     else:
    #         self.insc_members = []

    @property
    def champ(self):
        return self.ind_inscriptions.champ




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
        champ_id = self.champ.id
        event_id = self.event.code
        gender_id = self.gender_id
        category_id = self.category_id
        # Delete previous inscriptions
        sql = ('update ind_inscriptions set pool_length=?, chrono_type=?, '
                'mark_hundredth=?, equated_hundredth=?, date_time=?, venue=?, '
                'event_id=?, person_id=? where ind_inscription_id=? ')
        values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                self.equated_hundredth, self.date_time, 
                self.venue, self.event_id, self.person_id,
                self.ind_inscriptions_id),)
        # self.config.dbs.exec_sql(sql=sql, values=values)
               

