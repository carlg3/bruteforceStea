# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['bruteforceStea.py'],
             pathex=['C:\\Users\\gbert\\OneDrive - University of Pisa\\Altro\\Programmi\\bruteforceStea\\test_bruteforceStea (v.1.0.2)-20201101T203753Z-001\\test_bruteforceStea (v.1.0.2)\\v1.1.0'],
             binaries=[],
             datas=[],
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
          name='bruteforceStea',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Giovanni_Stea.ico')
