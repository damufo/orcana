# -*- coding: utf-8 -*- 


class EventCategory(object):
    
    def __init__(self, categories, event_category_id, pos, category):
        self.categories = categories
        self.config = self.categories.config  
        self.event_category_id = event_category_id
        self.pos = pos
        self.category = category

    @property
    def champ(self):
        return self.categories.champ

    @property
    def already_exists(self):
        exists = False
        for i in self.categories:
            if self.code == i.code and self.gender_id == i.gender_id:
                if i != self:
                    exists = True
                    break
        return exists





