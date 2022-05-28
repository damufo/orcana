# -*- coding: utf-8 -*-


import os
from specific_functions import datetimes 


class ResultMember(object):

    def __init__(self, **kwargs):
        self.result_members = kwargs['result_members']
        self.config = self.result_members.config
        self.result_member_id = kwargs['result_member_id']
        self.person = kwargs['person']

    @property
    def pos(self):
        return self.result_members.index(self) + 1

    @property
    def result_id(self):
        return self.result_members.result.result_id

    @property
    def person_id(self):
        return self.person.person_id

    def save(self):
        """
        Save
        """
        if self.result_member_id:
            sql = '''
update results_members set pos=? where result_member_id=?'''
            values = ((self.pos, self.result_member_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO results_members (result_id, pos, person_id)
VALUES(?, ?, ?) '''
            values = ((self.result_id, self.pos, self.person.person_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.result_member_id = self.config.dbs.last_row_id

