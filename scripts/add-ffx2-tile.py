#!/usr/bin/env python3
"""Add a "FINAL FANTASY X-2" non-Steam shortcut that runs ~/.local/bin/ffx2-play.

Steam rewrites shortcuts.vdf while it runs, so Steam must be fully stopped
(on SteamOS-style sessions: `systemctl --user stop steam-launcher.service`).
A timestamped backup of shortcuts.vdf is written next to it.

Usage: add-ffx2-tile.py [--steam-user ID]
"""
import argparse, glob, os, shutil, struct, subprocess, sys, time, zlib

NAME = 'FINAL FANTASY X-2'
EXE = '"%s"' % os.path.expanduser('~/.local/bin/ffx2-play')
START_DIR = '"%s/"' % os.path.expanduser('~/.local/bin')
STEAM = os.path.expanduser('~/.local/share/Steam')

def steam_running():
    out = subprocess.run(['ps', '-eo', 'args'], capture_output=True, text=True).stdout
    return any(l.startswith(os.path.join(STEAM, 'steamrt64/steam ')) or l.startswith(os.path.join(STEAM, 'ubuntu12_32/steam '))
               for l in out.splitlines())

def parse(d):
    i = 0
    def rs():
        nonlocal i
        j = d.index(b'\0', i); s = d[i:j].decode(); i = j + 1; return s
    def rm():
        nonlocal i
        m = []
        while True:
            t = d[i]; i += 1
            if t == 8: return m
            k = rs()
            if t == 0: m.append((k, 0, rm()))
            elif t == 1: m.append((k, 1, rs()))
            elif t == 2: m.append((k, 2, struct.unpack_from('<i', d, i)[0])); i += 4
            else: raise ValueError(f'unsupported VDF type {t}')
    return rm()

def dump(m):
    out = b''
    for k, t, v in m:
        out += bytes([t]) + k.encode() + b'\0'
        out += wm(v) if t == 0 else v.encode() + b'\0' if t == 1 else struct.pack('<i', v)
    return out

def wm(m):
    return dump(m) + b'\x08'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--steam-user', help='Steam userdata folder (numeric) if there is more than one')
    args = ap.parse_args()

    if steam_running():
        sys.exit('Steam is running; stop it first (systemctl --user stop steam-launcher.service).')
    users = [os.path.basename(p) for p in glob.glob(os.path.join(STEAM, 'userdata', '[0-9]*'))]
    if args.steam_user:
        users = [args.steam_user]
    if len(users) != 1:
        sys.exit(f'Found Steam users {users}; pass --steam-user with the right one.')
    cfg = os.path.join(STEAM, 'userdata', users[0], 'config')
    path = os.path.join(cfg, 'shortcuts.vdf')

    if os.path.exists(path):
        root = parse(open(path, 'rb').read())
        shutil.copy2(path, f'{path}.bak-{time.strftime("%Y%m%d-%H%M%S")}')
    else:
        os.makedirs(cfg, exist_ok=True)
        root = [('shortcuts', 0, [])]
    shortcuts = root[0][2]
    if any(dict((k, v) for k, _, v in e[2]).get('AppName') == NAME for e in shortcuts):
        sys.exit(f'"{NAME}" already exists; nothing changed.')

    appid = zlib.crc32((EXE + NAME).encode()) | 0x80000000
    entry = [
        ('appid', 2, struct.unpack('<i', struct.pack('<I', appid))[0]), ('AppName', 1, NAME),
        ('Exe', 1, EXE), ('StartDir', 1, START_DIR), ('icon', 1, ''), ('ShortcutPath', 1, ''),
        ('LaunchOptions', 1, ''), ('IsHidden', 2, 0), ('AllowDesktopConfig', 2, 1), ('AllowOverlay', 2, 1),
        ('OpenVR', 2, 0), ('Devkit', 2, 0), ('DevkitGameID', 1, ''), ('DevkitOverrideAppID', 2, 0),
        ('LastPlayTime', 2, 0), ('FlatpakAppID', 1, ''), ('sortas', 1, ''), ('tags', 0, []),
    ]
    shortcuts.append((str(len(shortcuts)), 0, entry))
    open(path, 'wb').write(wm(root))
    print(f'Added "{NAME}" (shortcut id {appid}) to {path}')
    print(f'Custom art goes in {cfg}/grid/ as {appid}p.png (cover), {appid}_hero.png, {appid}_logo.png, {appid}.png (wide)')

if __name__ == '__main__':
    main()
