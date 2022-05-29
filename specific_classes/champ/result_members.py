# -*- coding: utf-8 -*-


from numpy import true_divide
from specific_classes.champ.result_member import ResultMember
from specific_functions import datetimes 

class ResultMembers(list):

    def __init__(self, **kwargs):
        self.result = kwargs['result']
        self.config = self.result.config

    @property
    def champ(self):
        return self.result.champ

    # def get_person_from_dbs(self, person_id):
    #     name = ''
    #     year = ''
    #     sql = ("select surname||' '||name, substr(birthdate, 1,4)  "
    #            "from persons where person_id=? ")
    #     print(sql)
    #     values = ((person_id,),)
    #     res = self.config.dbs.exec_sql(sql=sql, values=values)
    #     if res:
    #         name = res[0][0]
    #         year = res[0][1]
    #     return name, year

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa

        sql = '''
select result_member_id, pos, person_id from results_members
where result_id=? order by pos'''
        values = ((self.result.result_id,),)

        res = self.config.dbs.exec_sql(sql=sql, values=values)
        (RESULT_MEMBER_ID, POS, PERSON_ID) = range(3)
        for i in res:
            person = self.champ.persons.get_person(i[PERSON_ID])
            if not person:
                print('falta a persoa')
            self.append(ResultMember(
                    result_members=self,
                    result_member_id=i[RESULT_MEMBER_ID],
                    person=person,
                    ))

    def add_member(self, person):
        member = ResultMember(
            result_members=self,
            result_member_id=0,
            person=person,
            )
        self.append(member)
        member.save()
    
    @property
    def num_members(self):
        '''
        get number of members from event id. Ex. 4X50L -> 4
        '''
        return self.result.heat.phase.event.num_members

    @property
    def has_set_members(self):
        if len(self) == self.num_members:
            has_set_members = True
        else:
            has_set_members = False
        return has_set_members


    # def save(self, force_insert=False):
    #     for i in self:
    #         if force_insert:
    #             i.result_member_id = 0
    #         i.save()

    # def reset_members(self):
    #     self.delete_items()
    #     for i in range(self.num_members):
    #         self.add_member(result_member_id=0,
    #                         pos=str(i+1),
    #                         person_id='',
    #                         name='',
    #                         year='',
    #                         )

    # def delete_item(self, idx):
    #     '''
    #     idx of result to delete
    #     '''
    #     result_member = self[idx]
    #     sql =  ("delete from results_members "
    #             "where result_member_id=? ")
    #     values = ((result_member.result_member_id,),)
    #     self.config.dbs.exec_sql(sql=sql, values=values)
    #     self.pop(idx) #remove element from list
    #     # Save new positions
    #     for i in self[idx:]:
    #         i.save()

    def delete_items(self, idxs):
        '''
        idx of result to delete
        '''
        values = ', '.join(map(str, [self[idx].result_member_id for idx in idxs]))
        sql = '''delete from results_members where result_member_id in ({})'''
        sql = sql.format(values)
        self.config.dbs.exec_sql(sql=sql)
        for idx in sorted(idxs, reverse = True):
            self.pop(idx)
        # Garda a posición dos que quedan debaixo
        for result_member in self:
            result_member.save()  

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
            )
    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for i in self:
            entity = self.champ.entities.get_entity(i.person.entity_id)
            values.append((
                i.person.surname,
                i.person.name,
                i.person.gender_id,
                i.person.year,
                entity and entity.entity_code or '',
                entity and entity.short_name or '',
                i.person.license,
                ))
        return  tuple(values)
    # @property
    # def list_fields(self):
    #     """
    #     list fields for form show
    #     (name as text, align[L:left, C:center, R:right] as text,
    #             width as integer)
    #     """
    #     return (
    #             (_('Pos.'), 'C', 40),
    #             (_('Name'), 'L', 120),
    #             (_('Age'), 'C', 40),
    #             )

    # @property
    # def list_values(self):
    #     """
    #     list values for form show
    #     """
    #     values = []
    #     for pos, member in enumerate(self, 1):
    #         values.append((
    #             str(pos),
    #             member.person.full_name,
    #             member.person.age,
    #             ))
    #     return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        return

    def move_down(self, pos):
        """ positions from 0 to ..."""
        if pos < (len(self) - 1):
            self[pos], self[pos + 1] = self[pos + 1], self[pos]
            self[pos].save()
            self[pos + 1].save()

    def move_up(self, pos):
        """ positions from 0 to ..."""
        if pos > 0:
            self[pos], self[pos - 1] = self[pos - 1], self[pos]
            self[pos].save()
            self[pos - 1].save()