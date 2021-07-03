# -*- coding: utf-8 -*-


import os
from pathlib import Path
from PIL import Image
from PIL import JpegImagePlugin as JIP
import wx
from specific_functions import utils

class Picture(object):

    def __init__(self, pictures, file_path):
        self.pictures = pictures
        self.file_path = file_path
        self._image = None
        self._image_pil = None
        self.size_bytes = 0
        self.modified = False
        self.resized = False
        self.factor = 100
        self.view_width = 0
        self.view_height = 0

    @property
    def config(self):
        return self.pictures.config

    @property
    def file_folder(self):
        return self.file_path.parent

    @property
    def file_name(self):
        return self.file_path.name

    @property
    def file_suffix(self):
        return self.file_path.suffix

    def check_new_file_path(self, new_file_path):
        message_error = ''
        if not new_file_path:
            message_error = _(
                    'Please, set a file name.') 
        else:
            name = new_file_path.stem
            suffix = new_file_path.suffix
            if not utils.get_valid_filename(name):
                message_error = _(
                    'Please, set a valid file name.\n'
                    'Example: picture.jpg.')
            elif suffix not in self.pictures.suffixes:
                message_error = _(
                    'The {} suffix is not supported.\n'
                    'Valid suffixes are: {}.').format(
                        suffix,
                        ', '.join(self.pictures.suffixes))
            elif new_file_path == self.file_path:
                message_error = _(
                    'The new filename is same.')
            elif new_file_path.exists():
                message_error = _(
                    'Already exists a file with this name.\n'
                    'Please, set another file name.')
        return message_error

    @property
    def width(self):
        return self.image_pil.width

    @property
    def height(self):
        return self.image_pil.height

    def _set_image_pil(self, value):
        self._image_pil = value

    def _get_image_pil(self):
        if not self._image_pil:
            self.load_from_file()
        return self._image_pil
    image_pil = property(_get_image_pil, _set_image_pil)

    def load_from_file(self):
        try:
            self._image_pil = Image.open(self.file_path).convert("RGB")
            self.size_bytes = os.stat(self.file_path).st_size
        except:
            mode = 'RGB'
            size = (640, 480)
            color = (0, 0, 0)
            self._image_pil = Image.new(mode, size, color)
        self.modified = False

    @property
    def bitmap(self):
        width, height = self.view_width, self.view_height
        if width:
            if width == self.image_pil.size[0]:
                height = self.image_pil.size[1]
            else:
                height = int(((width)/self.image_pil.size[0])*self.image_pil.size[1])
        elif height:
            if height == self.image_pil.size[1]:
                width = self.image_pil.size[0]
            else:
                width = int(((height)/self.image_pil.size[1])*self.image_pil.size[0])
        size = (width, height)
        img = self.image_pil.resize(size, Image.ANTIALIAS)
        bitmap = wx.Bitmap.FromBuffer(width, height, img.tobytes())
        return bitmap

    def crop(self, rectangle):
        if self.factor != 100:
            factor_h = self.factor/100
            rectangle = (
                int(rectangle[0]/factor_h),
                int(rectangle[1]/factor_h),
                int(rectangle[2]/factor_h),
                int(rectangle[3]/factor_h),
                )
        self.image_pil = self.image_pil.crop(rectangle)
        self.modified = True

    def rotate(self, angle=90):
        self.image_pil = self.image_pil.rotate(-angle, expand=1)
        self.modified = True

    def flip(self, method):
        if method == 'horizontally':
            method = Image.FLIP_LEFT_RIGHT
        elif method == 'vertically':
            method = Image.FLIP_TOP_BOTTOM
        self.image_pil = self.image_pil.transpose(method=method)
        self.modified = True

    def set_factor(self, action, size_to_fit=None):
        '''
        size is a tuple (width, height) for fit to window
        '''
        new_factor = self.factor
        self.view_width = 0
        self.view_height = 0
        if action == 'fit':
            width, height = size_to_fit
            new_factor_width =  (width*100)/self.image_pil.width
            new_factor_height = (height*100)/self.image_pil.height
            if new_factor_width < new_factor_height:
                new_factor = new_factor_width
                self.view_width = width
            else:
                new_factor = new_factor_height
                self.view_height = height
            fit_limit = self.pictures.fit_limit
            if fit_limit and new_factor > 100:
                new_factor = 100
                self.view_width = self.image_pil.width
        else:
            if action == 'in':
                new_factor += 20
                if new_factor > 200:
                    new_factor = 200
            elif action == 'out':
                new_factor -= 20
                if new_factor < 20:
                    new_factor = 20
            elif action == '100':
                new_factor = 100
            elif action == '200':
                new_factor = 200
            self.view_width = int(self.image_pil.size[0]*(new_factor/100))
        self.factor = new_factor

    @property
    def size_px(self):
        return "{}x{}".format(self.image_pil.width, self.image_pil.height)
    
    @property
    def pos(self):
        pos_self = 0
        for pos, item in enumerate(self.pictures):
            if self == item:
                pos_self = pos
                break
        return pos_self

    def autoresize(self, max_width, max_height, pr_ratio):
        '''
        max_width and max_height in px
        pr_ratio -> preserve aspect ratio
        '''
        width = 0
        height = 0
        if pr_ratio:
            new_height = 0
            new_width = 0
            if max_width and (max_width < self.width):
                width = max_width
                factor = max_width / self.width
                new_height = int(self.height * factor)
                if (new_height > 0 and (not max_height or
                        (max_height and new_height < max_height))):
                    height = new_height
            if not height and max_height and (max_height < self.height):
                height = max_height
                width = 0
                factor = max_height / self.height
                new_width = int(self.width * factor)
                if (new_width > 0 and (not max_width or
                        (max_width and new_width < max_width))):
                    width = new_width
        self.resize(width=width, height=height)

    def resize(self, width, height):
        if width and height:
            self.image_pil = self.image_pil.resize((width, height))
            self.resized = True
            self.modified = True

    def save(self):
        if self.file_suffix.lower() in ('.jpg', '.jpeg'):
            prefs = self.config.prefs
            quality = prefs.get_value('prefs.jpg.quality')
            optimize = prefs.get_value('prefs.jpg.optimize')
            progresive = prefs.get_value('prefs.jpg.progressive')
            subsampling = JIP.get_sampling(self.image_pil)
            self.image_pil.save(
                self.file_path,
                quality=quality,
                subsampling=subsampling,
                opatimize=optimize,
                comment=_("Saved from Encadra Image Viewer."))
        else:
            self.image_pil.save(self.file_path)
        
        self.load_from_file()
        self.modified = False

    @property
    def size_bytes_h(self):
        return utils.size_bytes_h(num=self.size_bytes, suffix='B')
