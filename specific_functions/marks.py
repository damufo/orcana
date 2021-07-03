# -*- coding: utf-8 -*-


values = (
    ':34',  # error
    '000044',  # error
    '000000',  # error
    '106.44',  # error
    '106.4',  # error
    '1:06.44',  # 1:06.44
    '1:6.44',  # 1:06.44
    '1:6.4',  # 1:06.40
    '16.44',  # 16.44
    '16:44',  # 16.44
    '16.4',  # 16.40
    '16.',  # 16.40
    ':16: ',  # 16.40
    '16: ',  # 16.40
    '.16: ',  # 16.40
    '34.15',  # 34.15
    '3415',  # 34.15
    '1:30:44',  # isto non se debería permitir e no caso de facelo tería qeu ser 1:30:44.00
    '13044',  # 1:30.44
    '1:60.44',  # error
    'A1b:6.44', # error
    '00:00.44', # error por ser inferior
    '00:10.4', # 10.44
    '59:00.44',  # 59:00.44
    '0:59:00.44',  # 59:00:44
    '23:59:59.99',  # 23:59:59.99 
    '10.00',  # 10.00
    '12:34:15',  # error por los : como separador de centésimas.
    '123415',  # 12:34.15
    '2:01:23.56',  # 2:01:23.56
    '2012356',  # 2:01:23.56
    '23:01:23.56',  # 23:01:23.56
    '23:01:23:56',  # esto pasa a 23:01:23:56.00 polo que error, valor máximo 23:59:59.99
    '25:01:23.56',  # error, el valor máximo es 23:59:59.99
    '25012356',  # error, el valor máximo es 23:59:59.99
    )




def validate(value):
    '''
    value is a mark string
    return hundredths
    '''
    hundredths = 0
    tempo_formatado = ''
    value = value.strip()
    error = ''
    partes = []
    if value.isdigit():  # valida introdución formato numerico
        digits = value
        len_digits = len(digits)
        if len_digits == 4:
            partes = [digits[-2:], digits[-4:-2]]
        elif len_digits in (5, 6):
            partes = [digits[-2:], digits[-4:-2], digits[-6:-4]]
        elif len_digits in (7, 8):
            partes = [digits[-2:], digits[-4:-2], digits[-6:-4], digits[-8:-6]]
        else:
            partes = []
            error = 'Exceeded the maximum number of digits.'
    else:  # valida formato con puntuación
        # busca a última puntuación e separa
        for pos in range((len(value)-1), -1, -1):
            if value[pos] in ('.',','):
                partes = value.split(value[pos])
                for x, i in enumerate(partes):  # repair void
                    if not i:
                        partes[x] = '00'
                if len(partes) > 2:
                    error = 'value mal formed'
                    partes = []
                else:
                    partes = partes[0].split(":") + [partes[1], ]
                    break
            elif value[pos] == ':':
                partes = value.split(":")
                for x, i in enumerate(partes):  # repair void
                    if not i:
                        partes[x] = '00'
                partes.append('00')
                break
        if len(partes) in (2, 3, 4): 
            partes = partes[::-1]  # reverse
            for x, i in enumerate(partes):
                if i.isdigit():
                    if len(i) == 1:
                        if x == 0:
                            partes[x] = '%s0' % i
                        else:
                            partes[x] = '0%s' % i
                else:
                    partes = []
                    error = 'ilegal characters'
                    break
        else:
            error = 'value mal formed'
            partes = []
    # print(partes[::-1])
    while len(partes) > 1 and int(partes[-1]) == 0:
        partes.pop()
    
    
    if len(partes) in (2, 3, 4):
        # check partes ranges 
        for x, i in enumerate(partes):
            if x == 0:
                if int(i) > 99:
                    error = 'value out range'
                    break
                else:
                    hundredths += int(i)
            elif x == 1:
                if int(i) > 59:
                    error = 'value out range'
                    hundredths = 0
                    break
                else:
                    hundredths += int(i) * 100
            elif x == 2:
                if int(i) > 59:
                    error = 'value out range'
                    hundredths = 0
                    break
                else:
                    hundredths += int(i) * 6000
            elif x == 3:
                if int(i) > 23:
                    error = 'value out range'
                    hundredths = 0
                    break
                else:
                    hundredths += int(i) * 360000
        if hundredths:
            tempo_formatado = partes[::-1]
            tempo_formatado[0] = str(int(tempo_formatado[0]))  # quita o cero incial
            tempo_formatado = ':'.join(tempo_formatado)
            tempo_formatado = tempo_formatado[::-1].replace(':', ',', 1)[::-1]
            
    print('{} -> {} -> {}  {}'.format(value, tempo_formatado, hundredths, error))
    return hundredths 

# for value in values:
#     validate(value)

def hun2mark(value, zero_fill=False, force_hours=False):
    """
    Convert a hundredths (integer) to mark (text)
    """
    time_text = ''

    if  isinstance(value, int):
        adjust = 100
        hundreds = value % 100
        seconds = int(value / adjust) % 60
        minutes = int((value / (60 * adjust)) % 60)
        hours = int((value / (3600 * adjust)))
        result = '0'
#            hours
        if hours:
            result = str(hours)
        elif force_hours:
            result = "00"

#            minutes
        if result != '0':
            result = '%s:%s' % (result, str(minutes).zfill(2))
        else:
            result = str(minutes)

        if result != '0':  # seconds
            result = '%s:%s' % (result, str(seconds).zfill(2))
        else:
            result = str(seconds)

        if result != '0':
            result = '%s.%s' % (result, str(hundreds).zfill(2))
        else:
            result = str(hundreds)
        if result:
            time_text = result

    return time_text

def mark2hun(value, precision='hun'):
    """
    convert a mark (string) to hundreths (integer)
    value is a string
    mark format examples:
        HH:MM:SS.ss (ss=hundredths)
        H:MM:SS.ss (ss=hundredths)
        MM:SS.ss (ss=hundredths)
        M:SS.ss (ss=hundredths)
        SS.ss (ss=hundredths)
    """
    result = 0
    adjust = 100

    value = value.strip().replace('.', ':').replace(',', ':')
    time_splits = value.split(":")

    if len(time_splits) == 1:
        result = int(time_splits[0])
    elif len(time_splits) == 2:
        result = (int(time_splits[0]) * adjust) + int(time_splits[1])
    elif len(time_splits) == 3:
        result = (
            (int(time_splits[0]) * (60 * adjust)) +
            (int(time_splits[1]) * adjust) + int(time_splits[2])
            )
    elif len(time_splits) == 4:
        result = (
            (int(time_splits[0]) * (3600 * adjust)) +
            (int(time_splits[1]) * (60 * adjust)) +
            (int(time_splits[2]) * adjust) +
            int(time_splits[3])
            )

    return result