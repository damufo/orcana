# -*- coding: utf-8 -*-


import os
from specific_functions import datetimes 


class RelayMember(object):

    def __init__(self, **kwargs):
        self.relay_members = kwargs['relay_members']
        self.config = self.relay_members.config
        self.relay_member_id = kwargs['relay_member_id']
        self.person = kwargs['person']

    @property
    def pos(self):
        return self.relay_members.index(self) + 1

    @property
    def relay_id(self):
        return self.relay_members.relay.relay_id

    @property
    def person_id(self):
        return self.person.person_id

    def save(self):
        """
        Save
        """
        if self.relay_member_id:
            sql = '''
update relays_members set pos=? where relay_member_id=?'''
            values = ((self.pos, self.relay_member_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO relays_members (relay_id, pos, person_id)
VALUES(?, ?, ?) '''
            values = ((self.relay_id, self.pos, self.person.person_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.relay_member_id = self.config.dbs.last_row_id

