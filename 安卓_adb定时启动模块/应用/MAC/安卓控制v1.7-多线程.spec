# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/jinjiangshan/Desktop/py/Leiteng_/安卓_adb定时启动模块/安卓控制v1.7-多线程.py'],
    pathex=[],
    binaries=[],
    datas=[('/opt/homebrew/bin/adb', './adb/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='安卓控制v1.7-多线程',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='安卓控制v1.7-多线程',
)
app = BUNDLE(
    coll,
    name='安卓控制v1.7-多线程.app',
    icon=None,
    bundle_identifier=None,
)
