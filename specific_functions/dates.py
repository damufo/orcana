# -*- coding: utf-8 -*-


import re
from datetime import date, timedelta, datetime


def validate(input_):
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
    date_valid = ''

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
                    date_valid = "{}-{}-{}".format(
                        date_valid.year,
                        str(date_valid.month).zfill(2),
                        str(date_valid.day).zfill(2),
                        )
                except:
                    print('err')
                    date_valid = ''

    return date_valid

def get_current():
    return datetime.now().strftime("%Y-%m-%d")

def get_numbers():
    return datetime.now().strftime("%Y%m%d")

def format(value, mask):
    '''
    value is a string date value: %Y-%m-%d
    format is a string format, example: '%d/%m/%Y' '%Y%m%d'
    return a string formated
    '''
    if mask == 'long_text':
        text_months = {
            1: _('xaneiro'),
            2: _('febreiro'),
            3: _('marzo'),
            4: _('abril'),
            5: _('maio'),
            6: _('xuño'),
            7: _('xullo'),
            8: _('agosto'),
            9: _('setembro'),
            10: _('outubro'),
            11: _('novembro'),
            12: _('decembro'),
            }
        value_date = datetime.strptime(
            value[:4] + value[5:7] + value[8:10], '%Y%m%d').date()
        result = _('{month} {day}, {year}').format(
            day=value_date.day,
            month=text_months[value_date.month],
            year=value_date.year
            )
    else:
        if len(value) == 8:
            value_date = datetime.strptime(
                value[:4] + value[4:6] + value[6:8], '%Y%m%d').date()
        elif len(value) == 10:
            value_date = datetime.strptime(
                value[:4] + value[5:7] + value[8:10], '%Y%m%d').date()
        value_date = value_date.strftime(mask)
    
    return value_date

def sum_days(value, days):
    '''
    value is a string date value: %Y-%m-%d
    days is a integer value
    '''
    if len(value) == 8:
        value_date = datetime.strptime(
            value[:4] + value[4:6] + value[6:8], '%Y%m%d').date()
        value_date = value_date + timedelta(days=days)
        date_final = value_date.strftime('%Y%m%d')
    elif len(value) == 10:
        value_date = datetime.strptime(
            value[:4] + value[5:7] + value[8:10], '%Y%m%d').date()
        value_date = value_date + timedelta(days=days)
        date_final = value_date.strftime('%Y-%m-%d')
    else:
        date_final = ""
    return date_final
    
def get_age(value):
    '''
    value birth_date is a string '%Y-%m-%d' or '%Y%m%d'
    '''
    today = date.today()
    if len(value) == 8:
        birth_date = datetime.strptime(
            value[:4] + value[4:6] + value[6:8], '%Y%m%d').date()
    elif len(value) == 10:
        birth_date = datetime.strptime(
            value[:4] + value[5:7] + value[8:10], '%Y%m%d').date()
    # birth_date = datetime.strptime(
    #         value[:4] + value[5:7] + value[8:10], '%Y%m%d').date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def get_age_for_year(birth_date, year):
    '''
    birth_date is a string '%Y-%m-%d' or '%Y%m%d'
    year is a string ex. 2021
    '''
    to_date =  datetime.strptime(str(year) + "12" + "31", '%Y%m%d').date()
    if len(birth_date) == 8:
        birth_date = datetime.strptime(
            birth_date[:4] + birth_date[4:6] + birth_date[6:8], '%Y%m%d').date()
    elif len(birth_date) == 10:
        birth_date = datetime.strptime(
            birth_date[:4] + birth_date[5:7] + birth_date[8:10], '%Y%m%d').date()
    # birth_date = datetime.strptime(
    #         birth_date[:4] + birth_date[5:7] + birth_date[8:10], '%Y%m%d').date()
    age = to_date.year - birth_date.year - (
        (to_date.month, to_date.day) < (birth_date.month, birth_date.day))
    return age

