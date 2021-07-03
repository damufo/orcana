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
        interactor = Interactor()
        interactor.install(self, self.view)
        self.view.set_buttons(has_champ=self.model.champ.champ_id)

    def about(self):
        self.view.about(config=self.model.config)

    def open_db(self):
        self.view.open_db(champ=self.model.champ)
        self.view.set_buttons(has_champ=self.model.champ.champ_id)

    def load_properties(self):
        from modules.properties import p_properties
        p_properties.create(parent=self, champ=self.model.champ)

    def load_categories(self):
        from modules.categories import p_categories
        p_categories.create(parent=self, categories=self.model.champ.categories)

    def load_events(self):
        from modules.events import p_events
        p_events.create(parent=self, events=self.model.champ.events)

    def load_persons(self):
        from modules.persons import p_persons
        p_persons.create(parent=self, persons=self.model.champ.persons)

    def load_per_inscriptions(self):
        from modules.ind_inscriptions import p_ind_inscriptions
        p_ind_inscriptions.create(parent=self, ind_inscriptions=self.model.champ.ind_inscriptions)
    
        # from modules.properties.p_properties import Presenter
        # self.view.panel = Properties(self)
        # self.main_sizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )
        # self.SetSizer(self.main_sizer)
        # self.Layout()

    def open(self):
        pictures = self.model.pictures
        file_path = self.view.msg.open_file(
            default_dir=str(pictures.work_folder),
            suffixes=pictures.suffixes,
            )
        if file_path and file_path.parent != pictures.work_folder:
            pictures.work_folder = file_path.parent
            if file_path.suffix.lower() in pictures.suffixes:
                pictures.path_picture_ini = file_path
            else:
                pictures.path_picture_ini = None
            pictures.load_pictures()
            self.go_picture_ini()

    def save(self):
        current_picture = self.model.pictures.current_picture
        current_picture.save()
        self.view.set_bottom_bar()

    def rename(self):
        current_picture = self.model.pictures.current_picture
        if current_picture.modified:
            message_error = _(
                    'Is not possible rename modified pictures.\n'
                    'Please, save the image first.')
            self.view.msg.error(message=message_error)
        else:
            self.save_as(remove_source=True)

    def save_as(self, remove_source=True):
        current_picture = self.model.pictures.current_picture
        new_file_path = self.view.msg.save_file(
            default_file=str(current_picture.file_name),
            default_dir=str(current_picture.file_path.parent),
            suffixes=current_picture.pictures.suffixes)
        message_error = current_picture.check_new_file_path(new_file_path)
        if message_error:
            self.view.msg.error(message=message_error)
        else:
            old_filepath = current_picture.file_path  
            current_picture.file_path = new_file_path
            current_picture.save()
            if remove_source:
                old_filepath.unlink()
            self.view.set_bottom_bar()

    def delete(self):
        picture = self.view.picture
        if picture:
            result = self.view.msg.question(
                message=_("Are you sure you want to delete the image?"))
            if result:
                if len(self.model.pictures) > 1:
                    if picture.pos == 0:
                        self.go_picture(action='next')
                    else:    
                        self.go_picture(action='prev')
                else:
                    self.view.picture = None
                    self.model.pictures.current_picture = None
                self.model.pictures.delete(picture)
                self.view.load_picture()

    def preferences(self):
        prefs = self.model.pictures.config.prefs
        from modules.prefs import p_prefs
        p_prefs.create(parent=self, prefs=prefs)

    def resize(self):
        current_picture = self.model.pictures.current_picture
        from modules.resize import p_resize
        p_resize.create(parent=self, picture=current_picture)
        if current_picture.resized:
            self.set_factor_to_fit()
            self.view.load_picture()
            current_picture.resized = False
            current_picture.modified = True

    def autoresize(self):
        reload_picture = False
        reload_status_bar = False
        prefs = self.model.pictures.config.prefs
        current_picture = self.model.pictures.current_picture
        max_width = prefs.get_value('prefs.autoresize.max_width')
        max_height = prefs.get_value('prefs.autoresize.max_height')
        pr_ratio = prefs.get_value('prefs.autoresize.pr_ratio')
        auto_save = prefs.get_value('prefs.autoresize.auto_save')
        current_picture.autoresize(
            max_width=max_width,
            max_height=max_height,
            pr_ratio=pr_ratio)
        if current_picture.resized:
            current_picture.resized = False
            self.set_factor_to_fit()
            reload_picture = True
        if auto_save:
            current_picture.save()
            if current_picture.modified == True:
                reload_picture = True            
            else:
                reload_status_bar = True
        if reload_picture:
            self.view.load_picture()
        elif reload_status_bar:
            self.view.set_bottom_bar()

    def rotate(self, angle):
        if angle == 0:
            angle = self.view.msg.entry(
                message=_("Insert an angle:"),
                caption=_("Angle"),
                value='')
            try:
                angle = angle.replace(',', '.')
                angle = float(angle)
            except:
                self.view.msg.error(message=_(
                    "The value is no valid. Please insert\n"
                    "a number (integer or float)."))
                angle = None
        if angle:
            self.model.pictures.current_picture.rotate(angle=angle)
            self.set_factor_to_fit()
            self.view.load_picture()

    def flip(self, method):
        self.model.pictures.current_picture.flip(method=method)
        self.view.load_picture()

    def go_picture_ini(self):
        picture_ini = self.model.pictures.get_picture_ini()
        if picture_ini:
            self.view.picture = picture_ini
            self.set_factor_to_fit()
            self.view.load_picture()
            self.view.set_bottom_bar()
        else:
            self.go_picture(action='next')

    def go_picture(self, action):
        current_picture = self.view.picture
        new_picture = None
        if action:
            if current_picture and current_picture.modified:
                result = self.view.msg.question(
                    message=_("Do you want to save the changes?"))
                if result:
                    current_picture.save()
            new_picture = self.model.pictures.get_picture(action)
            if current_picture != new_picture:
                new_picture.load_from_file()
                self.view.picture = new_picture
        else:
            new_picture = current_picture
        if new_picture:
            new_picture.factor = None
            self.set_factor_to_fit()
            self.view.load_picture()
            self.view.set_bottom_bar()

    def set_zoom(self, action):
        size_to_fit = None
        current_picture = self.model.pictures.current_picture
        current_factor = current_picture.factor
        if action == 'fit':
            size_to_fit = self.view.get_picture_frame_size()
        current_picture.set_factor(action=action, size_to_fit=size_to_fit)
        new_factor = current_picture.factor
        if current_factor != new_factor:
            self.view.load_picture()

    def set_factor_to_fit(self):
        current_picture = self.model.pictures.current_picture
        current_factor = current_picture.factor
        size_to_fit = self.view.get_picture_frame_size()
        current_picture.set_factor(action='fit', size_to_fit=size_to_fit)

    def crop_picture(self, rectangle):
        self.model.pictures.current_picture.crop(rectangle)
        self.set_factor_to_fit()
        self.view.load_picture()

    def show_fullscreen(self):
        if self.model.pictures.config.platform == 'lin':
            self.view.SetTransparent(0)
            new_value = not self.view.IsFullScreen()
            if new_value:
                self.model.pictures.fit_limit = False
                self.view.lbl_properties.Hide()
            else:
                self.model.pictures.fit_limit = True
                self.view.lbl_properties.Show()
            self.view.ShowFullScreen(new_value)
            self.view.force_fit = True
            self.view.on_size_enabled = False
        else:
            new_value = not self.view.IsFullScreen()
            if new_value:
                self.model.pictures.fit_limit = False
                self.view.lbl_properties.Hide()
            else:
                self.model.pictures.fit_limit = True
                self.view.lbl_properties.Show()
            self.view.ShowFullScreen(new_value)
            self.set_factor_to_fit()
            self.view.load_picture()
