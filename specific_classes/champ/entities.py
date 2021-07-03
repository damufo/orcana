# -*- coding: utf-8 -*-


from specific_classes.champ.entity import Entity


class Entities(list):

    def __init__(self, champ):     
        self.champ = champ
        self.config = self.champ.config

    @property
    def champ_id(self):
        return self.champ.champ_id

    def choices(self, add_empty=False, federation_id=None):
        values = []
        if add_empty:
            values.append(('', ''))
        for i in self:
            if federation_id and i.federation_id == federation_id:
                values.append(('%s %s' % (i.entity_id, i.short_name),
                               i.entity_id))
            elif not federation_id:
                values.append(('%s %s' % (i.entity_id, i.short_name),
                               i.entity_id))
        return values

    def delete_item(self, entity):
        self.remove(entity)

    def get_entities_with_name(self, desc):
        entities = []
        for i in self:
            if desc.upper() in i.short_name.upper() \
                            or desc.upper() in i.medium_name.upper() \
                            or desc.upper() in i.long_name.upper():
                entities.append(i)
        return entities

    def get_entity_name(self, entity_id, size="S"):
        """
        size S:short, M:dedium, L: long
        """
        entity_name = ''
        for i in self:
            if i.entity_id == entity_id:
                if size == "S":
                    entity_name = i.short_name
                elif size == "M":
                    entity_name = i.medium_name
                elif size == "L":
                    entity_name = i.long_name
                break
        return entity_name

    def get_entity(self, entity_id):
        """ return entity from entity_id """
        entity = None
        for i in self:
            if i.entity_id == entity_id:
                entity = i
                break
        return entity

    def load_items_from_dbs(self):
        del self[:]  # Borra os elementos que haxa
        sql = '''
select entity_id, entity_code, short_name, medium_name, long_name
from entities where champ_id=? order by entity_id'''
        (ENTITY_ID, ENTITY_CODE, SHORT_NAME, MEDIUM_NAME, LONG_NAME) = range(5)
        res = self.config.dbs.exec_sql(sql=sql, values=((self.champ_id,),))
        for i in res:
            current_entity = Entity(
                    entities=self,
                    entity_id=i[ENTITY_ID],
                    entity_code=i[ENTITY_CODE],
                    short_name=i[SHORT_NAME],
                    medium_name=i[MEDIUM_NAME],
                    long_name=i[LONG_NAME])
            self.append(current_entity)

    def update_entity(self, entity):
        '''
        entity: class entity
        '''
        for i in range(len(self)):
            if self[i].entity_id == entity.entity_id:
                self[i] = entity
                break

    @property
    def list_fields(self):
        pass

    @property
    def list_values(self):
        pass
