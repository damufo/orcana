# -*- coding: utf-8 -*-


from modules.main.m_main import Model
from modules.main.v_main import MainFrame, View
from modules.main.i_main import Interactor


class Presenter(object):

    def __init__(self, champ):
        self.model = Model(champ)
        self.main_frame = MainFrame()
        # self.view.config = config
        self.main_frame.SetTitle(self.model.champ.name or 'Orcana')
        # self.main_frame.SetTitle('Orcana')
        # self.model.champ.entities.load_items_from_dbs()
        # interactor = Interactor()
        # interactor.install(self, self.view)
        # self.model.pictures.set_paths(config.arg1)
        # self.model.pictures.load_pictures()
        self.load_me()
        self.view.parent.view_plus.start()

    def load_me(self):
        self.view = View(self.main_frame)
        self.view.SetName('main')
        interactor = Interactor()
        interactor.install(self, self.view)
        self.view.set_buttons(has_champ=self.model.champ.champ_id)

    def about(self):
        self.view.about(config=self.model.config)

    def open_db(self):
        self.view.open_db(champ=self.model.champ)
        self.view.set_buttons(has_champ=self.model.champ.champ_id)

    def report_results(self):
        self.model.champ.report_results()

    def export_results(self):
        self.model.champ.export_results()

    def load_properties(self):
        from modules.properties import p_properties
        p_properties.create(parent=self, champ=self.model.champ)

    def load_entities(self):
        from modules.entities import p_entities
        p_entities.create(parent=self, entities=self.model.champ.entities)

    def load_categories(self):
        from modules.categories import p_categories
        p_categories.create(parent=self, categories=self.model.champ.categories)

    def load_events(self):
        from modules.events import p_events
        p_events.create(parent=self, events=self.model.champ.events)

    def load_persons(self):
        from modules.persons import p_persons
        p_persons.create(parent=self, persons=self.model.champ.persons)

    def load_inscriptions(self):
        from modules.inscriptions import p_inscriptions
        p_inscriptions.create(parent=self, champ=self.model.champ)

    def load_heats(self):
        if not self.model.champ.heats:
            self.view.msg.warning(message=_('No heats in this championship.'))
        else:
            from modules.heats import p_heats
            p_heats.create(parent=self, heats=self.model.champ.heats)

    def load_result_members(self, parent, result_members=None):
        if not result_members:
            result_members = self.model.config.views['result_members']['result_members']
        from modules.result_members import p_result_members
        p_result_members.create(parent=parent, result_members=result_members)

    def load_results(self):
        from modules.results import p_results
        p_results.create(parent=self, champ=self.model.champ)
    
        # from modules.properties.p_properties import Presenter
        # self.view.panel = Properties(self)
        # self.main_sizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
        # self.SetSizer(self.main_sizer)
        # self.Layout()

    # def open(self):
    #     pictures = self.model.pictures
    #     file_path = self.view.msg.open_file(
    #         default_dir=str(pictures.work_folder),
    #         suffixes=pictures.suffixes,
    #         )
    #     if file_path and file_path.parent != pictures.work_folder:
    #         pictures.work_folder = file_path.parent
    #         if file_path.suffix.lower() in pictures.suffixes:
    #             pictures.path_picture_ini = file_path
    #         else:
    #             pictures.path_picture_ini = None
    #         pictures.load_pictures()
    #         self.go_picture_ini()

    # def save(self):
    #     current_picture = self.model.pictures.current_picture
    #     current_picture.save()
    #     self.view.set_bottom_bar()


    # def save_as(self, remove_source=True):
    #     current_picture = self.model.pictures.current_picture
    #     new_file_path = self.view.msg.save_file(
    #         default_file=str(current_picture.file_name),
    #         default_dir=str(current_picture.file_path.parent),
    #         suffixes=current_picture.pictures.suffixes)
    #     message_error = current_picture.check_new_file_path(new_file_path)
    #     if message_error:
    #         self.view.msg.error(message=message_error)
    #     else:
    #         old_filepath = current_picture.file_path  
    #         current_picture.file_path = new_file_path
    #         current_picture.save()
    #         if remove_source:
    #             old_filepath.unlink()
    #         self.view.set_bottom_bar()



    def preferences(self):
        prefs = self.model.pictures.config.prefs
        from modules.prefs import p_prefs
        p_prefs.create(parent=self, prefs=prefs)

