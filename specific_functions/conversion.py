# -*- coding: utf-8 -*- 


"""
values_raw = gender_id, event_id, from_man_to_ele, from_25_to_50
"""

_conversions_2016_2020 = {
    "F.100B": {"man_to_ele": 19, "25_to_50": 200},
    "F.100E": {"man_to_ele": 19, "25_to_50": 220},
    "F.100L": {"man_to_ele": 19, "25_to_50": 100},
    "F.100M": {"man_to_ele": 19, "25_to_50": 80},
    "F.100S": {"man_to_ele": 19, "25_to_50": 0},
    "F.1500L": {"man_to_ele": 19, "25_to_50": 2230},
    "F.200B": {"man_to_ele": 19, "25_to_50": 450},
    "F.200E": {"man_to_ele": 19, "25_to_50": 570},
    "F.200L": {"man_to_ele": 19, "25_to_50": 240},
    "F.200M": {"man_to_ele": 19, "25_to_50": 240},
    "F.200S": {"man_to_ele": 19, "25_to_50": 310},
    "F.400L": {"man_to_ele": 19, "25_to_50": 520},
    "F.400S": {"man_to_ele": 19, "25_to_50": 750},
    "F.4X100L": {"man_to_ele": 19, "25_to_50": 400},
    "F.4X100S": {"man_to_ele": 19, "25_to_50": 600},
    "F.4X200L": {"man_to_ele": 19, "25_to_50": 960},
    "F.4X50L": {"man_to_ele": 19, "25_to_50": 160},
    "F.4X50S": {"man_to_ele": 19, "25_to_50": 230},
    "F.50B": {"man_to_ele": 29, "25_to_50": 60},
    "F.50E": {"man_to_ele": 29, "25_to_50": 100},
    "F.50L": {"man_to_ele": 29, "25_to_50": 40},
    "F.50M": {"man_to_ele": 29, "25_to_50": 30},
    "F.800L": {"man_to_ele": 19, "25_to_50": 1190},
    "M.100B": {"man_to_ele": 19, "25_to_50": 230},
    "M.100E": {"man_to_ele": 19, "25_to_50": 250},
    "M.100L": {"man_to_ele": 19, "25_to_50": 160},
    "M.100M": {"man_to_ele": 19, "25_to_50": 130},
    "M.100S": {"man_to_ele": 19, "25_to_50": 0},
    "M.1500L": {"man_to_ele": 19, "25_to_50": 2950},
    "M.200B": {"man_to_ele": 19, "25_to_50": 600},
    "M.200E": {"man_to_ele": 19, "25_to_50": 570},
    "M.200L": {"man_to_ele": 19, "25_to_50": 340},
    "M.200M": {"man_to_ele": 19, "25_to_50": 310},
    "M.200S": {"man_to_ele": 19, "25_to_50": 490},
    "M.25M": {"man_to_ele": 0, "25_to_50": 0},
    "M.400L": {"man_to_ele": 19, "25_to_50": 720},
    "M.400S": {"man_to_ele": 19, "25_to_50": 1000},
    "M.4X100L": {"man_to_ele": 19, "25_to_50": 640},
    "M.4X100S": {"man_to_ele": 19, "25_to_50": 770},
    "M.4X200L": {"man_to_ele": 19, "25_to_50": 1360},
    "M.4X50L": {"man_to_ele": 19, "25_to_50": 280},
    "M.4X50S": {"man_to_ele": 19, "25_to_50": 290},
    "M.50B": {"man_to_ele": 29, "25_to_50": 80},
    "M.50E": {"man_to_ele": 29, "25_to_50": 110},
    "M.50L": {"man_to_ele": 29, "25_to_50": 70},
    "M.50M": {"man_to_ele": 29, "25_to_50": 30},
    "M.800L": {"man_to_ele": 19, "25_to_50": 1570},
    "X.4X100L": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X100S": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X200L": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X50L": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X50S": {"man_to_ele": 19, "25_to_50": 0}}

