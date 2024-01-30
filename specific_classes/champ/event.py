# -*- coding: utf-8 -*- 


class Event(object):

    def __init__(self, **kwargs):
        self.events = kwargs['events']
        self.config = self.events.config
        self.event_id = int(kwargs['event_id'])
        self.code = kwargs['code']
        self.gender_id = kwargs['gender_id']
        self.name = kwargs['name']
        self.insc_max = int(kwargs['insc_max'])

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
        '''
        Event total event distance
        '''
        event_code = self.code.upper()[:-1]  # [:-1] remove style 
        if 'X' in event_code:
            distance = event_code.split('X')[1]
        else:
            distance = event_code
        return int(distance)

    @property
    def num_splits(self):
        # return integer count splits
        distance = self.distance
        num_members = self.num_members
        distance_total = distance * num_members
        splits = int(distance_total / 50)
        if splits < 1:
            splits = 1
        return splits

    @property
    def splits(self):
        # default_event_splits
        sql = '''
select distance, split_code, official from splits_for_event where 
event_code=? order by distance; '''
        splits = self.config.dbs.exec_sql(sql=sql, values=((self.code, ), ))
        if not splits:  # create defatul final split
            distance = self.distance
            num_members = self.num_members
            distance_total = distance * num_members
            splits = ((distance_total, self.code, 1), )
        return splits

    @property
    def num_members(self):
        event_code = self.code.upper()
        if 'X' in event_code:
            num_members = int(event_code.split('X')[0]) 
        else:
            num_members = 1
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
        # FIXME: remove here: phases, event categories, event heats and event results
        print("FIXME: remove here: phases, event categories, event heats and event results")
        # sql = ''' delete from events where event_id={}'''
        # sql = sql.format(self.event_id)
        # self.config.dbs.exec_sql(sql=sql)
        pass
