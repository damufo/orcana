# -*- coding: utf-8 -*- 


class Session(object):

    def __init__(self, **kwargs):
        self.sessions = kwargs['sessions']
        self.config = self.sessions.config
        if 'session_id' in kwargs.keys():
            self.session_id = kwargs['session_id']
        else:
            self.session_id = 0
        if 'date' in kwargs.keys():
            self.date = kwargs['date']
        else:
            self.date = ''
        if 'time' in kwargs.keys():
            self.time = kwargs['time']
        else:
            self.time = ''

    @property
    def date_time(self):
        return "{} {}".format(self.date, self.time)

    def save(self):
        """
        Save
        """
        if self.session_id:
            sql = '''
update sessions set  'date'=?, 'time'=? where session_id=?'''
            values = ((self.date, self.time,
                self.session_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO sessions ('date', 'time') VALUES(?, ?) '''
            values = ((self.date, self.time, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.session_id = self.config.dbs.last_row_id

    def delete(self):
        if self.session_id:
            sql =  ("delete from sessions where session_id=?")
            values = ((self.session_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.session_id = 0
            self.sessions.remove(self)
