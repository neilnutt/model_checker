# -*- mode: python -*-
a = Analysis(['pyinstaller.py'],
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
          name='pyinstaller.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
