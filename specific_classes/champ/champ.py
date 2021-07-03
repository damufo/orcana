# -*- coding: utf-8 -*- 


# import os
from specific_classes.champ.entities import Entities
from specific_classes.champ.categories import Categories
from specific_classes.champ.events import Events
from specific_classes.champ.persons import Persons
from specific_classes.champ.ind_inscriptions import IndInscriptions
# # from specific_classes.champ.events_inscriptions import EventsInscriptions
# from specific_classes.champ.inscriptions import Inscriptions
# from specific_classes.champ.reserves import Reserves
# from specific_classes.champ.results import Results
# from specific_functions import files
# from specific_classes.core.manager import Manager


class Champ(object):

    def __init__(self, config):
        self.config = config
        self.champ_id = 0
        self.name = ''
        self.pool_length = 0
        self.pool_lanes = 0
        self.chrono_type = ''

    def load_dbs(self, dbs_path):
        self.config.dbs.connect(dbs_path=dbs_path)
        if self.config.dbs.connection:
            sql = '''
    select champ_id, name, pool_length, pool_lanes, chrono_type
    from champs '''
            (CHAMP_ID, NAME, POOL_LENGTH, POOL_LANES, CHRONO_TYPE) = range(5)
            res = self.config.dbs.exec_sql(sql=sql, n=1)
            if res == 'err' or not res:
                self.champ_id = 0
                self.name = ''
                self.pool_length = 0
                self.pool_lanes = 0
                self.chrono_type = ''
                self.config.prefs['last_path_dbs'] = ''
                self.config.prefs.save()
            else:
                values = res[0]
                self.champ_id = values[CHAMP_ID]
                self.name = values[NAME]
                self.pool_length = values[POOL_LENGTH]
                self.pool_lanes = values[POOL_LANES]
                self.chrono_type = values[CHRONO_TYPE]

                self.entities = Entities(champ=self)
                self.entities.load_items_from_dbs()
                self.categories = Categories(champ=self)
                self.categories.load_items_from_dbs()
                self.events = Events(champ=self)
                self.events.load_items_from_dbs()
                self.persons = Persons(champ=self)
                self.persons.load_items_from_dbs()
                self.ind_inscriptions = IndInscriptions(champ=self)
                self.ind_inscriptions.load_items_from_dbs()

                self.config.prefs['last_path_dbs'] = dbs_path
                self.config.prefs.save()

    def save(self):
        sql = '''
update champs set name=?, pool_length=?, pool_lanes=?, chrono_type=?
where champ_id=?'''
        values = ((self.name, self.pool_length, self.pool_lanes, 
                self.chrono_type, self.champ_id,),)
        res = self.config.dbs.exec_sql(sql=sql, values=values)


        # points_ind_text=i[POINTS_IND],
        # points_rel_text=i[POINTS_REL],
        # club_to_point_ind=i[CLUB_TO_POINT_IND],
        # club_to_point_rel=i[CLUB_TO_POINT_REL],
        # date_text=i[DATE_TEXT],
        # venue=i[VENUE],
        # method_results=i[METHOD_RESULTS],

        # self.categories = Categories(champ=self)
        # self.events = Events(champ=self)
        # self.inscriptions = Inscriptions(champ=self)
        # self.reserves = Reserves(champ=self)
        # self.results = Results(champ=self)
        # self.manager = Manager(
        #     config=self.config,
        #     module_name='champs',
        #     parent=self,
        #     )

    @property
    def is_manager(self):
        return self.manager.is_manager

    @property
    def league_champ_id(self):
        value = ''
        if self.league_id and self.league_pos:
            value = '{}{}'.format(
                self.league_id, str(self.league_pos).zfill(2))
        return value

    @property
    def venue(self):
        return self.config.venues.get_name(self.venue_id)


    def _set_points_ind_text(self, string_value):
        if string_value:
            if string_value == 'FINA':
                self.points_ind = 'FINA'
            else:
                self.points_ind = [int(i) for i in string_value.split('-')
                                   if i.isdigit()]
        else:
            self.points_ind = ''

    def _get_points_ind_text(self):

        if self.points_ind == 'FINA':
            value = self.points_ind
        else:
            value = '-'.join(["%s" % i for i in self.points_ind])
        return value

