# -*- coding: utf-8 -*-

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Copyright (C) 2017 Federacion Galega de Natación (FEGAN) http://www.fegan.org
# Author: Daniel Muñiz Fontoira (2017) <dani@damufo.com>

# from unicodedata import category
from reportlab.lib.units import mm
from specific_classes.fiarna.report_base_referee_tokens import ReportBaseRefereeTokens


class Club(object):
    def __init__(self, code, short_desc):
        self.code = code
        self.short_desc = short_desc


class Person(object):
    def __init__(self, license, name, surname, gender, club, year_of_birth):
        self.license= license
        self.name = name
        self.surname = surname
        self.gender = gender
        self.club = club
        self.year_of_birth = year_of_birth

    @property
    def full_name(self):
        full_name = ""
        if (len(self.surname) + len(self.name)) < 32:
            full_name = "{}, {}".format(self.surname, self.name)
        else:
            full_name = "{}, {}".format(self.surname[:20], self.name[:12])
        return full_name

class Relay(object):
    def __init__(self, relay_id, name,gender, club, category):
        self.relay_id = relay_id
        self.name = name
        self.gender = gender
        self.club = club
        self.category = category

    @property
    def full_name(self):
        return self.name[:32]

    @property
    def license(self):
        return self.club.code

    @property
    def year_of_birth(self):
        return self.category

class Event(object):
    def __init__(self, gender_id, event_id, category_id, phase_progression,
                 phase_order, order, date):
        self.gender_id = gender_id
        self.event_id = event_id
        self.category_id = category_id
        self.phase_progression = phase_progression  # fase 1 final, fase 2 Preliminar
        self.phase_order = phase_order
        self.order = order
        self.date = date

    @property
    def event_desc(self):

        if self.event_id.endswith("L"):
            style = _("FREE")
        elif self.event_id.endswith("M"):
            style = _("BUTTERFLY")
        elif self.event_id.endswith("B"):
            style = _("BREASTSTROKE")
        elif self.event_id.endswith("E"):
            style = _("BACKSTSTROKE")
        elif self.event_id.endswith("S"):
            style = _("STYLES")
        event_desc = "{}.- {}m {} {} {}".format(self.order,
                                                self.event_id[:-1],
                                                style,
                                                self.gender_desc,
                                                self.category_id)
        return event_desc

    @property
    def phase_desc(self):
        phase_desc = ""
        if self.phase_progression in ('TIM', 'FIN'):
            phase_desc = _("FINAL")
        elif self.phase_progression == 'PRE':
            phase_desc = _("PRELIM")
        return phase_desc

    @property
    def gender_desc(self):
        gender_desc = ""
        if self.gender_id == "F":
            gender_desc = _("FEM")
        elif self.gender_id == "M":
            gender_desc = _("MAS")
        elif self.gender_id == "X":
            gender_desc = _("MIX")
        return gender_desc

    @property
    def day(self):
        day = ""
        if self.date:
            day = int(self.date[8:10])
        return day

    @property
    def month_text(self):
        months = (_("january"), _("february"), _("march"), _("april"),
                  _("may"), _("june"), _("july"), _("august"), _("september"),
                  _("october"), _("november"), _("december"))
        month_text = ""
        if self.date:
            month_text = months[int(self.date[5:7])-1]
        return month_text

    @property
    def year(self):
        year = ""
        if self.date:
            year = self.date[:4]
        return year


class Token(object):
    def __init__(self, event, person, unit, lane):
        self.event = event  # gender event: fem, mas, mix
        self.person = person
        self.unit = unit  # serie
        self.lane = lane  # pista


class RefereeTokens(object):


    def __init__(self, champ):
        '''
        Constructor
        '''
        self.champ = champ
        from operator import attrgetter
        self.sort_order = 0

    @property
    def config(self):
        return self.champ.config

    def sort(self, values):
        from operator import attrgetter
        if self.sort_order == 0:
            values_sorted = sorted(values, key=attrgetter(
                'lane', 'event.order', 'event.phase_order', 'unit'))
        elif self.sort_order == 1:
            values_sorted = sorted(values, key=attrgetter(
                'event.order', 'event.phase_order', 'unit', 'lane'))
        return values_sorted

    def report(self, report_path, from_event, to_event, phase):
        '''
        Generate a PDF file with licenses to export.
        '''
        # self.config.dbs.connection(dbs_path=dbs_path)

