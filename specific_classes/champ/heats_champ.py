# -*- coding: utf-8 -*-


import os
from operator import attrgetter


class HeatsChamp(list):

    def __init__(self, champ):
        self.champ = champ
        self.config = champ.config
        self.sort_reverse = False
        self.sort_last_field = None
        self.load_items_from_champ()
    
    def load_items_from_champ(self):
        for i in self.champ.heats:
            self.append(i)

    # @property
    # def dict(self):
    #     dict_heats = {}
    #     for i in self:
    #         dict_heats[i.heat_id] = i
    #     return dict_heats

    # def get_heat(self, heat_id):
    #     heat = None
    #     for i in self:
    #         if i.heat_id == heat_id:
    #             heat = i
    #             break
    #     return heat

    # def get_result(self, result_id):
    #     for heat in self:
    #         heat.results.load_items_from_dbs()
    #         for result in heat.results:
    #             if result.result_id == result_id:
    #                 # result.result_splits.load_items_from_dbs()
    #                 return result
    #     return None

    # @property
    # def item_blank(self):
    #     return Heat(
    #         heats=self,
    #         heat_id=0,
    #         phase=None,
    #         pos=0,
    #         official=False,
    #         start_time='',
    #         )

#     def delete_items(self, idxs):
#         for idx in sorted(idxs, reverse=True):
#             self.delete_item(idx)

#     def delete_item(self, idx):
#         print("Aquí o código para borrar os elementos")
#         self.pop(idx)  # remove element from list

#     def load_items_from_dbs(self):
#         del self[:]  # borra os elementos que haxa
#         sql = '''
# select heat_id, pos, official, start_time 
# from heats where phase_id=? order by pos '''
#         values = ((self.phase.phase_id, ), )
#         res = self.config.dbs.exec_sql(sql=sql, values=values)
#         (HEAT_ID, POS, OFFICIAL, START_TIME) = range(4)
#         # for i in self.champ.phases:
#         #     i.heats = []
#         for i in res:
#             heat = Heat(
#                     heats=self,
#                     heat_id=i[HEAT_ID],
#                     phase=self.phase,
#                     pos=i[POS],
#                     official=i[OFFICIAL],
#                     start_time=i[START_TIME],
#                     )
#             # phase.heats.append(heat)
#             # print('append heat {}'.format(heat.heat_id))
#             # print('{} - {}'.format(phase.phase_id, heat.heat_id))
#             self.append(heat)
#             # print('{} - {}'.format(phase.phase_id, heat.heat_id))

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
