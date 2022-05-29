# -*- coding: utf-8 -*-


# from specific_classes.pictures import Pictures
# from specific_classes.champ.champ import Champ

class Model(object):

    def __init__(self, champ):
        self.config = champ.config
        self.champ = champ
        if 'last_path_dbs' in self.config.prefs and self.config.prefs['last_path_dbs']:
            champ.load_dbs(dbs_path=self.config.prefs['last_path_dbs'])
        # self.config.dbs.connect(dbs_path='/home/damufo/escritorio/20210619_festival_galego_promesas_rias_do_sur.sqlite')
        # if self.config.dbs.connection:
        #     self.champ = Champ(config=config)
        # else:
        #     self.champ = None
