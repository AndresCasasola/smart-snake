# -*- mode: python -*-

block_cipher = None

added_files = [
     ( 'sounds', 'sounds' ),
     ( 'images', 'images' ),
     ( 'fonts', 'fonts' )
     ]

a = Analysis(['snake_main.py'],
             pathex=['C:\\Users\\nos12\\Desktop\\pygame'],
             binaries=[],
             datas=added_files ,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='snake_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
