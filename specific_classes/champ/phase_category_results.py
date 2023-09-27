# -*- coding: utf-8 -*-


from operator import attrgetter
from specific_classes.champ.phase_category_result import PhaseCategoryResult


class PhaseCategoryResults(list):

    def __init__(self, phase_category):
        self.phase_category = phase_category
        self.config = phase_category.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ(self):
        return self.phase_category.champ

    @property
    def phase(self):
        return self.phase_category.phase

    # @property
    # def event(self):
    #     return self.result.event

    @property
    def ind_rel(self):
        return self.phase.ind_rel

    @property
    def item_blank(self):
        return PhaseCategoryResult(
            phase_category_results=self,
            phase_category_result_id=0,
            result=None,
            pos=0,
            points=0.0,
            clas_next_phase=False,
            )

    def delete_items_non_se_usa(self, idxs):
        for idx in sorted(idxs, reverse=True):
            result = self[idx]
            result.delete_item()
            self.remove(result)  # remove element from list

    def delete_all_items(self):
        sql = '''
delete from phases_categories_results where phase_category_id={}'''
        sql = sql.format(self.phase_category.phase_category_id)
        self.config.dbs.exec_sql(sql=sql)
        del self[:]

    def save_all_items(self):
        for i in self:
            i.save()

    def load_items_from_dbs(self):
        print("pendente")
        phase_results_dict = self.phase.results_dict
        del self[:]  # borra os elementos que haxa
        sql = '''
select phase_category_result_id, result_id, pos, points, clas_next_phase
from phases_categories_results 
where phase_category_id=? '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.phase_category.phase_category_id, ), ))
        (PHASE_CATEGORY_RESULT_ID, RESULT_ID, POS, POINTS, CLAS_NEXT_PHASE) = range(5)
        for i in res:
            result = phase_results_dict[i[RESULT_ID]]
            self.append(PhaseCategoryResult(
                    phase_category_results=self,
                    phase_category_result_id=i[PHASE_CATEGORY_RESULT_ID],
                    result=result,
                    pos=i[POS],
                    points=i[POINTS],
                    clas_next_phase=i[CLAS_NEXT_PHASE],
                    ))

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        if self.ind_rel == 'I':
            return (
                (_('Pos.'), 'C', 40),
                (_('Name'), 'L', 200),
                (_('Gender'), 'C', 40),
                (_('Year'), 'C', 80),
                (_('Club'), 'L', 60),
                (_('Mark'), 'R', 65),
                (_('License'), 'C', 80),
                (_('Heat'), 'C', 50),
                (_('Lane'), 'C', 50),
                (_('Points'), 'C', 50),
                (_('Clas'), 'C', 50),
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
                (_('Heat'), 'C', 50),
                (_('Lane'), 'C', 50),
                (_('Points'), 'C', 50),
                (_('Clas'), 'C', 50),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        if self.ind_rel == 'I':
            for pos, i in enumerate(self):
                values.append((
                    str(pos+1),
                    i.result.inscription.person.full_name,
                    i.result.inscription.person.gender_id,
                    i.result.inscription.person.birth_date[:4],
                    i.result.inscription.person.entity.short_name,
                    i.result.mark_time,
                    i.result.inscription.person.license,
                    i.result.inscription.heat_pos > -1 and i.result.inscription.heat_pos or '',
                    i.result.lane > -1 and i.result.lane or '',
                    i.points,
                    i.clas,
                    ))
        elif self.ind_rel == 'R':
            for pos, i in enumerate(self):
                if i.result.inscription.relay.relay_members.has_set_members:
                    has_set_members = '√'
                else:
                    has_set_members = ''
                values.append((
                    str(pos+1),
                    i.result.inscription.relay.name,
                    i.result.inscription.relay.gender_id,
                    has_set_members,
                    i.result.inscription.relay.category.name,
                    i.result.inscription.relay.entity.short_name,
                    i.result.mark_time,
                    i.result.inscription.heat_pos > -1 and i.result.inscription.heat_pos or '',
                    i.result.lane > -1 and i.result.lane or '',
                    i.points,
                    i.clas_next_phase and '√' or '',
  
                    ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        return
        field = None
        if self.ind_rel == 'I':
            cols = (
                '',
                'person.full_name_normalized',
                'person.gender_id',
                'person.birth_date',
                'person.entity.short_name_normalized',
                'mark_hundredth',
                'person.license',
                'heat_pos',
                'lane',
                'points',
                'clas',
                )

        elif self.ind_rel == 'R':
            cols = (
                '',
                'relay.name_normalized',
                'relay.gender_id',
                'relay.category.name_normalized',
                'relay.relay_members.has_set_members',
                'relay.entity.short_name_normalized',
                'mark_hundredth',
                'heat_pos',
                'lane',
                )


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
