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

# Copyright (C) 2019 Federacion Galega de Natación (FEGAN) http://www.fegan.org
# Author: Daniel Muñiz Fontoira (2017) <dani@damufo.com>


import re
from datetime import date, timedelta, datetime


def validate(value):
    """
    I do not remember the author of thus function, sorry.
    Conversion from string to datetime object.  Most of the common
    patterns are currently supported.
    If not valid '' is returned

    @param input_: Date time (of supported pattern)
    @type input_: String, or None
    @return: datetime.datetime

    >>> print str2date("10/4/2005 21:45")
    2005-10-04 21:45:00
    """
    date_valid = ''
    if value:
        if not isinstance(value, str):
            print('Value passed must be of type string.')
        else:
            ptime = {}
            parts = {'Y': r'(?P<y>(1|2)\d{3})',
                     'm': r'(?P<m>(1[0-2]|0[1-9]|[1-9]))',
                     'd': r'(?P<d>(0[1-9]|[12]\d|3[01]|[1-9]))',
                     'T': r'( (?P<H>([0-1]?[0-9])|([2][0-3])):(?P<M>[0-5]?[0-9])(:(?P<S>[0-5]?[0-9]))?)?'}
            regs = []
            regs.append('^%(Y)s\D%(m)s\D%(d)s%(T)s')
            regs.append('^%(Y)s%(m)s%(d)s%(T)s')
            regs.append('^%(d)s\D%(m)s\D%(Y)s%(T)s')
            regs.append('^%(d)s%(m)s%(Y)s$')
            regs.append('^%(m)s\D%(d)s\D%(Y)s%(T)s')
            regs.append('^%(m)s%(d)s%(Y)s%(T)s')

            for regexp in regs:
                ex = regexp % parts
                match = re.match(regexp % parts, value)
                if match is not None:
                    ptime.update(match.groupdict())
                    break
            if len(list(ptime.keys())) not in  (3, 6):
                print(
                    'Value passed must by 2005-10-04 or '
                    '2005-10-04 21:45 or 2005-10-04 21:45:00')
            elif ptime:
                try:
                    datetime_valid = datetime(
                        year=int(ptime['y']),
                        month=int(ptime['m']),
                        day=int(ptime['d']),
                        hour=int(ptime['H'] or '0'),
                        minute=int(ptime['M'] or '0'),
                        second=int(ptime['S'] or '0'))
                    date_valid = "{}-{}-{} {}:{}:{}".format(
                        datetime_valid.year,
                        str(datetime_valid.month).zfill(2),
                        str(datetime_valid.day).zfill(2),
                        str(datetime_valid.hour).zfill(2),
                        str(datetime_valid.minute).zfill(2),
                        str(datetime_valid.second).zfill(2),
                        )
                except:
                    print('err')
                    date_valid = ''

    return date_valid

def get_current():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_numbers():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def get_file_name():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def get_current_batch():
    return datetime.now().strftime("%Y-%V")


# =============================================================================
# Dates
# =============================================================================

def __date2str(value, output_format='YYYY/MM/DD'):
    """ value is a date object"""
    text = ''
    if isinstance(value, date):
        if output_format == 'YYYYMMDD':
            text = "%s%s%s" % (value.year,
                               str(value.month).zfill(2),
                               str(value.day).zfill(2))
        elif output_format == 'YYYY-MM-DD':
            text = "%s-%s-%s" % (value.year,
                               str(value.month).zfill(2),
                               str(value.day).zfill(2))
        elif output_format == 'DD/MM/YYYY':
            text = "%s/%s/%s" % (str(value.day).zfill(2),
                                 str(value.month).zfill(2),
                                 value.year)
        else:  # default
            text = "%s/%s/%s" % (value.year,
                                 str(value.month).zfill(2),
                                 str(value.day).zfill(2))
        
    return text

def __datetime2str(value, output_format='YYYY-MM-DD HH:MM:SS'):
    """ value is a date object"""
    text = ''
    if isinstance(value, datetime):
        if output_format == 'DD-MM-YYYY HH:MM:SS':
            text = "{}-{}-{} {}:{}:{}".format(
                str(value.day).zfill(2),
                str(value.month).zfill(2),
                value.year,
                str(value.hour).zfill(2),
                str(value.minute).zfill(2),
                str(value.second).zfill(2))
        elif output_format == 'YYYY/MM/DD HH:MM:SS':
            text = "{}/{}/{} {}:{}:{}".format(
                value.year,
                str(value.month).zfill(2),
                str(value.day).zfill(2),
                str(value.hour).zfill(2),
                str(value.minute).zfill(2),
                str(value.second).zfill(2))
        else:  # default YYYY-MM-DD HH:MM:SS
            text = "{}-{}-{} {}:{}:{}".format(
                value.year,
                str(value.month).zfill(2),
                str(value.day).zfill(2),
                str(value.hour).zfill(2),
                str(value.minute).zfill(2),
                str(value.second).zfill(2))
    return text

