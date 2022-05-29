
# Contorno virtual

```$ python -m venv .venv
$ source .venv/bin/activate```

## Requirements linux 2022-0529

```numpy==1.20.3
Pillow==8.2.0
reportlab==3.6.9
six==1.16.0
wxPython==4.1.1```

## Empaquetado

```
(.venv) $ echo "wxPython==4.1.1" > requirements.in
(.venv) $ echo "reportlab" >> requirements.in
(.venv) $ python -m pip install pip-tools
(.venv) $ python -m pip-compile
(.venv) $ cat requirements.txt
```
Para actualizar unha dependencia á versión actual

```
(.venv) $ pip-compile -P wxPython
```

Pon o noso contorno ó día


```
(.venv) $ pip-sync
```

