# -*- coding: utf-8 -*- 


from specific_classes.champ.param import Param


class Params(dict):

    def __init__(self, champ):
        self.champ = champ
        self.config = champ.config
        self.changed = []
        
    def load_items_from_dbs(self):
        '''
        load values
        '''
        self.clear() #borra os elementos que haxa
        # valid value types: int, str
        sql = ''' select name, value, type from params '''
        (NAME, VALUE, TYPE_) = range(3)
        res = self.config.dbs.exec_sql(sql=sql)
        for i in res:
            name = i[NAME]
            type_ = i[TYPE_]
            if type_ == 'int':
                value = int(i[VALUE])
            elif type_ == 'str':
                value = str(i[VALUE])
            self[name] = value
    
    def get_value(self, name): 
        return self[name]

    def set_value(self, name, value):
        if self[name] != value:  # changed
            self[name] = value
            if name not in self.changed:
                self.changed.append(name)
    

    def save(self):
        sql = '''
update params set value=? where name=?'''
        for name in self.changed:
            print('Save param\n - name: {}\n - value: {}'.format(name, self[name]))
            values = (( self[name], name), )
            self.config.dbs.exec_sql(sql=sql, values=values)
        self.changed.clear()
        

    # def get_style(self, style_id):
    #     style = None
    #     for i in self:
    #         if i.style_id == style_id:
    #             style = i
    #             break
    #     return style 
            
    # def choices(self, add_empty=False):
    #     '''
    #     return values for wxchoice with ClientData
    #     '''
    #     values = []
    #     if add_empty:
    #         values.append(('',  '')) 
    #     for i in self:
    #         values.append((i.style_id, i.long_name))
    #     return values



