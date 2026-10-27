# Mods and tools

This repo contains **no mod files**. Download everything from the original authors. Most mods are on [Nexus Mods](https://www.nexusmods.com/games/finalfantasyxx2hdremaster) (free account; free downloads are capped at about 3 MB/s, one at a time).

The checksums are of the exact archives used for the reference setup, so you can confirm a download is the same file. If an author has published a newer version, the checksum won't match. That isn't necessarily a problem, but re-check its install instructions.

## Mod loader (required by every mod below)

| Mod | File | Size | SHA-256 |
|---|---|---|---|
| [FFX/X-2 HD External File Loader](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/150?tab=files) by ffgriever | v1.2.0 ([file 1473](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/150?tab=files&file_id=1473)) | 50,778 B | `909023055bd6c9d3e7c17fad1075f8e4da85e548626a2547e4c7ab901b461c20` |

The game update of **30 September 2026** needs **v1.2.0 or later**; v1.1.2 logs `Invalid game version` and silently loads nothing.

## Textures: FFX/FFX-2 Re-Remastered by HitokageWorshipper

[Mod 244](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/244?tab=files). AI-upscaled versions of every texture, animation and UI file (except videos). Pick **one** size:

| Size | Best for | Files | Download size |
|---|---|---|---|
| Small (2x) | Steam Deck / 720p–800p | FFX Small version ([file 1176](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/244?tab=files&file_id=1176)) | ~10.5 GB |
| Medium (2.5x) | 1080p | FFX Medium version ([file 1177](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/244?tab=files&file_id=1177)) | ~17.6 GB |
| Extreme (3x) | 1440p / 4K | FFX Extreme version, file 1 of 2 ([1178](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/244?tab=files&file_id=1178)) **and** file 2 of 2 ([1179](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/244?tab=files&file_id=1179)) | ~23 GB |

Reference setup (Extreme, v4.0):

| Archive | Size | SHA-256 |
|---|---|---|
| `FFX Extreme version -- file 1 of 2-244-4-0-1744225114.7z` | 12,030,392,560 B | `33b6feda3effc6d5c0d726250a144472b8fb2520bd66a79bf7cf9c1aa89c7fb3` |
| `FFX Extreme version -- file 2 of 2-244-4-0-1744227176.7z` | 11,920,822,193 B | `fd735e77924bd30aa12da72e746b8404715f38cfea583d71b0537d73d0eecba6` |

Unpacked, Extreme is ~118 GB (~90 GB on disk on a compressing filesystem such as btrfs). The archives also contain an older copy of the loader and readme files; install **only the `ffx_data/` folder**.

## Cutscenes: FMVs Remastered v2.0 by Skopin

[Mod 121](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/121?tab=files). Use the **1080p** sets: the author notes the 4K videos stutter in the game's video player. You need set 1 for your voice language plus the shared set 2.

| Archive | Nexus file | Size | SHA-256 |
|---|---|---|---|
| `1080p FMVs - US set-121-2-0-1729921643.7z` (English) | [1059](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/121?tab=files&file_id=1059) | 3,906,570,037 B | `cd134f8d7695d55a85bf1ffea912e66bc71920a8e5db6df1c858ba7fd19279fa` |
| `1080p FMVs Shared set-121-2-0-1729919982.7z` (all languages) | [1058](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/121?tab=files&file_id=1058) | 2,185,538,543 B | `7ff34fcdc85ddf48838c77c6b83c2c758850e38c51f2ff60598400eb46738049` |
| 1080p FMVs set 1 (JP) (Japanese voices instead of US) | [1057](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/121?tab=files&file_id=1057) | ~3.6 GB | n/a (not used in the reference setup) |

Both archives wrap their content in an extra top folder (`ffx_fmvs_remastered_1080p_*/ffx_data/…`); strip it so `ffx_data/` lands directly in `data/mods/`.

## Character textures: Catachrism HD re-textures

Hand-painted 8K (or 4K) textures for the party, in External File Loader format (2024 versions, **UnX is not needed**). They replace some Re-Remastered textures for the same characters, which is what the Re-Remastered author recommends. Use 4K on a Steam Deck.

| Character | Mod | 8K file | 4K file | 8K archive size | 8K SHA-256 |
|---|---|---|---|---|---|
| Tidus | [32](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/32?tab=files) | 912 | 913 | 67,276,804 B | `aa56b6a9b2cfd30257c0a45541bc2ba273259a6e95b0a34029495ee186139b15` |
| Yuna | [81](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/81?tab=files) | 914 | 915 | 172,521,655 B | `7d9cc0f4a94f34f1b59c96c128a598fd72b1f79f6ec84004493382d8f27c1953` |
| Wakka | [39](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/39?tab=files) | 916 | 917 | 114,913,476 B | `6e9a9bc45980311d6d16024991a035e97d82758e1897d6c8d7cd75a8dacffbfa` |
| Lulu | [82](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/82?tab=files) | 926 | 927 | 68,563,203 B | `7066ae3c5738822bffc66112e5893fd91845b75a54710bdd4ddec0fd104253fe` |
| Auron | [40](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/40?tab=files) | 920 | 921 | 106,152,573 B | `89b8d7e8632d9cb56f16dd63dd386a8e77fce21a15322525d9e191d3bf375c20` |
| Rikku | [43](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/43?tab=files) | 918 | 919 | 109,239,829 B | `3a5b9d1cf95204d821cdfdf8521bd99d7e2a274805eb48e95e7912accd79bce3` |
| Kimahri | [48](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/48?tab=files) | 924 | 925 | 134,852,591 B | `145af629cd08a862a5ed752392c6ca0dfcdd3fbd14c12cd881a1234f6794ab3f` |

Each archive wraps its content in a `<Name> 8K/` folder; strip it. The seven packs don't overlap each other.

## High-poly character models by f80h

[Mod 226](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/226?tab=files). Smoother models for both the field/battle versions and the cutscene versions. Use the **"a" (vanilla shape)** meshes, not the "ALT body" variants (a user reports the Lulu alt body stretches her texture). These are model files only, so they work with the texture mods above. The difference is **subtle**: smoother silhouettes, same faces.

| File | Nexus file | Size | SHA-256 |
|---|---|---|---|
| `HP Tidus-226-1-0-1728488030.7z` (1a) | 1012 | 1,278,863 B | `7207a4e8604419faa1cef64ff396ed3e652378351377d4743f4ca4dd35734300` |
| `2a) HP Yuna mesh-226-1-1-1729084037.7z` | 1036 | 2,548,653 B | `7aab4ae9d3301ec024d8d142617502359a9fb85e0b9efb448e5f782ce2672cc9` |
| `5a) HP Wakka mesh-226-1-1-1729086988.7z` | 1040 | 1,504,457 B | `184f4a5dba2be6dbe131525e904cec2d6e10d2146088b6625de22ed23c6318bf` |
| `6a) HP Lulu mesh-226-1-0-1728662412.7z` | 1025 | 1,269,963 B | `76b1b1eb4518690dcb1a32c68e243a21447a4734f2f73874dff07ef381356c84` |
| `9) HP Shiva-226-1-0-1728662457.7z` | 1026 | 815,085 B | `955971b6579de25d0b6560e1c24f4b09a36987d723563d0283b240375058d386` |

Auron, Rikku and Kimahri have no high-poly model (yet).

## Frame generation

| Tool | Where | Notes |
|---|---|---|
| [Lossless Scaling](https://store.steampowered.com/app/993090/Lossless_Scaling/) | Steam (paid, ~$7) | Windows app: force a Proton version in its Compatibility settings so Steam offers Install, then select the **`lsfg-vk`** beta branch. It is never launched; lsfg-vk only reads its `Lossless.dll`. |
| [Decky Loader](https://decky.xyz/) | decky.xyz | Plugin framework for Steam Game Mode. |
| [Decky LSFG-VK](https://github.com/xXJSONDeruloXx/decky-lsfg-vk/releases) | GitHub releases (v0.14.4 used) | The Decky store had an older version; the GitHub zip includes **lsfg-vk 2.0.0** (Install via Decky ▸ Developer ▸ Install Plugin from Zip). |
| [ffx-lsfg-fast-loads](https://github.com/roblesi/ffx-lsfg-fast-loads) | GitHub | Turns frame generation off while FFX loads, removing ~10 s black screens around battles and area changes. |

## Tried and not recommended

| Mod | Why not |
|---|---|
| [UnX / Special K UnX](https://github.com/Kaldaien/UnX) | Unmaintained since 2017–2018, hooks fixed addresses that game updates move, fragile under Proton (replaces `dxgi.dll`), reported to crash with the External File Loader, and its frame-rate limiter makes loads slower. |
| [FFX HD – Ultra Remaster](https://www.nexusmods.com/finalfantasyxx2hdremaster/mods/168) | Its own pinned post says it stopped working with the 2024 Catachrism updates. |
| [Farplane](https://github.com/topher-au/Farplane) | Windows memory editor, last released 2016. |
| 4K FMVs | Stutter in the game's video player (per the author); 1080p looks great on a 4K TV. |
| Steam Game Mode's per-game refresh-rate slider on an external TV | Not supported for external displays; set the TV's mode in **Settings ▸ Display** instead. |
