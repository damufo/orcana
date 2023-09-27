# -*- coding: utf-8 -*- 


# Element for phase_category_results


class PhaseCategoryResult(object):

    def __init__(self, **kwargs):
        self.phase_category_results = kwargs['phase_category_results']
        self.config = self.phase_category_results.config
        self.phase_category_result_id = kwargs['phase_category_result_id']
        self.result = kwargs['result']
        self.pos = kwargs['pos']  # position in rank integer value
        self.points = kwargs['points']  # real value 0.00
        self.clas_next_phase = kwargs['clas_next_phase']  # 1 when is clasified to next phase
    
    @property
    def phase_category(self):
        return self.phase_category_results.phase_category
    
    @property
    def phase_category_id(self):
        return self.phase_category_results.phase_category.phase_category_id

    @property
    def phase(self):
        return self.phase_category_results.phase_category.phase

    @property
    def phase_id(self):
        return self.phase_category_results.phase_category.phase.phase_id

    @property
    def category(self):
        return self.phase_category_results.phase_category.category

    @property
    def result_id(self):
        return self.result.result_id

    def save(self):
        if self.phase_category_result_id:  # Edit
            sql = ('update phases_categories_results set pos=?, points=?, '
                   'clas_next_phase=? where phase_category_result_id=? ')
            values = ((self.pos, self.points, self.clas_next_phase, self.phase_category_result_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:  # Insert
            sql = '''
INSERT INTO phases_categories_results (phase_category_id, phase_id, result_id, pos, points, clas_next_phase)
VALUES(?, ?, ?, ?, ?, ?) '''
            values = ((self.phase_category_id, self.phase_id,
                    self.result_id, self.pos,
                    self.points, self.clas_next_phase),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.phase_category_result_id = self.config.dbs.last_row_id

    def delete__non_se_usa(self):
        if self.phase_category_result_id:
            sql =  ("delete from phases_categories_results where phase_category_result_id=?")
            values = ((self.phase_category_result_id, ), )
            self.phase_category_result_id = 0
            self.result_phases_categories.remove(self)
            # del(self)