# -*- coding: utf-8 -*- 


class Param(object):

    def __init__(self, **kwargs):
        self.value_ = kwargs['value']
        self.param_type = kwargs['param_type']  # [int|str]
        self.changed = False

    def __str__(self):
        return self.value

    @property
    def _set_value(self, string_value):
        if self.value_ and string_value != self.value_:
            self.changed = True
        self.value_ = string_value

    def _get_value(self):
        return self.value_

    value = property(fget=_get_value,
                               fset=_set_value)