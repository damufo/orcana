# -*- coding: utf-8 -*- 


from specific_classes.champ.session import Session


class Sessions(list):

    def __init__(self, champ):     
        self.champ = champ
        self.config = self.champ.config

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):
        assert "pendente de facer"
        self.pop(idx)  # remove element from list

    def get_session(self, session_id):
        session = None
        for i in self:
            if i.session_id == session_id:
                session = i
                break
        return session     

    @property        
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Session(
            sessions=self,
            session_id=0,
            xdate='',
            xtime='',
            )

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (SESSION_ID, XDATE, XTIME)  = range(3)
        sql = '''
select session_id, xdate, xtime
from sessions order by xdate, xtime '''
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
                self.append(Session(
                    sessions=self,
                    session_id=(i[SESSION_ID]),
                    xdate=(i[XDATE]),
                    xtime=(i[XTIME]),
                    ))

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return ((_('N.'), 'C', 35), (_('Date'), 'C', 70),
                (_('Time'), 'C', 60))

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for x, i in enumerate(self, 1):
            values.append((x, i.xdate, i.xtime))
        return tuple(values)

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', '')) 
        for i in self:
            values.append((i.date_time, i.session_id))
        return values
