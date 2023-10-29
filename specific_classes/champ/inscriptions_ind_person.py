# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
from specific_classes.champ.inscription import Inscription


class InscriptionsIndPerson(list):

    def __init__(self, person):
        self.person = person
        self.sort_reverse = False
        self.sort_last_field = None

    # def __iter__(self):
    #     inscriptions = []
    #     for phase in self.champ.phases:
    #         for inscription in phase.inscriptions:
    #             if inscription.person:
    #                 if inscription.person.person_id == self.person.person_id:
    #                     inscriptions.append(inscription)
    #     return inscriptions.__iter__()

    # def __len__(self):
    #     return len(self.list_values)


    @property
    def champ(self):
        return self.person.champ

    @property
    def config(self):
        return self.champ.config

    @property 
    def item_blank(self):

        inscription = Inscription(
                inscriptions=None,
                inscription_id=0,
                pool_length=self.champ.params['champ_pool_length'],
                chrono_type=self.champ.params['champ_chrono_type'],
                mark_hundredth=359999,
                equated_hundredth=359999,
                date='',
                venue='',
                person=self.person,
                relay=None,
                rejected=0,
                exchanged=0,
                score=1,
                classify=1,
            )
        return inscription

    # def append(self, item):
    #     # Engade a inscrición nas inscricións da phase se non está xa
    #     if item not in item.inscriptions:
    #         item.inscriptions.append(item)
    #     # engade a inscrición nesta mesma clase inscrición da persoa
    #     # estas inscricións son calculadas coa función load desta clase
    #     super().append(item)
    #     print("engadiuse")

    # def load(self):
    #     self.clear()  # borra os elementos que haxa
    #     # inscriptions = []
    #     for phase in self.champ.phases:
    #         for inscription in phase.inscriptions:
    #             if inscription.person:
    #                 if inscription.person.person_id == self.person.person_id:
    #                     self.append(inscription)

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            inscription = self[idx]
            inscription.delete()  # from phase.inscriptions

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """

        return (
            (_('Event'), 'L', 200),
            (_('Mark'), 'R', 65),
            (_('Pool'), 'C', 40),
            (_('Chrono'), 'C', 40),
            (_('Equated'), 'R', 65),
            (_('Date'), 'C', 75),
            (_('Venue'), 'L', 100),
            (_('Flags'), 'C', 50),
            (_('Heat'), 'C', 50),
            (_('Lane'), 'C', 50),
            )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []

        for pos, i in enumerate(self):
            flags = '{}{}{}{}'.format(
                i.rejected and _('R') or '',
                i.exchanged and _('E') or '',
                i.score and _('S') or '',
                i.classify and _('C') or '',
                )
            values.append((
                i.event.long_name,
                i.mark_time,
                i.pool_length,
                i.chrono_type,
                i.equated_time,
                i.date,
                i.venue,
                flags,
                i.heat_pos > -1 and i.heat_pos or '',
                i.lane > -1 and i.lane or '',
                ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (
            'event.long_name',
            'mark_hundredth',
            'pool_length',
            'chrono_type',
            'equated_hundredth',
            'date',
            'venue_normalized',
            'heat_pos',
            'lane',
            )
        order_cols = range(len(cols))
        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in order_cols:
                field = cols[kwargs['num_col']]
        if field:
            if self.sort_last_field == field:
                self.sort_reverse = not self.sort_reverse
            else:
                self.sort_reverse = False
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field

    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)

    def sort_default(self):
        fields = ('equated_hundredth', 'phase.pos')
        for field in fields:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field