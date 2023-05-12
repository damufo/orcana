# -*- coding: utf-8 -*-


import os
from operator import attrgetter
# from specific_classes.report_base import ReportBase
#from specific_classes.conversions import Conversions
# from specific_classes.champ.phases import Phases
from specific_classes.champ.heat import Heat
# from specific_functions import times
# from specific_functions import files


class Heats(list):

    def __init__(self, champ):
        self.champ = champ
        self.config = champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    def get_heat(self, heat_id):
        heat = None
        for i in self:
            if i.heat_id == heat_id:
                heat = i
                break
        return heat

    @property
    def item_blank(self):
        return Heat(
            heats=self,
            heat_id=0,
            phase=None,
            pos=0,
            official=False,
            start_time='',
            )

    @property
    def champs(self):
        return self.champ.champs

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):
        print("Aquí o código para borrar os elementos")
        self.pop(idx)  # remove element from list

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select heat_id, phase_id, pos, official, start_time
from heats u 
order by 
    (select xdate || " " || xtime from sessions where session_id=(
            select session_id from phases p where p.phase_id=phase_id)),
    (select pos from phases p where p.phase_id=phase_id),
    (select pos from events e where e.event_id=(
            select p.event_id from phases p where p.phase_id=u.phase_id)),
     pos '''
        res = self.config.dbs.exec_sql(sql=sql)
        (HEAT_ID, PHASE_ID, POS, OFFICIAL, START_TIME) = range(5)
        # for i in self.champ.phases:
        #     i.heats = []
        for i in res:
            phase = self.champ.phases.get_phase(i[PHASE_ID])
            heat = Heat(
                    heats=self,
                    heat_id=i[HEAT_ID],
                    phase=phase,
                    pos=i[POS],
                    official=i[OFFICIAL],
                    start_time=i[START_TIME],
                    )
            # phase.heats.append(heat)
            # print('append heat {}'.format(heat.heat_id))
            # print('{} - {}'.format(phase.phase_id, heat.heat_id))
            self.append(heat)
            # print('{} - {}'.format(phase.phase_id, heat.heat_id))

    # @property
    # def list_fields(self):
    #     """
    #     list fields for form show
    #     (name as text, align[L:left, C:center, R:right] as text,
    #             width as integer)
    #     """
    #     return ((_('N.'), 'C', 35), (_('Event'), 'C', 70),
    #             (_('Gender'), 'C', 60),
    #             (_('Category'), 'C', 60), (_('Name'), 'L', 240),
    #             (_('Ind/Rel'), 'C', 55),
    #             (_('Inscribed'), 'C', 65))

    # @property
    # def list_values(self):
    #     """
    #     list values for form show
    #     """
    #     values = []
    #     for x, i in enumerate(self, 1):
    #         values.append((
    #                        x,
    #                        i.event_id,
    #                        i.gender_id,
    #                        i.category_id,
    #                        i.name,
    #                        i.ind_rel,
    #                        i.count_inscriptions))
    #     return tuple(values)

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('N.'), 'C', 40),
                (_('Event'), 'L', 120),
                (_('Progression'), 'C', 90),
                (_('Heat'), 'C', 40),
                (_('Official'), 'C', 80),
                (_('Start time'), 'C', 90),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for pos, heat in enumerate(self, 1):
            values.append((
                str(pos),
                heat.phase.event.long_name,
                heat.phase.progression,
                str(heat.pos),
                heat.official and '√' or '',
                heat.start_time and heat.start_time or heat.phase.session.xtime,
                ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        return
        field = None
        cols = (  # cols valid to order
            'phase.event.long_name',
            'phase.progression',
            'pos',
            'official',
            'start_time',
            )
        order_cols = range(5)
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

    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)
