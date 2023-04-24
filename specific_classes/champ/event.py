# -*- coding: utf-8 -*- 

from specific_classes.champ.event_inscriptions_ind import EventInscriptionsInd
from specific_classes.champ.event_inscriptions_rel import EventInscriptionsRel
from specific_classes.champ.event_categories import EventCategories


class Event(object):

    def __init__(self, **kwargs):
        self.events = kwargs['events']
        self.config = self.events.config
        self.event_id = int(kwargs['event_id'])
        self.code = kwargs['code']
        self.gender_id = kwargs['gender_id']
        self.name = kwargs['name']
        self.insc_max = int(kwargs['insc_max'])
        if self.ind_rel == 'I':
            self.inscriptions = EventInscriptionsInd(event=self)
        elif self.ind_rel == 'R':
            self.inscriptions = EventInscriptionsRel(event=self)
        self.event_categories = EventCategories(event=self)

    @property
    def pos(self):
        return self.events.index(self) + 1

    @property
    def long_name(self):
        return '{}. {}'.format(self.pos, self.name)

    @property
    def file_name(self):
        if self.gender_id == 'M':
            gender = 'mas'
        elif self.gender_id == 'F':
            gender = 'fem'
        elif self.gender_id == 'X':
            gender = 'mix'
        return '{}_{}_{}'.format(str(self.pos).zfill(2), self.code.lower(), gender)

    @property
    def ind_rel(self):
        '''
        return I: individual, R: relay
        '''
        if 'X' in self.code.upper():
            value = 'R'
        else:
            value = 'I'
        return value

    @property
    def champ(self):
        return self.events.champ

    @property
    def distance(self):
        distance = self.code[:len(self.code)-1]
        if self.num_members != 1:
            # FIXME: revisar que isto estea ben xa que a distancia que pasa é a do parcial
            distance = distance.upper().split('X')[1]
        return int(distance)

    @property
    def num_splits(self):
        distance = self.distance
        num_members = self.num_members
        distance_total = distance * num_members
        splits = distance_total / 50
        if splits < 1:
            splits = 1
        return splits

    @property
    def num_members(self):
        code_split = self.code.upper().split('X')
        if len(code_split) == 1:
            num_members = 1
        else:
            num_members = int(code_split[0])
        return num_members

    @property
    def style_id(self):
        return self.code[len(self.code)-1]

    def change_event_code(self, new_code):
        self.code = new_code
        self.name = self.generate_name(code=self.code)
        self.save()

    def change_name(self, new_name):
        self.name = new_name
        self.save()

    def already_exists(self):
        """
        Code is event code, ex. 100L, 4X50S, 800L
        """
        code = self.code
        gender_id = self.gender_id
        exists = False
        for i in self.events:
            if i is not self:
                if (code == i.code and gender_id == i.gender_id):
                    exists = True
                    break
        return exists

    def generate_name(self, code, gender_id):
        '''
        return generated name
        '''
        name = ""
        if code and gender_id:
            code_without_style = code[:len(code)-1]
            style_id = code[-1]
            style = self.config.styles.get_style(style_id=style_id)
            if style:
                style_name = style.long_name
            else:
                style_name = ''
            gender_name = self.config.genders.get_long_name(gender_id)
            name = '{} m {} {}'.format(
                code_without_style.lower(),
                style_name,
                gender_name)
        return name

    def save(self):
        """
        Save event
        """
        if self.event_id:
            sql = '''
update events set pos=?, event_code=?, gender_id=?, name=?, ind_rel=?, insc_max=? 
where event_id=?'''
            values = ((self.pos, self.code, self.gender_id, self.name,
            self.ind_rel, self.insc_max, self.event_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO events (pos, event_code, gender_id, name, ind_rel, insc_max)
VALUES(?, ?, ?, ?, ?, ?) '''
            values = ((self.pos, self.code, self.gender_id,
            self.name, self.ind_rel, self.insc_max),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.event_id = self.config.dbs.last_row_id

    def delete(self):

        # Estas event_categoríes veñen do xesde, non hai acceso desde orcana
        self.event_categories.delete_all_items()

        sql = ''' delete from events where event_id={}'''
        sql = sql.format(self.event_id)
        self.config.dbs.exec_sql(sql=sql)