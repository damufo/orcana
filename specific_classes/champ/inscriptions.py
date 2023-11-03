# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
from specific_classes.champ.inscription import Inscription



class Inscriptions(list):

    def __init__(self, phase):
        self.phase = phase
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def dict(self):
        dict_inscriptions = {}
        for i in self:
            dict_inscriptions[i.inscription_id] = i
        return dict_inscriptions

    @property
    def champ(self):
        return self.phase.champ

    @property
    def config(self):
        return self.champ.config

    @property
    def event(self):
        return self.phase.event

    @property
    def ind_rel(self):
        return self.phase.event.ind_rel

    @property    
    def item_blank(self):
        if self.ind_rel == 'I':
            inscription = Inscription(
                inscriptions=self,
                inscription_id=0,
                pool_length=self.champ.params['champ_pool_length'],
                chrono_type=self.champ.params['champ_chrono_type'],
                mark_hundredth=359999,
                equated_hundredth=359999,
                date='',
                venue='',
                person=None,
                relay=None,
                rejected=0,
                exchanged=0,
                score=1,
                classify=1,
            )
        elif self.ind_rel == 'R':
            relay = self.champ.relays.item_blank
            relay.event = self.phase.event
            inscription = Inscription(
                inscriptions=self,
                inscription_id=0,
                pool_length=self.champ.params['champ_pool_length'],
                chrono_type=self.champ.params['champ_chrono_type'],
                mark_hundredth=359999,
                equated_hundredth=359999,
                date='',
                venue='',
                person=None,
                relay=relay,
                rejected=0,
                exchanged=0,
                score=1,
                classify=1,
            )
        return inscription

    def append(self, inscription):
        # if not isinstance(item, type):
        #     raise TypeError, 'item is not of type %s' % type
        super().append(inscription)
        print("engadiuse a inscricion")
        if inscription.person:
            if inscription not in inscription.person.inscriptions:
                inscription.person.inscriptions.append(inscription)
            else:
                print("isto non debería pasar nunca")

    def remove(self, inscription):
        # if not isinstance(item, type):
        #     raise TypeError, 'item is not of type %s' % type
        super().remove(inscription)
        print("eliminouse a inscricion")
        if inscription.person:
            if inscription in inscription.person.inscriptions:
                inscription.person.inscriptions.remove(inscription)
            else:
                print("isto non debería pasar nunca")

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()

    def search_relay(self, entity, category, name):
        match_inscription = None
        if self.phase.ind_rel == 'R':
            for i in self:
                if (i.relay.entity == entity and 
                        i.relay.category == category and 
                        i.relay.name == name):
                    match_inscription = i
                    break
        return match_inscription

    def load_items_from_dbs(self):
        self.clear()  # borra os elementos que haxa
        # isto de arriba ten que borrar tamén as inscricións das persoas
        for person in self.champ.persons:
            for inscription in person.inscriptions:
                if inscription.phase == self.phase:
                    person.inscriptions.remove(inscription)

        dict_persons = self.champ.persons.dict
        dict_relays = self.champ.relays.dict
        sql = '''
select inscription_id, pool_length, chrono_type, mark_hundredth,
equated_hundredth, date, venue, rejected, exchanged, score, classify,
phase_id, person_id, relay_id
from inscriptions i where phase_id=? order by equated_hundredth '''

        values = ((self.phase.phase_id,),)
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        (INSCRIPTION_ID, POOL_LENGTH, CHRONO_TYPE, MARK_HUNDREDTH,
EQUATED_HUNDREDTH, DATE, VENUE, REJECTED, EXCHANGED, SCORE, CLASSIFY,
PHASE_ID, PERSON_ID, RELAY_ID) = range(14)
        for i in res:
            if self.ind_rel == 'I':
                person = dict_persons[i[PERSON_ID]]
                relay = None
            elif self.ind_rel == 'R':
                person = None
                # print(id(dict_relays[i[RELAY_ID]]))
                relay = dict_relays[i[RELAY_ID]]
                # print(id(relay))
                relay.event = self.phase.event
                # print(id(relay))
            # phase = self.champ.phases.get_phase(i[PHASE_ID])
            if not person and not relay:
                AssertionError("Iston on pode ser.")
            else:
                inscription = Inscription(
                        inscriptions=self,
                        inscription_id=i[INSCRIPTION_ID],
                        pool_length=i[POOL_LENGTH],
                        chrono_type=i[CHRONO_TYPE],
                        mark_hundredth=i[MARK_HUNDREDTH],
                        equated_hundredth=i[EQUATED_HUNDREDTH],
                        date=i[DATE],
                        venue=i[VENUE],
                        rejected=i[REJECTED],
                        exchanged=i[EXCHANGED],
                        score=i[SCORE],
                        classify=i[CLASSIFY],
                        phase=self.phase,
                        person=person,
                        relay=relay,
                        )
                if self.ind_rel == 'R':  # Set inscription (one relay only has one inscription)
                    relay.inscription = inscription
                    # print(id(relay))
                # else:
                #     print("is individual")
                self.append(inscription)

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        if self.ind_rel == 'I':
            return (
                (_('N.'), 'C', 40),
                (_('Name'), 'L', 200),
                (_('Gender'), 'C', 40),
                (_('Year'), 'C', 80),
                (_('Club'), 'L', 60),
                (_('Mark'), 'R', 65),
                (_('Pool'), 'C', 40),
                (_('Chrono'), 'C', 40),
                (_('Equated'), 'R', 65),
                (_('Date'), 'C', 75),
                (_('Venue'), 'L', 100),
                (_('License'), 'C', 80),
                (_('Flags'), 'C', 50),
                (_('Heat'), 'C', 50),
                (_('Lane'), 'C', 50),
                )
        elif self.ind_rel == 'R':
            return (
                (_('N.'), 'C', 40),
                (_('Name'), 'L', 200),
                (_('Gender'), 'C', 40),
                (_('Members'), 'C', 40),
                (_('Category'), 'C', 40),
                (_('Club'), 'L', 60),
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
        if self.ind_rel == 'I':
            for pos, i in enumerate(self):
                flags = '{}{}{}{}'.format(
                    i.rejected and _('R') or '',
                    i.exchanged and _('E') or '',
                    i.score and _('S') or '',
                    i.classify and _('C') or '',
                    )
                values.append((
                    str(pos+1),
                    i.person.full_name,
                    i.person.gender_id,
                    i.person.birth_date[:4],
                    i.person.entity.short_name,
                    i.mark_time,
                    i.pool_length,
                    i.chrono_type,
                    i.equated_time,
                    i.date,
                    i.venue,
                    i.person.license,
                    flags,
                    i.heat_pos > -1 and i.heat_pos or '',
                    i.lane > -1 and i.lane or '',
                    ))
        elif self.ind_rel == 'R':
            for pos, i in enumerate(self):
                print(i.inscription_id)
                flags = '{}{}{}{}'.format(
                    i.rejected and _('R') or '',
                    i.exchanged and _('E') or '',
                    i.score and _('S') or '',
                    i.classify and _('C') or '',
                    )
                if i.relay.relay_members.has_set_members:
                    has_set_members = '√'
                else:
                    has_set_members = ''
                values.append((
                    str(pos+1),
                    i.relay.name,
                    i.relay.gender_id,
                    has_set_members,
                    i.relay.category.name,
                    i.relay.entity.short_name,
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
        if self.ind_rel == 'I':
            cols = (
                '',
                'person.full_name_normalized',
                'person.gender_id',
                'person.birth_date',
                'person.entity.short_name_normalized',
                'mark_hundredth',
                'pool_length',
                'chrono_type',
                'equated_hundredth',
                'date',
                'venue_normalized',
                'person.license',
                'heat_pos',
                'lane',
                )
            # cols valid to order
            valid_order_cols = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14)
        elif self.ind_rel == 'R':
            cols = (
                '',
                'relay.name_normalized',
                'relay.gender_id',
                'relay.category.name_normalized',
                'relay.relay_members.has_set_members',
                'relay.entity.short_name_normalized',
                'mark_hundredth',
                'pool_length',
                'chrono_type',
                'equated_hundredth',
                'date',
                'venue_normalized',
                'heat_pos',
                'lane',
                )
            # cols valid to order
            valid_order_cols = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)

        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in valid_order_cols:
                field = cols[kwargs['num_col']]
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

    def sort_default(self):
        fields = ('equated_hundredth', 'phase.pos')
        for field in fields:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field