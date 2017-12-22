# -*- mode: python -*-

block_cipher = None


a = Analysis(['mygame.py'],
             pathex=['C:\\Users\\aa\\Desktop\\조윤영\\대학교\\2-2\\2DGP\\DinoMelt'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mygame',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
