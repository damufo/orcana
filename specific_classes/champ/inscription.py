# -*- coding: utf-8 -*- 


from specific_functions import marks


class Inscription(object):

    def __init__(self, **kwargs):
        self.inscriptions = kwargs['inscriptions']
        self.config = self.inscriptions.config
        self.inscription_id = int(kwargs['inscription_id'])
        if 'pool_length' in list(kwargs.keys()):
            self.pool_length = int(kwargs['pool_length'])
        else:
            self.pool_length = 0
        if 'chrono_type' in list(kwargs.keys()):
            self.chrono_type = kwargs['chrono_type']
        else:
            self.chrono_type = ''
        self.mark_hundredth = int(kwargs['mark_hundredth'])
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

    @property
    def event(self):
        return self.inscriptions.event

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

    # def save(self):
    #     champ_id = self.champ.id
    #     event_id = self.event.code
    #     gender_id = self.gender_id
    #     category_id = self.category_id
    #     # Delete previous inscriptions
    #     sql = ('update inscriptions set pool_length=?, chrono_type=?, '
    #             'mark_hundredth=?, equated_hundredth=?, date=?, venue=?, '
    #             'event_id=?, person_id=?, relay_id=? where inscription_id=? ')
    #     values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
    #             self.equated_hundredth, self.date, 
    #             self.venue, self.event_id, self.person_id, self.relay_id,
    #             self.inscriptions_id),)
    #     # self.config.dbs.exec_sql(sql=sql, values=values)
               

