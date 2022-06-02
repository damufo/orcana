# -*- coding: utf-8 -*- 

import bisect
# from unicodedata import category
from specific_functions import marks
from specific_classes.champ.result_splits import ResultSplits
from specific_classes.champ.result_members import ResultMembers


class Result(object):

    def __init__(self, **kwargs):
        self.results = kwargs['results']
        self.config = self.results.config
        self.result_id = int(kwargs['result_id'])
        # self.heat = kwargs['heat']
        self.lane = kwargs['lane']
        self.person = kwargs['person']
        self.relay = kwargs['relay']
        self.arrival_pos = kwargs['arrival_pos']
        self.issue_id = kwargs['issue_id']
        self.issue_split = kwargs['issue_split']
        self.equated_hundredth = kwargs['equated_hundredth'] # marca de ordenación, predeterminada é a de inscricion 
        self.inscription = kwargs['inscription']
        # self.splits = Splits()
        self.result_splits = ResultSplits(result=self)
        if self.ind_rel == 'R':
            self.result_members = ResultMembers(result=self)
            self.result_members.load_items_from_dbs()
        else:
            self.result_members = None

    def __lt__(a, b):
        return a.lane < b.lane

    @property
    def champ(self):
        return self.results.champ

    @property
    def heat(self):
        return self.results.heat

    @property
    def event(self):
        return self.results.event

    @property
    def phase(self):
        return self.results.phase

    # def set_type_id(self, type_id):
    #     self.type_id = type_id
    #     if self.type_id == 'S':
    #         self.insc_members = InscMembers(inscription=self)
    #     else:
    #         self.insc_members = []

    @property
    def ind_rel(self):
        '''
        return I: individual, R: relay
        '''
        return self.heat.ind_rel
    
    @property
    def owner(self):
        '''
        return I: individual, R: relay
        '''
        if self.ind_rel == 'I':
            owner = self.person
        elif self.ind_rel == 'R':
            owner = self.relay
        else:
            owner = None
        return owner

    @property
    def category(self):
        category = ''
        if self.person:
            person = self.person
            for i in self.heat.phase.event.categories:
                category = i.category
                print('{} - {}'.format(category.from_age, category.to_age))
                if person.age > category.from_age and person.age < category.to_age and person.gender_id == category.gender_id:
                    category = category
        if self.relay:
            category = self.relay.category

        return category

    @property
    def category_name(self):
        if self.category:
            category_name = self.category.name
        else:
            category_name = ''
        return category_name

    @property
    def mark_hundredth(self):
        return self.result_splits[-1].mark_hundredth

    @property
    def arrival_hundredth(self):
        return self.mark_hundredth

    @property
    def issue_pos(self):
        return self.config.issues.get_pos(self.issue_id)

    def is_inscript(self, person_id):
        already_inscript = False
        if self.ind_rel == 'I':
            for heat in self.heat.heats:
                if heat.phase == self.heat.phase:
                    print(heat.pos)
                    if not heat.results:
                        heat.results.load_items_from_dbs()
                    for result in heat.results:
                        if result.person.person_id == person_id and result != self:
                            already_inscript = True
                            break
                if already_inscript:
                    break
        return already_inscript

    # def _get_mark_hundredth(self):
    #     return self._mark_hundredth

    # def _set_mark_hundredth(self, mark_hundredth):
    #     self._mark_hundredth = mark_hundredth

    # mark_hundredth = property(_get_mark_hundredth, _set_mark_hundredth)

    # @property
    # def equated_hundredth(self):
    #     champ_pool_length = self.champ.pool_length
    #     champ_chrono_type = self.champ.chrono_type

    #     equated_hundredth = conversion.conv_to_pool_chrono(
    #         mark_hundredth=self.mark_hundredth,
    #         event_id=self.event.code,
    #         gender_id=self.person.gender_id,
    #         chrono_type=self.chrono_type,
    #         pool_length=self.pool_length,
    #         to_pool_length=champ_pool_length,
    #         to_chrono_type=champ_chrono_type)
    #     return equated_hundredth
    @property
    def mark_time(self): 
        return marks.hun2mark(value=self.arrival_hundredth)

    @property
    def distance(self):
        return self.result_splits[-1].distance

    @property
    def style_id(self):
        return self.event.style_id

    @property
    def equated_time(self):
        return marks.hun2mark(value=self.equated_hundredth)

    # @property
    # def year(self):
    #     return self.birth_date[:4]

    def save(self):
        if self.result_id:  # Edit
            if self.ind_rel == 'I':
                sql = ('update results set person_id=?, relay_id=0, arrival_pos=?, issue_id=?, issue_split=? where result_id=? ')
                values = ((self.person.person_id, self.arrival_pos, self.issue_id, self.issue_split, self.result_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
            else:
                self.relay.save()
                sql = ('update results set person_id=0, relay_id=?, arrival_pos=?, issue_id=?, issue_split=? where result_id=? ')
                values = ((self.relay.relay_id, self.arrival_pos, self.issue_id, self.issue_split, self.result_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)

        else:  # Insert
            if self.ind_rel == 'I':
                sql = '''
    INSERT INTO results (heat_id, lane, person_id, arrival_pos, issue_id, issue_split)
    VALUES(?, ?, ?, ?, ?, ?) '''
                values = ((self.heat.heat_id, self.lane, self.person.person_id,
                        self.arrival_pos, self.issue_id, self.issue_split),)
                self.config.dbs.exec_sql(sql=sql, values=values)
                self.result_id = self.config.dbs.last_row_id
            else:
                self.relay.save()
                sql = '''
    INSERT INTO results (heat_id, lane, relay_id, arrival_pos, issue_id, issue_split)
    VALUES(?, ?, ?, ?, ?, ?) '''
                values = ((self.heat.heat_id, self.lane, self.relay.relay_id,
                self.arrival_pos, self.issue_id, self.issue_split),)
                self.config.dbs.exec_sql(sql=sql, values=values)
                self.result_id = self.config.dbs.last_row_id
            self.result_splits.create_splits()
            bisect.insort(self.results, self)
            print(len(self.results))


    def delete(self):
        if self.result_id:
            if self.ind_rel == 'R':  # borra tamén a remuda
                if not self.relay.is_in_use():
                    self.relay.delete()
            sql =  ("delete from results_members where result_id=?")
            values = ((self.result_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            sql =  ("delete from results_splits where result_id=?")
            values = ((self.result_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            sql =  ("delete from results where result_id=?")
            values = ((self.result_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.result_id = 0
            self.results.remove(self)
            # del(self)