# -*- coding: utf-8 -*- 


class EventCategory(object):
    
    def __init__(self, event_categories, event_category_id, category):
        self.event_categories = event_categories
        self.config = self.event_categories.config  
        self.event_category_id = event_category_id
        self.category = category

    @property
    def champ(self):
        return self.categories.champ

    @property
    def event(self):
        return self.event_categories.event

    @property
    def pos(self):
        return self.event_categories.index(self) + 1

    def delete(self):
        # delete results_events_categories
        self.results_event_category.delete_all_items()
        # delete self
        sql = '''
delete events_categories where event_category_id=?'''
        values = ((self.event_category_id, ),)
        self.config.dbs.exec_sql(sql=sql, values=values)

    def save(self):
        """
        Save
        """
        if self.event_category_id:
            sql = '''
update events_categories set pos=?, category_id=? 
where event_category_id=?'''
            values = ((self.pos, self.category.category_id, self.event_category_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO events_categories (pos, event_id, category_id)
VALUES(?, ?, ?) '''
            values = ((self.pos, self.event.event_id, self.category.category_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.event_category_id = self.config.dbs.last_row_id
            # self.champ.events_categories.append(self) non é boa idea facer 
            # isto aquí, mellor facelo antes xa que neste caso a propiedade 
            # pos casca
