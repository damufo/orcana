# -*- coding: utf-8 -*- 


# Element for results_phase_category


class ResultPhaseCategory(object):

    def __init__(self, **kwargs):
        self.results_phase_category = kwargs['results_phase_category']
        self.config = self.results_phase_category.config
        self.result_phase_category_id = kwargs['result_phase_category_id']
        self.result = kwargs['result']
        self.pos = kwargs['pos']  # position in rank integer value
        self.points = kwargs['points']  # real value 0.00
        self.clas = kwargs['clas']  # 1 when is clasified to next phase
    
    @property
    def phase_category(self):
        return self.results_phase_category.phase_category
    
    @property
    def phase_category_id(self):
        return self.results_phase_category.phase_category.phase_category_id

    @property
    def phase(self):
        return self.results_phase_category.phase_category.phase

    @property
    def phase_id(self):
        return self.results_phase_category.phase_category.phase.phase_id

    @property
    def category(self):
        return self.results_phase_category.phase_category.category

    @property
    def result_id(self):
        return self.result.result_id

    def save(self):
        if self.result_phase_category_id:  # Edit
            assert "isto non debería pasar nunca"
            # sql = ('update results_phases_categories set pos=?, points=?, '
            #        'clas=? where result_phase_category_id=? ')
            # values = ((self.pos, self.points, self.clas, self.result_phase_category_id),)
            # self.config.dbs.exec_sql(sql=sql, values=values)
        else:  # Insert
            sql = '''
INSERT INTO results_phases_categories (phase_category_id, phase_id, result_id, pos, points, clas)
VALUES(?, ?, ?, ?, ?, ?) '''
            values = ((self.phase_category_id, self.phase_id,
                    self.result_id, self.pos,
                    self.points, self.clas),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.result_phase_category_id = self.config.dbs.last_row_id

    def delete__non_se_usa(self):
        if self.result_phase_category_id:
            sql =  ("delete from results_phases_categories where result_phase_category_id=?")
            values = ((self.result_phase_category_id, ), )
            self.result_phase_category_id = 0
            self.result_phases_categories.remove(self)
            # del(self)