_conversions = {
    "F.100B": {"man_to_ele": 19, "25_to_50": 140},
    "F.100E": {"man_to_ele": 19, "25_to_50": 210},
    "F.100L": {"man_to_ele": 19, "25_to_50": 110},
    "F.100M": {"man_to_ele": 19, "25_to_50": 70},
    "F.100S": {"man_to_ele": 19, "25_to_50": 0},
    "F.1500L": {"man_to_ele": 19, "25_to_50": 2060},
    "F.200B": {"man_to_ele": 19, "25_to_50": 440},
    "F.200E": {"man_to_ele": 19, "25_to_50": 390},
    "F.200L": {"man_to_ele": 19, "25_to_50": 250},
    "F.200M": {"man_to_ele": 19, "25_to_50": 170},
    "F.200S": {"man_to_ele": 19, "25_to_50": 290},
    "F.400L": {"man_to_ele": 19, "25_to_50": 620},
    "F.400S": {"man_to_ele": 19, "25_to_50": 630},
    "F.4X100L": {"man_to_ele": 19, "25_to_50": 440},
    "F.4X100S": {"man_to_ele": 19, "25_to_50": 530},
    "F.4X200L": {"man_to_ele": 19, "25_to_50": 1000},
    "F.4X50L": {"man_to_ele": 19, "25_to_50": 160},
    "F.4X50S": {"man_to_ele": 19, "25_to_50": 210},
    "F.50B": {"man_to_ele": 29, "25_to_50": 50},
    "F.50E": {"man_to_ele": 29, "25_to_50": 90},
    "F.50L": {"man_to_ele": 29, "25_to_50": 40},
    "F.50M": {"man_to_ele": 29, "25_to_50": 30},
    "F.800L": {"man_to_ele": 19, "25_to_50": 1100},
    "M.100B": {"man_to_ele": 19, "25_to_50": 240},
    "M.100E": {"man_to_ele": 19, "25_to_50": 290},
    "M.100L": {"man_to_ele": 19, "25_to_50": 160},
    "M.100M": {"man_to_ele": 19, "25_to_50": 110},
    "M.100S": {"man_to_ele": 19, "25_to_50": 0},
    "M.1500L": {"man_to_ele": 19, "25_to_50": 2350},
    "M.200B": {"man_to_ele": 19, "25_to_50": 540},
    "M.200E": {"man_to_ele": 19, "25_to_50": 550},
    "M.200L": {"man_to_ele": 19, "25_to_50": 350},
    "M.200M": {"man_to_ele": 19, "25_to_50": 290},
    "M.200S": {"man_to_ele": 19, "25_to_50": 370},
    "M.25M": {"man_to_ele": 0, "25_to_50": 0},
    "M.400L": {"man_to_ele": 19, "25_to_50": 670},
    "M.400S": {"man_to_ele": 19, "25_to_50": 880},
    "M.4X100L": {"man_to_ele": 19, "25_to_50": 640},
    "M.4X100S": {"man_to_ele": 19, "25_to_50": 80},
    "M.4X200L": {"man_to_ele": 19, "25_to_50": 1400},
    "M.4X50L": {"man_to_ele": 19, "25_to_50": 240},
    "M.4X50S": {"man_to_ele": 19, "25_to_50": 320},
    "M.50B": {"man_to_ele": 29, "25_to_50": 70},
    "M.50E": {"man_to_ele": 29, "25_to_50": 150},
    "M.50L": {"man_to_ele": 29, "25_to_50": 60},
    "M.50M": {"man_to_ele": 29, "25_to_50": 40},
    "M.800L": {"man_to_ele": 19, "25_to_50": 1290},
    "X.4X100L": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X100S": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X200L": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X50L": {"man_to_ele": 19, "25_to_50": 0},
    "X.4X50S": {"man_to_ele": 19, "25_to_50": 0}}

def from_man_to_ele(gender_id, event_id, mark_hundredth):
    converted = mark_hundredth
    conv_key = "{}.{}".format(gender_id, event_id)
    if conv_key in _conversions:
        converted = converted + _conversions[conv_key]["man_to_ele"]
    return converted


def from_ele_to_man(gender_id, event_id, mark_hundredth):
    converted = mark_hundredth
    conv_key = "{}.{}".format(gender_id, event_id)
    if conv_key in _conversions:
        converted = converted - _conversions[conv_key]["man_to_ele"]
    return converted


def from_25_to_50(gender_id, event_id, mark_hundredth):
    converted = mark_hundredth
    conv_key = "{}.{}".format(gender_id, event_id)
    if conv_key in _conversions:
        converted = converted + _conversions[conv_key]["25_to_50"]
    return converted


def from_50_to_25(gender_id, event_id, mark_hundredth):
    converted = mark_hundredth
    conv_key = "{}.{}".format(gender_id, event_id)
    if conv_key in _conversions:
        converted = converted - _conversions[conv_key]["25_to_50"]
    return converted


def conv_25_man(gender_id, event_id, pool_length, chrono_type, mark_hundredth):
    """ convert a mark_hundredth to 25 man, if input 25 man no conversion
    return a equuated_hundredth """
    converted = mark_hundredth
    conv_key = "{}.{}".format(gender_id, event_id)
    if pool_length == 50:
        if conv_key in _conversions:
            converted = converted - _conversions[conv_key]["25_to_50"]
    if chrono_type == "E":
        if conv_key in _conversions:
            converted = converted - _conversions[conv_key]["man_to_ele"]
    return converted

def conv_man(event_id, chrono_type, mark_hundredth):
    """ convert a mark_hundredth to man chrono, if input is man no conversion
    return a equated_hundredth """
    converted = mark_hundredth
    conv_key = "{}.{}".format('M', event_id)
    if chrono_type == "E":
        if conv_key in _conversions:
            converted = converted - _conversions[conv_key]["man_to_ele"]
    return converted

def conv_to_pool_chrono(mark_hundredth, event_id, gender_id, pool_length,
        chrono_type, to_pool_length=25, to_chrono_type='M'):
    '''
    return mark_hundredth convert to  pool_length and chrono_type
    default: pool: 25, chrono: manual
    '''

    conv_hundredth = mark_hundredth

    if pool_length != to_pool_length:
        if pool_length == 25:
            conv_hundredth = from_25_to_50(
                    gender_id, event_id, conv_hundredth)
        elif pool_length == 50:
            conv_hundredth = from_50_to_25(
                    gender_id, event_id, conv_hundredth)
    if chrono_type != to_chrono_type:
        if chrono_type == 'M':
            conv_hundredth = from_man_to_ele(
                    gender_id, event_id, conv_hundredth)
        elif chrono_type == 'E':
            conv_hundredth = from_ele_to_man(
                    gender_id, event_id, conv_hundredth)

    return conv_hundredth

def exists_conversion(conv_key):
    exists = None
    if conv_key in _conversions:
        exists = True
    return exists
