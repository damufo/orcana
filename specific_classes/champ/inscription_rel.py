# -*- coding: utf-8 -*- 


from specific_functions import marks
from specific_functions import conversion
from specific_classes.champ.inscription import Inscription


class InscriptionRel(Inscription):

    def __init__(self, **kwargs):
        Inscription.__init__(self, **kwargs)
        self.relay = kwargs['relay']

    @property
    def equated_hundredth(self):
        champ_pool_length = self.champ.pool_length
        champ_chrono_type = self.champ.chrono_type
        equated_hundredth = conversion.conv_to_pool_chrono(
            mark_hundredth=self.mark_hundredth,
            event_id=self.event.code,
            gender_id=self.relay.gender_id,
            chrono_type=self.chrono_type,
            pool_length=self.pool_length,
            to_pool_length=champ_pool_length,
            to_chrono_type=champ_chrono_type)
        return equated_hundredth
        
    def save(self):
        # Delete previous inscriptions
        
        self.relay.save()
        if self.inscription_id:
            sql = ('update inscriptions set pool_length=?, chrono_type=?, '
                    'mark_hundredth=?, equated_hundredth=?, date=?, venue=?, '
                    'event_id=?, person_id=Null, relay_id=? where inscription_id=? ')
            values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                    self.equated_hundredth, self.date, 
                    self.venue, self.event.event_id, self.relay.relay_id,
                    self.inscription_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO inscriptions (pool_length, chrono_type, mark_hundredth, 
equated_hundredth, date, venue, event_id, relay_id)
VALUES(?, ?, ?, ?, ?, ?, ?, ?) '''
            values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                    self.equated_hundredth, self.date, 
                    self.venue, self.event.event_id, self.relay.relay_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.inscription_id = self.config.dbs.last_row_id
