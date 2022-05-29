# -*- coding: utf-8 -*- 


from specific_functions import utils


class Entity(object):
    
    def __init__(self, **kwargs):
        self.entities = kwargs['entities']
        self.config = self.entities.config
        self.entity_id = kwargs['entity_id']
        self.entity_code = kwargs['entity_code']
        self.short_name = kwargs['short_name']
        self.medium_name = kwargs['medium_name']
        self.long_name = kwargs['long_name']

    @property
    def short_name_normalized(self):
        return utils.normalize(self.short_name)

    @property
    def medium_name_normalized(self):
        return utils.normalize(self.medium_name)

    @property
    def long_name_normalized(self):
        return utils.normalize(self.long_name)

    @property
    def champ(self):
        return self.entities.champ

    @property
    def already_exists(self):
        exists = False
        for i in self.entities:
            if self.entity_code == i.entity_code:
                if i != self:
                    exists = True
                    break
        return exists
#     def fast_search(self, criterias):
#         """
#         return searched licenses
#         """
        
        
#         sql = '''
# select c.entitycode, c.entitycode || ' ' || cd.mediumdesc  || ' ' || cd.shortdesc 
# from entity as c inner join entitydesc as cd on
# c.entitycode=cd.entitycode 
# where 

# UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.entitycode||c.minidesc||cd.longdesc,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))
# like 
# UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(?,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))

#  order by c.entitycode'''

#         sql = '''
# select c.entity_id, c.entity_id || ' ' || c.medium_name  || ' ' || c.short_name 
# from entities as c
# where 

# UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.short_name||c.medium_name||c.long_name,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))
# like 
# UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(?,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))

#  order by c.entity_id'''
 
#         values = (('%%%s%%' % ('%'.join([i for i in criterias.split(' ') if i])), ), )
#         items = self.config.dbs.exec_sql(sql=sql, values=values)
#         return items

    # def clear(self):
    #         self.entity_id = None
    #         self.entity_code = None
    #         self.short_name = None
    #         self.medium_name = None
    #         self.long_name = None

    def save(self):
        """
        Save
        """
        if self.entity_id:
            sql = '''
UPDATE entities set entity_code=?, short_name=?, medium_name=?, long_name=?
WHERE entity_id=?'''
            values = ((self.entity_code, self.short_name, self.medium_name, 
                       self.long_name, self.entity_id), )
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO entities (entity_code, short_name, medium_name, long_name) 
values( ?, ?, ?, ?)'''
            values = ((self.entity_code, self.short_name, self.medium_name, 
                       self.long_name),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.entity_id = self.config.dbs.last_row_id
            self.champ.entities.append(self)

    def delete(self):
        if self.entity_id:
            sql = '''delete from entities where entity_id=?'''
            values = ((self.entity_id,), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.entity_id = 0
            self.entities.remove(self)

    @property
    def is_in_use(self):
        in_use = None
        sql = '''
select entity_id from persons where entity_id=? union
select entity_id from relays where entity_id=? ; '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.entity_id, self.entity_id), ))
        if res:
            in_use = True
        return in_use