# -*- coding: utf-8 -*- 


import os
import json
from reportlab.lib.units import cm
from specific_classes.report_base import ReportBase
from specific_classes.champ.entities import Entities
from specific_classes.champ.categories import Categories
from specific_classes.champ.sessions import Sessions
from specific_classes.champ.events import Events
from specific_classes.champ.persons import Persons
from specific_classes.champ.relays import Relays
from specific_classes.champ.phases import Phases
from specific_classes.champ.heats import heats
from specific_functions import files


class Champ(object):

    def __init__(self, config):
        self.config = config
        self.champ_id = 0
        self.name = ''
        self.pool_length = 0
        self.pool_lanes = 0
        self.chrono_type = ''
        self.estament_id = ''
        self.date_age_calculation = ''
        self.venue = ''
        self.pool_lane_min = 0
        self.pool_lane_max = 9

    def load_dbs(self, dbs_path):
        self.config.dbs.connect(dbs_path=dbs_path)
        if self.config.dbs.connection:
            sql = '''
    select champ_id, name, pool_length, pool_lanes, chrono_type, estament_id, 
    date_age_calculation, venue, pool_lane_min, pool_lane_max from champs '''
            (CHAMP_ID, NAME, POOL_LENGTH, POOL_LANES, CHRONO_TYPE, ESTAMENT_ID, 
             DATE_AGE_CALCULATION, VENUE, POOL_LANE_MIN, POOL_LANE_MAX) = range(10)
            res = self.config.dbs.exec_sql(sql=sql, n=1)
            if res == 'err' or not res:
                self.champ_id = 0
                self.name = ''
                self.pool_length = 0
                self.pool_lanes = 0
                self.chrono_type = ''
                self.estament_id = ''
                self.date_age_calculation = ''
                self.venue = ''
                self.pool_lane_min = 0
                self.pool_lane_max = 9
                self.config.prefs['last_path_dbs'] = ''
                self.config.prefs.save()
            else:
                values = res[0]
                self.champ_id = values[CHAMP_ID]
                self.name = values[NAME]
                self.pool_length = values[POOL_LENGTH]
                self.pool_lanes = values[POOL_LANES]
                self.chrono_type = values[CHRONO_TYPE]
                self.estament_id = values[ESTAMENT_ID]
                self.date_age_calculation = values[DATE_AGE_CALCULATION]
                self.venue = values[VENUE]
                self.pool_lane_min = values[POOL_LANE_MIN]
                self.pool_lane_max = values[POOL_LANE_MAX]

                self.entities = Entities(champ=self)
                self.entities.load_items_from_dbs()
                self.sessions = Sessions(champ=self)
                self.sessions.load_items_from_dbs()
                self.categories = Categories(champ=self)
                self.categories.load_items_from_dbs()
                self.events = Events(champ=self)
                self.events.load_items_from_dbs()
                self.persons = Persons(champ=self)
                self.persons.load_items_from_dbs()
                self.relays = Relays(champ=self)
                self.relays.load_items_from_dbs()
                # self.inscriptions = Inscriptions(champ=self)
                # self.inscriptions.load_items_from_dbs()
                self.phases = Phases(champ=self)
                self.phases.load_items_from_dbs()
                self.heats = heats(champ=self)
                self.heats.load_items_from_dbs()

    def save(self):
        sql = '''
update champs set name=?, pool_length=?, pool_lanes=?, chrono_type=?, 
estament_id=?, date_age_calculation=?, venue=?, pool_lane_min=?, pool_lane_max=?
where champ_id=?'''
        values = ((self.name, self.pool_length, self.pool_lanes, 
                self.chrono_type, self.estament_id, 
                self.date_age_calculation, self.venue, self.pool_lane_min,
                self.pool_lane_max, self.champ_id),)
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

    # @property
    # def venue(self):
    #     return self.config.venues.get_name(self.venue_id)


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
        tables = ('phases', 'results', 'results_members', 'results_splits', 'heats')
        for table in tables:
            sql = ''' Delete from {} where 1; '''.format(table)
            self.config.dbs.exec_sql(sql=sql)

        # Phases
        sql = '''
insert into phases (pos, event_id,  pool_lanes, progression, session_id) 
select pos, event_id, (select pool_lanes from champs c) as pool_lanes,
    'TIM', (select session_id from sessions s) as session_id from events e; '''
        self.config.dbs.exec_sql(sql=sql)

        # heats and results
        # Get inscriptions, sorted by time asc
        sql = '''
select phase_id, pos, event_id,  pool_lanes, progression, session_id
from phases order by pos; '''
        res = self.config.dbs.exec_sql(sql=sql)
        (PHASE_ID, POS, EVENT_ID,  POOL_LANES, PROGRESSION, SESSION_ID
        ) = range(6)
        for i in res:
            print(i)
            if i[POOL_LANES] == 5:
                lanes_sort = (3, 4, 2, 5, 1)
            if i[POOL_LANES] == 6:
                lanes_sort = (3, 4, 2, 5, 1, 6)
            elif i[POOL_LANES] == 8:
                lanes_sort = (4, 5, 3, 6, 2, 7, 1, 8)

            sql2 = '''
select (select person_id from persons p where p.person_id=i.person_id) person_id,
(select relay_id from relays r where r.relay_id=i.relay_id) relay_id,
equated_hundredth
from inscriptions i where event_id={} order by equated_hundredth; '''
            sql2 = sql2.format(i[EVENT_ID])
            res2 = self.config.dbs.exec_sql(sql=sql2)
            count_inscriptions = len(res2)
            inscriptions = list(res2)
            results = []
            heats = []
            if count_inscriptions:
                tot_heats, first_heat = divmod(count_inscriptions, i[POOL_LANES])
                if first_heat != 0:
                    tot_heats += 1
                sql_heat = '''
insert into heats (phase_id, pos) values(?, ?)'''
                sql_result = '''
insert into results (heat_id, lane, person_id, relay_id, equated_hundredth)
values(?, ?, ?, ?, ?)'''
                sql_splits_for_event = '''
select distance, split_code, official from splits_for_event where 
event_code=(select event_code from events where event_id=
(select event_id from phases where phase_id=?))
order by distance; '''
                sql_result_split = '''
insert into results_splits (result_id, distance, result_split_code, official) 
values( ?, ?, ?, ?)'''
                for heat_pos in range(tot_heats, 0, -1):
                    values = ((i[PHASE_ID], heat_pos), )
                    self.config.dbs.exec_sql(sql=sql_heat, values=values)
                    heat_id = self.config.dbs.last_row_id
                    for lane in lanes_sort:
                        inscription = inscriptions.pop(0)
                        PERSON_ID, RELAY_ID, EQUATED_HUNDREDTH = range(3) 
                        values = ((
                            heat_id,
                            lane,
                            inscription[PERSON_ID],
                            inscription[RELAY_ID],
                            inscription[EQUATED_HUNDREDTH]
                            ),)
                        self.config.dbs.exec_sql(sql=sql_result, values=values)
                        result_id = self.config.dbs.last_row_id
                        # Create splits
                        splits_for_event = self.config.dbs.exec_sql(
                            sql=sql_splits_for_event, values=((i[PHASE_ID], ), ))
                        DISTANCE, RESULT_SPLIT_CODE, OFFICIAL = range(3)
                        for event_split in splits_for_event:
                            self.config.dbs.exec_sql(
                                sql=sql_result_split,
                                values=((
                                    result_id, event_split[DISTANCE],
                                    event_split[RESULT_SPLIT_CODE],
                                    event_split[OFFICIAL]), ))
                        if heat_pos == 2 and len(inscriptions) == 3:
                            print("Recoloca para gantir 3")
                            break
                        elif len(inscriptions) == 0:
                            break
