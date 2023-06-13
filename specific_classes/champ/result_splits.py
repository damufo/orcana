# -*- coding: utf-8 -*-


from cgi import print_environ_usage
import os
from operator import itemgetter, attrgetter
# from specific_classes.report_base import ReportBase
#from specific_classes.conversions import Conversions
from specific_classes.champ.phases import Phases
from specific_classes.champ.result_split import ResultSplit
# from specific_functions import times
# from specific_functions import files


class ResultSplits(list):

    def __init__(self, result):
        self.result = result
        self.config = result.config
        self.sort_reverse = False
        self.sort_last_field = None

    @property
    def champ(self):
        return self.result.results.heat.heats.champ

    @property
    def item_blank(self):
        return ResultSplit(
            result_splits=self,
            result_split_id=0,
            distance=0,
            mark_hundredth=0,
            result_split_code="",
            official=0,
            )

    def set_value(self, value, distance):
        for i in self:
            if i.distance == distance:
                result_split = i
        result_split.mark_time = value
        return result_split


    def delete_items(self, idxs):
        for idx in sorted(idxs, reverse=True):
            self.delete_item(idx)

    def delete_item(self, idx):
        print("Aquí o código para borrar os elementos")
        self.pop(idx)  # remove element from list

    def load_items_from_dbs(self):
        del self[:]  # borra os elementos que haxa
        sql = '''
select result_split_id, distance, mark_hundredth, result_split_code, official
from results_splits
where result_id={} order by distance '''
        sql = sql.format(self.result.result_id)
        res = self.config.dbs.exec_sql(sql=sql)
        (SPLIT_ID, DISTANCE, MARK_HUNDREDTH, RESULT_SPLIT_CODE, OFFICIAL
        ) = range(5)
        for i in res:
            # phase = self.champ.phases.get_phase(i[PHASE_ID])
            # person = self.champ.persons.get_person(i[PERSON_ID])
            # relay = self.champ.relays.get_relay(i[RELAY_ID])
            self.append(ResultSplit(
                    result_splits=self,
                    result_split_id=i[SPLIT_ID],
                    distance=i[DISTANCE],
                    mark_hundredth=i[MARK_HUNDREDTH],
                    result_split_code=i[RESULT_SPLIT_CODE],
                    official=i[OFFICIAL],
                    ))

    @property
    def list_fields(self):
        """
        list fields for form show
        (name as text, align[L:left, C:center, R:right] as text,
                width as integer)
        """
        return (
                (_('Distance'), 'R', 60),
                (_('Mark'), 'R', 100),
                (_('Event code'), 'C', 60),
                )

    @property
    def list_values(self):
        """
        list values for form show
        """
        values = []
        for result_split in self:
            values.append((
                    str(result_split.distance),
                    str(result_split.mark_hundredth),
                    result_split.result_split_code,
                    ))
        return tuple(values)

    def list_sort(self, **kwargs):
        '''
        Sort results by column num or column name
        '''
        field = None
        cols = (  # cols valid to order
            'distance',
            'mark_hundredth',
            'result_split_code',
            )
        order_cols = range(3)
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

    def create_splits(self):
        # delete previous splits
        sql_splits_delete_previous = '''
delete from results_splits where result_id=? '''
        self.config.dbs.exec_sql(
            sql=sql_splits_delete_previous,
            values=((self.result.result_id, ), ))
        sql_splits_for_event = '''
select distance, split_code, official from splits_for_event where 
event_code=(select event_code from events where event_id=
(select event_id from phases where phase_id=?))
order by distance; '''
        sql_result_split = '''
insert into results_splits (result_id, distance, result_split_code, official) 
values( ?, ?, ?, ?)'''
        # Create splits
        splits_for_event = self.config.dbs.exec_sql(
            sql=sql_splits_for_event, values=((self.result.phase.phase_id, ), ))
        if splits_for_event:
            DISTANCE, SPLIT_CODE, OFFICIAL = range(3)
            for event_split in splits_for_event:
                self.config.dbs.exec_sql(
                    sql=sql_result_split,
                    values=((
                        self.result.result_id,
                        event_split[DISTANCE],
                        event_split[SPLIT_CODE],
                        event_split[OFFICIAL]), ))
                self.append(ResultSplit(
                        result_splits=self,
                        result_split_id=self.config.dbs.last_row_id,
                        distance=event_split[DISTANCE],
                        mark_hundredth=0,
                        result_split_code=event_split[SPLIT_CODE],
                        official=event_split[OFFICIAL],
                        ))
        else:
            distance = int(self.result.event.distance * self.result.event.num_members)
            self.config.dbs.exec_sql(
                sql=sql_result_split,
                values=((
                    self.result.result_id,
                    distance,
                    self.result.event.code,
                    1), ))
            self.append(ResultSplit(
                    result_splits=self,
                    result_split_id=self.config.dbs.last_row_id,
                    distance=distance,
                    mark_hundredth=0,
                    result_split_code=self.result.event.code,
                    official=1,
                    ))
            
