# -*- coding: utf-8 -*- 


from specific_classes.champ.phase_category_results import PhaseCategoryResults


class PhaseCategory(object):
    
    def __init__(self, phase_categories, phase_category_id, action, category):
        self.phase_categories = phase_categories
        self.config = self.phase_categories.config  
        self.phase_category_id = phase_category_id
        self.action = action
        self.category = category
        self.phase_category_results = PhaseCategoryResults(self)

    @property
    def champ(self):
        return self.phase_categories.champ

    @property
    def phase(self):
        return self.phase_categories.phase

    @property
    def pos(self):
        return self.phase_categories.index(self) + 1

    def delete(self):
        # delete phases_categories_results
        self.phase_category_results.delete_all_items()
        # delete self
        sql = '''
delete phases_categories where phase_category_id=?'''
        values = ((self.phase_category_id, ),)
        self.config.dbs.exec_sql(sql=sql, values=values)

    def save(self):
        """
        Save
        """
        if self.phase_category_id:
            sql = '''
update phases_categories set pos=?, category_id=?, action=? 
where phase_category_id=?'''
            values = ((self.pos, self.category.category_id, self.action,
            self.phase_category_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO phases_categories (pos, phase_id, category_id, action)
VALUES(?, ?, ?, ?) '''
            values = ((self.pos, self.phase.phase_id, self.category.category_id,
            self.action),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.phase_category_id = self.config.dbs.last_row_id
            # self.champ.phases_categories.append(self) non é boa idea facer 
            # isto aquí, mellor facelo antes xa que neste caso a propiedade 
            # pos casca