#         Championship


        champ_desc = self.champ.params.get_value('champ_name')
        venue = self.champ.params.get_value('champ_venue')

#         Clubes
        sql = """
select entity_id, entity_code, short_name
from entities """
        res = self.config.dbs.exec_sql(sql=sql)

        ENTITY_ID, CODE, SHORT_NAME = range(3)
        clubs = {}
        for i in res:
            clubs[i[ENTITY_ID]] = Club(
                code=i[CODE],
                short_desc=i[SHORT_NAME])

#         Persons
        sql = """
select person_id, license, surname, name, gender_id, entity_id,
strftime('%Y', birth_date) from persons """
        res = self.config.dbs.exec_sql(sql=sql)
        (PERSON_ID, LICENSE, SURNAME,
         NAME, GENDER, ENTITY_ID, YEAR_OF_BIRTH) = range(7)
        persons = {}
        for i in res:
            persons[i[PERSON_ID]] = Person(
                    license=i[LICENSE],
                    name=i[NAME],
                    surname=i[SURNAME],
                    gender=i[GENDER],
                    club=clubs[i[ENTITY_ID]],
                    year_of_birth=i[YEAR_OF_BIRTH])

#         relays
        sql = """
select r.relay_id, r.name, r.gender_id, r.entity_id, c.name
from relays r left join categories c on r.category_id=c.category_id"""
        res = self.config.dbs.exec_sql(sql=sql)
        (RELAY_ID, NAME, GENDER, ENTITY_ID, CATEGORY) = range(5)
        relays = {}
        for i in res:
            relays[i[RELAY_ID]] = Relay(
                    relay_id=i[RELAY_ID],
                    name=i[NAME],
                    gender=i[GENDER],
                    club=clubs[i[ENTITY_ID]],
                    category=i[CATEGORY],
)

#         Events
#         sql = """
# select gendercode, eventcode, categorycode, phasecode, phaseorder,
# sessionorder, startdate from phases p inner join events on  """
        sql = """
select p.phase_id, e.gender_id, e.event_code, p.progression, p.pos, e.pos, s.date ||' '|| s.time 
from (phases p inner join events e on p.event_id=e.event_id) inner join 
sessions s on s.session_id=p.session_id order by s.date, s.time, p.pos;  """
        res = self.config.dbs.exec_sql(sql=sql)
        (PHASE_ID, GENDER_ID, EVENT_ID,
         PHASE_PROGRESSION, PHASE_ORDER, ORDER, DATE) = range(7)
        events = {}
        for i in res:
            # event_code = "{}.{}.{}.{}".format(i[GENDER_ID], i[EVENT_ID],
            #                                   i[CATEGORY_ID], i[PHASE_ID])
            events[i[PHASE_ID]] = Event(
                    gender_id=i[GENDER_ID],
                    event_id=i[EVENT_ID],
                    category_id='',
                    phase_progression=i[PHASE_PROGRESSION],
                    phase_order=int(i[PHASE_ORDER]),
                    order=int(i[ORDER]),
                    date=i[DATE])

#         heats
        sql = """
select e.gender_id, e.event_id, '', p.phase_id, i.person_id, i.relay_id, h.pos,
lane from ((((results r 
left join heats h on r.heat_id=h.heat_id) 
left join phases p on h.phase_id=p.phase_id) 
left join events e on p.event_id=e.event_id)
left join inscriptions i on i.inscription_id=r.inscription_id);
"""
        tokens = self.config.dbs.exec_sql(sql=sql)
        (GENDER_ID, EVENT_ID, CATEGORY_ID,
         PHASE_ID, PERSON_ID, RELAY_ID, UNIT, LANE) = range(8)
        values = []
        for i in tokens:
            if i[PERSON_ID]:
                person = persons[i[PERSON_ID]]
                relay = ''
            elif i[RELAY_ID]:
                person = relays[i[RELAY_ID]]
            values.append(Token(
                    event=events[i[PHASE_ID]],
                    person=person,
                    unit=int(i[UNIT]),
                    lane=int(i[LANE])))

        values = self.sort(values)
