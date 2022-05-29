# -*- coding: utf-8 -*- 


from specific_functions import utils


class Category(object):
    
    def __init__(self, **kwargs):
        self.categories = kwargs['categories']
        self.config = self.categories.config          
        if 'category_id' in kwargs.keys():
            self.category_id = int(kwargs['category_id'])
        else:
            self.category_id = 0
        if 'code' in kwargs.keys():
            self.code = kwargs['code']
        else:
            self.code = ''
        if 'gender_id' in kwargs.keys():
            self.gender_id = kwargs['gender_id']
        else:
            self.gender_id = ''
        if 'name' in kwargs.keys():
            self.name = kwargs['name']
        else:
            self.name = ''
        if 'from_age' in kwargs.keys():
            self.from_age = int(kwargs['from_age'])
        else:
            self.from_age = 0
        if 'to_age' in kwargs.keys():
            self.to_age = int(kwargs['to_age'])
        else:
            self.to_age = 0

    @property
    def champ(self):
        return self.categories.champ

    @property
    def pos(self):
        return self.result_members.index(self) + 1

    @property
    def name_normalized(self):
        return utils.normalize(self.name)

    def already_exists(self, code, gender_id):
        exists = False
        for i in self.categories:
            if code == i.code and gender_id == i.gender_id and i != self:
                exists = True
                break
        return exists

    def save(self):
        """
        Save
        """
        if self.category_id:
            sql = '''
update categories set  category_code=?, gender_id=?, name=?, from_age=?, to_age=?
where category_id=?'''
            values = ((self.code, self.gender_id,
            self.name, self.from_age, self.to_age, self.category_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO categories (category_code, gender_id, name, from_age, to_age)
VALUES(?, ?, ?, ?, ?) '''
            values = ((self.code, self.gender_id, self.name,
            self.from_age, self.to_age),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.category_id = self.config.dbs.last_row_id
            self.champ.categories.append(self)

    def delete(self):
        if self.category_id:
            sql =  ("delete from categories where category_id=?")
            values = ((self.category_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.category_id = 0
            self.categories.remove(self)

    @property
    def is_in_use(self):
        uses = 0
        sql = '''
select category_id from events_categories where category_id=?; '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.category_id, ), ))
        if res:
            uses = len(res)
        return uses
