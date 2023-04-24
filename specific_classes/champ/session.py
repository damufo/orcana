# -*- coding: utf-8 -*- 


class Session(object):

    def __init__(self, **kwargs):
        self.sessions = kwargs['sessions']
        self.config = self.sessions.config
        if 'session_id' in kwargs.keys():
            self.session_id = kwargs['session_id']
        else:
            self.session_id = 0
        if 'xdate' in kwargs.keys():
            self.xdate = kwargs['xdate']
        else:
            self.xdate = ''
        if 'xtime' in kwargs.keys():
            self.xtime = kwargs['xtime']
        else:
            self.xtime = ''

    @property
    def date_time(self):
        return "{} {}".format(self.xdate, self.xtime)