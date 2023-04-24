# -*- coding: utf-8 -*- 


from specific_classes.champ.event import Event


class Events(list):

    def __init__(self, champ):     
        self.champ = champ
        self.config = self.champ.config

    @property
    def champ_id(self):
        return self.champ.champ_id

    # @property
    # def activity_id(self):
    #     return self.champ.activity_id    

    # @property
    # def estament_id(self):
    #     return self.champ.estament_id 

    # @property
    # def scope_id(self):
    #     return self.champ.scope_id 

    @property
    def pool_length(self):
        return self.champ.pool_length

    @property
    def chrono_type(self):
        return self.champ.chrono_type

    @property
    def results_from_date(self):
        return self.champ.results_from_date

    @property
    def results_to_date(self):
        return self.champ.results_to_date 

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):

        query = """ mutation($id: Int!) { deleteEvent(id: $id) { id } } """
        variables = {"id": self[idx].id}
        self.config.com_api.execute(query, variables)

        self.pop(idx)  # remove element from list

    def get_event(self, event_id):
        event = None
        for i in self:
            if i.event_id == event_id:
                event = i
                break
        return event

    # def delete_item(self, pos):
    #     champ_event = self[pos]
    #     sql =  ("delete from champ_events where champ_id=? and event_id=? "
    #             "and gender_id=? and category_id=? ")
    #     values = ((self.champ.id, champ_event.event_id, 
    #                champ_event.gender_id, champ_event.category_id),)
    #     self.config.dbs.exec_sql(sql=sql, values=values)
    #     self.pop(pos) #remove element from list
    #     self.update_items_on_dbs() 

    # def delete_items(self, idxs):
    #     """
    #     Delete indexes items. idx is a tuple
    #     """
    #     sql =  ("delete from champ_events where champ_id=? and event_id=? "
    #             "and gender_id=? and category_id=? ")
        
    #     if idxs:
    #         values = []
    #         for idx in sorted(idxs, reverse=True):
    #             champ_event = self[idx]
    #             values.append((champ_event.champ_id, champ_event.event_id, 
    #                champ_event.gender_id, champ_event.category_id))
    #             self.pop(idx)
    #         if values:
    #             self.config.dbs.exec_sql(sql=sql, values=values)

    #         self.update_items_on_dbs()              

    @property        
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Event(
            events=self,
            event_id=0,
            pos=0,
            code='',
            gender_id='',
            name='',
            insc_max=0,
            save_action='I')

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (EVENT_ID, POS, CODE, GENDER_ID, NAME, IND_REL,
         INSC_MAX)  = range(7)
        sql = '''
select event_id, pos, event_code, gender_id, name, ind_rel, insc_max
from events order by pos '''
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
                event = Event(
                    events=self,
                    event_id=(i[EVENT_ID]),
                    pos=(i[POS]),
                    code=(i[CODE]),
                    gender_id=(i[GENDER_ID]),
                    name=i[NAME],
                    ind_rel=i[IND_REL],
                    insc_max=i[INSC_MAX]
                    )
                event.event_categories.load_items_from_dbs()
                self.append(event)

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
            (_('N.'), 'C', 35),
            (_('Event'), 'C', 70),
            (_('Gender'), 'C', 60), 
            (_('Name'), 'L', 240),
            (_('Ind/Rel'), 'C', 55),
            (_('I. Max'), 'C', 65),
            (_('Categorías'), 'L', 120),)

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for x, i in enumerate(self, 1):
            values.append((
                           x,
                           i.code,
                           i.gender_id,
                        #    i.category.code,
                           i.name,
                           i.ind_rel,
                           i.insc_max,
                           i.event_categories.list_text))
        return tuple(values)

    def move_down(self, pos):
        if pos < (len(self)-1):
            self[pos], self[pos+1] = self[pos+1], self[pos]
            self.update_items_on_dbs([pos, pos+1])

    def move_up(self, pos):
        if pos > 0:
            self[pos], self[pos-1] = self[pos-1], self[pos]
            self.update_items_on_dbs([pos, pos-1])

    def update_items_on_dbs(self, items=None):
        '''
        update position
        '''
        if not items:
            items = range(len(self))
        for pos in items:
            i = self[pos]
            i.save()

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', 0))
        for i in self:
            values.append(("{}. {}".format(i.pos, i.name), i.event_id))
        return values
