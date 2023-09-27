# -*- coding: utf-8 -*- 


import locale
locale.setlocale(locale.LC_ALL, "")

def get_float(value):
    if isinstance(value, str):
        value = value.replace(',', '.')
        try:
            value = float(value)
        except:
            value = 0.0
    elif not isinstance(value, float):
        value = 0.0
    return value

def get_str(value, decimals=2):
    '''
    value is a float
    return a string formated
    '''
    mask = '%.{}f'.format(decimals)
    return locale.format_string(mask, value)
