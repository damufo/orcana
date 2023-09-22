# -*- coding: utf-8 -*- 


from datetime import date
from specific_functions import utils
from specific_functions import dates
from specific_classes.champ.inscriptions_ind_person import InscriptionsIndPerson

class Person(object):
    
    def __init__(self, **kwargs):
        self.persons = kwargs['persons']
        self.config = self.persons.config
        
        # self.config = self.categories.config          
        if 'person_id' in list(kwargs.keys()):
            self.person_id = int(kwargs['person_id'])
        else:
            self.person_id = 0
        if 'license' in list(kwargs.keys()):
            self.license = kwargs['license']
        else:
            self.license = ''
        if 'surname' in list(kwargs.keys()):
            self.surname = kwargs['surname']
        else:
            self.surname = ''
        if 'name' in list(kwargs.keys()):
            self.name = kwargs['name']
        else:
            self.name = ''
        if 'gender_id' in list(kwargs.keys()):
            self.gender_id = kwargs['gender_id']
        else:
            self.gender_id = ''
        if 'birth_date' in list(kwargs.keys()):
            self.birth_date = kwargs['birth_date']
        else:
            self.birth_date = ''
        if 'entity' in list(kwargs.keys()):
            self.entity = kwargs['entity']
        else:
            self.entity = None
        self.inscriptions = InscriptionsIndPerson(self)

    @property
    def champ(self):
        return self.persons.champ

    @property
    def champ_id(self):
        return self.persons.champ.champ_id

    @property
    def full_name(self):
        return '{}, {}'.format(self.surname.upper(), self.name.title())

    @property
    def full_name_normalized(self):
        return '{}, {}'.format(self.surname_normalized, self.name_normalized)

    @property
    def year(self):
        year = ''
        if self.birth_date:
            year = self.birth_date[0:4]
        return year

    @property
    def age(self):
        age = dates.get_age_for_date(
            birth_date=self.birth_date,
            date_age_calculation=self.champ.params['champ_date_age_calculation'])
        return age

    @property
    def count_inscriptions(self):
        count_inscriptions = 0
        sql = '''select count(person_id) from inscriptions where person_id=? '''
        values = ((self.person_id, ), )
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        if res:
            count_inscriptions = res[0][0]
        return count_inscriptions

    @property
    def count_results(self):
        # é moito máis rápido consultar a base de datos que percorrer os
        # resultados na  procura da participación
        # seguramente se poida mellorar cando se busca por resultados
        count_results = 0
        sql = '''
select count(*) from results r
where inscription_id in 
    (select i.inscription_id from inscriptions i where r.inscription_id=i.inscription_id and person_id=?); '''
        values = ((self.person_id, ), )
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        if res:
            count_results = res[0][0]
        return count_results

    @property
    def count_inscriptions_relays(self):
        # é moito máis rápido consultar a base de datos que percorrer os
        # resultados na  procura da participación
        # seguramente se poida mellorar cando se busca por resultados
        count_relays = 0
        sql = '''
select count(*) from inscriptions
        where relay_id in (select relay_id from relays_members where person_id=?); '''
        values = ((self.person_id, ), )
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        if res:
            count_results = res[0][0]
        return count_results

    @property
    def count_results_relays(self):
        # é moito máis rápido consultar a base de datos que percorrer os
        # resultados na  procura da participación
        # seguramente se poida mellorar cando se busca por resultados
        count_relays = 0
        sql = '''
select count(*) from results r
where inscription_id in 
    (select i.inscription_id from inscriptions i 
        where r.inscription_id=i.inscription_id and relay_id in
            (select relay_id from relays_members where person_id=?)); '''
        values = ((self.person_id, ), )
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        if res:
            count_results = res[0][0]
        return count_results

    @property
    def surname_normalized(self):
        return utils.normalize(self.surname)

    @property
    def name_normalized(self):
        return utils.normalize(self.name)

    @property
    def already_exists(self):
        exists = False
        for i in self.persons:
            if (self.license == i.license and
                self.surname == i.surname and
                self.name == i.name):
                if i != self:
                    exists = True
                    break
        return exists

    # @property
    # def inscriptions(self):
    #     inscriptions = []
    #     for phase in self.champ.phases:
    #         for inscription in phase.inscriptions:
    #             if inscription.person:
    #                 if inscription.person.person_id == self.person_id:
    #                     inscriptions.append(inscription)
    #     return inscriptions

    @property
    def results_de_momento_non_se_usa_pode_borrarse(self):
        results = []
        for phase in phases:
            for inscription in phase.inscriptions:
                if inscription.result:
                    results.append(inscription.result)

    def get_phase_insc(self, phase_id):
        # check if person or relay has another inscription
        inscription = None
        for i in self.inscriptions:
            if i.phase.phase_id == phase_id:
                inscription = i
                break
        return inscription

    def _get_entity_id(self):
        value = None
        if self.entity:
            value = self.entity.entity_id
        return value

    def _set_entity_id(self, entity_id):
        self.entity = self.config.entities.get_entity(entity_id)

    entity_id = property(_get_entity_id, _set_entity_id)

    def _get_entity_short_name(self):
        value = ''
        if self.entity:
            value = self.entity.short_name
        return value

    def _set_entity_short_name(self, entity_name):
        print("OLLO!! Isto non debería pasar nunca!!")
        self.entity_id = self.config.entities.get_entity_id(entity_name)

    entity_name = property(_get_entity_short_name, _set_entity_short_name)
