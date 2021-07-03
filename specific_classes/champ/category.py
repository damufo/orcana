# -*- coding: utf-8 -*- 


class Category(object):
    
    def __init__(self, **kwargs):
        self.categories = kwargs['categories']
        self.config = self.categories.config          
        if 'category_id' in list(kwargs.keys()):
            self.category_id = int(kwargs['category_id'])
        else:
            self.category_id = 0
        if 'pos' in list(kwargs.keys()):
            self.pos = int(kwargs['pos'])
        else:
            self.pos = 0
        if 'code' in list(kwargs.keys()):
            self.code = kwargs['code']
        else:
            self.code = ''
        if 'gender_id' in list(kwargs.keys()):
            self.gender_id = kwargs['gender_id']
        else:
            self.gender_id = ''
        if 'name' in list(kwargs.keys()):
            self.name = kwargs['name']
        else:
            self.name = ''
        if 'type_id' in list(kwargs.keys()):
            self.type_id = kwargs['type_id']
        else:
            self.type_id = ''
        if 'from_year' in list(kwargs.keys()):
            self.from_year = int(kwargs['from_year'])
        else:
            self.from_year = 0
        if 'to_year' in list(kwargs.keys()):
            self.to_year = int(kwargs['to_year'])
        else:
            self.to_year = 0
        if 'save_action' in list(kwargs.keys()):
            self.save_action = kwargs['save_action']
        else:
            self.save_action = None

    @property
    def champ(self):
        return self.categories.champ

    @property
    def exists_item_id(self):
        exists = False
        for i in self.categories:
            if self.code == i.code and self.gender_id == i.gender_id:
                if i != self:
                    exists = True
                    break
        return exists

    @property
    def save_dict(self):
        pos = len(self.categories)
        for idx, item in enumerate(self.categories):
            if item == self:
                pos = idx
                break
        variables = {
            "id": self.id,
            "pos": pos,
            "code": self.code,
            "genderId": self.gender_id,
            "name": self.name,
            "typeId": self.type_id,
            "fromYear": self.from_year,
            "toYear": self.to_year,
            "champId": self.champ.id
        }
        return variables

    def save(self):
        pos = len(self.categories)
        for idx, item in enumerate(self.categories):
            if item == self:
                pos = idx
                break

        query = """
mutation(
    $id: Int!,
    $pos: Int!,
    $code: String!,
    $genderId: String!,
    $name: String!,
    $typeId: String!,
    $fromYear: Int!,
    $toYear: Int!,
    $champId: Int!) {
  saveCategory(
    id: $id,
    pos: $pos,
    code: $code,
    genderId: $genderId,
    name: $name,
    typeId: $typeId,
    fromYear: $fromYear,
    toYear: $toYear,
    champId: $champId
  ) {
    id
    pos
    code
    genderId
    name
    typeId
    fromYear
    toYear
    createdAt
    createdBy
    updatedAt
    updatedBy
    champId
  }
}
"""
        variables = self.save_dict
        result = self.config.com_api.execute(query, variables)
        if result:
            self.id = result["data"]["saveCategory"]["id"]
            self.created_by = result["data"]["saveCategory"]["createdBy"]
            self.save_action = "U"

    @property
    def champ_id(self):
        return self.categories.champ.id
