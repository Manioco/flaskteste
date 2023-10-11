# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['open_port_checker.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['asgiref', 'bcrypt', 'cffi', 'click', 'colorama', 'dnspython', 'email-validator', 'Flask', 'Flask_Bcrypt', 'Flask_Login', 'Flask_SQLAlchemy', 'Flask_WTF', 'greenlet', 'idna', 'importlib_metadata', 'itsdangerous', 'Jinja2', 'MarkupSafe', 'pycparser', 'six', 'SQLAlchemy', 'sqlparse', 'typing_extensions', 'Werkzeug', 'WTForms', 'zipp'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='meu_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
