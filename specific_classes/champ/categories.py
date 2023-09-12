# -*- coding: utf-8 -*- 


from operator import attrgetter
from .category import Category


class Categories(list):

    def __init__(self, **kwargs):    
        self.champ = kwargs['champ']
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ_id(self):
        return self.champ.champ_id

    @property
    def dict(self):
        dict_categories = {}
        for i in self:
            dict_categories[i.category_id] = i
        return dict_categories

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        (CATEGORY_ID, CODE, GENDER_ID, NAME,
         FROM_AGE, TO_AGE, PUNCTUATION_ID, SHOW_REPORT)  = range(8)
        sql = '''
select category_id, category_code, gender_id, name, from_age, to_age,
punctuation_id, show_report
from categories order by category_code, gender_id '''
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
            punctuation = self.champ.punctuations.get_punctuation(punctuation_id=i[PUNCTUATION_ID])
            self.append(Category(
                    categories=self,
                    category_id=i[CATEGORY_ID],
                    code=i[CODE],
                    gender_id=i[GENDER_ID],
                    name=i[NAME],
                    from_age=i[FROM_AGE],
                    to_age=i[TO_AGE],
                    punctuation=punctuation,
                    show_report=i[SHOW_REPORT],
                    ))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()       

    def get_category(self, category_id):
        category = None
        for i in self:
            if i.category_id == category_id:
                category = i
                break
        return category

    @property    
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Category(
            categories=self,
            category_id=0,
            code='',
            gender_id='',
            name='',
            from_age=0,
            to_age=0,
            punctuation=None,
            show_report=0,
            )

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """

        return (
            (_('Code'), 'C', 75),
            (_('Gender'), 'C', 65), 
            (_('Name'), 'L', 100),
            (_('From age'), 'C', 80),
            (_('To age'), 'C', 80),
            (_('Punctuation'), 'L', 100),
            (_('Show report'), 'C', 100),
            )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            values.append((
                i.code,
                i.gender_id,
                i.name,
                str(i.from_age),
                str(i.to_age), 
                i.punctuation_name, 
                i.show_report and _('S') or '', 
                ))
        return  tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            'code',
            'gender_id',
            'name_normalized',
            'from_age',
            'to_age',
            'punctuation_name',
            'show_report',
            )
        order_cols = range(6)
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
            values.append((i.name, i.category_id))
        return values