def get_age_for_date(birth_date, date_age_calculation):
    '''
    birth_date is a string '%Y-%m-%d' or '%Y%m%d'
    date_age_calcularion is a string '%Y-%m-%d' or '%Y%m%d'ex. 2021-12-31
    '''
    if len(date_age_calculation) == 8:
        date_age_calculation = datetime.strptime(
            date_age_calculation[:4] + date_age_calculation[4:6] + date_age_calculation[6:8], '%Y%m%d').date()
    elif len(date_age_calculation) == 10:
        date_age_calculation = datetime.strptime(
            date_age_calculation[:4] + date_age_calculation[5:7] + date_age_calculation[8:10], '%Y%m%d').date()

    if len(birth_date) == 8:
        birth_date = datetime.strptime(
            birth_date[:4] + birth_date[4:6] + birth_date[6:8], '%Y%m%d').date()
    elif len(birth_date) == 10:
        birth_date = datetime.strptime(
            birth_date[:4] + birth_date[5:7] + birth_date[8:10], '%Y%m%d').date()
    # birth_date = datetime.strptime(
    #         birth_date[:4] + birth_date[5:7] + birth_date[8:10], '%Y%m%d').date()
    age = date_age_calculation.year - birth_date.year - (
        (date_age_calculation.month, date_age_calculation.day) < (birth_date.month, birth_date.day))
    return age

def get_days_until_today(value):
    '''
    value is a past date
    '''
    if len(value) == 8:
        date_to_calculate = datetime.strptime(value,'%Y%m%d').date()
    elif len(value) == 10:
        date_to_calculate = datetime.strptime(
            value,'%Y-%m-%d').date()

    # Creo una variable con la operación aritmética
    calc_date = datetime.now().date() - date_to_calculate
    return calc_date.days

# =============================================================================



# def __date2str(value, output_format='YYYY/MM/DD'):
#     """ value is a date object"""
#     text = ''
#     if isinstance(value, date):
#         if output_format == 'YYYYMMDD':
#             text = "%s%s%s" % (value.year,
#                                str(value.month).zfill(2),
#                                str(value.day).zfill(2))
#         elif output_format == 'DD/MM/YYYY':
#             text = "%s/%s/%s" % (str(value.day).zfill(2),
#                                  str(value.month).zfill(2),
#                                  value.year)
#         elif output_format == 'YYYY-MM-DD':
#             text = "%s-%s-%s" % (value.year,
#                                  str(value.month).zfill(2),
#                                  str(value.day).zfill(2))
#         else:  # default
#             text = "%s/%s/%s" % (value.year,
#                                  str(value.month).zfill(2),
#                                  str(value.day).zfill(2))
#     return text


# def __date2text(value, output_format='YYYY/MM/DD'):
#     return date2str(value, output_format)


# def __day_of_week(value):
#     """date is a date format, days is a integer value"""
#     value = text2date(value)
#     days = ('Luns', 'Martes', 'Mércores', 'Xoves', 'Venres', 'Sábado',
#             'Domingo', )
#     str_day = days[value.weekday()]
#     return str_day[0].upper() + str_day[1:].lower()


# def __text2date(value):
#     """
#     deprecated function
#     value is a unicode 'YYYY/MM/DD' format
#     return a date object
#     """
#     return str2date(value)


# def __sum_days_to_date(date, days):
#     """date is a date format, days is a integer value"""
#     return date + timedelta(days=days)


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


def __validate_text_value(value):
    """
    Value is a YYYY-MM-DD, YYYY/MM/DD or YYYYMMDD
    """
    result = None
    value = value.replace('/', '')
    value = value.replace('-', '')
    if len(value) == 8:
        result = '%s-%s-%s' % (value[:4], value[4:6], value[6:8])
    elif len(value) == 10:
        result = '%s-%s-%s' % (value[:4], value[5:7], value[8:10])
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


def __days_from_date(d):
    """
    d: date format string YYYYMMDD
    """
#         d = datea.split('/')
    date_to_calculate = datetime.strptime(d[:4] + d[4:6] + d[6:8],
                                          '%Y%m%d').date()

    # Creo una variable con la operación aritmética
    calc_date = datetime.now().date() - date_to_calculate
    return calc_date.days



def __format_str(value, output_format='YYYY/MM/DD'):
    """
    value is a string YYYYMMDD
    """
    return date2str(str2date(value), output_format)


def __format_lev(value, output_format='YYYY-MM-DD'):
    """
    value is a string YYYYMMDD
    return lev format YYYY-MM-DD HH:MM:SS
    """
    date_time = '{} 00:00:00'.format(date2str(str2date(value), output_format))
    return date_time