# -*- mode: python -*-


block_cipher = None

added_files = [
    ('./images', 'images'),
    ('./fonts', 'fonts'),
    ('./locale', 'locale')]

a = Analysis(['orcana.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=['PIL._tkinter_finder'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False,)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          # contents_directory='.', con isto pon todo no cartafol do executable
          exclude_binaries=True,
          name='orcana',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='orcana.ico')

coll = COLLECT(exe,
               a.binaries,
               a.datas,
               strip=False,
               upx=True,
               name='orcana')
