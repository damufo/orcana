# -*- coding: utf-8 -*- 


from operator import attrgetter
from .punctuation import Punctuation


class Punctuations(list):

    def __init__(self, **kwargs):    
        self.champ = kwargs['champ']
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ_id(self):
        return self.champ.champ_id

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        (PUNCTUATION_ID, NAME, POINTS_IND, POINTS_REL,
         ENTITY_TO_POINT_IND, ENTITY_TO_POINT_REL)  = range(6)
        sql = '''
select punctuation_id, name, points_ind, points_rel, entity_to_point_ind,
entity_to_point_rel from punctuations order by name '''
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
            self.append(Punctuation(
                    punctuations = self,
                    punctuation_id = i[PUNCTUATION_ID],
                    name = i[NAME],
                    points_ind = i[POINTS_IND],
                    points_rel = i[POINTS_REL],
                    entity_to_point_ind = i[ENTITY_TO_POINT_IND],
                    entity_to_point_rel = i[ENTITY_TO_POINT_REL],
                    ))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()       

    def get_punctuation(self, punctuation_id):
        punctuation = None
        for i in self:
            if i.punctuation_id == punctuation_id:
                punctuation = i
                break
        return punctuation

    @property    
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Punctuation(
            punctuations=self,
            punctuation_id=0,
            name='',
            points_ind='',
            points_rel='',
            entity_to_point_ind='',
            entity_to_point_rel='',
            )

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """

        return (
            (_('Name'), 'L', 75),
            (_('P. Ind.'), 'L', 150), 
            (_('P. Rel.'), 'L', 150),
            (_('Entity to Point Ind.'), 'L', 150), 
            (_('Entity to Point Rel.'), 'L', 150), 
            )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            values.append((
                i.name,
                i.points_ind,
                i.points_rel,
                i.entity_to_point_ind,
                i.entity_to_point_rel,
                ))
        return  tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            'name',
            'points_ind',
            'points_rel',
            'entity_to_point_ind',
            'entity_to_point_rel',
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

    # def move_down(self, pos):
    #     if pos < (len(self)-1):
    #         self[pos], self[pos+1] = self[pos+1], self[pos]
    #         self.update_items_on_dbs([pos, pos+1])

    # def move_up(self, pos):
    #     if pos > 0:
    #         self[pos], self[pos-1] = self[pos-1], self[pos]
    #         self.update_items_on_dbs([pos, pos-1])
   
    # def update_items_on_dbs(self, items=[]):
    #     '''
    #     for year add/substract and up/down
    #     '''
    #     if not items:
    #         items = range(len(self))
    #     for pos in items:
    #         i = self[pos]
    #         i.save()

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', ''))
        if not self:
            self.load_items_from_dbs()
        for i in self:
            values.append((i.name, i.punctuation_id))
        return values
