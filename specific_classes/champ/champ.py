# -*- coding: utf-8 -*- 


import os
import json
from operator import attrgetter
from reportlab.lib.units import cm
from specific_classes.report_base import ReportBase
from specific_classes.champ.entities import Entities
from specific_classes.champ.categories import Categories
from specific_classes.champ.sessions import Sessions
from specific_classes.champ.events import Events
from specific_classes.champ.persons import Persons
from specific_classes.champ.relays import Relays
from specific_classes.champ.inscriptions import Inscriptions
from specific_classes.champ.phases import Phases
from specific_classes.champ.heats import heats
from specific_functions import files
from specific_functions.files import get_file_content


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
                self.inscriptions = Inscriptions(champ=self)
                self.inscriptions.load_items_from_dbs()
                self.inscriptions.sort_default()
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
equated_hundredth, inscription_id
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
insert into results (heat_id, lane, person_id, relay_id, equated_hundredth, inscription_id)
values(?, ?, ?, ?, ?,?)'''
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
                        PERSON_ID, RELAY_ID, EQUATED_HUNDREDTH, INSCRIPTION_ID = range(4) 
                        values = ((
                            heat_id,
                            lane,
                            inscription[PERSON_ID] or 0,
                            inscription[RELAY_ID] or 0,
                            inscription[EQUATED_HUNDREDTH],
                            inscription[INSCRIPTION_ID],
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
        self.phases.load_items_from_dbs()
        self.heats.load_items_from_dbs()
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

    def report_inscriptions_by_club(self, entity=None):
        if entity:
            entities = [entity, ]
            file_path = os.path.join(
                self.config.app_path_folder,
                _('inscriptions_by_club_{}.pdf').format(entity.entity_code),
                )
        else:
            entities = self.entities
            file_path = os.path.join(
                self.config.app_path_folder,
                _('inscriptions_by_club_full.pdf'),
                )

        def save_table(lines, inscription):
            col_widths = ['7%', '22%', '10%', '10%', '8%', '7%', '10%', '11%', '15%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, d.colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('ALIGN', (8, 0), (8, -1), 'LEFT'),
            ]

            table = lines
            d.insert_table(table=table, colWidths=col_widths, 
                           style=style, pagebreak=False)


        if self.chrono_type == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')
        subtitle = _("{}. Pool course {} m. Timing system {}.").format(
            self.venue, self.pool_length, chrono_text)
        d =  ReportBase(
                config= self.config,
                file_name = file_path, 
                orientation='landscape',
                title=self.name,
                subtitle=subtitle)

        d.insert_title_1(text=_("Inscriptions by entity"), alignment=1)

        last_entity = None
        entities = sorted(entities, key=attrgetter('entity_code'), reverse=False)
        for entity in entities:
            # check has inscriptions
            has_inscriptions =  False
            for i in self.inscriptions:
                if i.ind_rel == 'I' and i.person.entity == entity:
                    has_inscriptions = True
                    break
                elif i.ind_rel == 'R' and i.relay.entity == entity:
                    has_inscriptions = True
                    break
            if not has_inscriptions:
                continue
            # end check has inscriptions
            if last_entity:
                d.insert_page_break()
            d.insert_paragraph("")
            last_entity = entity
            style = [
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
            ]
            col_widths = ['100%', ]

            table = [["%s %s" % (
                entity.entity_code, entity.long_name), ], ]
            d.insert_table(
                table=table, colWidths=col_widths,
                style=style, pagebreak=False)

            inscriptions_ind = [i for i in self.inscriptions if i.ind_rel == 'I']
            inscriptions_ind = [i for i in inscriptions_ind if i.person.entity == entity]
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('event.pos'), reverse=False)
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('person.name'), reverse=False)
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('person.surname'), reverse=False)

            lines = []
            last_person = None
            prev_row = None
            for row in inscriptions_ind:
                if row.person != last_person:
                    if lines:
                        save_table(lines=lines, inscription=prev_row)
                        d.insert_paragraph("")
                        lines = []
                    style = [
                        ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ]
                    col_widths = ['100%', ]  
                    table = [
                        ["%s %s, %s (%s)" % (
                            row.person.license, row.person.surname, 
                            row.person.name, row.person.birth_date[:4]),],]
                    d.insert_table(
                        table=table, colWidths=col_widths,
                        style=style, pagebreak=False)
                    last_person = row.person

                mark_time = row.mark_time
                equated_time = row.equated_time
                lines.append([
                    row.event.pos, row.event.name, row.category.code,
                    mark_time, '%sm' % row.pool_length, row.chrono_type,
                    equated_time, row.date, row.venue],)
                prev_row = row

            else:
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    print("rematou individual")
                    lines = []

            # #remudas
            inscriptions_rel = [i for i in self.inscriptions if i.ind_rel == 'R']
            inscriptions_rel= [i for i in inscriptions_rel if i.relay.entity == entity]
            inscriptions_rel = sorted(inscriptions_rel, key=attrgetter('relay.name'), reverse=False)
            inscriptions_rel = sorted(inscriptions_rel, key=attrgetter('event.pos'), reverse=False)

            lines = []
            prev_row = None
            for row in inscriptions_rel:
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    d.insert_paragraph("")
                    lines = []
                style = [
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
                col_widths = ['100%', ]  
                table = [
                    ["{} {}".format(
                        row.relay.entity.entity_code, row.relay.name),],]
                d.insert_table(
                    table=table, colWidths=col_widths,
                    style=style, pagebreak=False)

                mark_time = row.mark_time
                equated_time = row.equated_time
                lines.append([
                    row.event.pos, row.event.name, row.category.code,
                    mark_time, '%sm' % row.pool_length, row.chrono_type,
                    equated_time, row.date, row.venue],)
                prev_row = row

            else:
                if lines:
                    save_table(lines=lines, inscription=prev_row)
                    print("rematou bucle remudas")

        d.build_file()
        print("feito")

    def report_inscriptions_by_event(self, phase=None):
        if phase:
            phases = [phase, ]
            file_path = os.path.join(
                self.config.app_path_folder,
                _('inscriptions_by_event_{}.pdf').format(phase.file_name),
                )
        else:
            phases = self.phases
            file_path = os.path.join(
                self.config.app_path_folder,
                _('inscriptions_by_event_full.pdf'),
                )

        def save_lines_ind(lines):
            col_widths = ['4%', '8%', '34%', '4%', '10%', '12%', '8%', '8%', '12%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('ALIGN', (10, 0), (10, -1), 'LEFT'),
            ]
            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        def save_lines_rel(lines):
            col_widths = ['4%', '8%', '24%', '14%', '10%', '12%', '8%', '8%', '12%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                ('ALIGN', (10, 0), (10, -1), 'LEFT'),
            ]
            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        if self.chrono_type == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')
        subtitle = _("{}. Pool course {} m. Timing system {}.").format(
            self.venue, self.pool_length, chrono_text)
        d =  ReportBase(
                config= self.config,
                file_name = file_path, 
                orientation='portrait',
                title=self.name,
                subtitle=subtitle)

        d.insert_title_1(text=_("Inscriptions by event"), alignment=1)

        last_event = None
        for event in self.events:
            if last_event:
                d.insert_page_break()
            d.insert_paragraph("")
            last_event = event
            style = [
                ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ]
            col_widths = ['100%', ]

            table = [["%s. %s" % (event.pos, event.name), ], ]
            d.insert_table(table=table, colWidths=col_widths,
                               style=style, pagebreak=False)
    
            inscriptions_ind = [i for i in self.inscriptions if i.event == event]
            inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('equated_hundredth'), reverse=False)
            lines = []
            for row in inscriptions_ind:
                if row.ind_rel == 'I':
                    license = row.person.license
                    name = row.person.full_name
                    birth_year = row.person.birth_date[2:4]
                    entity_name = row.person.entity.short_name
                elif row.ind_rel == 'R':
                    license = row.relay.entity.entity_code
                    name = row.relay.name
                    birth_year = row.relay.category.name
                    entity_name = row.relay.entity.short_name
                else:
                    print("Erro")
                    AssertionError("produciuse un erro")

                mark_time = '{} {}{}'.format(
                    row.mark_time,
                    row.pool_length,
                    row.chrono_type)
                    # pool_chrono = '{}{}'.format(
                    #     self.pool_length,
                    #     self.chrono_type)
                equated_time = row.equated_time
                lines.append([
                    len(lines) + 1, license, name, birth_year,
                    entity_name, mark_time, equated_time, row.date, row.venue])
            else:
                if lines:
                    if event.ind_rel == 'I':
                        save_lines_ind(lines=lines)
                    else:
                        save_lines_rel(lines=lines)
                    print("rematou bucle")

        d.build_file()
        print("feito")

    def report_sumary_participants(self, entity=None):
        if entity:
            entities = [entity, ]
            file_path = os.path.join(
                self.config.app_path_folder,
                _('sumary_participants_{}.pdf').format(entity.entity_code),
                )
        else:
            entities = self.entities
            file_path = os.path.join(
                self.config.app_path_folder,
                _('sumary_participants_full.pdf'),
                )

        def save_lines(lines):
            # col_widths = ['4%', '8%', '24%', '14%', '10%', '12%', '8%', '8%', '12%']
            col_widths = ['40%', '6%', '6%', '8%', '6%', '6%', '8%', '6%', '6%', '6%', '6%']
            style = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                # ('ALIGN', (2, 0), (2, -1), 'LEFT'),
                # ('ALIGN', (10, 0), (10, -1), 'LEFT'),
                ('FONT', (0, 0), (0, -1), 'Open Sans Bold'),
            ]
            table = lines
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

        if self.chrono_type == 'M':
            chrono_text = _('manual')
        else:
            chrono_text = _('electronic')
        subtitle = _("{}. Pool course {} m. Timing system {}.").format(
            self.venue, self.pool_length, chrono_text)
        d =  ReportBase(
                config= self.config,
                file_name = file_path, 
                orientation='portrait',
                title=self.name,
                subtitle=subtitle)

        d.insert_title_1(text=_("Sumary participantes"), alignment=1)
        d.insert_paragraph("")
        d.insert_paragraph("")
        # calculate
        calculations = {}
        for person in self.persons:
            if person.entity.entity_code in calculations:
                entity = calculations[person.entity.entity_code]
            else:
                entity = {
                    'per_fem': 0,
                    'per_mas': 0,
                    'per_tot': 0,
                    'ind_fem': 0,
                    'ind_mas': 0,
                    'ind_tot': 0,
                    'rel_fem': 0,
                    'rel_mas': 0,
                    'rel_mix': 0,
                    'rel_tot': 0,
                    }
                calculations[person.entity.entity_code] = entity
            if person.gender_id == 'F':
                entity['per_fem'] += 1
            elif person.gender_id == 'M':
                entity['per_mas'] += 1
            entity['per_tot'] += 1

        for inscription in self.inscriptions:
            if inscription.ind_rel == 'I':
                person = inscription.person
                entity_code = inscription.person.entity.entity_code
                if entity_code in calculations:
                    entity = calculations[entity_code]
                else:
                    entity = {
                        'per_fem': 0,
                        'per_mas': 0,
                        'per_tot': 0,
                        'ind_fem': 0,
                        'ind_mas': 0,
                        'ind_tot': 0,
                        'rel_fem': 0,
                        'rel_mas': 0,
                        'rel_mix': 0,
                        'rel_tot': 0,
                        }
                    calculations[entity_code] = entity
                if person.gender_id == 'F':
                    entity['ind_fem'] += 1
                elif person.gender_id == 'M':
                    entity['ind_mas'] += 1
                entity['ind_tot'] += 1
            elif inscription.ind_rel == 'R':
                relay = inscription.relay
                entity_code = inscription.relay.entity.entity_code
                if entity_code in calculations:
                    entity = calculations[entity_code]
                else:
                    entity = {
                        'per_fem': 0,
                        'per_mas': 0,
                        'per_tot': 0,
                        'ind_fem': 0,
                        'ind_mas': 0,
                        'ind_tot': 0,
                        'rel_fem': 0,
                        'rel_mas': 0,
                        'rel_mix': 0,
                        'rel_tot': 0,
                        }
                    calculations[entity_code] = entity
                if relay.gender_id == 'F':
                    entity['rel_fem'] += 1
                elif relay.gender_id == 'M':
                    entity['rel_mas'] += 1
                elif relay.gender_id == 'X':
                    entity['rel_mix'] += 1
                entity['rel_tot'] += 1

        last_entity = None
        entities = sorted(entities, key=attrgetter('entity_code'), reverse=False)
        # col headers
        style = [
            ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
        ]
        # col_widths = ['100%', ]
        col_widths = ['36%', '20%', '20%', '24%']
        table = [[
            _('Entity'),
            _('Participants'),
            _('Insc. individuals'),
            _('Insc. relays'),
             ], ]
        d.insert_table(
            table=table, colWidths=col_widths,
            style=style, pagebreak=False)

        style = [
            ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
        ]
        # col_widths = ['100%', ]
        col_widths = ['40%', '6%', '6%', '8%', '6%', '6%', '8%', '6%', '6%', '6%', '6%']
        table = [[
            '',
            _('Fem.'),
            _('Mas.'),
            _('Tot.'),
            _('Fem.'),
            _('Mas.'),
            _('Tot.'),
            _('Fem.'),
            _('Mas.'),
            _('Mix.'),
            _('Tot.'),
             ], ]
        d.insert_table(
            table=table, colWidths=col_widths,
            style=style, pagebreak=False)

        lines = []
        totals = {
                'per_fem': 0,
                'per_mas': 0,
                'per_tot': 0,
                'ind_fem': 0,
                'ind_mas': 0,
                'ind_tot': 0,
                'rel_fem': 0,
                'rel_mas': 0,
                'rel_mix': 0,
                'rel_tot': 0,
                }
        for entity_code, values in calculations.items():

            lines.append([
                self.entities.get_entity_by_code(entity_code).long_name,
                values['per_fem'],
                values['per_mas'],
                values['per_tot'],
                values['ind_fem'],
                values['ind_mas'],
                values['ind_tot'],
                values['rel_fem'],
                values['rel_mas'],
                values['rel_mix'],
                values['rel_tot'],
                ])
                
            totals['per_fem'] += values['per_fem']
            totals['per_mas'] += values['per_mas']
            totals['per_tot'] += values['per_tot']
            totals['ind_fem'] += values['ind_fem']
            totals['ind_mas'] += values['ind_mas']
            totals['ind_tot'] += values['ind_tot']
            totals['rel_fem'] += values['rel_fem']
            totals['rel_mas'] += values['rel_mas']
            totals['rel_mix'] += values['rel_mix']
            totals['rel_tot'] += values['rel_tot']
        else:
            if lines:
                save_lines(lines)
                style = [
                    ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BACKGROUND', (0, 0), (-1, 0), d.colors.lightgrey)
                ]
                # col_widths = ['100%', ]
                col_widths = ['40%', '6%', '6%', '8%', '6%', '6%', '8%', '6%', '6%', '6%', '6%']
                table = [[
                    '',
                    totals['per_fem'],
                    totals['per_mas'],
                    totals['per_tot'],
                    totals['ind_fem'],
                    totals['ind_mas'],
                    totals['ind_tot'],
                    totals['rel_fem'],
                    totals['rel_mas'],
                    totals['rel_mix'],
                    totals['rel_tot'],
                    ], ]
                d.insert_table(
                    table=table, colWidths=col_widths,
                    style=style, pagebreak=False)

            # if last_event:
            #     d.insert_page_break()
            # d.insert_paragraph("")
            # last_event = event
            # style = [
            #     ('FONT', (0, 0), (-1, -1), 'Open Sans Bold'),
            #     ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            #     ('FONTSIZE', (0, 0), (-1, -1), 9),
            #     ]
            # col_widths = ['100%', ]

            # table = [["%s. %s" % (event.pos, event.name), ], ]
            # d.insert_table(table=table, colWidths=col_widths,
            #                    style=style, pagebreak=False)
    
            # inscriptions_ind = [i for i in self.inscriptions if i.event == event]
            # inscriptions_ind = sorted(inscriptions_ind, key=attrgetter('equated_hundredth'), reverse=False)
            # lines = []
            # for row in inscriptions_ind:
            #     if row.ind_rel == 'I':
            #         license = row.person.license
            #         name = row.person.full_name
            #         birth_year = row.person.birth_date[2:4]
            #         entity_name = row.person.entity.short_name
            #     elif row.ind_rel == 'R':
            #         license = row.relay.entity.entity_code
            #         name = row.relay.name
            #         birth_year = row.relay.category.name
            #         entity_name = row.relay.entity.short_name
            #     else:
            #         print("Erro")
            #         AssertionError("produciuse un erro")

            #     mark_time = '{} {}{}'.format(
            #         row.mark_time,
            #         row.pool_length,
            #         row.chrono_type)
            #         # pool_chrono = '{}{}'.format(
            #         #     self.pool_length,
            #         #     self.chrono_type)
            #     equated_time = row.equated_time
            #     lines.append([
            #         len(lines) + 1, license, name, birth_year,
            #         entity_name, mark_time, equated_time, row.date, row.venue])
            # else:
            #     if lines:
            #         if event.ind_rel == 'I':
            #             save_lines_ind(lines=lines)
            #         else:
            #             save_lines_rel(lines=lines)
            #         print("rematou bucle")

        d.build_file()
        print("feito")

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
        subtitle = _("{}. Pool course {} m. Timing system {}.").format(
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
            inscriptions =  phase.event.inscriptions
            inscriptions.load_items_from_dbs()
            for heat in heats:
                heat_title = _('Heat {} of {}').format(heat.pos, count_heats)
                add_heat_title([[heat_title], ])
                heat.results.load_items_from_dbs()
                # FIXME: poñer isto na clase resultados
                # crear unha lista de inscricións con todas as inscricións
                # e poñela en champ
                for result in heat.results:
                    if result.inscription:
                        time_sart_list = '{} {}{}'.format(
                            result.inscription.mark_time,
                            result.inscription.pool_length,
                            result.inscription.chrono_type)
                        equated_time = result.equated_time
                    else:
                        time_sart_list = ''
                        equated_time = result.equated_time

                    line_result = [[
                            str(result.lane), 
                            'X' not in result.event.code.upper() and result.person.license or result.relay.entity.entity_code, 
                            'X' not in result.event.code.upper() and result.person.full_name or result.relay.name, 
                            'X' not in result.event.code.upper() and result.person.year[2:] or "", 
                            'X' not in result.event.code.upper() and result.person.entity.short_name or result.relay.entity.short_name, 
                            time_sart_list, equated_time],]
                    add_result(line_result)
                    if result.ind_rel == 'R':
                        if not result.result_members:
                            result.result_members.load_items_from_dbs()
                        members = '; '.join([i.person.full_name for i in result.result_members])
                        print(members)
                        if members:
                            add_relay_members([[members], ])

        d.build_file()
        print('fin')

    def import_insc_from_file(self, file_path):
        print(file_path)
        lines = get_file_content(file_path=file_path,
                                            mode="csv",
                                            compressed=False,
                                            encoding='utf-8-sig')
        if not lines:
            print("O ficheiro está baleiro!!")
            raise ValueError("O ficheiro está baleiro!!")
            

        start_line = 1
        for pos, i in enumerate(lines):
            if i[0]== 'RFEN ID':
                start_line = pos + 1
                break

        (LICENSE, SURNAME, NAME, GENDER_ID, BIRTH_DATE, ENTITY_CODE,
        ENTITY_NAME, EVENT_POS, EVENT_CODE, MARK_TIME, POOLCHRONO) = range(11)
        for i in lines[start_line:]:
            license = i[LICENSE]
            person = self.persons.get_person_by_license(license=i[LICENSE])
            if person:
                print("This person {} already exists.".format(person.full_name))
            else:
                # add person
                entity = self.entities.get_entity_by_code(entity_code=i[ENTITY_CODE])
                if entity:
                    print("This entity {} already exists.".format(entity.code))
                else:
                    # add entity
                    entity = self.entities.item_blank
                    entity.entity_code = i[ENTITY_CODE]
                    entity.short_name = i[ENTITY_NAME]
                    entity.medium_name = i[ENTITY_NAME]
                    entity.long_name = i[ENTITY_NAME]
                    # FIXME: revisar que garde o código da entidade cando se importa de csv
                    entity.save()
                person = self.persons.item_blank
                person.license = i[LICENSE]
                person.surname = i[SURNAME]
                person.name = i[NAME]
                person.gender_id = i[GENDER_ID]
                person.birth_date = i[BIRTH_DATE]
                person.entity = entity
                person.save()
            event = self.events[int(i[EVENT_POS]) - 1]
            if event.code != i[EVENT_CODE]:
                print("This event {}.- {} not exists.".format(i[EVENT_POS], i[EVENT_CODE]))
            else:
                
                inscriptions = event.inscriptions
                inscriptions.load_items_from_dbs()
                # if not self.check_exists(person=person, event=event):
                exists_inscription = False
                for j in inscriptions:
                    if j.person == person and j.event == event:
                        exists_inscription = True
                        break
                if exists_inscription:
                    # add inscription
                    print('Inscription already exists.')
                else:
                    print('add inscription')
                    if len(i[POOLCHRONO]) == 3:
                        pool_length = int(i[POOLCHRONO][:2])
                        chrono_type = i[POOLCHRONO][2].upper()
                    else:
                        pool_length = 0
                        chrono_type = ''
                    inscription = inscriptions.item_blank
                    inscription.person = person
                    inscription.mark_time = i[MARK_TIME]
                    inscription.pool_length = pool_length
                    inscription.chrono_type = chrono_type
                    inscription.date = ''
                    inscription.venue = ''
                    inscription.save()
            print(i)
        return True