#     @property
#     def save_dict(self):
#         pos = len(self.categories)
#         for idx, item in enumerate(self.categories):
#             if item == self:
#                 pos = idx
#                 break
#         variables = {
#             "id": self.id,
#             "pos": pos,
#             "code": self.code,
#             "genderId": self.gender_id,
#             "name": self.name,
#             "typeId": self.type_id,
#             "fromYear": self.from_age,
#             "toYear": self.to_age,
#             "champId": self.champ.id
#         }
#         return variables

#     def save(self):
#         pos = len(self.categories)
#         for idx, item in enumerate(self.categories):
#             if item == self:
#                 pos = idx
#                 break

#         query = """
# mutation(
#     $id: Int!,
#     $pos: Int!,
#     $code: String!,
#     $genderId: String!,
#     $name: String!,
#     $typeId: String!,
#     $fromYear: Int!,
#     $toYear: Int!,
#     $champId: Int!) {
#   saveCategory(
#     id: $id,
#     pos: $pos,
#     code: $code,
#     genderId: $genderId,
#     name: $name,
#     typeId: $typeId,
#     fromYear: $fromYear,
#     toYear: $toYear,
#     champId: $champId
#   ) {
#     id
#     pos
#     code
#     genderId
#     name
#     typeId
#     fromYear
#     toYear
#     createdAt
#     createdBy
#     updatedAt
#     updatedBy
#     champId
#   }
# }
# """
#         variables = self.save_dict
#         result = self.config.com_api.execute(query, variables)
#         if result:
#             self.id = result["data"]["saveCategory"]["id"]
#             self.created_by = result["data"]["saveCategory"]["createdBy"]
#             self.save_action = "U"

    def save(self):
        """
        Save
        """
        if self.person_id:
            sql = '''
update persons set license=?, surname=?, name=?, gender_id=?, birth_date=?, 
entity_id=? where person_id=?'''
            values = ((self.license, self.surname, self.name,
            self.gender_id, self.birth_date, self.entity_id, self.person_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
        else:
            sql = '''
INSERT INTO persons (license, surname, name, gender_id, birth_date, entity_id)
VALUES(?, ?, ?, ?, ?, ?) '''
            values = ((self.license, self.surname, self.name,
            self.gender_id, self.birth_date, self.entity_id),)
            self.config.dbs.exec_sql(sql=sql, values=values)
            self.person_id = self.config.dbs.last_row_id
            self.champ.persons.append(self)

    def delete(self):
        sql =  ("delete from persons where person_id=?")
        values = ((self.person_id, ), )
        self.config.dbs.exec_sql(sql=sql, values=values)
        self.person_id = 0
        self.persons.remove(self)

    @property
    def is_in_use(self):
        uses = 0
        sql = '''
select person_id from inscriptions where person_id=?
union select person_id from relays_members where person_id=?; '''
        values = ((self.person_id, self.person_id), )
        res = self.config.dbs.exec_sql(sql=sql, values=values)
        if res:
            uses = len(res)
        return uses

    @property
    def is_in_use_rel(self):
        # check if in result relay members
        uses = 0
        sql = '''select person_id from relays_members where person_id=?; '''
        res = self.config.dbs.exec_sql(sql=sql, values=((self.person_id, ), ))
        if res:
            uses = len(res)
        return uses