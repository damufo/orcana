# -*- coding: utf-8 -*- 


from specific_classes.champ.person import Person
from operator import attrgetter
from specific_functions import utils

class Persons(list):
    
    def __init__(self, champ):   
        self.champ = champ
        self.config = self.champ.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ_id(self):
        return self.champ.champ_id

    def load_items_from_dbs(self):
        del self[:] #borra os elementos que haxa
        
        (PERSON_ID, LICENSE, SURNAME, NAME, GENDER_ID, BIRTH_DATE,
         ENTITY_ID)  = range(7)
        sql = '''
select person_id, license, surname, name, gender_id, birth_date, entity_id 
from persons order by surname, name '''
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
        self.list_sort(num_col=1)
        self.list_sort(num_col=0)

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self[idx].delete()

    def get_persons_with_name(self, criterias, gender_id=None):
        # entities = []
        # for i in self:
        #     if name.upper() in i.short_name.upper() \
        #                     or name.upper() in i.medium_name.upper() \
        #                     or name.upper() in i.long_name.upper():
        #         entities.append(i)
        # return entities

        """
        dbs: databse connection
        return searched licenses
        activity_id and season_id for referee search
        """
        criterias_normalized = utils.normalize(criterias)
        persons = []
        match = '[{}]'.format(
            '].*['.join([i for i in criterias_normalized.split(' ') if i]))
        # regex ='[alv].*[mar].*[jos]'
        import re

        # pattern = '^a...s$'
        if len(criterias_normalized.split(' ')) > 1:
            pattern = '.*'.join([i for i in criterias_normalized.split(' ') if i])
        else:
            pattern = criterias_normalized.split(' ')[0]
        pattern = '.*{}.*'.format(pattern)
        for i in self:
            if not gender_id or i.gender_id == gender_id:
                full_name_normalized = i.full_name_normalized
                result = re.match(pattern, full_name_normalized)
                if result:
                    persons.append(i)



    #     sql = '''
    # select p.person_id,
    # case 
    #     when p.rfen_id != 0 then (p.rfen_id || '. ' || p.surname  || ', ' || p.name)
    #     else (p.person_id || '. ' || p.surname  || ', ' || p.name)
    # end
    # from persons as p where
    # {}
    # {} like {}
    # order by p.surname, p.name '''
    #     sql = sql.format(
    #         dbs.normalize("p.person_id||' ' ||p.surname||' ' ||p.name||' ' ||p.lev_id||' ' ||p.rfen_id"),
    #         dbs.normalize("?"))

    #     values = (('%{}%'.format(
    #         '%'.join([i for i in criterias.split(' ') if i])), ), )
    #     coincidences = dbs.exec_sql(sql=sql, values=values)

        return persons

    def get_person(self, person_id):
        person = None
        for i in self:
            if i.person_id == person_id:
                person = i
                break
        return person

    def get_person_by_license(self, license):
        person = None
        for i in self:
            if i.license == license:
                person = i
                break
        return person

    @property    
    def item_blank(self):
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
            (_('Surname'), 'L', 100),
            (_('Name'), 'L', 100), 
            (_('Gender'), 'C', 60),
            (_('Year'), 'C', 60),
            (_('Entity ID'), 'C', 65),
            (_('Entity name'), 'C', 100),
            (_('License ID'), 'C', 75),
            (_('Inscriptions'), 'C', 75),
            (_('Results'), 'C', 75),
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
                i.count_inscriptions,
                i.count_results,
                ))
        return  tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            'surname_normalized',
            'name_normalized',
            'gender_id',
            'year',
            'entity.entity_code',
            'entity.short_name',
            'license',
            'count_inscriptions'
            'count_results'
            )
        order_cols = range(8)
        if 'num_col' in list(kwargs.keys()):
            if kwargs['num_col'] in order_cols:
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
