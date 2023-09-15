# -*- coding: utf-8 -*- 


from specific_functions import utils


class Classification(object):
    
    def __init__(self, **kwargs):
        self.classifications = kwargs['classifications']
        self.config = self.classifications.config          
        if 'classification_id' in kwargs.keys():
            self.classification_id = int(kwargs['classification_id'])
        else:
            self.classification_id = 0
        if 'name' in kwargs.keys():
            self.name = kwargs['name']
        else:
            self.name = ''
        if 'gender_id' in kwargs.keys():
            self.gender_id = kwargs['gender_id']
        else:
            self.gender_id = ''
        if 'categories' in kwargs.keys():
            self.categories = kwargs['categories']
        else:
            self.categories = []


    @property
    def champ(self):
        return self.classifications.champ

    @property
    def pos(self):
        return self.classifications.index(self) + 1

    @property
    def categories_ids(self):
        list_ids = [str(i.category_id) for i in self.categories]
        text_ids = ','.join(list_ids)
        return text_ids

    @property
    def categories_code_genders(self):
        list_code_genders = ['{}_{}'.format(i.code, i.gender_id) for i in self.categories]
        text_code_genders = ', '.join(list_code_genders)
        return text_code_genders

    @property
    def name_normalized(self):
        return utils.normalize(self.name)

    def save(self):
        """
        Save
        """
        if self.classification_id:
            sql = '''
update classifications set  pos=?, name=?, gender_id=?, categories=?
where classification_id=?'''
            values = ((self.pos, self.name, self.gender_id, self.categories_ids,
                self.classification_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO classifications (pos, name, gender_id, categories) VALUES(?, ?, ?, ?) '''
            values = ((self.pos, self.name, self.gender_id, self.categories_ids),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.classification_id = self.config.dbs.last_row_id

    def delete(self):
        if self.classification_id:
            sql =  ("delete from classifications where classification_id=?")
            values = ((self.classification_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.classification_id = 0
            self.classifications.remove(self)
