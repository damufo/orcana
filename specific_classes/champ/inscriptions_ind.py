# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
# from specific_classes.report_base import ReportBase
#from specific_classes.conversions import Conversions
from specific_classes.champ.inscription_ind import InscriptionInd
from specific_classes.champ.inscriptions import Inscriptions
# from specific_functions import times
# from specific_functions import files


class InscriptionsInd(Inscriptions):

    def __init__(self, **kwargs):
        Inscriptions.__init__(self, **kwargs)

    @property    
    def item_blank(self):
        return InscriptionInd(
            inscriptions=self,
            inscription_id=0,
            pool_length=self.champ.pool_length,
            chrono_type=self.champ.chrono_type,
            mark_hundredth=0,
            equated_hundredth=0,
            date='',
            venue='',
            event=self.event,
            person=None
        )

    @property
    def ind_rel(self):
        return 'I'

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select inscription_id, pool_length, chrono_type, mark_hundredth,
equated_hundredth, date, venue, event_id, person_id, relay_id
from inscriptions where event_id={} order by equated_hundredth '''
        sql = sql.format(self.event.event_id)

        res = self.config.dbs.exec_sql(sql=sql)
        (INSCRIPTION_ID, POOL_LENGTH, CHRONO_TYPE, MARK_HUNDREDTH,
EQUATED_HUNDREDTH, DATE, VENUE, EVENT_ID, PERSON_ID, RELAY_ID) = range(10)
        for i in res:
            event = self.champ.events.get_event(self.event.event_id)
            person = self.champ.persons.get_person(i[PERSON_ID])
            self.append(InscriptionInd(
                    inscriptions=self,
                    inscription_id=i[INSCRIPTION_ID],
                    pool_length=i[POOL_LENGTH],
                    chrono_type=i[CHRONO_TYPE],
                    mark_hundredth=i[MARK_HUNDREDTH],
                    equated_hundredth=i[EQUATED_HUNDREDTH],
                    date=i[DATE],
                    venue=i[VENUE],
                    event=event,
                    person=person
                    ))

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('Name'), 'L', 200),
                (_('Gender'), 'C', 40),
                (_('Year'), 'C', 80),
                (_('Club'), 'L', 60),
                (_('Pool'), 'C', 40),
                (_('Chrono'), 'C', 40),
                (_('Mark'), 'R', 65),
                (_('Equated'), 'R', 65),
                (_('Date'), 'C', 75),
                (_('Venue'), 'L', 100),
                (_('License'), 'C', 80),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            values.append((
                i.person.full_name,
                i.person.gender_id,
                i.person.birth_date[:4],
                i.person.entity.short_name,
                i.pool_length,
                i.chrono_type,
                i.mark_time,
                i.equated_time,
                i.date,
                i.venue,
                i.person.license,
                ))

        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (
            'person.full_name_normalized',
            'person.gender_id',
            'person.birth_date',
            'person.entity.short_name',
            'pool_length',
            'chrono_type',
            'mark_hundredth',
            'equated_hundredth',
            'date',
            'venue',
            'person.license',
            )
        # cols valid to order
        order_cols = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in order_cols:
                field = cols[kwargs['num_col']]

        if self.sort_last_field == field:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        if field:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field
