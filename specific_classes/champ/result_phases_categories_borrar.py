# -*- coding: utf-8 -*- 


class ResultPhaseCategory(object):

    def __init__(self, **kwargs):
        self.result_phases_categories = kwargs['result_phases_categories']
        self.config = self.result_puntuations.config
        self.result_phase_category_id = kwargs['result_puntuation_id']
        self.phase_category = kwargs['phase_category']
        self.pos = kwargs['pos']  # position in rank integer value
        self.points = kwargs['points']  # real value 0.00
        self.clas = kwargs['points']  # 1 when is clasified to next phase

    def save__non_se_usa(self):
        if self.result_phase_category_id:  # Edit
            sql = ('update results_phases_categories set pos=?, points=?, '
                   'clas=? where result_phase_category_id=? ')
            values = ((self.pos, self.points, self.clas, self.result_phase_category_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:  # Insert
            sql = '''
INSERT INTO results_phases_categories (phase_category_id, pos, points, clas)
VALUES(?, ?, ?, ?) '''
            values = ((self.phase_category.phase_category_id, self.pos,
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