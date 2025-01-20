# -*- coding: utf-8 -*-


'''
Created on 23/12/2024
@author: damufo
'''


class Lenex(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.registration = 'Galicia'
        self.version = '11.80519'
        self.stroke = {
            'M': 'FLY',
            'E': 'BACK',
            'B': 'BREAST',
            'L': 'FREE',
            'S': 'MEDLEY',
            }


        self.header = (
"""<?xml version="1.0" encoding="UTF-8"?>\n<LENEX version="3.0">\n"""
"""  <CONSTRUCTOR name="SPLASH Meet Manager 11" registration="{}" version="{}">\n"""
"""    <CONTACT name="Splash Software GmbH" street="Ahornweg 41" """
"""city="Spiegel b. Bern" zip="3095" country="CH" """
"""email="sales@swimrankings.net" internet="https://www.swimrankings.net" />\n"""
"""  </CONSTRUCTOR>\n""").format(self.registration, self.version)
        self.footer = """</LENEX>"""
        self.record_base_ind = """    <RECORDLIST course="{}" gender="{}" name="{}" nation="ESP" region="111" type="{}" updated="2019-03-13">
      <AGEGROUP agemax="{}" agemin="{}" />
      <RECORDS>
        <RECORD swimtime="{}">
          <SWIMSTYLE distance="{}" relaycount="1" stroke="{}" />
          <MEETINFO city="{}" date="{}" name="{}" />
          <ATHLETE firstname="{}" gender="{}" lastname="{}">
            <CLUB code="{}" name="{}" />
          </ATHLETE>
        </RECORD>
      </RECORDS>
    </RECORDLIST>"""
        self.record_base_rel = """    <RECORDLIST course="{}" gender="{}" name="{}" nation="ESP" region="111" type="{}" updated="2019-03-13">
      <AGEGROUP agemax="{}" agemin="{}" />
      <RECORDS>
        <RECORD swimtime="{}">
          <SWIMSTYLE distance="{}" relaycount="{}" stroke="{}" />
          <MEETINFO city="{}" date="{}" name="{}" />
          <RELAY>
            <CLUB code="{}" name="{}" />
          </RELAY>
        </RECORD>
      </RECORDS>
    </RECORDLIST>"""

    def save_file(self, file_path):
        file_records = open(file_path, 'w')
        file_records.write(self.header)
        file_records.write(self.file_content)
        file_records.write(self.footer)
        file_records.close()

    def gen_results(self, champ):
        """
        Generate file export lef format
        """

        pool_lanes_sort = champ.validade_pool_lanes_sort(champ.params["champ_pool_lanes_sort"],)
        pool_lanes = pool_lanes_sort.replace(' ', '')
        pool_lanes = tuple([int(i) for i in pool_lanes.split(',')
                                   if i.isdigit()])
        pool_lanes_count =  len(pool_lanes)
        pool_lane_min = min(pool_lanes)
        pool_lane_max = max(pool_lanes)


        content="""  <MEETS>
    <MEET city="{7}" name="{0}" course="{1}" startmethod="1" timing="{2}" touchpad="ONESIDE" masters="F" nation="ESP" maxentriesathlete="4" hytek.courseorder="S">
      <AGEDATE value="{4}" type="YEAR" />
      <POOL lanemin="{5}" lanemax="{6}" />
      <FACILITY city="{7}" nation="ESP" />
      <POINTTABLE pointtableid="3017" name="AQUA Point Scoring" version="2024" />
""".format(
        champ.params["champ_name"],
        champ.params["champ_pool_length"]==25 and "SCM" or "LCM",
        champ.params["champ_chrono_type"]=="E" and "AUTOMATIC" or "MANUAL",
        champ.params["champ_name"],
        champ.params["champ_date_age_calculation"],
        pool_lane_min,
        pool_lane_max,
        champ.params["champ_venue"],
)
        content += "      <SESSIONS>\n"
        current_session = None
        for phase in champ.phases:
            if not current_session or current_session.session_id != phase.session.session_id:
                current_session = phase.session
                content += (
"""        <SESSION date="{0}" daytime="{1}" endtime="" number="{2}" """
"""maxentriesathlete="">\n          <EVENTS>\n""").format(
            current_session.date,
            current_session.time,
            current_session.session_id
          )
            content += (
"""            <EVENT eventid="{0}" gender="{1}" number="{2}" order="{3}" """
"""round="{4}" maxentries="" preveventid="{5}">\n              <SWIMSTYLE """
"""distance="{6}" relaycount="{7}" stroke="{8}" />\n              """
"""<AGEGROUPS>\n""").format(
                    phase.phase_id,
                    phase.gender_id,
                    phase.event.pos,
                    phase.pos,
                    phase.progression,
                    phase.parent and phase.parent.pahse_id or '-1',
                    phase.event.distance,
                    phase.event.num_members,
                    self.stroke[phase.event.style_id],
            )
            for phase_category in  phase.phase_categories:
                content += (
"""                <AGEGROUP agegroupid="{0}" agemax="{1}" agemin="{2}">\n"""
"""                  <RANKINGS>\n""").format(
                    phase_category.phase_category_id,
                    phase_category.category.to_age,
                    phase_category.category.from_age,
                )
                # orde dos resultados
                phase_category.phase_category_results.load_items_from_dbs()
                for order, phase_category_result in  enumerate(phase_category.phase_category_results, start=1):
                    content += (
"""                    <RANKING order="{0}" place="{1}" resultid="{2}" />\n"""
                    ).format(
                        order,
                        phase_category_result.result.issue_id and "-1" or phase_category_result.pos,
                        phase_category_result.result_id,
                    )
                # series
                content += """                  </RANKINGS>\n"""
                content += """                </AGEGROUP>\n"""
            content += """              </AGEGROUPS>\n"""

            content += """              <HEATS>\n"""
            # phase.heats.load_items_from_dbs()
            for order, heat in  enumerate(phase.heats, start=1):
                if not heat.official:
                    assert ("a serie non está oficial ver que texto se pon no "
                        "estado nestes casos")
                # SCHEDULED: The heat is scheduled but not seeded yet.
                # SEEDED: The heat is seeded
                # INOFFICIAL: Results are available but not official.
                # OFFICIAL: Results of the heat are official.
                content += (
"""                    <HEAT heatid="{0}" number="{1}" order="{2}" """
"""status="OFFICIAL" />\n""").format(
                    heat.heat_id,
                    heat.pos,
                    order,
                )
            content += """              </HEATS>\n"""


        content += """            </EVENT>\n"""
        content += """          </EVENTS>\n"""
        content += """        </SESSION>\n"""
        content += """      </SESSIONS>\n"""
        content += """      <CLUBS>\n"""
        for entity in champ.entities:
            content += (
"""        <CLUB type="CLUB" code="{}" nation="ESP" region="" clubid="{}" """
"""name="{}" shortname="{}">\n""").format(
                entity.entity_code,
                'ESP',  #FIXME: add field nation for entity
                '',  # FIXME: add field region for entity 
                entity.long_name,
                entity.short_name,
                )
            content += """          <ATHLETES>\n"""
            for person in champ.persons:
              if person.entity == entity:
                content += (
"""            <ATHLETE firstname="{}" lastname="{}" birthdate="{}" """
"""gender="{}" nation="{}" license="{}" athleteid="{}">\n"""
"""              <RESULTS>\n""").format(
                    person.name,
                    person.surname,
                    person.birth_date,
                    person.gender_id,
                    "",  # FIXME: engadir o campo nationality a person
                    person.license,
                    person.person_id,
                )
                for inscription in person.inscriptions:
                    if inscription.result:
                        result = inscription.result
                        # eventid is phase_id
                        status = ""
                        if result.issue_id:
                            # EXH: exhibition swim.
                            # DSQ: athlete/relay disqualified.
                            # DNS: athlete/relay did not start (no reason given or to late
                            # withdrawl).
                            # DNF: athlete/relay did not finish.
                            # SICK: athlete is sick. Está enfermo
                            # WDR: athlete/relay was withdrawn (on time). Retirouse
                            if result.issue_id not in ('DSQ', 'DNS', 'DNF', 'SICK', 'WDR'):
                                print(result.issue_id)
                                if result.issue_id == 'NPR':
                                    status = 'DNS'
                                elif result.issue_id == 'BAI':
                                    status = 'WDR'
                                elif result.issue_id == 'RET':
                                    status = 'DNF'
                                else:
                                    status = 'DSQ'
                            else:
                                status =  """status="{}" """.format(result.issue_id)
                        elif not inscription.classify:
                            status =  """status="EXH" """                        

                        if len(result.result_splits) == 1:
                            content += (
"""                <RESULT eventid="{}" {}points="{}" swimtime="{}" resultid="{}" """
"""heatid="{}" lane="{}" entrytime="{}" entrycourse="{}" />\n""").format(
                            result.phase.phase_id,
                            status,
                            0,  #FIXME: pendente engadir os puntos waq
                            result.mark_time_st,
                            result.result_id,
                            result.heat.heat_id,
                            result.lane,
                            inscription.mark_time_st,
                            inscription.pool_length == 25 and "SCM" or "LCM",
                        )
                        else:  # Has more 1 split
                            content += (
    """                <RESULT eventid="{}" {}points="{}" swimtime="{}" resultid="{}" """
    """heatid="{}" lane="{}" entrytime="{}" entrycourse="{}">\n""").format(
                                result.phase.phase_id,
                                status,
                                result.category.punctuation or 0,
                                result.mark_time_st,
                                result.result_id,
                                result.heat.heat_id,
                                result.lane,
                                inscription.mark_time_st,
                                inscription.pool_length == 25 and "SCM" or "LCM",
                            )
                            content += """                  <SPLITS>\n"""
                            for split in result.result_splits[:-1]:
                                content += (
"""                    <SPLIT distance="{}" swimtime="{}" />\n""").format(
                                    split.distance,
                                    split.mark_time_st,
                                )
                            content += """                  </SPLITS>\n"""
                        content += """                </RESULT>\n"""
                content += """              </RESULTS>\n"""
            content += """          </ATHLETES>\n"""
            content += """          <RELAYS>\n"""
            for relay in champ.relays:
              if relay.entity == entity:
                content += (
"""            <RELAY agemax="{}" agemin="{}" agetotalmax="{}" agetotalmin="{}" """
"""gender="{}" number="{}">\n              <RESULTS>\n""").format(
                    relay.category.to_age,
                    relay.category.from_age,
                    "-1",  #FIXME: for master competition
                    "-1",  #FIXME: for master competition
                    relay.gender_id,
                    relay.relay_id,  #FIXME: relay number
                )

                """
                continuar aquí:
                <RESULTS> (de relay)
                buscar o ficheiro lenex de resultados da copa de españa div2 
                que está dentro de doc en ordcana e ir á liña 1983.
                basicamente sería copiar do mesmo que as persoas.
                """
                if relay.inscription and relay.inscription.result:
                    result = relay.inscription.result
                    # eventid is phase_id
                    status = ""
                    if result.issue_id:
                        # EXH: exhibition swim.
                        # DSQ: athlete/relay disqualified.
                        # DNS: athlete/relay did not start (no reason given or to late
                        # withdrawl).
                        # DNF: athlete/relay did not finish.
                        # SICK: athlete is sick. Está enfermo
                        # WDR: athlete/relay was withdrawn (on time). Retirouse
                        if result.issue_id not in ('DSQ', 'DNS', 'DNF', 'SICK', 'WDR'):
                            print(result.issue_id)
                            if result.issue_id == 'NPR':
                                status = 'DNS'
                            elif result.issue_id == 'BAI':
                                status = 'WDR'
                            elif result.issue_id == 'RET':
                                status = 'DNF'
                            else:
                                status = 'DSQ'
                        else:
                            status =  """status="{}" """.format(result.issue_id)
                    elif not inscription.classify:
                        status =  """status="EXH" """                        

                    if len(result.result_splits) == 1:
                        content += (
"""                <RESULT eventid="{}" {}points="{}" swimtime="{}" resultid="{}" """
"""heatid="{}" lane="{}" entrytime="{}" entrycourse="{}" />\n""").format(
                        result.phase.phase_id,
                        status,
                        result.category.punctuation or 0,
                        result.mark_time_st,
                        result.result_id,
                        result.heat.heat_id,
                        result.lane,
                        inscription.mark_time_st,
                        inscription.pool_length == 25 and "SCM" or "LCM",
                    )
                    else:  # Has more 1 split
                        content += (
"""                <RESULT eventid="{}" {}points="{}" swimtime="{}" resultid="{}" """
"""heatid="{}" lane="{}" entrytime="{}" entrycourse="{}">\n""").format(
                            result.phase.phase_id,
                            status,
                            result.category.punctuation or 0,
                            result.mark_time_st,
                            result.result_id,
                            result.heat.heat_id,
                            result.lane,
                            inscription.mark_time_st,
                            inscription.pool_length == 25 and "SCM" or "LCM",
                        )
                        content += """                  <SPLITS>\n"""
                        for split in result.result_splits[:-1]:
                            content += (
"""                    <SPLIT distance="{}" swimtime="{}" />\n""").format(
                                split.distance,
                                split.mark_time_st,
                            )
                        content += """                  </SPLITS>\n"""
                        content += """                  <RELAYPOSITIONS>\n"""

                        for member in relay.relay_members:
                            content += (
"""                    <RELAYPOSITION athleteid="{}" number="{}" />\n""").format(
                                member.person_id,
                                member.pos,
                            )
                        content += """                  </RELAYPOSITIONS>\n"""
                    content += """                </RESULT>\n"""
                content += """              </RESULTS>\n"""
        content += """      </CLUBS>\n"""
        content += """    </MEET>\n"""
        content += """  </MEETS>\n"""

# liña 2456 viraxe irregular
        print(content)
        return content


            

        
        # for phase in champ.phases:
        #     if phase.official:
        #         for result in phase.results:
        #             print(result)
