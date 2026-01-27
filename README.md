# Orcana

A pool swimming championship management application.


## Actualizado de pip

```$ python -m pip install --upgrade pip```
## Contorno virtual

```$ python -m venv .venv
$ source .venv/bin/activate```

### Requirements linux 2022-05-29

```numpy==1.20.3
Pillow==8.2.0
reportlab==3.6.9
six==1.16.0
wxPython==4.1.1```

### Requiriments python 3.13 (tested on windows 11 2026-01-27)
```
python -m pip install --upgrade pip
python -m venv .venv
.venv/Scripts/activate
pip install requests
pip install wxpython
pip installreportlab
pip installlegacy-cgi
pip installnumpy
```

### Empaquetado windows
```
.venv/Scripts/activate
pip install pyinstaller
pyinstaller orcana_pyinstaller_win_mac.spec --workpath=./build_win --distpath=./dist_win
```

