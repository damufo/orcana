# -*- coding: utf-8 -*- 


from specific_functions import utils


class Person(object):
    
    def __init__(self, **kwargs):
        self.persons = kwargs['persons']
        
        # self.config = self.categories.config          
        if 'person_id' in list(kwargs.keys()):
            self.person_id = int(kwargs['person_id'])
        else:
            self.person_id = 0
        if 'license' in list(kwargs.keys()):
            self.license = int(kwargs['license'])
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

    @property
    def champ(self):
        return self.persons.champ

    @property
    def year(self):
        year = ''
        if self.birth_date:
            year = self.birth_date[0:4]
        return year

    @property
    def surname_normalized(self):
        return utils.normalize(self.surname)

    @property
    def name_normalized(self):
        return utils.normalize(self.name)
        
    @property
    def exists_item_id(self):
        exists = False
        for i in self.persons:
            if (self.license == i.license and
                self.surname == i.surname and
                self.name == i.name):
                if i != self:
                    exists = True
                    break
        return exists

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
#             "fromYear": self.from_year,
#             "toYear": self.to_year,
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

    @property
    def champ_id(self):
        return self.persons.champ.champ_id
