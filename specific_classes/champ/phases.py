# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
# from specific_classes.report_base import ReportBase
#from specific_classes.conversions import Conversions
from specific_classes.champ.phase import Phase
# from specific_functions import times
# from specific_functions import files


class Phases(list):

    def __init__(self, champ):
        self.champ = champ
        self.config = champ.config

        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def item_blank(self):
        return Phase(
            phases=self,
            phase_id=0,
            event=None,
            pool_lanes=0,
            progression='',
            session=None,
            )

    def get_phase(self, phase_id):
        phase = None
        for i in self:
            if i.phase_id == phase_id:
                phase = i
                break
        return phase

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):
        # Primeiro borra os results phase category
        # logo os results da phase
        # logo as heats da phase
        # logo phase categories
        # logo borra a phase
        phase = self[idx]
        phase.delete()
        self.pop(idx)  # remove element from list

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select phase_id, pos, event_id, pool_lanes, progression, session_id
from phases p 
order by (select s.xdate || " " ||s.xtime from sessions s where s.session_id=p.session_id), pos; '''
        res = self.config.dbs.exec_sql(sql=sql)
        (PHASE_ID, POS, EVENT_ID, POOL_LANES, PROGRESSION, SESSION_ID) = range(6)
        for i in res:
            event = self.champ.events.get_event(i[EVENT_ID])
            session = self.champ.sessions.get_session(i[SESSION_ID])
            phase = Phase(
                    phases=self,
                    phase_id=i[PHASE_ID],
                    pos=i[POS],
                    event=event,
                    pool_lanes=i[POOL_LANES],
                    progression=i[PROGRESSION],
                    session=session,
                    )
            phase.phase_categories.load_items_from_dbs()
            self.append(phase)

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                # (_('Pos.'), 'C', 80),
                (_('Event'), 'L', 200),
                (_('Pool Lanes'), 'C', 100),
                (_('Progression'), 'C', 100),
                (_('Session'), 'L', 100),
                (_('Categories'), 'L', 100),
                (_('Official'), 'C', 100),
                (_('Heats'), 'C', 100),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            values.append((
                    # i.pos,
                    i.event.long_name,
                    str(i.pool_lanes),
                    i.progression,
                    i.session.date_time,
                    i.categories_text,
                    i.official and _('S') or "",
                    str(len(i.heats)),
                    ))
        return tuple(values)

    def list_sort(self, **kwargs):
        """
        Phases no sor option
        """
        pass
        # '''
        # Sort results by column num or column name
        # '''
        # field = None
        # cols = (
        #         'pos',
        #         'event.long_name',
        #         'pool_lanes',
        #         'progression',
        #         'session.date_time',
        #         'categories_names',
        #         )
        # # cols valid to order
        # order_cols = (0, 1, 2, 3, 4)

        # if 'num_col' in list(kwargs.keys()):
        #     if kwargs['num_col'] in order_cols:
        #         field = cols[kwargs['num_col']]

        # if self.sort_last_field == field:
        #     self.sort_reverse = not self.sort_reverse
        # else:
        #     self.sort_reverse = False
        # if field:
        #     self.sort_by_field(field=field, reverse=self.sort_reverse)
        #     self.sort_last_field = field

    # def sort_by_field(self, field, reverse=False):
    #     self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
    #     del self[:]
    #     self.extend(self_sort)

    def move_down(self, pos):
        if pos < (len(self)-1):
            self[pos], self[pos+1] = self[pos+1], self[pos]
            self.update_items_on_dbs([pos, pos+1])

    def move_up(self, pos):
        if pos > 0:
            self[pos], self[pos-1] = self[pos-1], self[pos]
            self.update_items_on_dbs([pos, pos-1])

    def update_items_on_dbs(self, items=[]):
        '''
        for year add/substract and up/down
        '''
        if not items:
            items = range(len(self))
        for pos in items:
            i = self[pos]
            i.save()