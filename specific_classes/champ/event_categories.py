# -*- coding: utf-8 -*- 


from operator import attrgetter
from .event_category import EventCategory


class EventCategories(list):

    '''
    classdocs
    '''
    
    def __init__(self, **kwargs):
        '''
        Constructor
        '''       
        self.event = kwargs['event']
        self.config = self.event.config

        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ(self):
        return self.event.champ

    @property
    def list_text(self):
        return ", ".join([i.category.code for i in self])

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (EVENT_CATEGORY_ID, CATEGORY_ID, POS)  = range(3)
        sql = '''
select event_category_id, category_id 
from events_categories where event_id=? order by pos '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.event.event_id,),))
        for i in res:
            category = self.champ.categories.get_category(i[CATEGORY_ID])
            self.append(EventCategory(
                    event_categories = self,
                    event_category_id = i[EVENT_CATEGORY_ID],
                    category = category,
                    ))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):

        event_category = self[idx]
        sql =  ("delete from event_categories "
                "where event_category_id=? ")
        values = ((event_category.event_category_id,),)
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.remove(event_category)
            

    def delete_all_items(self):
        sql =  ("delete from events_categories where event_id=? ")
        values = ((self.event.event_id,),)
        self.config.dbs.exec_sql(sql=sql, values=values)
        del self[:] #borra os elementos que haxa

    def paste_event_categories(self, event_categories_clipboard):
        
        event_gender_id = self.event.gender_id
        for event_category_clipboard in event_categories_clipboard:
            cat_gender_id = event_category_clipboard.category.gender_id
            add_cat = False
            if ((cat_gender_id == event_gender_id) or 
            (event_gender_id == "X" and self.event.ind_rel == "I")):   
                event_category = EventCategory(
                        event_categories = self,
                        event_category_id = 0,
                        category = event_category_clipboard.category,
                        )
                self.append(event_category)
                event_category.save()

    def add_items(self, categories):
        """
        categories: list of categories
        """
        for category in categories:
            event_category = EventCategory(
                    event_categories = self,
                    event_category_id = 0,
                    category = category,
                    )
            self.append(event_category)
            event_category.save()

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('Pos.'), 'C', 90),
                (_('Code'), 'C', 110),
                (_('Gender'), 'C', 110),
                (_('Name'), 'L', 350),
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
            values.append((i.category.name, i.category.category_id))
        return values
