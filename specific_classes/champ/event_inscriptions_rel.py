# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
from specific_classes.champ.inscription_rel import InscriptionRel



class EventInscriptionsRel(list):

    def __init__(self, **kwargs):
        self.event = kwargs['event']
        self.config = self.event.config

    @property
    def champ(self):
        return self.event.champ

    @property
    def ind_rel(self):
        return 'R'

    @property    
    def item_blank(self):
        return InscriptionRel(
            inscriptions=self,
            inscription_id=0,
            pool_length=0,
            chrono_type='',
            mark_hundredth=0,
            equated_hundredth=0,
            date='',
            venue='',
            event=self.event,
            relay=self.champ.relays.item_blank
        )

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        for i in self.champ.inscriptions:
            if i.event == self.event:
                self.append(i)

#     def load_items_from_dbs(self):
#         del self[:]  # borra os elementos que haxa
#         sql = '''
# select inscription_id, pool_length, chrono_type, mark_hundredth,
# equated_hundredth, date, venue, event_id, person_id, relay_id
# from inscriptions where event_id={} order by equated_hundredth '''
#         sql = sql.format(self.event.event_id)
#         res = self.config.dbs.exec_sql(sql=sql)
#         (INSCRIPTION_ID, POOL_LENGTH, CHRONO_TYPE, MARK_HUNDREDTH,
# EQUATED_HUNDREDTH, DATE, VENUE, EVENT_ID, PERSON_ID, RELAY_ID) = range(10)
#         for i in res:
#             relay = self.champ.relays.get_relay(i[RELAY_ID])
#             event = self.champ.events.get_event(i[EVENT_ID])
#             self.append(InscriptionRel(
#                     inscriptions=self,
#                     inscription_id=i[INSCRIPTION_ID],
#                     pool_length=i[POOL_LENGTH],
#                     chrono_type=i[CHRONO_TYPE],
#                     mark_hundredth=i[MARK_HUNDREDTH],
#                     equated_hundredth=i[EQUATED_HUNDREDTH],
#                     date=i[DATE],
#                     venue=i[VENUE],
#                     event=event,
#                     relay=relay,
#                     ))

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('N.'), 'C', 40),
                (_('Name'), 'L', 200),
                (_('Gender'), 'C', 40),
                (_('Category'), 'C', 40),
                (_('Club'), 'L', 60),
                (_('Mark'), 'R', 65),
                (_('Pool'), 'C', 40),
                (_('Chrono'), 'C', 40),
                (_('Equated'), 'R', 65),
                (_('Date'), 'C', 75),
                (_('Venue'), 'L', 100),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for pos, i in enumerate(self):
            print(i.inscription_id)
            values.append((
                str(pos+1),
                i.relay.name,
                i.relay.gender_id,
                i.relay.category.name,
                i.relay.entity.short_name,
                i.mark_time,
                i.pool_length,
                i.chrono_type,
                i.equated_time,
                i.date,
                i.venue,
                ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (
            'relay.name',
            'relay.gender_id',
            'relay.category.name',
            'relay.entity.short_name',
            'mark_hundredth',
            'pool_length',
            'chrono_type',
            'equated_hundredth',
            'date',
            'venue',
            )
        # cols valid to order
        order_cols = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in order_cols:
                field = cols[kwargs['num_col'] + 1]

        if self.sort_last_field == field:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        if field:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field

    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)
