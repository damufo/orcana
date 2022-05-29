# -*- coding: utf-8 -*- 


class Choice():
    
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Choices(list):

    def __init__(self, choices):
        """
        choices is a tuple of tuples (id, name)
        Example: ((25, '25'), (50, '50'),
            )
        """
        for i in choices:
            self.append(Choice(
                    id = i[0],
                    name = i[1]
                    ))

    def choices(self, add_empty=False):
        '''
        return values for wxchoice with ClientData
        '''
        values = []
        if add_empty:
            values.append(('', '')) 
        for i in self:
            values.append((i.name, i.id))
        return values



