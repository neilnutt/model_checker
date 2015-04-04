# -*- mode: python -*-
a = Analysis(['check_routines.py'],
             pathex=['C:\\Users\\nut67271\\workspace\\model_checker'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='check_routines.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
