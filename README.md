# ffx-steamos-setup

A reproducible recipe for a heavily upgraded **Final Fantasy X HD Remaster** on a SteamOS-style Linux machine, written for [Claude Code](https://claude.com/claude-code) to carry out with you.

## What you get

- **Everything re-textured:** AI-upscaled textures for the whole game ([FFX Re-Remastered](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/244)), plus hand-painted 8K party textures (Catachrism).
- **Remastered cutscenes** in 1080p, cleaned of compression artifacts.
- **Smoother high-poly models** for Tidus, Yuna, Wakka, Lulu and Shiva.
- **120 FPS** (or 60/90, to match your display) with Lossless Scaling frame generation, on a game that's hard-locked to 30.
- **~1-second loads** around battles and area changes. Frame generation normally stretches them to ~10 s; [ffx-lsfg-fast-loads](https://github.com/roblesi/ffx-lsfg-fast-loads) fixes that.
- **No launcher:** Play goes straight into FFX, with a separate **FINAL FANTASY X-2** tile in your library.

## What you need

- A SteamOS-style machine running Steam Game Mode (Steam Deck, SteamOS, Bazzite, CachyOS handheld edition, …) with FFX/X-2 HD Remaster installed and launched once.
- Claude Code, either on that machine or on another computer that can reach it over SSH (key-based login).
- A free [Nexus Mods](https://www.nexusmods.com/) account, logged in in your browser.
- [Lossless Scaling](https://store.steampowered.com/app/993090/Lossless_Scaling/) on Steam (paid) and [Decky Loader](https://decky.xyz/), for frame generation.
- Disk space: the texture pack grows about 5× when unpacked. The 4K setup (Extreme) is a ~23 GB download and ~118 GB unpacked; Small and Medium are smaller downloads. Leave room for the downloaded archives too.

## How to use it

```bash
git clone https://github.com/roblesi/ffx-steamos-setup.git
cd ffx-steamos-setup
claude
```

Then ask something like *"Set up FFX on my gaming PC following this repo"*. Claude reads [`CLAUDE.md`](CLAUDE.md), asks about your hardware, picks the right texture sizes and frame-generation settings, and works through the steps with you. It checks each step before moving on and tells you when something needs your hands: downloads through your browser, purchases, Steam and Decky menus.

You can also follow [`CLAUDE.md`](CLAUDE.md) by hand. It's a normal step-by-step guide with commands.

## What's in here

| File | Purpose |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | The playbook: steps, checks, rollback, and the pitfalls found along the way |
| [`mods.md`](mods.md) | Every mod and tool, with links, exact files, sizes and SHA-256 checksums, plus what was tried and dropped |
| [`scripts/ffx-launch`](scripts/ffx-launch) | Launch-option wrapper: skips the launcher; starts FFX-2 when the X-2 tile asks |
| [`scripts/ffx2-play`](scripts/ffx2-play) | What the FINAL FANTASY X-2 tile runs |
| [`scripts/add-ffx2-tile.py`](scripts/add-ffx2-tile.py) | Adds that tile to Steam (with Steam stopped) |
| [`scripts/install-launch-scripts.sh`](scripts/install-launch-scripts.sh) | Installs the two scripts into `~/.local/bin` |

**No mod files are included.** Download them from their authors, linked in `mods.md`.

## Caveats

- Tested on one machine: CachyOS Game Mode, AMD RX 9070-class GPU, 4K 120 Hz TV. Steam Deck recommendations come from the mod authors' own guidance, not from testing on a Deck.
- **Steam updates to FFX can break the mod loader.** The game then silently runs without mods until the loader's author publishes an update. `CLAUDE.md` explains how to check for this and how to update.

## Credits

All the hard work is by the mod and tool authors: ffgriever (External File Loader), HitokageWorshipper (FFX Re-Remastered), Skopin (FMVs Remastered), CATACHR1SM (HD re-textures), f80h (high-poly models), THS (Lossless Scaling), PancakeTAS and contributors (lsfg-vk), xXJSONDeruloXx (Decky LSFG-VK), and the Decky Loader team.

The scripts in this repo are MIT-licensed; the mods and tools keep their own licenses and permissions.
