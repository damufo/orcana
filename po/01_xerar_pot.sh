#!/bin/bash

xgettext --language=Python --from-code=UTF-8 --keyword=_ --output=orcana.pot `find /home/damufo/dev/orcana/ ! -path "*/.venv/*" -name "*.py"`

exit 0


