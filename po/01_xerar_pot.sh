#!/bin/bash

xgettext --language=Python --from-code=UTF-8 --keyword=_ --output=messages.pot `find /home/damufo/dev/orcana/ -name "*.py"`

exit 0