#         filter from_event
        if phase == 0:  # All
            phase_id = None
        elif phase == 1:  # Final
            phase_id = 'TIM'
        elif phase == 2:  # Preliminar
            phase_id = 'PRE'
        values_filtered = []
        for i in values:
            if i.event.order >= from_event and \
                    i.event.order <= to_event:
                if phase_id and i.event.phase_id == phase_id:
                    values_filtered.append(i)
                elif not phase_id:
                    values_filtered.append(i)
        values = values_filtered

        d = ReportBaseRefereeTokens(app_path_folder=self.config.app_path_folder,
                                    file_path=report_path,
                                    orientation='portrait',
                                    title=_("Referee's tokens"))

        tot = len(values)
        for x in range(0, tot, 2):
            if x > 0 and divmod(x, 4)[1] == 0:
                d.insert_page_break()
            i = values[x]
            if x < (tot-1):
                k = values[x+1]
            else:
                k = None

            table = [[champ_desc, "", champ_desc]]
            style = [
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')
                ]
            col_widths = ['48%', '4%', '48%']
            row_heghts = [7*mm]
            d.insert_table(table=table, colWidths=col_widths,
                           rowHeights=row_heghts,
                           style=style, pagebreak=False)

            table = [["{} ({})".format(i.event.event_desc, i.event.phase_desc),
                      "",
                      "",
                      "{} ({})".format(k and k.event.event_desc or "",
                                       k and k.event.phase_desc or ""),
                      ""],
                     [_("UNIT: {}").format(i.unit),
                      _("LANE: {}").format(i.lane),
                      "",
                      _("UNIT: {}").format(k and k.unit or ""),
                      _("LANE: {}").format(k and str(k.lane) or "")]]
            style = [
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP')]
            col_widths = ['15%', '33%', '4%', '15%', '33%']
            row_heghts = [5*mm, 7*mm]
            d.insert_table(table=table, colWidths=col_widths,
                           rowHeights=row_heghts,
                           style=style, pagebreak=False)

            table = [["{} {} ({})".format(i.person.license,
                                          i.person.full_name,
                                          i.person.year_of_birth),
                      "",
                      "{} {} ({})".format(k and k.person.license or "",
                                          k and k.person.full_name or "",
                                          k and k.person.year_of_birth or "")],
                     ["{} {}".format(i.person.club.code,
                                     i.person.club.short_desc,),
                      "",
                      "{} {}".format(k and k.person.club.code or "",
                                     k and k.person.club.short_desc or "",)]]
            style = [('FONTSIZE', (0, 0), (-1, -1), 9),
                     ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                     ('VALIGN', (0, 0), (-1, -1), 'TOP')]
            col_widths = ['48%', '4%', '48%']
            row_heghts = [5*mm, 6*mm]
            d.insert_table(table=table, colWidths=col_widths,
                           rowHeights=row_heghts,
                           style=style, pagebreak=False)
            table = [
                    [_("SPLITS LOG"), "", "", "", _("SPLITS LOG"), "", ""],
                    ["50:", "550:", "1050:", "", "50:", "550:", "1050:"],
                    ["100:", "600:", "1100:", "", "100:", "600:", "1100:"],
                    ["150:", "650:", "1150:", "", "150:", "650:", "1150:"],
                    ["200:", "700:", "1200:", "", "200:", "700:", "1200:"],
                    ["250:", "750:", "1250:", "", "250:", "750:", "1250:"],
                    ["300:", "800:", "1300:", "", "300:", "800:", "1300:"],
                    ["350:", "850:", "1350:", "", "350:", "850:", "1350:"],
                    ["400:", "900:", "1400:", "", "400:", "900:", "1400:"],
                    ["450:", "950:", "1450:", "", "450:", "950:", "1450:"],
                    ["500:", "1000:", "1500:", "", "500:", "1000:", "1500:"],
                    [_("RECORDING END TIMES"), "",    "", "",
                     _("RECORDING END TIMES"), "", ""],
                    [_("CHRONO 1"), _("CHRONO 2"), _("CHRONO 3"), "",
                     _("CHRONO 1"), _("CHRONO 2"), _("CHRONO 3")],
                    ["", "", "", "", "", "", ""]]
            style = [
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('SPAN', (0, 0), (2, 0)),
                    ('SPAN', (4, 0), (-1, 0)),
                    ('GRID', (0, 1), (2, 10), 0.5, d.colors.lightgrey),
                    ('GRID', (4, 1), (-1, 10), 0.5, d.colors.lightgrey),
                    ('FONTSIZE', (0, 1), (-1, 10), 9),
                    ('ALIGN', (0, 11), (-1, -1), 'CENTER'),
                    ('SPAN', (0, 11), (2, 11)),
                    ('SPAN', (4, 11), (-1, 11)),
                    ('GRID', (0, 12), (2, 13), 0.5, d.colors.lightgrey),
                    ('GRID', (4, 12), (-1, 13), 0.5, d.colors.lightgrey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]
            col_widths = ['16%', '16%', '16%', '4%', '16%', '16%', '16%']
            row_heghts = [6*mm, 5*mm, 5*mm, 5*mm, 5*mm, 5*mm, 5*mm, 5*mm,
                          5*mm, 5*mm, 5*mm, 6*mm, 5*mm, 5*mm]
            d.insert_table(table=table, colWidths=col_widths,
                           rowHeights=row_heghts,
                           style=style, pagebreak=False)

            table = [[_("END TIME DEFINITIVE"), _("Arrival"),
                      _("Clasific."), _("Points"), "",
                      _("END TIME DEFINITIVE"), _("Arrival"),
                      _("Clasific."), _("Points")],
                     ["", "", "", "", "", "", ""]]
            style = [
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 1), (3, 1), 0.5, d.colors.lightgrey),
                    ('GRID', (5, 1), (-1, 1), 0.5, d.colors.lightgrey),
                ]
            col_widths = ['24%', '8%', '8%', '8%', '4%',
                          '24%', '8%', '8%', '8%']
            d.insert_table(table=table, colWidths=col_widths,
                           style=style, pagebreak=False)

            data_i = _("{venue} on {month} {day}, {year}").format(
                    venue=venue.title(),
                    day=i.event.day,
                    month=i.event.month_text,
                    year=i.event.year)
            if k:
                data_k = _("{venue} on {month} {day}, {year}").format(
                    venue=venue.title(),
                    day=k.event.day,
                    month=k.event.month_text,
                    year=k.event.year)
            table = [[_("Signature timekeeper"),
                      _("Sinature secretary desk"), "",
                      _("Signature timekeeper"),
                      _("Sinature secretary desk")],
                     ["", "", ""],
                     [data_i, "", "", data_k, ""]]
            style = [
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
                    ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                    ('ALIGN', (4, 0), (4, 0), 'RIGHT'),
                    ('SPAN', (0, 2), (1, 2)),
                    ('SPAN', (3, 2), (-1, 2)),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]
            col_widths = ['24%', '24%', '4%', '24%', '24%']
            row_heghts = [6*mm, 8*mm, 5*mm]
            d.insert_table(table=table, colWidths=col_widths,
                           rowHeights=row_heghts,
                           style=style, pagebreak=False)

            if divmod(x, 4)[1] == 0:
                table = [[" "]]
                style = []
                col_widths = ['100%']
                row_heghts = [15*mm]
                d.insert_table(table=table, colWidths=col_widths,
                               rowHeights=row_heghts,
                               style=style, pagebreak=False)

        d.build_file()
