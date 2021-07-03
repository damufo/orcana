# -*- coding: utf-8 -*- 


class Entity(object):
    
    def __init__(self, **kwargs):
        if 'entities' in list(kwargs.keys()):
            self.entities = kwargs['entities'] #database and preferences
            self.config = self.entities.config
        else:
            self.entities = None
            self.config = None
        if 'config' in list(kwargs.keys()):
            self.config = kwargs['config']                  
        if 'entity_id' in list(kwargs.keys()):
            self.entity_id = kwargs['entity_id']
        else:
            self.entity_id = 0
        if 'entity_code' in list(kwargs.keys()):
            self.entity_code = kwargs['entity_code']
        else:
            self.entity_code = ''
        if 'short_name' in list(kwargs.keys()):
            self.short_name = kwargs['short_name']
        else:
            self.short_name = ''
        if 'medium_name' in list(kwargs.keys()):
            self.medium_name = kwargs['medium_name']
        else:
            self.medium_name = ''
        if 'long_name' in list(kwargs.keys()):
            self.long_name = kwargs['long_name']
        else:
            self.long_name = ''
        if 'save_action' in list(kwargs.keys()):
            self.save_action = kwargs['save_action']
        else:
            self.save_action = 'I' # de xeito predeterminado engade
            
    def delete(self):
        """
        delete this entity
        """
#         self.entities.delete_item(self)

        sql = '''
delete from entities where entity_id=?'''
        values = ((self.entity_id,), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.clear()
             
    def fast_search(self, criterias):
        """
        return searched licenses
        """
        
        
        sql = '''
select c.entitycode, c.entitycode || ' ' || cd.mediumdesc  || ' ' || cd.shortdesc 
from entity as c inner join entitydesc as cd on
c.entitycode=cd.entitycode 
where 

UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.entitycode||c.minidesc||cd.longdesc,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))
like 
UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(?,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))

 order by c.entitycode'''

        sql = '''
select c.entity_id, c.entity_id || ' ' || c.medium_name  || ' ' || c.short_name 
from entities as c
where 

UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(c.short_name||c.medium_name||c.long_name,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))
like 
UPPER(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(?,'Á','A'), 'É','E'),'Í','I'),'Ó','O'),'Ú','U'),'Ñ','N'),'á','a'), 'é','e'),'í','i'),'ó','o'),'ú','u'),'ñ','n'))

 order by c.entity_id'''
 
        values = (('%%%s%%' % ('%'.join([i for i in criterias.split(' ') if i])), ), )
        items = self.config.dbs.exec_sql(sql=sql, values=values)
        return items
    
#     def get_item_from_db(self, entity_id):
#         sql = '''
# select entity_id, fed_prov_id, short_name, medium_name, long_name,  
# city, email, web, observations, creation_date, export_to_sync, 
# timestamp from entities where entity_id=?'''
#         (ENTITY_ID, FED_PROV_ID, SHORT_NAME, MEDIUM_NAME, LONG_NAME,  
#             CITY, EMAIL, WEB, OBSERVATIONS, CREATION_DATE, 
#             EXPORT_TO_SYNC, TIMESTAMP) = list(range(12))

#         res = self.config.dbs.exec_sql(sql=sql, values=((entity_id,),))
#         if res:
#             i = res[0]
#             self.entity_id = i[ENTITY_ID]
#             self.fed_prov_id = i[FED_PROV_ID]
#             self.short_name = i[SHORT_NAME]
#             self.medium_name = i[MEDIUM_NAME]
#             self.long_name = i[LONG_NAME]
#             self.city = i[CITY]
#             self.email = i[EMAIL]
#             self.web = i[WEB]
#             self.observations = i[OBSERVATIONS]
#             self.creation_date = i[CREATION_DATE]
#             self.export_to_sync = i[EXPORT_TO_SYNC]
#             self.timestamp = i[TIMESTAMP]
#             self.save_action = 'U'
#         else:
#             self.clear()
            
    def clear(self):
            self.entity_id = None
            self.entity_code = None
            self.short_name = None
            self.medium_name = None
            self.long_name = None
            self.save_action = 'I'

    
    def save(self):
        if not self.save_action:
            print("error on save")
        timestamp = self.config.timestamp
        if self.save_action == 'I':
#            table entity
            sql = '''
insert into entities (entity_code, long_name,  medium_name, short_name, champ_id) 
values( ?, ?, ?, ?, ?)'''
            values = ((self.entity_code, self.long_name, self.medium_name, 
                       self.short_name, self.champ_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.entity_id = self.config.dbs.last_row_id
            self.save_action = 'U'
            self.config.entities.update_entity(entity=self)
        elif self.save_action == 'U':
#            table entity
            sql = '''
UPDATE entities set entity_code=?, short_name=?, medium_name=?, long_name=?
where entity_id=?'''
            values = ((self.entity_code, self.short_name, self.medium_name, 
                       self.long_name, self.entity_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.config.entities.update_entity(entity=self)
        else:
            print('ATENCION! NON GARDOU!!!   ERRO ERRO ERRO ERRO????')


