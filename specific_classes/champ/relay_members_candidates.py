# -*- coding: utf-8 -*- 


from operator import itemgetter, attrgetter
from specific_classes.champ.person import Person


class RelayMembersCandidates(list):
    
    def __init__(self, relay_members):   
        self.champ = relay_members.champ
        self.relay_members = relay_members
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ_id(self):
        return self.champ.champ_id

    @property
    def gender_id(self):
        return self.relay_members.relay.gender_id

    @property
    def entity_id(self):
        return self.relay_members.relay.entity.entity_id

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        criterias = []
        (PERSON_ID, LICENSE, SURNAME, NAME, GENDER_ID, BIRTH_DATE,
         ENTITY_ID)  = range(7)

        criterias = ' entity_id="{}" '.format(self.entity_id)
        if self.gender_id != 'X':
            criterias += ' and gender_id="{}" '.format(self.gender_id)

        sql = '''
select person_id, license, surname, name, gender_id, birth_date, entity_id 
from persons where {} order by surname, name '''
        sql =  sql.format(criterias)
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
            entity = self.champ.entities.get_entity(entity_id = i[ENTITY_ID])
            self.append(Person(
                    persons=self,
                    person_id=i[PERSON_ID],
                    license=i[LICENSE],
                    surname=i[SURNAME],
                    name=i[NAME],
                    gender_id=i[GENDER_ID],
                    birth_date=i[BIRTH_DATE],
                    entity=entity
                    ))

    # def delete_items(self, idxs):
    #     for idx in sorted(idxs, reverse=True):
    #         self.delete_item(idx)

    # def delete_item(self, idx):
    #     person = self[idx]
    #     sql =  ("delete from persons "
    #             "where champ_id=? and person_id=?")
    #     values = ((self.champ_id, person.person_id),)
    #     self.config.dbs.exec_sql(sql=sql, values=values)
    #     self.pop(idx) #remove element from list

    def remove_person(self, person_id):
        person = None
        for i in self:
            if i.person_id == person_id:
                person = i
                break
        if person:
            self.remove(person)


    def get_person(self, person_id):
        person = None
        for i in self:
            if i.person_id == person_id:
                person = i
                break
        return person

    @property    
    def item_blank(self):
        '''
        add item on last and return last position.
        '''
        return Person(
                persons=self,
                person_id=0,
                license='',
                surname='',
                name='',
                gender_id='',
                birth_date='',
                entity=None,
                )

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text, 
                width as integer)
        """
        return (
            (_('Surname'), 'L', 250),
            (_('Name'), 'L', 250), 
            (_('Gender'), 'C', 80),
            (_('Year'), 'C', 80),
            (_('Entity ID'), 'C', 95),
            (_('Entity name'), 'C', 150),
            (_('License ID'), 'C', 95),
            )
    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            print(i.entity_id)
            entity = self.champ.entities.get_entity(i.entity_id)
            values.append((
                i.surname,
                i.name,
                i.gender_id,
                i.year,
                entity and entity.entity_code or '',
                entity and entity.short_name or '',
                i.license,
                ))
        return  tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (
            'surname_normalized',
            'name_normalized',
            'gender_id',
            'year',
            '',
            '',
            'license',
            )
        # cols valid to order
        valid_order_cols = (0, 1, 2, 3, 6)

        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in valid_order_cols:
                field = cols[kwargs['num_col']]

        if self.sort_last_field == field:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        if field:
            self.sort_by_field(field=field, reverse=self.sort_reverse)
            self.sort_last_field = field

    def sort_by_field(self, field, reverse=False):
        self_sort = sorted(self, key=attrgetter(field), reverse=reverse)
        del self[:]
        self.extend(self_sort)

    # def year_add(self):
    #     for i in self:
    #         i.from_age = i.from_age + 1
    #         i.to_age = i.to_age + 1
    #     self.update_items_on_dbs()

    # def year_subtract(self):
    #     for i in self:
    #         i.from_age = i.from_age - 1
    #         i.to_age = i.to_age - 1
    #     self.update_items_on_dbs()

    # def move_down(self, pos):
    #     if pos < (len(self)-1):
    #         self[pos], self[pos+1] = self[pos+1], self[pos]
    #         self.update_items_on_dbs([pos, pos+1])

    # def move_up(self, pos):
    #     if pos > 0:
    #         self[pos], self[pos-1] = self[pos-1], self[pos]
    #         self.update_items_on_dbs([pos, pos-1])
   
    # def update_items_on_dbs(self, items=[]):
    #     '''
    #     for year add/substract and up/down
    #     '''
    #     if not items:
    #         items = range(len(self))
    #     for pos in items:
    #         i = self[pos]
    #         i.save()

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', ''))
        if not self:
            self.load_items_from_dbs()
        for i in self:
            values.append((i.name, i.id))
        return values

    def sort(self):
        self_sort = sorted(self, key=attrgetter('surname', 'name'), reverse=False)
        del self[:]
        self.extend(self_sort)