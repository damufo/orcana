# -*- coding: utf-8 -*- 

import bisect
# from unicodedata import category
from specific_functions import marks
from specific_classes.champ.result_splits import ResultSplits


class Result(object):

    def __init__(self, **kwargs):
        self.inscription = kwargs['inscription']
        self.config = self.inscription.config
        self.result_id = int(kwargs['result_id'])
        self.heat = kwargs['heat']
        self.lane = kwargs['lane']
        self.arrival_pos = kwargs['arrival_pos']
        self.issue_id = kwargs['issue_id']
        self.issue_split = kwargs['issue_split']
        self.equated_hundredth = kwargs['equated_hundredth'] # marca de ordenación, predeterminada é a de inscricion 
        self.result_splits = ResultSplits(result=self)
        self.result_splits.load_items_from_dbs()

    def __lt__(a, b):
        return a.lane < b.lane

    @property
    def champ(self):
        return self.inscription.champ

    @property
    def event(self):
        return self.heat.event

    @property
    def official(self):
        return self.heat.official

    @property
    def person(self):
        return self.inscription.person

    @property
    def relay(self):
        return self.inscription.relay

    @property
    def event(self):
        return self.inscription.event

    @property
    def phase(self):
        return self.inscription.phase

    @property
    def entity(self):
        entity = None
        if self.person:
            entity = self.person.entity
        elif self.relay:
            entity = self.relay.entity
        return entity

    # def set_type_id(self, type_id):
    #     self.type_id = type_id
    #     if self.type_id == 'S':
    #         self.insc_members = InscMembers(inscription=self)
    #     else:
    #         self.insc_members = []

    @property
    def ind_rel(self):
        return self.heat.phase.event.ind_rel
    
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
        """
        Úsase na exportación dos resultados CSV, colle a primeira que atopa
        """
        category = ''
        if self.ind_rel == 'I':
            person = self.person
            for i in self.heat.phase.phase_categories:
                category = i.category
                # print('{} - {}'.format(category.from_age, category.to_age))
                if person.age >= category.from_age and person.age <= category.to_age and person.gender_id == category.gender_id:
                    category = category
                    return category
        elif self.ind_rel == 'R':
            category = self.relay.category
            return category
        return category

    @property
    def categories(self):
        categories = []
        if self.ind_rel == 'I':
            person = self.person
            for i in self.heat.phase.phase_categories:
                category = i.category
                # print('{} {} - {}'.format(category.name, category.from_age, category.to_age))
                if (person.age >= category.from_age 
                    and person.age <= category.to_age 
                    and (person.gender_id == category.gender_id 
                        or category.gender_id == 'X')):
                    categories.append(category)
        elif self.ind_rel == 'R':
            categories.append(self.relay.category)
        return categories

    @property
    def category_code(self):
        # Return code of first category match
        category_code = ''
        categories  = self.categories
        if categories:
            if len(categories) == 1:
                category_code = self.categories[0].code
            else:  # add "+" as multiple category indicator 
                category_code = "{}+".format(self.categories[0].code)
        
        return category_code

    @property
    def points(self):  # points for first category match, de momento non usado
        points = 0
        phase_category = ''
        if self.inscription.person:
            person = self.person
            for i in self.inscription.phase.phase_categories:

                if (self.inscription.person.age >  i.category.from_age and 
                        self.inscription.person.age <  i.category.to_age and 
                        self.inscription.person.gender_id ==  i.category.gender_id):
                    phase_category = i
                    break
        elif self.inscirption.relay:
            for i in self.inscription.phase.phase_categories:
                if self.inscription.relay.category.category_id == i.category.category_id:
                    phase_category = i
                    break

        if phase_category:
            for result in phase_category.phase_category_results:
                if result.result_id == self.result_id:
                    points = result.points
                    break
        return points

    @property
    def mark_hundredth(self):           
        return self.result_splits[-1].mark_hundredth

    @property
    def arrival_hundredth(self):
        return self.mark_hundredth

    @property
    def issue_pos(self):
        pos = 0
        if self.issue_id:
            pos = self.config.issues.get_pos(self.issue_id)
        return pos

    def is_inscript_xa_existe_en_inscrions_pode_borrarse(self, person_id):
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
    #     champ_pool_length = self.champ.params['champ_pool_length']
    #     champ_chrono_type = self.champ.params['champ_chrono_type']

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
    def mark_time_st(self):  # lenex swim time 
        return marks.hun2mark(value=self.arrival_hundredth, force='hours')

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
                sql = (
                    'update results set heat_id=?, lane=?, arrival_pos=?, '
                    'issue_id=?, issue_split=? where result_id=? ')
                values = ((
                    self.heat.heat_id, self.lane, self.arrival_pos,
                    self.issue_id, self.issue_split, self.result_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
            else: 
                sql = ('update results set heat_id=?, lane=?, arrival_pos=?, issue_id=?, issue_split=? where result_id=? ')
                values = ((self.heat.heat_id, self.lane, self.arrival_pos, self.issue_id, self.issue_split, self.result_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)

        else:  # Insert
            if self.ind_rel == 'I':
                sql = '''
INSERT INTO results (heat_id, lane, arrival_pos, issue_id, issue_split, equated_hundredth, inscription_id)
VALUES(?, ?, ?, ?, ?, ?, ?) '''
                values = ((self.heat.heat_id, self.lane,
                    self.arrival_pos, self.issue_id, self.issue_split,
                    self.equated_hundredth, self.inscription.inscription_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
                self.result_id = self.config.dbs.last_row_id
            else:
                sql = '''
INSERT INTO results (heat_id, lane, arrival_pos, issue_id, issue_split, equated_hundredth, inscription_id)
VALUES(?, ?, ?, ?, ?, ?, ?) '''
                values = ((self.heat.heat_id, self.lane,
                    self.arrival_pos, self.issue_id, self.issue_split,
                    self.equated_hundredth, self.inscription.inscription_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
                self.result_id = self.config.dbs.last_row_id
            self.result_splits.create_splits()
            # bisect.insort(self.results, self)
            # print(len(self.results))


    def delete(self):
        if self.result_id:
            sql =  ("delete from results_splits where result_id=?")
            values = ((self.result_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            sql =  ("delete from results where result_id=?")
            values = ((self.result_id, ), )
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.result_id = 0
            self.inscription.result = None
            del self