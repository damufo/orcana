# -*- coding: utf-8 -*-


from operator import attrgetter
from specific_classes.champ.entity import Entity


class Entities(list):

    def __init__(self, champ):     
        self.champ = champ
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ_id(self):
        return self.champ.champ_id

    @property    
    def item_blank(self):
        return Entity(
                entities=self,
                entity_id=0,
                entity_code='',
                short_name='',
                medium_name='',
                long_name='',
                )

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

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()

    def get_entities_with_name(self, name):
        entities = []
        for i in self:
            if (name.upper() in i.short_name.upper()
                    or name.upper() in i.medium_name.upper()
                    or name.upper() in i.long_name.upper()
                    or name.upper() in i.entity_code):
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

    def get_entity_by_code(self, entity_code):
        """ return entity from entity_id """
        entity = None
        for i in self:
            if i.entity_code == entity_code:
                entity = i
                break
        return entity

    def load_items_from_dbs(self):
        del self[:]  # Borra os elementos que haxa
        sql = '''
select entity_id, entity_code, short_name, medium_name, long_name
from entities order by entity_id'''
        (ENTITY_ID, ENTITY_CODE, SHORT_NAME, MEDIUM_NAME, LONG_NAME) = range(5)
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
            current_entity = Entity(
                    entities=self,
                    entity_id=i[ENTITY_ID],
                    entity_code=i[ENTITY_CODE],
                    short_name=i[SHORT_NAME],
                    medium_name=i[MEDIUM_NAME],
                    long_name=i[LONG_NAME])
            self.append(current_entity)

    # def update_entity(self, entity):
    #     '''
    #     entity: class entity
    #     '''
    #     for i in range(len(self)):
    #         if self[i].entity_id == entity.entity_id:
    #             self[i] = entity
    #             break

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """
        return (
            (_('Code'), 'L', 100),
            (_('Short name'), 'L', 80), 
            (_('Medium name'), 'L', 120),
            (_('Long name'), 'L', 160),
            )
    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            values.append((
                i.entity_code,
                i.short_name,
                i.medium_name,
                i.long_name,
                ))
        return  tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            'entity_code',
            'short_name_normalized',
            'medium_name_normalized',
            'long_name_normalized',
            )
        order_cols = range(7)
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
