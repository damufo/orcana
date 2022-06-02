# -*- coding: utf-8 -*-


import os
from operator import itemgetter, attrgetter
# from specific_classes.report_base import ReportBase
#from specific_classes.conversions import Conversions
from specific_classes.champ.phases import Phases
from specific_classes.champ.result import Result
# from specific_functions import times
# from specific_functions import files
from specific_classes.champ.event_inscriptions import EventInscriptions

class Results(list):

    def __init__(self, heat):
        self.heat = heat
        self.config = heat.config
        self.sort_reverse = False
        self.sort_last_field = None


    @property
    def champ(self):
        return self.heat.champ

    @property
    def event(self):
        return self.heat.event

    @property
    def phase(self):
        return self.heat.phase

    @property
    def item_blank(self):
        return Result(
            results=self,
            result_id=0,
            # heat=None,
            lane=0,
            person=None,
            relay=None,
            arrival_pos=0,
            issue_id='',
            issue_split=0,
            equated_hundredth=0,
            inscription_id=0  #subtituir isto pola clase inscription, igual que person e relay
            )

    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            result = self[idx]
            result.delete_item()
            self.remove(result)  # remove element from list

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select result_id, heat_id, lane, person_id, relay_id, arrival_pos, issue_id,
issue_split, equated_hundredth, inscription_id
from results r
where heat_id={} order by lane '''
        sql = sql.format(self.heat.heat_id)
        res = self.config.dbs.exec_sql(sql=sql)
        (RESULT_ID, HEAT_ID, LANE, PERSON_ID, RELAY_ID, ARRIVAL_POS, 
        ISSUE_ID, ISSUE_SPLIT, EQUATED_HUNDREDTH, INSCRIPTION_ID
        ) = range(10)
        for i in res:
            # phase = self.champ.phases.get_phase(i[PHASE_ID])
            person = self.champ.persons.get_person(i[PERSON_ID])
            relay = self.champ.relays.get_relay(i[RELAY_ID])
            # heat = self.champ.heats.get_heat(i[HEAT_ID])
            self.append(Result(
                    results=self,
                    result_id=i[RESULT_ID],
                    # heat=self.heat,
                    lane=i[LANE],
                    person=person,
                    relay=relay,
                    arrival_pos=i[ARRIVAL_POS],
                    issue_id=i[ISSUE_ID],
                    issue_split=i[ISSUE_SPLIT],
                    equated_hundredth=i[EQUATED_HUNDREDTH],
                    inscription_id=i[INSCRIPTION_ID]
                    ))

    def get_result(self, lane):
        result = None
        for i in self:
            if i.lane == lane:
                result = i
                break
        return result
    # @property
    # def list_fields(self):
    #     """
    #     list fields for form show
    #     (name as text, align[L:left, C:center, R:right] as text,
    #             width as integer)
    #     """
    #     return ((_('N.'), 'C', 35), (_('Event'), 'C', 70),
    #             (_('Gender'), 'C', 60),
    #             (_('Category'), 'C', 60), (_('Name'), 'L', 240),
    #             (_('Ind/Rel'), 'C', 55),
    #             (_('Inscribed'), 'C', 65))

    # @property
    # def list_values(self):
    #     """
    #     list values for form show
    #     """
    #     values = []
    #     for x, i in enumerate(self, 1):
    #         values.append((
    #                        x,
    #                        i.event_id,
    #                        i.gender_id,
    #                        i.category_id,
    #                        i.name,
    #                        i.ind_rel,
    #                        i.count_inscriptions))
    #     return tuple(values)



    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('Lane'), 'C', 40),
                (_('Name'), 'L', 120),
                (_('Entity'), 'C', 40),
                (_('Mark'), 'C', 90),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        pool_lanes = (1, 2, 3, 4, 5, 6)
        results_dict = {}
        for i in self:
            results_dict[i.lane] = i

        for lane in pool_lanes:
            if lane in results_dict:
                result = results_dict[lane]
                values.append((
                    str(result.lane),
                    result.person.full_name,
                    str(result.person.entity.short_name),
                    '0:00.00',
                    ))
            else:
                values.append((
                    str(lane),
                    '',
                    '',
                    '',
                    ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            'lane',
            'person.full_name',
            'person.entity.short_name',
            '',
            )
        order_cols = range(4)
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
