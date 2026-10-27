#!/usr/bin/env bash
# Install ffx-launch and ffx2-play into ~/.local/bin.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
install -Dm755 "$here/ffx-launch" "$HOME/.local/bin/ffx-launch"
install -Dm755 "$here/ffx2-play" "$HOME/.local/bin/ffx2-play"
echo "Installed $HOME/.local/bin/ffx-launch and $HOME/.local/bin/ffx2-play"
echo
echo "FFX launch options (Steam > FFX/X-2 > Properties > Launch Options):"
echo "  WINEDLLOVERRIDES=\"dinput8=n,b\" PROTON_FORCE_LARGE_ADDRESS_AWARE=0 $HOME/.local/bin/ffx-launch %command%"
