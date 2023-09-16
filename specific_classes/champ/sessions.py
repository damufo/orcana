# -*- coding: utf-8 -*- 


from operator import attrgetter
from specific_classes.champ.session import Session


class Sessions(list):

    def __init__(self, champ):     
        self.champ = champ
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def dict(self):
        dict_sessions = {}
        for i in self:
            dict_sessions[i.session_id] = i
        return dict_sessions

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
            date='',
            time='',
            )

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (SESSION_ID, DATE, TIME)  = range(3)
        sql = '''
select session_id, date, time
from sessions order by date, time '''
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
                self.append(Session(
                    sessions=self,
                    session_id=(i[SESSION_ID]),
                    date=(i[DATE]),
                    time=(i[TIME]),
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
            values.append((x, i.date, i.time))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            '',
            'date',
            'time',
            )
        order_cols = range(len(cols))
        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in order_cols:
                field = cols[kwargs['num_col']]
        if field:
            if self.sort_last_field == field:
                self.sort_reverse = not self.sort_reverse
            else:
                self.sort_reverse = False
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field
    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)

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
