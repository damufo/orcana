# -*- coding: utf-8 -*- 


from specific_functions import utils


class Punctuation(object):
    
    def __init__(self, **kwargs):
        self.punctuations = kwargs['punctuations']
        self.config = self.punctuations.config          
        self.punctuation_id = int(kwargs['punctuation_id'])
        self.name = kwargs['name']
        self.points_ind = kwargs['points_ind']
        self.points_rel = kwargs['points_rel']
        self.entity_to_point_ind = kwargs['entity_to_point_ind']
        self.entity_to_point_rel = kwargs['entity_to_point_rel']


    @property
    def champ(self):
        return self.puntuations.champ

    def save(self):
        """
        Save
        """
        if self.punctuation_id:
            sql = '''
update punctuations set  name=?, points_ind=?, points_rel=?
where punctuation_id=?'''
            values = ((self.name, self.points_ind, self.points_rel),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO punctuations (name, points_ind, points_rel)
VALUES(?, ?, ?) '''
            values = ((self.name, self.points_ind, self.points_rel),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.punctuation_id = self.config.dbs.last_row_id
            self.champ.punctuations.append(self)

    def delete(self):
        if self.punctuation_id:
            sql =  ("delete from punctuations where punctuation_id=?")
            values = ((self.punctuation_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.punctuation_id = 0
            self.punctuations.remove(self)

    @property
    def is_in_use(self):
        uses = 0
        sql = '''
select punctuation_id from punctuations where punctuation_id=?; '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.punctuation_id, ), ))
        if res:
            uses = len(res)
        return uses
