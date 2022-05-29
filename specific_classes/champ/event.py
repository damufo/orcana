# -*- coding: utf-8 -*- 

from specific_classes.champ.inscriptions_ind import InscriptionsInd
from specific_classes.champ.inscriptions_rel import InscriptionsRel
from specific_classes.champ.event_categories import EventCategories


class Event(object):

    def __init__(self, **kwargs):
        self.events = kwargs['events']
        self.config = self.events.config
        self.event_id = int(kwargs['event_id'])
        self.pos = int(kwargs['pos']) 
        self.code = kwargs['code']
        self.gender_id = kwargs['gender_id']
        self.name = kwargs['name']
        self.insc_max = int(kwargs['insc_max'])
        if self.ind_rel == 'I':
            self.inscriptions = InscriptionsInd(event=self)
        elif self.ind_rel == 'R':
            self.inscriptions = InscriptionsRel(event=self)
        self.categories = EventCategories(event=self)

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

    # @property
    # def champ_id(self):
    #     return self.events.champ.id

    # @property
    # def category(self):
    #     return self.events.champ.categories.get_category(self.category_id)

    @property
    def distance(self):
        distance = self.code[:len(self.code)-1]
        if self.num_members != 1:
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

    # @property
    # def gender_id(self):
    #     return self.category.gender_id

    def change_event_code(self, new_code):
        self.code = new_code
        self.name = self.generate_name(code=self.code,
                                       gender_id=self.gender_id,
                                       category_code=self.category.code)
        self.save()

    def change_name(self, new_name):
        self.name = new_name
        self.save()

    def already_exists(self):
        """
        Code is event code, ex. 100L, 4X50S, 800L
        Category code: ex. ALEV, SENI
        """
        code = self.code
        category = self.category
        gender_id = category.gender_id
        category_code = category.code
        exists = False
        for i in self.events:
            if i is not self:
                if self.ind_rel == 'R':
                    if (code == i.code and gender_id == i.category.gender_id and
                            category_code == i.category.code):
                        exists = True
                        break
                elif self.ind_rel == 'I':
                    # Non se permite unha proba individual e tamén mixta á vez
                    if (code == i.code and
                            ((gender_id == i.category.gender_id or i.category.gender_id == 'X') or
                            (gender_id == 'X' and i.category.gender_id in ('F', 'M'))) and
                            category_code == i.category.code):
                        exists = True
                        break
        return exists

    def generate_name(self, code, category_id, show_category=True):
        '''
        return generated name
        '''
        name = ""
        if code and category_id:
            code_without_style = code[:len(code)-1]
            style_id = code[-1]
            style = self.config.styles.get_style(style_id=style_id)
            if style:
                style_name = style.long_desc
            else:
                style_name = ''
            category = self.events.champ.categories.get_category(category_id)
            gender_id = category.gender_id
            category_code = category.code
            gender_name = self.config.get_gender_name(gender_id)
            name = '%s m %s %s%s' % (
                code_without_style.lower(), style_name, gender_name,
                (show_category and " {}".format(category_code) or ''))
        return name

#     @property
#     def save_dict(self):
#         pos = len(self.events) + 1
#         for idx, item in enumerate(self.events):
#             if item == self:
#                 pos = idx + 1
#                 break
#         variables = {
#             "id": self.id,
#             "pos": pos,
#             "code": self.code,
#             "name": self.name,
#             "indRel": self.ind_rel,
#             "inscMax": self.insc_max,
#             "champId": self.champ.id,
#             "categoryId": self.category.id
#         }
#         return variables

#     def save(self):
#         pos = len(self.events) + 1
#         for idx, item in enumerate(self.events):
#             if item == self:
#                 pos = idx + 1
#                 break

#         query = """
# mutation(
#     $id: Int!,
#     $pos: Int!,
#     $code: String!,
#     $name: String!,
#     $indRel: String!,
#     $inscMax: Int!,
#     $champId: Int!,
#     $categoryId: Int!
#     ) {
#   saveEvent(
#     id: $id,
#     pos: $pos,
#     code: $code,
#     name: $name,
#     indRel: $indRel,
#     inscMax: $inscMax,
#     champId: $champId,
#     categoryId: $categoryId
#   ) {
#     id
#     pos
#     code
#     name
#     indRel
#     inscMax
#     createdAt
#     createdBy
#     updatedAt
#     updatedBy
#     champId
#     categoryId
#   }
# }
# """
#         variables = self.save_dict
#         result = self.config.com_api.execute(query, variables)
#         if result:
#             self.id = result["data"]["saveEvent"]["id"]
#             self.created_by = result["data"]["saveEvent"]["createdBy"]
#             self.save_action = "U"
    