def __date_numbers_to_iso(value):
    '''
    Value is a YYYYMMDD string
    return a YYYY-MM-DD string
    '''
    return datetime.strptime(value, '%Y%m%d').strftime('%Y-%m-%d')

def __day_of_week(value):
    """date is a date format, days is a integer value"""
    value = str2date(value)
    days = ('Luns', 'Martes', 'Mércores', 'Xoves', 'Venres', 'Sábado',
            'Domingo', )
    str_day = days[value.weekday()]
    return str_day[0].upper() + str_day[1:].lower()


def __sum_days_to_date(date, days):
    """date is a date format, days is a integer value"""
    return date + timedelta(days=days)


# def get_now_text(format_date='YYYYMMDD'):
#     """
#     date is a date format, days is a integer value
#     """
#     if format_date == 'YYYYMMDD':
#         date_text = datetime.now().strftime("%Y%m%d")
#     elif format_date == 'HHMMSS':
#         date_text = datetime.now().strftime("%H%M%S")
#     elif format_date == 'YYYYMMDD_HHMMSS':
#         date_text = datetime.now().strftime("%Y%m%d_%H%M%S")
#     return date_text


def __validate_str_value(value):
    """
    Value is a YYYY-MM-DD, YYYY/MM/DD or YYYYMMDD
    """
    result = None
    value = value.replace('/', '')
    value = value.replace('-', '')
    if len(value) == 8 and value.isdigit():
        result = '%s/%s/%s' % (value[:4], value[4:6], value[6:8])
    return result


def __str2date(input_):
    """
    I do not remember the author of thus function, sorry.
    Conversion from string to datetime object.  Most of the common
    patterns are currently supported.  If None is passed None will be
    returned

    @param input_: Date time (of supported pattern)
    @type input_: String, or None
    @return: datetime.datetime

    >>> print str2date("10/4/2005 21:45")
    2005-10-04 21:45:00
    """
    date_valid = None

    if input_:
        if not isinstance(input_, str):
            print('Value passed must be of type string.')
        else:
            ptime = {}
            parts = {'Y': r'(?P<y>(1|2)\d{3})',
                     'm': r'(?P<m>(1[0-2]|0[1-9]|[1-9]))',
                     'd': r'(?P<d>(0[1-9]|[12]\d|3[01]|[1-9]))'}
            regs = []
            regs.append('^%(Y)s\D%(m)s\D%(d)s$')
            regs.append('^%(Y)s%(m)s%(d)s$')
            regs.append('^%(d)s\D%(m)s\D%(Y)s$')
            regs.append('^%(d)s%(m)s%(Y)s$')
            regs.append('^%(m)s\D%(d)s\D%(Y)s$')
            regs.append('^%(m)s%(d)s%(Y)s$')
            for regexp in regs:
                match = re.match(regexp % parts, input_)
                if match is not None:
                    ptime.update(match.groupdict())
                    break
            if len(list(ptime.keys())) != 3:
                print('Value passed must by year, month and day.')
            elif ptime:
                try:
                    date_valid = date(year=int(ptime['y']),
                                      month=int(ptime['m']),
                                      day=int(ptime['d']))
                except ValueError as err:
                    print(err)
                    date_valid = None

    return date_valid

def __str2datetime(input_):
    """
    I do not remember the author of thus function, sorry.
    Conversion from string to datetime object.  Most of the common
    patterns are currently supported.  If None is passed None will be
    returned

    @param input_: Date time (of supported pattern)
    @type input_: String, or None
    @return: datetime.datetime

    >>> print str2date("10/4/2005 21:45")
    2005-10-04 21:45:00
    """
    date_valid = None

    if input_ is not None:
        if not isinstance(input_, str):
            print('Value passed must be of type string.')
        else:
            ptime = {}
            parts = {'Y': r'(?P<y>(1|2)\d{3})',
                     'm': r'(?P<m>(1[0-2]|0[1-9]|[1-9]))',
                     'd': r'(?P<d>(0[1-9]|[12]\d|3[01]|[1-9]))',
                     'T': r'( (?P<H>([0-1]?[0-9])|([2][0-3])):(?P<M>[0-5]?[0-9])(:(?P<S>[0-5]?[0-9]))?)?'}
            regs = []
            regs.append('^%(Y)s\D%(m)s\D%(d)s%(T)s')
            regs.append('^%(Y)s%(m)s%(d)s%(T)s')
            regs.append('^%(d)s\D%(m)s\D%(Y)s%(T)s')
            regs.append('^%(d)s%(m)s%(Y)s$')
            regs.append('^%(m)s\D%(d)s\D%(Y)s%(T)s')
            regs.append('^%(m)s%(d)s%(Y)s%(T)s')
            for regexp in regs:
                ex = regexp % parts
                match = re.match(regexp % parts, input_)
                if match is not None:
                    ptime.update(match.groupdict())
                    break
            if len(list(ptime.keys())) not in  (3, 6):
                print('Value passed must by 2005-10-04 or 2005-10-04 21:45 or 2005-10-04 21:45:00')
            elif ptime:
                try:
                    date_valid = datetime(year=int(ptime['y']),
                                      month=int(ptime['m']),
                                      day=int(ptime['d']),
                                      hour=int(ptime['H'] or '0'),
                                      minute=int(ptime['M'] or '0'),
                                      second=int(ptime['S'] or '0'))
                except ValueError as err:
                    print(err)
                    date_valid = None

    return date_valid

