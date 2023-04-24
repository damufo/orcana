#!/bin/bash

cd /home/damufo/dev/orcana/
source /home/damufo/dev/orcana/.venv/bin/activate
pyinstaller orcana_pyinstaller_linux.spec --workpath=./build_lin --distpath=./dist_lin 

exit 0
