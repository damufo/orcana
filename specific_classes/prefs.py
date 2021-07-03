# -*- coding: utf-8 -*-


import codecs
import json


DEFAULT_PREFS = {
            'general.lsc_font_size': '',
            }


class Prefs(dict):

    def __init__(self, config_app_dir_path, file_name='settings.json'):
        self.file_path = config_app_dir_path.joinpath(file_name)

    def get_value(self, key):
        if key in self:
            value = self[key]
        elif key in DEFAULT_PREFS:
            value = DEFAULT_PREFS[key]
        else:
            value = None
        return value

    def set_value(self, key, value):
        self[key] = value

    def set_defaults(self):
        self.values = DEFAULT_PREFS
        self.save()

    def load(self):
        try:
            file_settings = codecs.open(self.file_path, 'r', 'utf-8')
        except IOError:
            self.save()
            file_settings = codecs.open(self.file_path, 'r', 'utf-8')
        try:
            settings_file_values = json.loads(file_settings.read())
            self.update(settings_file_values)
        except ValueError:
            self.set_defaults()
        file_settings.close()

    def save(self):
        file_settings = codecs.open(self.file_path, 'w', 'utf-8')
        file_settings.write(json.dumps(self, indent=4, sort_keys=True))
        file_settings.close()

    def save_clean(self):
        cleaned = {}
        for key in DEFAULT_PREFS:
            if key in self:
               cleaned[key] = self[key]
            else:
               cleaned[key] = DEFAULT_PREFS[key]
        self.clear()
        self.update(cleaned)
        file_settings = codecs.open(CONFIG_APP_FILE_PATH, 'w', 'utf-8')
        file_settings.write(json.dumps(self, indent=4, sort_keys=True))
        file_settings.close()

    def __str__(self):
        ans = ''
        for key in sorted(self.keys()):
            ans += '{0}: {1}\n'.format(key, self[key])
        return ans