def __days_from_date(d):
    """
    d: date format string AAAAMMAA
    """
#         d = datea.split('/')
    date_to_calculate = datetime.strptime(d[:4] + d[4:6] + d[6:8],
                                          '%Y%m%d').date()

    # Creo una variable con la operaciÃ³n aritmÃ©tica
    calc_date = datetime.now().date() - date_to_calculate
    return calc_date.days


def __format_str(value, output_format='YYYY/MM/DD'):
    """
    value is a string date YYYY-MM-DD
    """
    if output_format in('YYYY/MM/DD', 'YYYY-MM-DD'):
        result = date2str(str2date(value), output_format)
    elif output_format == 'long_text':
        text_months = {
            1: _('january'),
            2: _('february'),
            3: _('march'),
            4: _('april'),
            5: _('may'),
            6: _('june'),
            7: _('july'),
            8: _('august'),
            9: _('september'),
            10: _('october'),
            11: _('november'),
            12: _('december'),
            }
        value_date = str2date(value)
        result = '{} de {} de {}'.format(
            value_date.day,
            text_months[value_date.month],
            value_date.year
            )
    return result

def __get_str_date(value, output_format='YYYY/MM/DD'):
    """
    value is a validated iso string date YYYY-MM-DD HH:MM:SS
    return a string date YYYY/MM/DD
    """
    return value[:10].replace('-', '/')

# def get_current_week_number():
#     value = datetime.now().strftime("%V")
#     return value


def __get_current_date():
    return datetime.now().strftime("%Y%m%d")

# def current_time():
#     return datetime.now().strftime("%H%M%S")

def __get_current_date_time():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def __get_timestamp():
    return datetime.now().strftime("%Y%m%d%H%M%S")
    
def __get_timestamp_iso():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =============================================================================
# Times
# =============================================================================


def int2time(value, precision='hun', zero_fill=False,
             default='', force_hours=False):
    """
    Convert a centesimas (integer) to time (text)
    precison ['hun', 'sec'] hundredths, seconds
    """
    time_text = default

    if isinstance(value, int):
        if precision == 'hun':
            adjust = 100
            hundreds = value % 100
        else:
            adjust = 1
            hundreds = 0
        seconds = int(value / adjust) % 60
        minuts = int((value / (60 * adjust)) % 60)
        hours = int((value / (3600 * adjust)))
        result = '0'
#            hours
        if hours:
            result = str(hours).zfill(2)
        elif force_hours:
            result = "00"

#            minuts
        if result != '0':
            result = '%s:%s' % (result, str(minuts).zfill(2))
        else:
            result = str(minuts)

        if result != '0':  # seconds
            result = '%s:%s' % (result, str(seconds).zfill(2))
        else:
            result = str(seconds)

        if precision == 'hun':  # hundreds
            if result != '0':
                result = '%s.%s' % (result, str(hundreds).zfill(2))
            else:
                result = str(hundreds)
        if result:
            time_text = result

    return time_text


def time2int(value, precision='hun'):
    """
    time value is a string
    time format: HH:MM:SS or HH:MM:SS.ss (ss=hundredths)
    Convert a time (string) to integer, retrun a integer
    time text is previous valided
    precision= hun: hundredths | sec: seconds
    """
    result = 0
    if precision == 'hun':
        adjust = 100
    else:
        adjust = 60

    value = value.strip().replace('.', ':').replace(',', ':')
    time_splits = value.split(":")

    if len(time_splits) == 1:
        result = int(time_splits[0])
    elif len(time_splits) == 2:
        result = (int(time_splits[0]) * adjust) + int(time_splits[1])
    elif len(time_splits) == 3:
        result = (int(time_splits[0]) * (60 * adjust)) + \
                (int(time_splits[1]) * adjust) + int(time_splits[2])

    return result

