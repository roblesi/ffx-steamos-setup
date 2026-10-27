# FFX HD Remaster on SteamOS — setup playbook

This file tells Claude Code how to reproduce a modded **Final Fantasy X/X-2 HD Remaster** setup on a SteamOS-style Linux machine (SteamOS, Bazzite, CachyOS handheld edition, or similar Steam Game Mode sessions). The mods themselves are **not** in this repo; [`mods.md`](mods.md) lists every file with links, sizes and SHA-256 checksums.

**End state:**
- AI-upscaled textures for everything (FFX Re-Remastered), remastered 1080p cutscenes, hand-painted 8K/4K party textures, smoother high-poly party models.
- Lossless Scaling frame generation (lsfg-vk), e.g. 30 → 120 FPS on a 120 Hz display.
- Loads near-instant despite frame generation ([ffx-lsfg-fast-loads](https://github.com/roblesi/ffx-lsfg-fast-loads)).
- Steam's Play button goes straight into FFX (no launcher), plus a separate **FINAL FANTASY X-2** library tile.

Reference machine: CachyOS (Steam Game Mode), AMD RX 9070-class GPU, 4K 120 Hz TV over HDMI 2.1, Proton 11.0, game build 25501027 (Steam update of 30 Sept 2026), External File Loader 1.2.0, lsfg-vk 2.0.0, Decky LSFG-VK 0.14.4. Everything was verified there and nowhere else, so **verify every step on the new machine** instead of assuming.

## Ground rules

- **Downloads need the user's OK.** Before downloading, list each file, its source and size. Nexus Mods downloads require the user's own logged-in browser; never handle their credentials or API keys.
- **Purchases are the user's.** Lossless Scaling is a paid Steam app; the user buys it.
- **UI-only steps are the user's:** Decky Loader install, Decky plugin installs (the plugin folder is root-owned), Steam beta branch and compatibility settings, Steam ▸ Settings ▸ Display.
- **Steam restarts need the game closed and a heads-up.** The screen goes blank for about a minute.
- **Back up before overwriting anything**, and record files you add, so every step can be undone.
- **Do, then verify.** Each step below has a *Verify* section; don't move on until it passes.
- Never commit mod files or anything from the user's machine (IPs, Steam IDs, saves) to this repo.

## Step 0: discover the machine and ask the user

Ask the user:
1. **Device and display:** Steam Deck (LCD 800p / OLED 90 Hz) or a PC on a TV/monitor? Resolution and maximum refresh rate?
2. **How you reach it:** is Claude Code running on that machine, or on another computer with SSH access (key-based)? Prefer `ssh user@<hostname>.local`: DHCP addresses change, and mDNS follows the machine.
3. **Where downloads happen:** which browser is logged into Nexus Mods, and on which machine.
4. **Voice language** (English or Japanese) for the cutscene pack.
5. Has the game been **installed and launched once**? The Proton prefix and `data/` folder only exist after the first launch.

Then inspect (read-only):

```bash
uname -a; grep -E '^(NAME|VARIANT_ID)=' /etc/os-release; echo "$SHELL"
lspci | grep -Ei 'vga|3d'                                     # GPU
for c in /sys/class/drm/card*-*; do [ "$(cat $c/status 2>/dev/null)" = connected ] && echo "$c: $(head -1 $c/modes)"; done
df -h ~                                                      # Extreme textures need ~120 GB unpacked
G="$HOME/.local/share/Steam/steamapps/common/FINAL FANTASY FFX&FFX-2 HD Remaster"   # or a microSD/other library
ls "$G" "$G/data"; ls ~/.local/share/Steam/steamapps/compatdata/359870/pfx >/dev/null && echo "prefix ok"
ls ~/homebrew/plugins 2>/dev/null && echo "Decky installed"
command -v bsdtar 7z unzip python3
grep -rh KillUserProcesses /etc/systemd/logind.conf /etc/systemd/logind.conf.d/ 2>/dev/null
systemctl --user list-units --type=service | grep -Ei 'steam|gamescope'
```

If the game is in another Steam library (e.g. a microSD card under `/run/media/...`), use that path as `G` everywhere below.

## Sizing

| Display | Re-Remastered pack | Catachrism | Cutscenes | Frame generation |
|---|---|---|---|---|
| Steam Deck LCD (800p, 60 Hz) | Small | 4K | 1080p | 2x (30 → 60) |
| Steam Deck OLED (800p, 90 Hz) | Small | 4K | 1080p | 3x (30 → 90) |
| 1080p, 60 Hz | Medium | 4K or 8K | 1080p | 2x |
| 1440p/4K, 120 Hz, 16 GB VRAM | Extreme | 8K | 1080p | 4x (30 → 120) |

FFX runs at a fixed 30 FPS, so the multiplier is `refresh rate / 30`.

## Conventions and gotchas (read before running anything)

- **The remote login shell may be fish.** Wrap commands in `bash -c '…'` or `ssh host bash -s <<'EOF' … EOF`.
- **Background processes started over SSH can be killed when the session closes** (several SteamOS-like distros set `KillUserProcesses=yes`). Use `systemd-run --user …` or a user service for anything long-running.
- **`pgrep -f FFX.exe` over SSH matches its own command line.** Use `ps -eo args | grep -E '[F]FX\.exe'`. The same goes for `pkill -f`: it can kill your own SSH session.
- **Never run `/usr/bin/steam` on SteamOS-style systems.** It is often the `steam-jupiter` wrapper, which can delete `~/.local/share/Steam` under some conditions. To hand a URL to the running Steam, use `~/.local/share/Steam/steam.sh steam://…`.
- **Steam rewrites `localconfig.vdf` and `shortcuts.vdf` while running.** Edit them only with Steam fully stopped: `systemctl --user stop steam-launcher.service`, edit, `systemctl --user start steam-launcher.service` (service name may differ, so check `systemctl --user list-units`). Prefer having the user change launch options in Steam's UI.
- **Copying from macOS:** plain `tar` adds `._*` AppleDouble files. Use `bsdtar --no-xattrs --no-mac-metadata --format=ustar -cf - … | ssh host 'tar -xf - -C …'`.
- **Comparing file lists between machines:** use `LC_ALL=C sort` on both sides, or `comm` reports false differences.
- **Steam Game Mode on an external TV/monitor:** the per-game refresh-rate slider isn't available. The refresh rate is set in **Steam ▸ Settings ▸ Display** and saved in `~/.config/gamescope/modes.cfg`. If that file gets emptied, the TV falls back to 60 Hz.
- **Game updates break the mod loader.** After any FFX update, check line 5 of `$G/hook.log`: `Invalid game version. Unable to find proper hook values.` means every mod is silently off until a newer External File Loader exists.

## Step 1: External File Loader

**Do:** download v1.2.0+ (see `mods.md`). Unpack its contents into `$G` (`dinput8.dll`, `hook.ini`, `simpleLog.dll`, `modules/…`, `data/mods/`). Then turn on access logging, which verification and the fast-load switcher both need:

```bash
cd "$G/modules/config" && cp -n ff10-file-loader.ini ff10-file-loader.ini.bak && sed -i 's/^logAccess=false/logAccess=true/' ff10-file-loader.ini
```

The loader only works with this launch option: `WINEDLLOVERRIDES="dinput8=n,b" … %command%`. Step 2 sets the final launch options.

**Verify** (after step 2 and one launch): `head -8 "$G/hook.log"` shows `FFX detected` (1.1.x) or `FFX open, existence and file-size hooks installed` (1.2.x), and the version. It must **not** show `Invalid game version`.

**Rollback:** delete the loader files, or remove `WINEDLLOVERRIDES=…` from the launch options.

## Step 2: launch scripts and launch options

**Do:** install the scripts from this repo on the gaming machine (`git clone` there, or copy `scripts/`):

```bash
./scripts/install-launch-scripts.sh     # installs ~/.local/bin/ffx-launch and ~/.local/bin/ffx2-play
```

Ask the user to set FFX/X-2's **Properties ▸ Launch Options** to (absolute path; the installer prints it):

```
WINEDLLOVERRIDES="dinput8=n,b" PROTON_FORCE_LARGE_ADDRESS_AWARE=0 /home/<user>/.local/bin/ffx-launch %command%
```

- `WINEDLLOVERRIDES="dinput8=n,b"` makes Proton load the mod loader's `dinput8.dll`.
- `PROTON_FORCE_LARGE_ADDRESS_AWARE=0` came from a Steam Deck guide as a fix for green-screen cutscenes and was kept in the reference setup. If the game crashes with big textures, try removing it.
- `ffx-launch` swaps the FFX/X-2 launcher for `FFX.exe` (or `FFX-2.exe` when the X-2 tile asks for it, see step 10).

**Verify:** Play opens FFX directly, no launcher. `ps -eo args | grep -E '[F]FX\.exe'` shows `FFX.exe` and no `LAUNCHER`. To change graphics settings later, temporarily remove `…/ffx-launch` from the launch options to get the launcher back.

## Step 3: FFX Re-Remastered textures

**Do:** download the size chosen in *Sizing* (2 files for Extreme). Extract and copy **only** `ffx_data/` into `$G/data/mods/`; the archives also contain readme files and an old loader copy. Large packs are best extracted in the background or streamed (see gotchas).

**Verify:** the number of files under `$G/data/mods/ffx_data` equals the number of non-directory `ffx_data/…` entries in the archives (Extreme: 21,612 + 21,612). No `._*` files.

## Step 4: FMVs Remastered (1080p)

**Do:** download set 1 for the voice language plus the shared set 2. Strip the archives' top folder so files land in `$G/data/mods/ffx_data/gamedata/ps3data/video/`.

**Verify:** 62 `.webm` files in that folder (29 shared + 33 US).

## Step 5: Catachrism character textures (8K or 4K)

These **replace** Re-Remastered textures for the same characters, so back those up first.

**Do:**
1. Extract all seven archives to a staging folder and strip each `<Name> 8K/` top folder.
2. List the staged files (`cd <stage> && find ffx_data -type f > staged.txt`). Back up the ones that already exist in `data/mods`:
   ```bash
   mkdir -p ~/ffx-mod-backups && cd "$G/data/mods"
   while read -r f; do [ -e "$f" ] && echo "$f"; done < staged.txt > ~/ffx-mod-backups/catachrism-files.txt
   tar -cf ~/ffx-mod-backups/before-catachrism.tar -T ~/ffx-mod-backups/catachrism-files.txt
   ```
3. Copy the staged `ffx_data/` over.

**Verify:** compare checksums of the copied files with the staged ones. In the reference setup all 83 files replaced existing ones.

**Rollback:** `cd "$G/data/mods" && tar -xf ~/ffx-mod-backups/before-catachrism.tar`

## Step 6: high-poly models

**Do:** download the five "a" meshes (`mods.md`) and copy their `ffx_data/` into `$G/data/mods/`. They add 14 `.dae.phyre` files and replace nothing (check first). Record the list in `~/ffx-mod-backups/highpoly-models-files.txt`.

**Verify (after launching and loading a save):**
```bash
grep -E 'chr/pc/c00[1256]/mdl/d3d11/.*\.dae\.phyre' "$G/hook.log" | head
```
Lines should say `Opening DIR: data/mods\…` (1.2.x) or `Reading DIR: …` (1.1.x), meaning they were read from the mods folder.

**Rollback:** delete the listed files.

## Step 7: confirm all mods load

Launch, load a save, walk around, then:

```bash
grep -cE '(Opening|Reading) DIR' "$G/hook.log"                           # hundreds or more
grep -E '(Opening|Reading) DIR' "$G/hook.log" | grep -oE 'ps3data/[a-z_]+' | sort | uniq -c | sort -rn | head
```

## Step 8: display refresh rate

- **External TV/monitor:** the user sets the maximum refresh rate in **Steam ▸ Settings ▸ Display**. Check `~/.config/gamescope/modes.cfg` (e.g. `…:3840x2160@120 0`) and `journalctl --user | grep 'refresh cycle'` (8.33 ms = 120 Hz, 16.67 ms = 60 Hz). Only expect 120 Hz if the display's EDID offers it: HDMI 2.1 or DisplayPort.
- **Steam Deck:** the built-in display's refresh rate is in the Quick Access ▸ Performance tab.

## Step 9: Lossless Scaling frame generation (lsfg-vk)

1. User: buy and install [Lossless Scaling](https://store.steampowered.com/app/993090/). It's a Windows app, so first set **Properties ▸ Compatibility ▸ Force … Proton** or Steam won't offer Install. Then select the **`lsfg-vk`** beta branch.
   **Verify:** `ls ~/.local/share/Steam/steamapps/common/"Lossless Scaling"/` shows `Lossless.dll` and `lsfg-vk.dll`, and `appmanifest_993090.acf` has `"BetaKey" "lsfg-vk"`.
2. User: install [Decky Loader](https://decky.xyz/) if missing, then the [Decky LSFG-VK](https://github.com/xXJSONDeruloXx/decky-lsfg-vk/releases) zip (Decky ▸ cog ▸ Developer Mode ▸ Developer ▸ Install Plugin from Zip; you can download the zip to `~/Downloads` with the user's OK). In the plugin, press **Install lsfg-vk**.
   A "flatpak not available" warning is harmless when Flatpak isn't installed.
   **Verify:** `~/.local/lib/liblsfg-vk-layer*.so`, `~/.local/share/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation*.json` and `~/.config/lsfg-vk/conf.toml` exist.
3. Add an FFX profile, either from the plugin while the game runs or by appending to `~/.config/lsfg-vk/conf.toml` (back it up first):
   ```toml
   [[profile]]
   name = "FINAL FANTASY X/X-2 HD Remaster"
   active_in = [ "359870" ]
   pacing_mode = "vsync"
   multiplier = 4          # refresh / 30
   flow_scale = 0.8
   performance_mode = false   # true on weaker GPUs / Steam Deck
   override_present_mode = true
   preserve_swapchain_image_count = false
   ```
   lsfg-vk hot-reloads `multiplier`, `flow_scale` and `performance_mode`. A multiplier of `1` means off.
   **Verify:** `journalctl --user | grep lsfg-vk` shows `Using profile with name 'FINAL FANTASY X/X-2 HD Remaster' (identified via Steam App ID)` and the multiplier. Steam's performance overlay shows the target FPS.

## Step 10: fast loads with frame generation

**Why:** FFX loads a fixed amount per real frame, and lsfg-vk's vsync pacing caps real frames at `refresh / multiplier` (30), even during loads. That stretches loads around battles and area changes to ~10 s.

**Do:** on the gaming machine:
```bash
git clone https://github.com/roblesi/ffx-lsfg-fast-loads.git && cd ffx-lsfg-fast-loads && ./install.sh
```
It needs step 1's `logAccess=true` (the installer also sets it) and step 9's profile name (override with `FFX_LSFG_PROFILE`; a missing profile is logged as a warning). Restart the game afterwards.

**Verify:** `journalctl --user -u ffx-fg-switch -f` during a battle shows `battle loading: …`, `field loading: …` and `loading done (≈1s)`. If some area still loads slowly, the first reads of that load in `hook.log` show what to add to the switcher's triggers.

## Step 11: FINAL FANTASY X-2 tile

Pressing this tile writes a short-lived note and launches the real Steam game. `ffx-launch` sees the note and starts `FFX-2.exe` (same prefix, saves, achievements and overlay).

**Do**, either:
- **User, in Desktop Mode:** Steam ▸ Add a Game ▸ Add a Non-Steam Game ▸ Browse ▸ `~/.local/bin/ffx2-play`, then rename it to "FINAL FANTASY X-2"; **or**
- **You, with the game closed and the user's OK:** stop Steam, run `python3 scripts/add-ffx2-tile.py` (it backs up `shortcuts.vdf` and refuses to run while Steam is running), then start Steam.

**Verify:** after the user presses the tile, `ps -eo args | grep -E '[F]FX-2\.exe'` shows FFX-2, and `~/.cache/ffx-launch-target` has been removed. The main tile still starts FFX.

Custom tile art: SteamGridDB images go in `~/.local/share/Steam/userdata/<id>/config/grid/` as `<shortcutid>p.png` (cover), `<shortcutid>_hero.png`, `<shortcutid>_logo.png` and `<shortcutid>.png` (wide). The tile script prints the ID. The SteamGridDB Decky plugin v1.7.1 crashed (React error #130) with Steam builds from late 2026, so copying the files there directly is the reliable route.

## After a game update

1. `sed -n 5p "$G/hook.log"`: does it say `Invalid game version`? Check [the loader's Nexus page](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/150?tab=files) for a newer version, and back up `modules/ff10-file-loader.dll` before replacing it. Keep the existing `.ini` files (`logAccess=true`).
2. Loader updates may change the log format. In 1.2, paths read from the game's own data keep their capitalization (`Opening native: ../../../FFX_Data/GameData/PS3Data/…`). The fast-load switcher matches case-insensitively; confirm it still logs `battle loading` / `field loading`.

## Undo everything

- Mods: remove `$G/data/mods/ffx_data` (or restore from backups).
- Loader: delete `dinput8.dll`, `hook.ini`, `simpleLog.dll`, `modules/`.
- Launch options: clear them.
- Switcher: `./uninstall.sh` in `ffx-lsfg-fast-loads`.
- Frame generation: remove the FFX profile from `conf.toml`, or uninstall the plugin.
- Tile: delete it in Steam.
- Scripts: `rm ~/.local/bin/ffx-launch ~/.local/bin/ffx2-play`.
