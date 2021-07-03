# -*- coding: utf-8 -*- 


from .category import Category


class Categories(list):

    '''
    classdocs
    '''
    
    def __init__(self, **kwargs):
        '''
        Constructor
        '''       
        self.champ = kwargs['champ']
        self.config = self.champ.config


    @property
    def champ_id(self):
        return self.champ.champ_id

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (CATEGORY_ID, POS, CODE, GENDER_ID, NAME,
         TYPE_ID, FROM_YEAR, TO_YEAR)  = range(8)
        sql = '''
select category_id, pos, code, gender_id, name, type_id, from_year, to_year 
from categories where champ_id=? order by pos '''
        values = ((self.champ_id,),)
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        for i in res:
            self.append(Category(
                    categories = self,
                    category_id = i[CATEGORY_ID],
                    pos=i[POS],
                    code = i[CODE],
                    gender_id = i[GENDER_ID],
                    name = i[NAME],
                    type_id = i[TYPE_ID],
                    from_year = i[FROM_YEAR],
                    to_year = i[TO_YEAR],
                    save_action='U'))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):

        category = self[idx]
        sql =  ("delete from categories "
                "where champ_id=? and id=? and gender_id=? ")
        values = ((self.champ_id, category.category_id, 
                   category.gender_id),)
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.pop(idx) #remove element from list
    
    # def delete_item(self, pos):

    #     category = self[pos]
    #     sql =  ("delete from champ_categories "
    #             "where champ_id=? and category_id=? and gender_id=? ")
    #     values = ((self.champ_id, category.category_id, 
    #                category.gender_id),)
    #     self.config.dbs.exec_sql(sql=sql, values=values)
    #     self.pop(pos) #remove element from list

    #     self.update_items_on_dbs()

    # def delete_items(self, idxs):
    #     """
    #     Delete indexes items. idx is a tuple
    #     """
    #     sql =  ("delete from champ_categories "
    #             "where champ_id=? and category_id=? and gender_id=? ")

    #     if idxs:
    #         values = []
    #         for idx in sorted(idxs, reverse=True):
    #             champ_category = self[idx]
    #             values.append((self.champ_id, champ_category.category_id,
    #                champ_category.gender_id))
    #             self.pop(idx)
    #         if values:
    #             self.config.dbs.exec_sql(sql=sql, values=values)

    #         self.update_items_on_dbs()          

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
                id=0,
                pos=0,
                code='',
                gender_id='',
                name='',
                type_id='',
                from_year=0,
                to_year=0,
                created_at="",
                created_by="",
                updated_at="",
                updated_by="",
                save_action='I')

    def import_categories(self, idxs):
        '''
        idxs is a list of general categories positions 
        '''
        for i in idxs:
            general_category = self.config.categories[i]
            champ_category = Category(
                categories=self,
                id=0,
                code=general_category.category_id,
                gender_id=general_category.gender_id,
                name=general_category.name,
                type_id=general_category.type_id,
                from_year=general_category.from_year,
                to_year=general_category.to_year,
                created_at="",
                created_by="",
                updated_at="",
                updated_by="",
                save_action='I')
            if not champ_category.exists_item_id:
                self.append(champ_category)
                champ_category.save()
            else:
                print("a categoría xa existe")

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """

        return ((_('Category'), 'C', 75),(_('Gender'), 'C', 65), 
                (_('Name'), 'L', 100), (_('Type'), 'C', 65),
                (_('From year'), 'C', 80), (_('To year'), 'C', 80),)
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
                i.type_id,
                str(i.from_year),
                str(i.to_year),))
        return  tuple(values)

    def year_add(self):
        for i in self:
            i.from_year = i.from_year + 1
            i.to_year = i.to_year + 1
        self.update_items_on_dbs()

    def year_subtract(self):
        for i in self:
            i.from_year = i.from_year - 1
            i.to_year = i.to_year - 1
        self.update_items_on_dbs()

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
            values.append((i.name, i.id))
        return values
