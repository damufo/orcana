# -*- coding: utf-8 -*- 


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

    @property
    def champ(self):
        return self.event.champ

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (EVENT_CATEGORY_ID, CATEGORY_ID, POS)  = range(3)
        sql = '''
select event_category_id, category_id 
from events_categories where event_id=? order by pos '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.event.event_id,),))
        for pos, i in enumerate(res):
            category = self.champ.categories.get_category(i[CATEGORY_ID])
            self.append(EventCategory(
                    categories = self,
                    event_category_id = i[EVENT_CATEGORY_ID],
                    pos=pos,
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
            

    # def get_category(self, category_id):
    #     category = None
    #     for i in self:
    #         if i.category_id == category_id:
    #             category = i
    #             break
    #     return category
    # 
    # @property    
    # def item_blank(self):
    #     '''
    #     add item on last and return last position.
    #     '''
    #     return EventCategory(
    #             categories=self,
    #             event_category_id=0,
    #             pos=0,
    #             category='',
    #             )

    # def import_categories(self, idxs):
    #     '''
    #     idxs is a list of general categories positions 
    #     '''
    #     for i in idxs:
    #         general_category = self.config.categories[i]
    #         champ_category = Category(
    #             categories=self,
    #             id=0,
    #             code=general_category.category_id,
    #             gender_id=general_category.gender_id,
    #             name=general_category.name,
    #             type_id=general_category.type_id,
    #             from_age=general_category.from_age,
    #             to_age=general_category.to_age,
    #             created_at="",
    #             created_by="",
    #             updated_at="",
    #             updated_by="",
    #             save_action='I')
    #         if not champ_category.already_exists:
    #             self.append(champ_category)
    #             champ_category.save()
    #         else:
    #             print("a categoría xa existe")

    # @property
    # def list_fields(self):
    #     """
    #     list fields for form show
    #     (name as text, align[L:left, C:center, R:right] as text, 
    #             width as integer)
    #     """

    #     return ((_('Category'), 'C', 75),(_('Gender'), 'C', 65), 
    #             (_('Name'), 'L', 100), (_('Type'), 'C', 65),
    #             (_('From year'), 'C', 80), (_('To year'), 'C', 80),)
    # @property
    # def list_values(self):
    #     """
    #     list values for form show
    #     """
    #     values = []
    #     for i in self:
    #         values.append((
    #             i.code,
    #             i.gender_id,
    #             i.name,
    #             i.type_id,
    #             str(i.from_age),
    #             str(i.to_age),))
    #     return  tuple(values)


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
            self.load_items_from_server()
        for i in self:
            values.append((i.category.name, i.category.category_id))
        return values
