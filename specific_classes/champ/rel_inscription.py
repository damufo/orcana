# -*- coding: utf-8 -*- 


from specific_classes.champ.result_members import RelayMembers
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
        champ_pool_length = self.champ.params['champ_pool_length']
        champ_chrono_type = self.champ.params['champ_chrono_type']

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