#             sql_result = '''
# insert into results (phase_id, heat,  lane, person_id, relay_id, mark_hundredth) 
# values( ?, ?, ?, ?, ?, ?)'''

#             for result in results:
#                 self.config.dbs.exec_sql(sql=sql_result, values=(result, ))
#                 result_id = self.config.dbs.last_row_id
#                 # Create splits
#                 splits_for_event = self.config.dbs.exec_sql(
#                     sql=sql_splits_for_event, values=((result[0], ), ))
#                 for event_split in splits_for_event:
#                     self.config.dbs.exec_sql(
#                         sql=sql_result_split,
#                         values=((result_id, event_split[0], event_split[1]), ))
                    
#         sql = '''
# insert into phases (pos, event_id,  pool_lanes, progression, session_id, champ_id) 
# select pos, event_id,
#     (select pool_lanes from champs c where c.champ_id=e.champ_id) as pool_lanes,
#     'TIM', (select session_id from sessions s where s.champ_id=e.champ_id)
#     as session_id, champ_id  from events e; '''
#         # values = ((self.entity_code, self.long_name, self.medium_name, 
#         #             self.short_name, self.champ_id),)
#         # self.config.dbs.exec_sql(sql=sql, values=values)
#         self.config.dbs.exec_sql(sql=sql)
        print('Fin')

    def export_results(self):
        self.gen_lev()

    def gen_lev(self):
        """
        Generate file export lev format
        """
        categorias = (
            ("ABSO", "MENORES OPEN FEMENINO"),
            ("ABSO", "MENORES OPEN MASCULINO"),
            ("ABSO", "ABSOLUTO OPEN FEMENINA"),
            ("ABSO", "ABSOLUTO OPEN MASCULINO"),
            ("INFA", "Infantil Femenino (Invierno)"),
            ("ABSO", "SENIOR-JUNIOR 1 - JUNIOR 2 FEM."),
            ("ABSO", "SENIOR-JUNIOR 1 - JUNIOR 2 MAS."),
            ("JUNI", "JUNIOR 1"),
            ("JUNI", "JUNIOR 2"),
            ("SENI", "SENIOR"),
            ("ABSO", "INFANTIL MASCULINO LD"),
            ("ABSO", "INFANTIL FEMENINO LD"),
            ("ABSO", "INFANTIL-JUNIOR FEMENINO"),
            ("ABSO", "INFANTIL-JUNIOR MASCULINO"),
            ("9 A", "9 años"),
            ("10 A", "10 años"),
            ("11 A", "11 años"),
            ("12 A", "12 años"),
            ("13 A", "13 años"),
            ("14 A", "14 años"),
            ("15 A", "15 años"),
            ("16 A", "16 años"),
            ("17 A", "17 años"),
            ("18 A", "18 años"),
            ("20+", "20+"),
            ("+80", "+80"),
            ("+100", "+100"),
            ("+120", "+120"),
            ("+160", "+160"),
            ("+200", "+200"),
            ("+240", "+240"),
            ("+280", "+280"),
            ("+320", "+320"),
            ("95+", "95+"),
            ("90+", "90+"),
            ("85+", "85+"),
            ("80+", "80+"),
            ("75+", "75+"),
            ("70+", "70+"),
            ("65+", "65+"),
            ("60+", "60+"),
            ("55+", "55+"),
            ("50+", "50+"),
            ("45+", "45+"),
            ("40+", "40+"),
            ("35+", "35+"),
            ("30+", "30+"),
            ("25+", "25+"),
            ("ABSO.mixed", "Absoluto Mixto"),
            ("ABSO.female", "Absoluto Femenino"),
            ("ABSO.male", "Absoluto Masculino"),
            ("ABSJ.mixed", "Absouto Joven Mixto"),
            ("ABSJ.female", "Absoluto Joven Femenino"),
            ("ABSJ.male", "Absoluto Joven Masculino"),
            ("JUNI.", "JUNIOR"),
            ("JUNI.mixed", "Junior Mixto"),
            ("JUNI.female", "Junior Femenino"),
            ("JUNI.male", "Junior Masculino"),
            ("INFA.mixed", "Infantil Mixto"),
            ("INFA.female", "Infantil Femenino"),
            ("INFA.male", "Infantil Masculino"),
            ("ALEV.mixed", "Alevín Mixto"),
            ("ALEV.female", "Alevín Femenino"),
            ("ALEV.male", "Alevín Masculino"),
            ("BENJ.mixed", "Benjamín Mixto"),
            ("BENJ.female", "Benjamín Femenino"),
            ("BENJ.male", "Benjamín Masculino"),
            ("PROM.mixed", "Prebenjamín Mixto"),
            ("PROM.female", "Prebenjamín Femenino"),
            ("PROM.male", "Prebenjamín Masculino"),
        )
        cat_dic = {}
        for i in categorias:
            cat_dic[i[0].lower()] = i[1]

        head = [
            "phaseresult.last_name",
            "phaseresult.first_name",
            "phaseresult.resultable.profile_number",
            "phaseresult.resultable.@where:code",
            "phaseresult.resultable.@type",
            "phaseresult.style.code",
            "phaseresult.value",
            "phaseresult.goal",
            "phaseresult.date",
            "phaseresult.custom_fields.result_point",
            "phaseresult.custom_fields.result_lane",
            "phaseresult.custom_fields.result_heat",
            "phaseresult.category.maximum_age",
            "phaseresult.category.minimum_age",
            "phaseresult.category.name",
            "phaseresult.category.@where:categorydisciplines.discipline.id",
            "phaseresult.competition",
            "phaseresult.location",
            "phaseresult.discipline_fields.pool_size",
            "phaseresult.discipline_fields.chronometer",
            "phaseresult.custom_fields.pool_name",
            "phaseresult.custom_fields.pool_lanemin",
            "phaseresult.custom_fields.pool_lanemax",
            "phaseresult.gender",
            "phaseresult.custom_fields.event_number",
            "phaseresult.custom_fields.event_round",
            "phaseresult.official",
            "phaseresult.office.code",
            "phaseresult.participants_amount",
            "phaseresult.participants_names.0",
            "phaseresult.participants_names.1",
            "phaseresult.participants_names.2",
            "phaseresult.participants_names.3",
            "phaseresult.participants_names.4",
            "phaseresult.participants_names.5",
            "phaseresult.participants_names.6",
            "phaseresult.participants_names.7",
            "phaseresult.custom_fields.leveradeid",
            "phaseresult.position",
            "phaseresult.phaseresult.last_name",
            "phaseresult.phaseresult.first_name",
            "phaseresult.phaseresult.resultable.profile_number",
            "phaseresult.phaseresult.resultable.@where:code",
            "phaseresult.phaseresult.resultable.@type",
            "phaseresult.phaseresult.style.code",
            "phaseresult.phaseresult.value",
            "phaseresult.phaseresult.goal",
            "phaseresult.phaseresult.date",
            "phaseresult.phaseresult.custom_fields.result_point",
            "phaseresult.phaseresult.custom_fields.result_lane",
            "phaseresult.phaseresult.custom_fields.result_heat",
            "phaseresult.phaseresult.category.maximum_age",
            "phaseresult.phaseresult.category.minimum_age",
            "phaseresult.phaseresult.category.name",
            "phaseresult.phaseresult.category.@where:categorydisciplines.discipline.id",
            "phaseresult.phaseresult.competition",
            "phaseresult.phaseresult.location",
            "phaseresult.phaseresult.discipline_fields.pool_size",
            "phaseresult.phaseresult.discipline_fields.chronometer",
            "phaseresult.phaseresult.custom_fields.pool_name",
            "phaseresult.phaseresult.custom_fields.pool_lanemin",
            "phaseresult.phaseresult.custom_fields.pool_lanemax",
            "phaseresult.phaseresult.gender",
            "phaseresult.phaseresult.custom_fields.event_number",
            "phaseresult.phaseresult.custom_fields.event_round",
            "phaseresult.phaseresult.official",
            "phaseresult.phaseresult.office.code",
            "phaseresult.phaseresult.participants_amount",
            "phaseresult.phaseresult.participants_names.0",
            "phaseresult.phaseresult.participants_names.1",
            "phaseresult.phaseresult.participants_names.2",
            "phaseresult.phaseresult.participants_names.3",
            "phaseresult.phaseresult.participants_names.4",
            "phaseresult.phaseresult.participants_names.5",
            "phaseresult.phaseresult.participants_names.6",
            "phaseresult.phaseresult.participants_names.7",
            "phaseresult.phaseresult.custom_fields.leveradeid",
            "phaseresult.phaseresult.position"
            ]
        head_str_line = ';'.join(head)
        head_str_line += '\n'
        lines = []
        for heat in self.heats:
            if heat.official:
                heat.results.load_items_from_dbs()
                for result in heat.results:
                    result.result_splits.load_items_from_dbs()
                    # Determina se o resultado se ten en conta ou non
                    if result.issue_id:
                        if result.ind_rel == 'I':
                            print(('issue', result.person.name, result.person.surname, result.issue_id))
                            continue
                        elif result.ind_rel == 'R':
                            result.result_members.load_items_from_dbs()
                            num_members = result.result_members.num_members
                            num_splits = len(result.result_splits)
                            if result.issue_split<=(num_splits/num_members):
                                print(('issue', result.relay.name, result.issue_id))
                                continue
                    if result.ind_rel == 'R': # non envía remudas sen remudistas
                        result.result_members.load_items_from_dbs()
                        if result.result_members.num_members == 0:
                            print('Erro:  remuda sen membros, isto non debería pasar nunca')
                            continue
                    style_names = {
                        'M':'butterfly',
                        'E':'backstroke',
                        'B':'breaststroke',
                        'L':'freestyle',
                        'S':'medley',
                        }
                    genders = {
                        'M':'male',
                        'F':'female',
                        'X':'mixed',
                        }
                    
                    #result final parcial
                    line = []
                    members = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: ''}
                    members_licenses_str = ''
                    if result.ind_rel == 'I':
                        line.append(result.person.surname)  # phaseresult.last_name
                        line.append(result.person.name)  # phaseresult.first_name
                        line.append(result.person.license)  # phaseresult.resultable.profile_number
                        line.append('')  # phaseresult.resultable.@where:code
                        line.append('license')  # phaseresult.resultable.@type
                    else:
                        line.append('')  # phaseresult.last_name
                        line.append('')  # phaseresult.first_name
                        line.append('')  # phaseresult.resultable.profile_number
                        line.append(result.relay.entity.entity_code)  # phaseresult.resultable.@where:code
                        line.append('club')  # phaseresult.resultable.@type
                        members_licenses = []
                        for pos, member in enumerate(result.result_members):
                            members[pos] = member.person.full_name
                            members_licenses.append(member.person.license)
                        if members_licenses:
                            members_licenses_str = json.dumps(members_licenses)
                        distance_per_member = int(result.distance / result.result_members.num_members)
                        num_member = result.result_members.num_members  # for splits calculations

                    line.append(style_names[result.style_id])  # phaseresult.style.code
                    line.append(result.mark_hundredth)  # phaseresult.value
                    line.append(result.distance)  # phaseresult.goal
                    line.append('{}:00'.format(result.heat.start_time or result.phase.date_time))  # phaseresult.date
                    #FIXME: points
                    line.append('0')  # phaseresult.custom_fields.result_point
                    line.append(str(result.lane))  # phaseresult.custom_fields.result_lane
                    line.append(str(result.heat.pos))  # phaseresult.custom_fields.result_heat
                    line.append(int(result.category.to_age))  # phaseresult.category.maximum_age
                    line.append(int(result.category.from_age))  # phaseresult.category.minimum_age
                    line.append(result.category.name)  # phaseresult.category.name
                    line.append('38')  # phaseresult.category.@where:categorydisciplines.discipline.id
                    line.append(self.name)  # phaseresult.competition
                    line.append(self.venue)  # phaseresult.location
                    line.append(str(self.pool_length))  # phaseresult.discipline_fields.pool_size
                    line.append(self.chrono_type == 'M' and 'manual' or 'electronic')  # phaseresult.discipline_fields.chronometer
                    line.append(self.venue)  # phaseresult.custom_fields.pool_name
                    line.append(str(self.pool_lane_min))  # phaseresult.custom_fields.pool_lanemin
                    line.append(str(self.pool_lane_max))  # phaseresult.custom_fields.pool_lanemax
                    #FIXME: coller o sexo da persoa ou remuda
                    line.append(genders[result.event.gender_id])  # phaseresult.gender
                    line.append(str(result.event.pos))  # phaseresult.custom_fields.event_number
                    line.append(result.phase.progression)  # phaseresult.custom_fields.event_round
                    line.append(1)  # phaseresult.official
                    line.append('athlete')  # phaseresult.office.code
                    line.append(int(result.event.num_members))  # phaseresult.participants_amount
                    line.append(members[0])  # phaseresult.participants_names.0
                    line.append(members[1])  # phaseresult.participants_names.1
                    line.append(members[2])  # phaseresult.participants_names.2
                    line.append(members[3])  # phaseresult.participants_names.3
                    line.append(members[4])  # phaseresult.participants_names.4
                    line.append(members[5])  # phaseresult.participants_names.5
                    line.append(members[6])  # phaseresult.participants_names.6
                    line.append(members[7])  # phaseresult.participants_names.7
                    line.append(members_licenses_str)  # phaseresult.custom_fields.leveradeid
                    line.append(int(result.arrival_pos))  # phaseresult.position (in heat)        
                    
                    lines.append(line)
                    line_parent = line

                    if result.ind_rel == 'I':
                        splits = reversed(result.result_splits[:-1])
                    else:
                        splits = reversed(result.result_splits)
                    mark_hundredth_adjust = 0
                    for split in splits:
                        line = []
                        members = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: ''}
                        members_licenses_str = ''
                        if result.ind_rel == 'I':
                            line.append(result.person.surname)  # phaseresult.last_name
                            line.append(result.person.name)  # phaseresult.first_name
                            line.append(result.person.license)  # phaseresult.resultable.profile_number
                            line.append('')  # phaseresult.resultable.@where:code
                            line.append('license')  # phaseresult.resultable.@type
                            split_gender = genders[result.person.gender_id]
                            split_mark_hundredth = split.mark_hundredth
                        else:
                            # FIXME: este cálculo seguro que se pode mellorar
                            if int(split.distance % distance_per_member) == 0:
                                num_member -= 1
                                if num_member > 0:
                                    # calcula o tempo de axuste para o membro
                                    for i in result.result_splits:
                                        if i.distance == distance_per_member * num_member:
                                            mark_hundredth_adjust = i.mark_hundredth
                                            break
                                else:
                                    mark_hundredth_adjust = 0
                            member_distance = split.distance - (num_member * distance_per_member)
                            if num_member < len(result.result_members):
                                member = result.result_members[num_member]
                                line.append(member.person.surname)  # phaseresult.last_name
                                line.append(member.person.name)  # phaseresult.first_name
                                line.append(member.person.license)  # phaseresult.resultable.profile_number
                                split_gender = genders[member.person.gender_id]
                            else:
                                line.append('')  # phaseresult.last_name
                                line.append('')  # phaseresult.first_name
                                line.append('')  # phaseresult.resultable.profile_number
                                split_gender = ''
                            split_mark_hundredth = split.mark_hundredth - mark_hundredth_adjust
                            line.append('')  # phaseresult.resultable.@where:code
                            line.append('license')  # phaseresult.resultable.@type
                        line.append(style_names[split.style_id])  # phaseresult.style.code
                        line.append(split_mark_hundredth)  # phaseresult.value
                        line.append(member_distance)  # phaseresult.goal
                        line.append('{}:00'.format(result.heat.start_time or result.phase.date_time))  # phaseresult.date
                        #FIXME: points
                        line.append('0')  # phaseresult.custom_fields.result_point
                        line.append(str(result.lane))  # phaseresult.custom_fields.result_lane
                        line.append(str(result.heat.pos))  # phaseresult.custom_fields.result_heat
                        line.append(int(result.category.to_age))  # phaseresult.category.maximum_age
                        line.append(int(result.category.from_age))  # phaseresult.category.minimum_age
                        line.append(result.category.name)  # phaseresult.category.name
                        line.append('38')  # phaseresult.category.@where:categorydisciplines.discipline.id
                        line.append(self.name)  # phaseresult.competition
                        line.append(self.venue)  # phaseresult.location
                        line.append(str(self.pool_length))  # phaseresult.discipline_fields.pool_size
                        line.append(self.chrono_type == 'M' and 'manual' or 'electronic')  # phaseresult.discipline_fields.chronometer
                        line.append(self.venue)  # phaseresult.custom_fields.pool_name
                        line.append(str(self.pool_lane_min))  # phaseresult.custom_fields.pool_lanemin
                        line.append(str(self.pool_lane_max))  # phaseresult.custom_fields.pool_lanemax
                        #FIXME: coller o sexo da persoa ou remuda
                        line.append(split_gender)  # phaseresult.gender
                        line.append(str(result.event.pos))  # phaseresult.custom_fields.event_number
                        line.append(result.phase.progression)  # phaseresult.custom_fields.event_round
                        line.append(split.official)  # phaseresult.official
                        line.append('athlete')  # phaseresult.office.code
                        line.append(1)  # phaseresult.participants_amount
                        line.append(members[0])  # phaseresult.participants_names.0
                        line.append(members[1])  # phaseresult.participants_names.1
                        line.append(members[2])  # phaseresult.participants_names.2
                        line.append(members[3])  # phaseresult.participants_names.3
                        line.append(members[4])  # phaseresult.participants_names.4
                        line.append(members[5])  # phaseresult.participants_names.5
                        line.append(members[6])  # phaseresult.participants_names.6
                        line.append(members[7])  # phaseresult.participants_names.7
                        line.append(members_licenses_str)  # phaseresult.custom_fields.leveradeid
                        line.append(int(result.arrival_pos))  # phaseresult.position (in heat)

                        last_split_mark_hundredth = split.mark_hundredth  # to calculate relay member time

                        lines.append(line + line_parent)


        lines.append(head)
        lines.reverse()
        for i in lines:
            print(i)

        datos = []
        int_cols = [6, 7, 8, 10, 11]
        for i in lines:
            row = ""
            for col, j in enumerate(i):
                if isinstance(j, str):
                    value = '"{}"'.format(j)
                elif isinstance(j, int):
                    value = '{}'.format(j)
                else:
                    print('Isto non debería pasar.')

                # if not j:
                #     value = '""'
                # else:
                #     value = j
                #     if col in int_cols:
                #         value = '{}'.format(j)
                #     else:
                #         value = '"{}"'.format(j)
                row += ';{}'.format(str(value))

            datos.append(row[1:])


        datos = "\n".join(datos)
        datos += "\n"
        # datos = head_str_line + datos

        files.set_file_content(content=datos,
                               file_path="res_lev.csv",
                               compress=False,
                               binary=False,
                               encoding='utf-8-sig',
                               end_line="\n")
        print('Fin')

    def report_start_list(self, phase=None):
        if phase:
            phases = [phase, ]
            file_name = os.path.join(
                self.config.app_path_folder,
                _('start_list_{}.pdf').format(phase.file_name),
                )
        else:
            phases = self.phases
            file_name = os.path.join(
                self.config.app_path_folder,
                _('start_list_full.pdf'),
                )
        if self.chrono_type == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')

        file_name = os.path.join(
            self.config.app_path_folder,
            _('start_list.pdf'))
        subtitle = "{}. Piscina de {} m. Cronometraxe {}.".format(
            self.venue, self.pool_length, chrono_text)
        d =  ReportBase(
                config= self.config,
                file_name = file_name, 
                orientation='portrait',
                title=self.name,
                subtitle=subtitle)
        style = [
            ('FONT',(0,0),(-1,-1), 'Open Sans Regular'), 
            # ('FONTSIZE',(0,0),(-1,-1), 8),
            ('ALIGN',(0,0),(-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'), 
            # ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
            # ('BOTTOMPADDING', (0,0), (-1,-1), 3), 
            # ('GRID', [ 0, 0 ], [ -1, -1 ], 0.05, 'grey' ),
            ]
        def add_phase_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['100%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_title,
                pagebreak=False)

        def add_heat_title(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['100%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.8*cm,
                style=style_title,
                pagebreak=False)

        def add_result(lines):
            style_result = [
                ('FONTSIZE',(0,0),(-1,-1), 8),
                ('ALIGN',(2,0),(2,-1), 'LEFT'),
                ('ALIGN',(5,0),(5,-1), 'RIGHT'),  #mark
                ('ALIGN',(6,0),(6,-1), 'RIGHT'),  #points
                ('FONT', (2,0),(2,-1), 'Open Sans Bold'),
                # ('FONT', (5,0),(5,-1), 'Open Sans Bold'),
                # ('FONT', (6,0),(6,-1), 'Open Sans Bold'),
                ]
            style_result = style + style_result

            col_widths = ['4%', '10%', '40%', '6%', '20%', '10%', '10%']
            row_heights = (1.5*cm, 2.5*cm)
            row_heights = [.8*cm] * len(lines)
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.4*cm,
                style=style_result,
                pagebreak=False)

        def add_relay_members(lines):
            style_title = [
                ('ALIGN',(0,0),(-1,-1), 'LEFT'),
                # ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                # ('VALIGN', (0,0), (-1,-1), 'MIDDLE'), 
                ]
            style_title = style + style_title
            col_widths = ['86%']
            d.insert_table(
                table=lines,
                colWidths=col_widths,
                rowHeights=.4*cm,
                style=style_title,
                pagebreak=False,
                alignment='RIGHT')

        for phase in phases:
            phase_title = '{}.- {} ({})'.format(phase.event.pos, phase.event.name, phase.progression)
            add_phase_title([[phase_title], ])
            heats = [heat for heat in self.heats if heat.phase == phase]
            count_heats = len(heats)
            for heat in heats:
                heat_title = 'Heat {} of {}'.format(heat.pos, count_heats)
                add_heat_title([[heat_title], ])
                heat.results.load_items_from_dbs()
                for result in heat.results:
                    line_result = [[
                            str(result.lane), 
                            'X' not in result.event.code.upper() and result.person.license or result.relay.entity.entity_code, 
                            'X' not in result.event.code.upper() and result.person.full_name or result.relay.name, 
                            'X' not in result.event.code.upper() and result.person.year[2:] or "", 
                            'X' not in result.event.code.upper() and result.person.entity.short_name or result.relay.entity.short_name, 
                            result.equated_time, ''],]
                    add_result(line_result)
                    if result.ind_rel == 'R':
                        if not result.result_members:
                            result.result_members.load_items_from_dbs()
                        members_full_name = ''
                        members = '; '.join([i.person.full_name for i in result.result_members])
                        print(members)
                        if members:
                            add_relay_members([[members], ])



        d.build_file()
        print('fin')