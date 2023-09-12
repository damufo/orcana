# -*- coding: utf-8 -*- 


from specific_classes.champ.result import Result
from specific_functions import marks
from specific_functions import conversion
from specific_functions import utils



class Inscription(object):

    def __init__(self, **kwargs):
        self.inscriptions = kwargs['inscriptions']
        self.config = self.inscriptions.config
        self.inscription_id = int(kwargs['inscription_id'])
        self.mark_hundredth = int(kwargs['mark_hundredth'])
        self.phase = kwargs['phase']
        if 'pool_length' in list(kwargs.keys()):
            self.pool_length = int(kwargs['pool_length'])
        else:
            self.pool_length = 0
        if 'chrono_type' in kwargs.keys():
            self.chrono_type = kwargs['chrono_type']
        else:
            self.chrono_type = ''
        if 'date' in kwargs.keys():
            self.date = kwargs['date']
        else:
            self.date = ''
        if 'venue' in kwargs.keys():
            self.venue = kwargs['venue']
        else:
            self.venue = ''
        if 'rejected' in kwargs.keys():
            self.rejected = kwargs['rejected']
        else:
            self.rejected = False
        if 'exchanged' in kwargs.keys():
            self.exchanged = kwargs['exchanged']
        else:
            self.exchanged = False
        if 'score' in kwargs.keys():
            self.score = kwargs['score']
        else:
            self.score = True
        if 'clasificate' in kwargs.keys():
            self.clasificate = kwargs['clasificate']
        else:
            self.clasificate = True
        if 'person' in kwargs.keys():
            self.person = kwargs['person']
        else:
            self.person = None
        if 'relay' in kwargs.keys():
            self.relay = kwargs['relay']
        else:
            self.relay = None
        if 'result' in kwargs.keys():
            self.result = kwargs['result_id']
        else:
            self.result = None

    @property
    def champ(self):
        return self.inscriptions.champ

    @property
    def ind_rel(self):
        return self.phase.event.ind_rel

    @property
    def event(self):
        return self.phase.event

    @property
    def lane(self):
        lane_ = -1
        if self.result:
            lane_ = self.result.lane
        return lane_

    def add_result(self, heat, lane):
        if not self.result:
            self.result = Result(
                inscription=self,
                result_id=0,
                heat=heat,
                lane=lane,
                arrival_pos=0,
                issue_id='',
                issue_split=0,
                equated_hundredth=359999,
                )

        else:
            assert "Error: this inscriptions already has result"

    @property
    def heat_pos(self):
        heat_pos_ = -1
        if self.result:
            heat_pos_ = self.result.heat.pos
        return heat_pos_

    @property
    def category(self):
        category = ''
        if self.person:
            person = self.person
            for i in self.phase.phase_categories:
                category = i.category
                print('{} - {}'.format(category.from_age, category.to_age))
                if person.age > category.from_age and person.age < category.to_age and person.gender_id == category.gender_id:
                    category = category
        elif self.relay:
            category = self.relay.category
        return category

    @property
    def year(self):
        return self.birth_date[:4]

    def _get_mark_time(self):
        mark_time = marks.hun2mark(value=self.mark_hundredth)
        return mark_time

    def _set_mark_time(self, mark_time):  
        if not isinstance(mark_time, str) and not isinstance(mark_time, str):
            mark_time = 0
        self.mark_hundredth = marks.mark2hun(value=mark_time)

    mark_time = property(_get_mark_time, _set_mark_time)

    @property
    def equated_hundredth(self):
        if self.ind_rel == 'I':
            gender_id = self.person.gender_id
        elif self.ind_rel == 'R':
            gender_id = self.relay.gender_id
        champ_pool_length = self.champ.params['champ_pool_length']
        champ_chrono_type = self.champ.params['champ_chrono_type']
        equated_hundredth = conversion.conv_to_pool_chrono(
            mark_hundredth=self.mark_hundredth,
            event_id=self.event.code,
            gender_id=gender_id,
            chrono_type=self.chrono_type,
            pool_length=self.pool_length,
            to_pool_length=champ_pool_length,
            to_chrono_type=champ_chrono_type)
        return equated_hundredth
  
    @property
    def equated_time(self):
        return marks.hun2mark(value=self.equated_hundredth)

    @property
    def venue_normalized(self):
        return utils.normalize(self.venue)
 
    def save(self):
        if self.ind_rel == 'I':
            if self.inscription_id:        
                sql = ('update inscriptions set pool_length=?, chrono_type=?, '
                        'mark_hundredth=?, equated_hundredth=?, date=?, venue=?, '
                        'rejected=?, exchanged=?, score=?, clasificate=?, '
                        'phase_id=?, person_id=?, relay_id=0 '
                        ' where inscription_id=? ')
                values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                        self.equated_hundredth, self.date, self.venue, 
                        self.rejected, self.exchanged, self.score, self.clasificate, 
                        self.phase.phase_id, self.person.person_id,
                        self.inscription_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
            else:
                sql = '''
    INSERT INTO inscriptions (pool_length, chrono_type, mark_hundredth, 
    equated_hundredth, date, venue, rejected, exchanged, score, clasificate, phase_id, person_id)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                        self.equated_hundredth, self.date, self.venue, 
                        self.rejected, self.exchanged, self.score, self.clasificate,
                        self.phase.phase_id, self.person.person_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
                self.inscription_id = self.config.dbs.last_row_id
                self.inscriptions.append(self)
            self.inscriptions.sort_default()
        elif self.ind_rel == 'R':
            if self.inscription_id:
                sql = ('update inscriptions set pool_length=?, chrono_type=?, '
                        'mark_hundredth=?, equated_hundredth=?, date=?, venue=?, '
                        'rejected=?, exchanged=?, score=?, clasificate=?, '
                        'phase_id=?, person_id=0, relay_id=? where inscription_id=? ')
                values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                        self.equated_hundredth, self.date, self.venue,
                        self.rejected, self.exchanged, self.score, self.clasificate,
                        self.phase.phase_id, self.relay.relay_id,
                        self.inscription_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
            else:
                sql = '''
    INSERT INTO inscriptions (pool_length, chrono_type, mark_hundredth, 
    equated_hundredth, date, venue, rejected, exchanged, score, clasificate, phase_id, relay_id)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                        self.equated_hundredth, self.date, self.venue, 
                        self.rejected, self.exchanged, self.score, self.clasificate,
                        self.phase.phase_id, self.relay.relay_id),)
                self.config.dbs.exec_sql(sql=sql, values=values)
                self.inscription_id = self.config.dbs.last_row_id
                self.inscriptions.append(self)
            self.inscriptions.sort_default() 


    def delete(self):
        '''
        Delete inscription, relay (if exists), relay_members (if exists),
        result and result_splits
        '''
        # delete result_splits
        sql =  ("delete from results_splits where result_id=(select result_id from results where inscription_id=?)")
        values = ((self.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        # delete relay_members
        sql =  ("delete from relays_members where relay_id=(select relay_id from inscriptions where inscription_id=?)")
        values = ((self.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        # delete relay
        sql =  ("delete from relays where relay_id=(select relay_id from inscriptions where inscription_id=?)")
        values = ((self.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        # delete results
        sql =  ("delete from results where inscription_id=?")
        values = ((self.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        # delete inscription
        sql =  ("delete from inscriptions where inscription_id=?")
        values = ((self.inscription_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.inscription_id = 0  # Isto non debería facer falta
        self.phase.inscriptions.remove(self) #remove element from list

    def is_inscript(self, person_id):
        already_inscript = False
        if self.ind_rel == 'I':
            for inscription in self.inscriptions:
                if inscription.person.person_id == person_id and inscription != self:
                # if hasattr(inscription, 'result') and inscription.result:
                    already_inscript = True
                    break
        return already_inscript