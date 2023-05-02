# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
from specific_classes.champ.inscription_ind import InscriptionInd
from specific_classes.champ.inscription_rel import InscriptionRel


class Inscriptions(list):

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        self.champ = kwargs['champ']
        self.config = self.champ.config

        self.sort_reverse = False
        self.sort_last_field = None


    @property
    def activity_id(self):
        return self.champ.activity_id

    @property
    def estament_id(self):
        return self.champ.estament_id

    @property
    def scope_id(self):
        return self.champ.scope_id

    @property
    def pool_length(self):
        return self.champ.pool_length

    @property
    def chrono_type(self):
        return self.champ.chrono_type

    def item_blank_ind(self, event):
        return InscriptionInd(
            inscriptions=self,
            inscription_id=0,
            pool_length=self.champ.pool_length,
            chrono_type=self.champ.chrono_type,
            mark_hundredth=0,
            equated_hundredth=0,
            date='',
            venue='',
            event=event,
            person=None
        )

    def item_blank_rel(self, event):
        return InscriptionRel(
            inscriptions=self,
            inscription_id=0,
            pool_length=0,
            chrono_type='',
            mark_hundredth=0,
            equated_hundredth=0,
            date='',
            venue='',
            event=event,
            relay=self.champ.relays.item_blank
        )

    # def delete_items(self, idxs):
    #     for idx in sorted(idxs, reverse=True):
    #         self.delete_item(idx)

    def delete_item(self, inscription):
        sql =  ("delete from inscriptions where inscription_id=?")
        values = ((inscription.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        sql =  ("delete from inscriptions_members where inscription_id=?")
        values = ((inscription.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.remove(inscription) #remove element from list

    def get_inscription(self, inscription_id):
        inscription = None
        for i in self:
            if i.inscription_id == inscription_id:
                inscription = i
                break
        return inscription

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select inscription_id, pool_length, chrono_type, mark_hundredth,
equated_hundredth, date, venue, event_id, person_id, relay_id
from inscriptions i order by (select pos from events e where e.event_id=i.event_id), equated_hundredth '''

        res = self.config.dbs.exec_sql(sql=sql)
        (INSCRIPTION_ID, POOL_LENGTH, CHRONO_TYPE, MARK_HUNDREDTH,
EQUATED_HUNDREDTH, DATE, VENUE, EVENT_ID, PERSON_ID, RELAY_ID) = range(10)
        for i in res:
            person = self.champ.persons.get_person(i[PERSON_ID])
            relay = self.champ.relays.get_relay(i[RELAY_ID])
            event = self.champ.events.get_event(i[EVENT_ID])
            if person and relay:
                AssertionError("Iston on pode ser.")
            elif relay:
                self.append(InscriptionRel(
                        inscriptions=self,
                        inscription_id=i[INSCRIPTION_ID],
                        pool_length=i[POOL_LENGTH],
                        chrono_type=i[CHRONO_TYPE],
                        mark_hundredth=i[MARK_HUNDREDTH],
                        equated_hundredth=i[EQUATED_HUNDREDTH],
                        date=i[DATE],
                        venue=i[VENUE],
                        event=event,
                        relay=relay,
                        ))
            elif person:
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
                        person=person,
                        ))

    def sort_default(self):
        fields = ('equated_hundredth', 'event.pos')
        for field in fields:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field

    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)        
 
#     def check_insc_max_person_sen_uso_pode_borrarse(self):
        
#         champ_id = self.champ_id
#         insc_max_person = self.champ.insc_max_person
        
#         #  Check maximum inscriptions by person
#         sql = '''
# Select person_id, surname, name, event_id, gender_id, category_id 
# from champ_inscriptions where champ_id=? and inscribed=1 and 
# person_id in (select person_id from champ_inscriptions where champ_id=? 
#     and inscribed=1 and upper(event_id) not like '%X%' 
#     group by person_id having count(*)>?)
# order by surname, name, birth_date, event_id '''
#         values = ((champ_id, champ_id, insc_max_person),)
#         rows = self.config.dbs.exec_sql(sql=sql, values=values)
#         PERSON_ID, SURNAME, NAME, EVENT_ID, GENDER_ID, CATEGORY_ID = list(range(6))
#         message = ''
#         person_id = None
#         for i in rows:
#             if person_id != i[PERSON_ID]:
#                 if message:
#                     message += '\n'
#                 message += '{}, {}: '.format(i[SURNAME], i[NAME])
#                 events = None
#                 person_id = i[PERSON_ID]
            
#             if events:
#                 message += ', {}'.format(i[EVENT_ID])
#             else:
#                 events = True
#                 message += '{}'.format(i[EVENT_ID])
#         if message:
#             message=_('People with excess events:\n{}').format(message)
#         return message
 
#     def check_insc_max_club_sen_uso_pode_borrarse(self):        
#         # Check maximum inscriptions by event and club
#         champ_id = self.champ_id
#         sql = '''
# select ci.club_id, ci.event_id, 
#     (select ce.gender_id from champ_events as ce 
#                 where ce.champ_id=? 
#                     and ce.event_id=ci.event_id 
#                     and case when ce.gender_id<>'X' then ce.gender_id=ci.gender_id else 1 end 
#                     and ce.category_id=ci.category_id) as ce_gender_id, 
#     ci.category_id, count(*) as conta, 
#     (select insc_max from champ_events as ce 
#         where ce.champ_id=? 
#             and ce.event_id=ci.event_id 
#             and case when ce.gender_id<>'X' then ce.gender_id=ci.gender_id else 1 end 
#                 and ce.category_id=ci.category_id) as insc_max
# from champ_inscriptions as ci where ci.champ_id=? and ci.inscribed=1 and ci.type_id in ("I", "R", "S")
# group by ci.club_id, ci.event_id, ce_gender_id, ci.category_id
# having
# count(*) > (select insc_max from champ_events as ce 
#             where ce.champ_id=? 
#                 and ce.event_id=ci.event_id 
#                 and case when ce.gender_id<>'X' then ce.gender_id=ci.gender_id else 1 end 
#                 and ce.category_id=ci.category_id)
# order by ci.club_id, ci.event_id '''
#         values = ((champ_id, champ_id, champ_id , champ_id),)
#         rows = self.config.dbs.exec_sql(sql=sql, values=values)
#         CLUB_ID, EVENT_ID, GENDER_ID, CATEGORY_ID, INSC, INSC_MAX = list(range(6))
#         message = ''
#         for i in rows:
#             club = self.config.clubs.get_club(i[CLUB_ID])
#             message += _('{} {} {} {} Insc.: {} Max.: {}\n').format(
#                     club.short_desc, i[EVENT_ID], i[GENDER_ID], i[CATEGORY_ID], i[INSC], i[INSC_MAX])
#         if message:
#             message=_('Clubs with excess inscriptions:\n{}').formatmessage
#         return message
            


#     def delete_club_inscriptions(self, champ_id, club_id):
#         '''
#         delete current inscriptios for champ_id and club_id
#         '''
#         sql = '''
# delete from champ_inscriptions where champ_id=? and club_id=? '''  #and inscribed=0
#         self.config.dbs.exec_sql(sql=sql, values=((champ_id, club_id),))
