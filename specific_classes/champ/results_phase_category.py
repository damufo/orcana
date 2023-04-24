# -*- coding: utf-8 -*-


from operator import attrgetter
from specific_classes.champ.result_phase_category import ResultPhaseCategory


class ResultsPhaseCategory(list):

    def __init__(self, phase_category):
        self.phase_category = phase_category
        self.config = phase_category.config
        self.sort_reverse = False
        self.sort_last_field = None

    # @property
    # def champ(self):
    #     return self.result.champ

    # @property
    # def event(self):
    #     return self.result.event

    # @property
    # def phase(self):
    #     return self.result.phase

    @property
    def item_blank(self):
        return ResultPhaseCategory(
            results_phase_category=self,
            result_phase_category_id=0,
            result=None,
            pos=0,
            points=0.0,
            clas=False,
            )

    def delete_items_non_se_usa(self, idxs):
        for idx in sorted(idxs, reverse=True):
            result = self[idx]
            result.delete_item()
            self.remove(result)  # remove element from list

    def delete_all_items(self):
        sql = '''
delete from results_phases_categories where phase_category_id={}'''
        sql = sql.format(self.phase_category.phase_category_id)
        self.config.dbs.exec_sql(sql=sql)
        del self[:]

    def save_all_items(self):
        for i in self:
            i.save()

#     def load_items_from_dbs(self):
#         del self[:]  # borra os elementos que haxa
#         sql = '''
# select result_phase_category_id, result_id, pos, points, clas
# from results_phases_categories 
# where phase_category_id=? '''
#         # FIXME: pendente de rematar
#         res = self.config.dbs.exec_sql(sql=sql, values=((self.result.result_id, ), ))
#         (RESULT_PHASE_CATEGORY_ID, PHASE_CATEGORY_ID, POS, POINTS, CLAS
#         ) = range(5)
#         for i in res:
#             result = self.champ.results.get_result(i[RESULT_ID])
#             self.append(ResultPhaseCategory(
#                     results_phase_category=self,
#                     result_phase_category_id=i[RESULT_PHASE_CATEGORY_ID],
#                     result=result,
#                     pos=i[POS],
#                     points=i[POINTS],
#                     clas=i[CLAS],
#                     ))

#     @property
#     def list_fields(self):
#         """
#         list fields for form show
#         (name as text, align[L:left, C:center, R:right] as text,
#                 width as integer)
#         """
#         return (
#                 (_('Lane'), 'C', 40),
#                 (_('Name'), 'L', 120),
#                 (_('Entity'), 'C', 40),
#                 (_('Mark'), 'C', 90),
#                 )

#     @property
#     def list_values(self):
#         """
#         list values for form show
#         """
#         values = []
#         pool_lanes = (1, 2, 3, 4, 5, 6)
#         results_dict = {}
#         for i in self:
#             results_dict[i.lane] = i

#         for lane in pool_lanes:
#             if lane in results_dict:
#                 result = results_dict[lane]
#                 values.append((
#                     str(result.lane),
#                     result.person.full_name,
#                     str(result.person.entity.short_name),
#                     '0:00.00',
#                     ))
#             else:
#                 values.append((
#                     str(lane),
#                     '',
#                     '',
#                     '',
#                     ))
#         return tuple(values)

#     def list_sort(self, **kwargs):
#         '''
#         Sort results by column num or column name
#         '''
#         field = None
#         cols = (  # cols valid to order
#             'lane',
#             'person.full_name',
#             'person.entity.short_name',
#             '',
#             )
#         order_cols = range(4)
#         if 'num_col' in list(kwargs.keys()):
#             if kwargs['num_col'] in order_cols:
#                 field = cols[kwargs['num_col']]
#         if self.sort_last_field == field:
#             self.sort_reverse = not self.sort_reverse
#         else:
#             self.sort_reverse = False
#         if field:
#             self.sort_by_field(field=field, reverse=self.sort_reverse)
#             self.sort_last_field = field

#     def sort_by_field(self, field, reverse=False):
#         self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
#         del self[:]
#         self.extend(self_sort)
