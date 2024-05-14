# -*- coding: utf-8 -*- 

from specific_classes.champ.relay_members import RelayMembers
from specific_functions import utils


class Relay(object):
    
    def __init__(self, **kwargs):
        self.relays = kwargs['relays']
        self.config = self.relays.config          
        if 'relay_id' in list(kwargs.keys()):
            self.relay_id = int(kwargs['relay_id'])
        else:
            self.relay_id = 0
        if 'name' in list(kwargs.keys()):
            self.name = kwargs['name']
        else:
            self.name = ''
        if 'gender_id' in list(kwargs.keys()):
            self.gender_id = kwargs['gender_id']
        else:
            self.gender_id = ''
        if 'category' in list(kwargs.keys()):
            self.category = kwargs['category']
        else:
            self.category = ''
        if 'entity' in list(kwargs.keys()):
            self.entity = kwargs['entity']
        else:
            self.entity = None
        if 'event' in list(kwargs.keys()):
            self.event = kwargs['event']
        else:
            self.event = None
        self.relay_members = RelayMembers(relay=self)
        self.relay_members.load_items_from_dbs()

    @property
    def champ(self):
        return self.relays.champ

    @property
    def event_id(self):
        event_id = 0
        if self.event:
            event_id = self.event.event_id
        else:
            AssertionError("Iston on pode ser.")
        return event_id

    @property
    def num_members(self):
        '''
        get number of members from event id. Ex. 4X50L -> 4
        '''
        return self.event.num_members

    @property
    def has_members(self):
        return self.relay_members.has_members

    @property
    def sum_years(self):
        sum_years = 0
        for i in  self.relay_members:
            sum_years += int(i.person.age)
        return sum_years

    @property
    def long_name(self):
        gender_name = self.config.genders.get_long_name(self.gender_id)
        return '{} ({}) - {} - {}'.format(
            self.name.upper(),
            self.entity.short_name.upper(),
            gender_name,
            self.category.code )

    @property
    def name_normalized(self):
        return utils.normalize(self.name)
        
    # @property
    # def already_exists(self):
    #     exists = False
    #     for i in self.relays:
    #         if (self.license == i.license and
    #             self.surname == i.surname and
    #             self.name == i.name):
    #             if i != self:
    #                 exists = True
    #                 break
    #     return exists

    def _get_entity_id(self):
        value = None
        if self.entity:
            value = self.entity.entity_id
        return value

    def _set_entity_id(self, entity_id):
        self.entity = self.config.entities.get_entity(entity_id)

    entity_id = property(_get_entity_id, _set_entity_id)

    def _get_entity_short_name(self):
        value = ''
        if self.entity:
            value = self.entity.short_name
        return value

    def _set_entity_short_name(self, entity_name):
        print("OLLO!! Isto non debería pasar nunca!!")
        self.entity_id = self.config.entities.get_entity_id(entity_name)

    entity_name = property(_get_entity_short_name, _set_entity_short_name)

    @property
    def champ_id(self):
        return self.relays.champ.champ_id

    def save(self):
        """
        Save
        """
        if self.relay_id:
            sql = '''
update relays set name=?, gender_id=?, category_id=?, entity_id=? 
where relay_id=?'''
            values = ((self.name, self.gender_id, self.category.category_id,
            self.entity.entity_id, self.relay_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO relays (name, gender_id, category_id, entity_id)
VALUES(?, ?, ?, ?) '''
            values = ((self.name, self.gender_id, self.category.category_id,
            self.entity.entity_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.relay_id = self.config.dbs.last_row_id
            # self.champ.relays.append(self)

    def delete(self):
        if self.relay_id:
            sql =  ("delete from relays where relay_id=?")
            values = ((self.relay_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.relay_id = 0
            self.relays.remove(self)

    @property
    def is_in_use(self):
        # check if the relay in use
        uses = 0
        sql = '''
select relay_id from inscriptions where relay_id=? union 
select relay_id from relays where relay_id=?; '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.relay_id, self.relay_id), ))
        if res:
            uses = len(res)
        return uses