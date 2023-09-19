# -*- coding: utf-8 -*- 


from operator import attrgetter
from .classification import Classification


class Classifications(list):

    def __init__(self, **kwargs):    
        self.champ = kwargs['champ']
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    # @property
    # def dict(self):
    #     dict_categories = {}
    #     for i in self:
    #         dict_categories[i.category_id] = i
    #     return dict_categories

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        (CLASSIFICATION_ID, NAME, GENDER_ID, CATEGORIES)  = range(4)
        sql = '''
select classification_id, name, gender_id, categories
from classifications order by pos '''
        res = self.config.dbs.exec_sql(sql=sql)
        categories_dict = self.champ.categories.dict
        for i in res:
            categories = []
            for category_id in i[CATEGORIES].split(','):
                categories.append(categories_dict[int(category_id)])
            self.append(Classification(
                    classifications=self,
                    classification_id=i[CLASSIFICATION_ID],
                    name=i[NAME],
                    gender_id=i[GENDER_ID],
                    categories=categories,
                    ))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()       

    # def get_category(self, category_id):
    #     category = None
    #     for i in self:
    #         if i.category_id == category_id:
    #             category = i
    #             break
    #     return category

    @property    
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Classification(
            classifications=self,
            classification_id=0,
            name='',
            gender_id='',
            categories=[],
            )

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """

        return (
            (_('Name'), 'L', 200),
            (_('Gender'), 'C', 100), 
            (_('Categories'), 'L', 500),
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
                i.gender_id,
                i.categories_code_genders,
                ))
        return  tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        pass

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

    def update_items_on_dbs(self, items=None):
        '''
        Update position
        '''
        if not items:
            items = range(len(self))
        for pos in items:
            i = self[pos]
            i.save()

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', ''))
        # if not self:
        #     self.load_items_from_dbs()
        for i in self:
            values.append((i.name, i.classification_id))
        return values
