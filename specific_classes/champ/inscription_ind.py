# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import conversion
from specific_classes.champ.inscription import Inscription


class InscriptionInd(Inscription):

    def __init__(self, **kwargs):
        Inscription.__init__(self, **kwargs)
        self.person = kwargs['person']

    @property
    def year(self):
        return self.birth_date[:4]

    @property
    def equated_hundredth(self):
        champ_pool_length = self.champ.pool_length
        champ_chrono_type = self.champ.chrono_type
        equated_hundredth = conversion.conv_to_pool_chrono(
            mark_hundredth=self.mark_hundredth,
            event_id=self.event.code,
            gender_id=self.person.gender_id,
            chrono_type=self.chrono_type,
            pool_length=self.pool_length,
            to_pool_length=champ_pool_length,
            to_chrono_type=champ_chrono_type)
        return equated_hundredth

    def is_inscript(self, person):
        already_inscript = False
        for i in self.inscriptions:
            if i.person.person_id == person.person_id and i != self:
                already_inscript = True
                break
        return already_inscript

    def save(self):
        if self.inscription_id:        
            sql = ('update inscriptions set pool_length=?, chrono_type=?, '
                    'mark_hundredth=?, equated_hundredth=?, date=?, venue=?, '
                    'event_id=?, person_id=?, relay_id=0 where inscription_id=? ')
            values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                    self.equated_hundredth, self.date, 
                    self.venue, self.event.event_id, self.person.person_id,
                    self.inscription_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO inscriptions (pool_length, chrono_type, mark_hundredth, 
equated_hundredth, date, venue, event_id, person_id)
VALUES(?, ?, ?, ?, ?, ?, ?, ?) '''
            values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                    self.equated_hundredth, self.date, 
                    self.venue, self.event.event_id, self.person.person_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.inscription_id = self.config.dbs.last_row_id
            self.champ.inscriptions.append(self)
        self.champ.inscriptions.sort_default()