#    text format for points
    points_ind_text = property(fget=_get_points_ind_text,
                               fset=_set_points_ind_text)
        
    def _set_points_rel_text(self, string_value):
        if string_value:
            if string_value == 'FINA':
                self.points_rel = 'FINA'
            else:
                self.points_rel = [int(i) for i in string_value.split('-') 
                               if i.isdigit()]
        else:
            self.points_rel = ''

    def _get_points_rel_text(self):
        if self.points_rel == 'FINA':
            value = self.points_rel
        else:
            value = '-'.join(["%s" % i for i in self.points_rel])
        return value
    
#    text format for points    
    points_rel_text = property(fget=_get_points_rel_text, 
                               fset=_set_points_rel_text)

    def choices_categories(self, gender_id=None, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', ''))
        if not self.categories:
            self.categories.load_items_from_dbs()
        for i in self.categories:
            if gender_id:
                if gender_id == i.gender_id and (i.category_id, i.category_id) not in values:
                    values.append((i.category_id, i.category_id))
            else:
                if (i.category_id, i.category_id) not in values:
                    values.append((i.category_id, i.category_id))
        return values

    def auto_gen_heats(self):
        '''
        Xera as fases como TIM
        Xera as series
        Xera as liñas de resultados (aquí é onde vai a serie e a pista)
        '''
        print("Auto generate series")
        # clear
        tables = ('phases', 'results')
        for i in tables:
            sql = ''' Delete from {} where 1; '''.format(table)
            self.config.dbs.exec_sql(sql=sql)

        # Phases
        sql = '''
insert into phases (pos, event_id,  pool_lanes, progression, session_id, champ_id) 
select pos, event_id,
    (select pool_lanes from champs c where c.champ_id=e.champ_id) as pool_lanes,
    'TIM', (select session_id from sessions s where s.champ_id=e.champ_id)
    as session_id, champ_id  from events e; '''
        # self.config.dbs.exec_sql(sql=sql)

        # Heats and results
        # Get inscriptions, sorted by time asc
        sql = '''
select pos, event_id,  pool_lanes, progression, session_id
from phases where champ_id={} order by pos; '''
        sql = sql.format(self.champ_id)
        res = self.config.dbs.exec_sql(sql=sql)
        (POS, EVENT_ID,  POOL_LANES, PROGRESSION, SESSION_ID) = range(5)
        for i in res:
            print(i)
            if i[POOL_LANES] == 5:
                lanes_sort = (3, 4, 2, 5, 1)
            if i[POOL_LANES] == 6:
                lanes_sort = (3, 4, 2, 5, 1, 6)
            elif i[POOL_LANES] == 8:
                lanes_sort = (4, 5, 3, 6, 2, 7, 1, 8)

            sql2 = '''
select ind_inscription_id, equated_hundredth 
from ind_inscriptions where event_id={} and champ_id={} order by equated_hundredth; '''
            sql2 = sql2.format(i[EVENT_ID], self.champ_id)
            res2 = self.config.dbs.exec_sql(sql=sql2)
            count_inscriptions = len(res2)
            ind_inscriptions = list(res2)
            results = []
            if count_inscriptions:
                tot_heats, first_heat = divmod(count_inscriptions, i[POOL_LANES])
                if first_heat != 0:
                    tot_heats += 1
                for heat in range(tot_heats, 0, -1):
                    for lane in lanes_sort:
                        inscription = ind_inscriptions.pop(0)
                        results.append(
                            (i[EVENT_ID], heat, lane,
                            inscription[0], inscription[1]))
                        if heat == 2 and len(ind_inscriptions) == 3:
                            print("Recoloca para gantir 3")
                            break
                        elif len(ind_inscriptions) == 0:
                            break

            for result in results:
                print(result)



            for j in res2:
                print(j)
            break


        


        

        sql = '''
insert into phases (pos, event_id,  pool_lanes, progression, session_id, champ_id) 
select pos, event_id,
    (select pool_lanes from champs c where c.champ_id=e.champ_id) as pool_lanes,
    'TIM', (select session_id from sessions s where s.champ_id=e.champ_id)
    as session_id, champ_id  from events e; '''
        # values = ((self.entity_code, self.long_name, self.medium_name, 
        #             self.short_name, self.champ_id),)
        # self.config.dbs.exec_sql(sql=sql, values=values)
        self.config.dbs.exec_sql(sql=sql)
