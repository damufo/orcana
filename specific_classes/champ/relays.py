# -*- coding: utf-8 -*- 


from specific_classes.champ.relay import Relay


class Relays(list):
    
    def __init__(self, champ):   
        self.champ = champ
        self.config = self.champ.config

    @property
    def champ_id(self):
        return self.champ.champ_id

    @property    
    def item_blank(self):
        return Relay(
            relays=self,
            relay_id=0,
            gender_id='',
            category=None,
            entity=None,
        )

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (RELAY_ID, NAME, GENDER_ID, CATEGORY_ID, ENTITY_ID)  = range(5)
        sql = '''
select relay_id, name, gender_id, category_id, entity_id 
from relays order by entity_id, name '''
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
            entity = self.champ.entities.get_entity(entity_id = i[ENTITY_ID])
            category = self.champ.categories.get_category(category_id = i[CATEGORY_ID])
            self.append(Relay(
                    relays=self,
                    relay_id=i[RELAY_ID],
                    name=i[NAME],
                    gender_id=i[GENDER_ID],
                    category=category,
                    entity=entity
                    ))

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()

    def get_relay(self, relay_id):
        relay = None
        for i in self:
            if i.relay_id == relay_id:
                relay = i
                break
        return relay

    @property    
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Relay(
                relays=self,
                relay_id=0,
                name='',
                gender_id='',
                category=None,
                entity=None,
                )

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """
        return (
            (_('Name'), 'L', 100), 
            (_('Gender'), 'C', 60),
            (_('Category'), 'C', 60),
            (_('Entity ID'), 'C', 65),
            (_('Entity name'), 'C', 100),
            )
    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            print(i.entity_id)
            entity = self.champ.entities.get_entity(i.entity_id)
            values.append((
                i.name,
                i.gender_id,
                i.category.name,
                entity and entity.entity_code or '',
                entity and entity.short_name or '',
                i.license,
                ))
        return  tuple(values)

    def year_add(self):
        for i in self:
            i.from_age = i.from_age + 1
            i.to_age = i.to_age + 1
        self.update_items_on_dbs()

    def year_subtract(self):
        for i in self:
            i.from_age = i.from_age - 1
            i.to_age = i.to_age - 1
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
            self.load_items_from_dbs()
        for i in self:
            values.append((i.name, i.id))
        return values
