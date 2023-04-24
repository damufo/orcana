# -*- coding: utf-8 -*- 


from operator import attrgetter
from .phase_category import PhaseCategory


class PhaseCategories(list):

    '''
    classdocs
    '''
    
    def __init__(self, **kwargs):
        '''
        Constructor
        '''       
        self.phase = kwargs['phase']
        self.config = self.phase.config

        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ(self):
        return self.phase.champ

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (PHASE_CATEGORY_ID, CATEGORY_ID, ACTION)  = range(3)
        sql = '''
select phase_category_id, category_id, action 
from phases_categories where phase_id=? order by pos '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.phase.phase_id,),))
        for i in res:
            category = self.champ.categories.get_category(i[CATEGORY_ID])
            self.append(PhaseCategory(
                    phase_categories = self,
                    phase_category_id = i[PHASE_CATEGORY_ID],
                    action = i[ACTION],
                    category = category,
                    ))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):
        phase_category = self[idx]
        sql =  ("delete from phases_categories "
                "where phase_category_id=? ")
        values = ((phase_category.phase_category_id,),)
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.remove(phase_category)
        # update position for following categories 
        sql =  ("update phases_categories set pos=pos-1 "
                "where phase_id=? and pos>?")
        values = ((self.phase.phase_id, idx + 1),)
        self.config.dbs.exec_sql(sql=sql, values=values)

    def delete_all_items(self):
        # Delete all results_phase_category
        for phase_category in self:
            phase_category.results_phase_category.delete_all_items()

        sql =  ("delete from phases_categories where phase_id=? ")
        values = ((self.phase.phase_id,),)
        self.config.dbs.exec_sql(sql=sql, values=values)
        del self[:] #borra os elementos que haxa
    
    def paste_phase_categories(self, phase_categories_clipboard):
        
        phase_gender_id = self.phase.event.gender_id
        for phase_category_clipboard in phase_categories_clipboard:
            cat_gender_id = phase_category_clipboard.category.gender_id
            add_cat = False
            if ((cat_gender_id == phase_gender_id) or 
            (phase_gender_id == "X" and self.phase.event.ind_rel == "I")):   
                phase_category = PhaseCategory(
                        phase_categories = self,
                        phase_category_id = 0,
                        action = phase_category_clipboard.action,
                        category = phase_category_clipboard.category,
                        )
                self.append(phase_category)
                phase_category.save()

    # def save_all_items(self):
    #     for i in self:
    #         i.save()

    def add_items(self, categories, action):
        """
        categories: list of categories
        """
        for category in categories:
            phase_category = PhaseCategory(
                    phase_categories = self,
                    phase_category_id = 0,
                    action = action,
                    category = category,
                    )
            self.append(phase_category)
            phase_category.save()

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
            values.append((i.category.name, i.category.category_id))
        return values

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('Pos.'), 'C', 90),
                (_('C. code'), 'C', 110),
                (_('C. gender'), 'C', 110),
                (_('C. name'), 'L', 200),
                (_('Action'), 'L', 110),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            values.append((
                    i.pos,
                    i.category.code,
                    i.category.gender_id,
                    i.category.name,
                    i.action,
                    ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (
                'pos',
                'category.code',
                'category.gender_id',
                'category.name',
                'action',
                )
        # cols valid to order
        order_cols = range(4)
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