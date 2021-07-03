# -*- coding: utf-8 -*- 


from specific_classes.champ.insc_members import InscMembers
from specific_functions import times
from specific_functions import conversion
from specific_functions import normalize


class RelInscription(object):

    def __init__(self, **kwargs):
        self.inscriptions = kwargs['inscriptions']
        self.config = self.inscriptions.champ
        self.id = int(kwargs['id'])
        self.event_id = int(kwargs['event_id'])
        if 'person_id' in list(kwargs.keys()):
            self.person_id = kwargs['person_id']
        else:
            self.person_id = ''
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
        if 'club_id' in list(kwargs.keys()):
            self.club_id = kwargs['club_id']
        else:
            self.club_id = ''
        if 'pool_length' in list(kwargs.keys()):
            self.pool_length = int(kwargs['pool_length'])
        else:
            self.pool_length = 0
        if 'chrono_type' in list(kwargs.keys()):
            self.chrono_type = kwargs['chrono_type']
        else:
            self.chrono_type = ''
        # self._mark_hundredth = 0
        self.mark_hundredth = int(kwargs['mark_hundredth'])
        if 'date_time' in list(kwargs.keys()):
            self.date_time = kwargs['date_time']
        else:
            self.date_time = ''
        if 'venue' in list(kwargs.keys()):
            self.venue = kwargs['venue']
        else:
            self.venue = None
        if 'inscribed' in list(kwargs.keys()):
            self.inscribed = kwargs['inscribed']
        else:
            self.inscribed = False
        self.created_at = kwargs["created_at"]
        self.created_by = kwargs["created_by"]
        self.updated_at = kwargs["updated_at"]
        self.updated_by = kwargs["updated_by"]
        if 'save_action' in list(kwargs.keys()):
            self.save_action = kwargs['save_action']
        else:
            self.save_action = 'I'
        # type_i = [I:individual, R:relay, S: relay by sum, M:relay member]
        if 'type_id' in list(kwargs.keys()):
            self.type_id = kwargs['type_id']

        self._is_manager = None

    @property
    def is_manager(self):
        if self._is_manager is None:
            self._is_manager = False
            if self.champ.is_manager:
                self._is_manager = True
            elif self.config.com_api.username == self.created_by:
                self._is_manager = True
        return self._is_manager

    def set_type_id(self, type_id):
        self.type_id = type_id
        if self.type_id == 'S':
            self.insc_members = InscMembers(inscription=self)
        else:
            self.insc_members = []

    @property
    def champ(self):
        return self.inscriptions.champ

    @property
    def event(self):
        return self.inscriptions.champ.events.get_event(self.event_id)

    @property
    def category(self):
        return self.inscriptions.champ.categories.get_category(
            self.event.category.id)

    @property
    def surname_normalized(self):
        return normalize.normalize(self.surname)

    @property
    def name_normalized(self):
        return normalize.normalize(self.name)

    @property
    def type_id_sort(self):
        type_id_sort = 1
        if self.type_id in ('R', 'S'):
            type_id_sort = 2
        return type_id_sort

    def _get_club_id(self):
        value = None
        if self.club:
            value = self.club.club_id
        return value

    def _set_club_id(self, club_id):
        self.club = self.config.clubs.get_club(club_id)

    club_id = property(_get_club_id, _set_club_id)

    def _get_club_desc(self):
        value = ''
        if self.club:
            value = self.club.short_desc
        return value

    def _set_club_desc(self, club_desc):
        print("OLLO!! Isto non debería pasar nunca!!")
        self.club_id = self.config.clubs.get_club_id(club_desc)

    club_desc = property(_get_club_desc, _set_club_desc)

    # def _get_mark_hundredth(self):
    #     return self._mark_hundredth

    # def _set_mark_hundredth(self, mark_hundredth):
    #     self._mark_hundredth = mark_hundredth

    # mark_hundredth = property(_get_mark_hundredth, _set_mark_hundredth)

    @property
    def equated_hundredth(self):
        champ_pool_length = self.champ.pool_length
        champ_chrono_type = self.champ.chrono_type

        equated_hundredth = conversion.conv_to_pool_chrono(
            mark_hundredth=self.mark_hundredth,
            event_id=self.event.code,
            gender_id=self.gender_id,
            chrono_type=self.chrono_type,
            pool_length=self.pool_length,
            to_pool_length=champ_pool_length,
            to_chrono_type=champ_chrono_type)
        return equated_hundredth

    def _get_mark_time(self):
        mark_time = times.int2time(value=self.mark_hundredth, precision='hun')
        return mark_time

    def _set_mark_time(self, mark_time):  
        if not isinstance(mark_time, str) and not isinstance(mark_time, str):
            mark_time = 0
        self.mark_hundredth = times.time2int(value=mark_time, precision='hun')

    mark_time = property(_get_mark_time, _set_mark_time)

    @property
    def equated_time(self):
        return times.int2time(value=self.equated_hundredth, precision='hun')

    @property
    def year(self):
        return self.birth_date[:4]

    @property
    def item_blank_for_sum(self):
        inscription = Inscription(
            inscriptions=self.inscriptions,
            id=0,
            person_id='',
            surname='',
            name='',
            gender_id='',
            birth_date='',
            club_id='',
            pool_length=0,
            chrono_type='',
            mark_hundredth=354000,
            xdate='',
            venue='',
            type_id='',
            event_id=0,
            created_at="",
            created_by="",
            updated_at="",
            updated_by="",
            save_action='I')
        # inscription.insc_event_add = self.model.insc_event_add
        inscription.club_id = self.club_id
        inscription.event_id = self.event_id
        inscription.gender_id = self.event.gender_id
        inscription.chrono_type = self.champ.chrono_type
        inscription.pool_length = self.champ.pool_length
        inscription.set_type_id('S')
        inscription.parent_inscription = self
        return inscription

    @property
    def save_dict(self):
        variables = {
            "id": self.id,
            "personId": self.person_id,
            "surname": self.surname,
            "name": self.name,
            "genderId": self.gender_id,
            "birthDate": self.birth_date,
            "clubId": self.club_id,
            "poolId": self.pool_length,
            "chronoId": self.chrono_type,
            "markHundredth": self.mark_hundredth,
            "equatedHundredth": self.equated_hundredth,
            "xdate": self.xdate,
            "venue": self.venue,
            "typeId": self.type_id,
            "champId": self.champ.id,
            "eventId": self.event.id,
        }
        return variables

    def save(self):

        query = """
mutation(
    $id: Int!,
    $personId: String!,
    $surname: String!,
    $name: String!,
    $genderId: String!,
    $birthDate: String!,
    $clubId: String!,
    $poolId: Int!,
    $chronoId: String!,
    $markHundredth: Int!,
    $equatedHundredth: Int!,
    $xdate: String!,
    $venue: String!,
    $typeId: String!,
    $champId: Int!,
    $eventId: Int!
    ) {
  saveInscription(
    id: $id,
    personId: $personId,
    surname: $surname,
    name: $name,
    genderId: $genderId,
    birthDate: $birthDate,
    clubId: $clubId,
    poolId: $poolId,
    chronoId: $chronoId,
    markHundredth: $markHundredth,
    equatedHundredth: $equatedHundredth,
    xdate: $xdate,
    venue: $venue,
    typeId: $typeId,
    champId: $champId,
    eventId: $eventId
  ) {
    id
    personId
    surname
    name
    genderId
    birthDate
    clubId
    poolId
    chronoId
    markHundredth
    equatedHundredth
    xdate
    venue
    typeId
    createdAt
    createdBy
    updatedAt
    updatedBy
    champId
    eventId
  }
}
"""
        variables = self.save_dict
        result = self.config.com_api.execute(query, variables)
        if result:
            self.id = result["data"]["saveInscription"]["id"]
            self.created_by = result["data"]["saveInscription"]["createdBy"]
            self.save_action = "U"
        if self.type_id == 'S':
            # save members
            self.insc_members.save()

    def save_old(self):
        champ_id = self.champ.id
        event_id = self.event.code
        gender_id = self.gender_id
        category_id = self.category_id
        # Delete previous inscriptions
        sql = ('update champ_inscriptions set pool_length=?, chrono_type=?, '
                'mark_hundredth=?, equated_hundredth=?, xdate=?, venue=?, inscribed=? where champ_id=? '
                'and event_id=? and gender_id=? and category_id=? and person_id=?')
        values = ((self.pool_length, self.chrono_type, self.mark_hundredth, 
                self.equated_hundredth, self.xdate, 
                self.venue, self.inscribed,
                champ_id, event_id, gender_id, category_id, self.person_id),)
        self.config.dbs.exec_sql(sql=sql, values=values)
               

