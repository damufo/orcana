# -*- coding: utf-8 -*-


from pathlib import Path
from specific_classes.picture import Picture


class Pictures(list):

    def __init__(self, config):
        self.config = config
        self.current_picture = None
        self.path_picture_ini = None
        self.work_folder = None
        self.suffixes = ('.jpg', '.jpeg', '.png', '.bmp')
        self.fit_limit = True  # Limit fit to 100%

    def set_paths(self, arg1):
        if not arg1:
            self.work_folder = Path.home()
        else:
            arg1 = Path(arg1)
            if arg1.is_file() and arg1.exists():
                if arg1.suffix.lower() in self.suffixes:
                    self.path_picture_ini = arg1
                self.work_folder = arg1.parent
            elif arg1.is_dir() and arg1.exists():
                self.work_folder = arg1
            else:
                self.work_folder = Path.home()
    
    def load_pictures(self):
        del self[:]
        for i in sorted(self.work_folder.iterdir()):
            if i.suffix.lower() in self.suffixes:
                self.append(Picture(pictures=self, file_path=i))

    def delete(self, picture):
        picture.file_path.unlink(missing_ok=True)
        del self[picture.pos]

    def update_path_current_picture(self, file_path):
        cur_pic = self.current_picture
        same_folder = False
        if cur_pic:
            new_path = Path(file_path)
            if cur_pic.file_path.parent == new_path.parent:
                same_folder = True
            cur_pic.file_path = Path(file_path)
            if same_folder:
                # Check if rewrite exists item
                for i in self:
                    if str(i.file_path) == str(cur_pic.file_path) and i != cur_pic:
                        del self[i.pos]
                        break

    def get_picture(self, action):
        if self:
            if not self.current_picture:
                self.current_picture = self[0]
            elif action == 'first':
                self.current_picture = self[0]
            elif action == 'last':
                self.current_picture = self[-1]
            elif len(self) > 1:
                current_pos = self.current_picture.pos
                if action == 'next':
                    if current_pos + 1 == len(self):
                        self.current_picture = self[0]
                    else:
                        self.current_picture = self[current_pos + 1]
                elif action == 'prev':
                    if current_pos - 1 < 0:
                        self.current_picture = self[-1]
                    else:
                        self.current_picture = self[current_pos - 1]
        else:
            self.current_picture = None
        return self.current_picture

    def get_picture_ini(self):
        if self.path_picture_ini:
            for picture in self:
                if picture.file_path == self.path_picture_ini:
                    picture_ini = picture
                    self.current_picture = picture
                    break
        return self.current_picture
