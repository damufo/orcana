# -*- coding: utf-8 -*-


from numpy import true_divide
from specific_classes.champ.relay_member import RelayMember
from specific_functions import datetimes 

class RelayMembers(list):

    def __init__(self, **kwargs):
        self.relay = kwargs['relay']
        self.config = self.relay.config

    @property
    def champ(self):
        return self.relay.champ

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select relay_member_id, pos, person_id from relays_members
where relay_id=? order by pos'''
        values = ((self.relay.relay_id,),)
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        (RELAY_MEMBER_ID, POS, PERSON_ID) = range(3)
        for i in res:
            person = self.champ.persons.get_person(i[PERSON_ID])
            if not person:
                print('falta a persoa')
            self.append(RelayMember(
                    relay_members=self,
                    relay_member_id=i[RELAY_MEMBER_ID],
                    person=person,
                    ))

    def add_member(self, person):
        member = RelayMember(
            relay_members=self,
            relay_member_id=0,
            person=person,
            )
        self.append(member)
        member.save()
    
    @property
    def num_members(self):
        '''
        get number of members from event id. Ex. 4X50L -> 4
        '''
        return self.relay.event.num_members

    @property
    def has_members(self):
        if len(self) == self.num_members:
            has_members = '√'  # square root 
            sum_years = self.relay.sum_years
            if self.champ.params['champ_estament_id'] == 'MASTE':
                if (sum_years < self.relay.category.from_age or
                        sum_years > self.relay.category.to_age):
                    has_members += '!'
        else:
            has_members = ''
        return has_members

    def delete_items(self, idxs):
        '''
        idx of relay to delete
        '''
        values = ', '.join(map(str, [self[idx].relay_member_id for idx in idxs]))
        sql = '''delete from relays_members where relay_member_id in ({})'''
        sql = sql.format(values)
        self.config.dbs.exec_sql(sql=sql)
        for idx in sorted(idxs, reverse = True):
            self.pop(idx)
        # Garda a posición dos que quedan debaixo
        for relay_member in self:
            relay_member.save()  

    def delete_all_items(self):
        sql = ''' delete from relays_members where relay_id=? '''
        values = ((self.relay.relay_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.clear()

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

    def list_sort(self, **kwargs):
        '''
        Sort relays by column num or column name
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