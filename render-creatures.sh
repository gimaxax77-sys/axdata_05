#!/usr/bin/env bash
# 펫·가디언 아이콘 일괄 렌더 — Quaternius Cute Monsters(glTF) → EEVEE 256px 투명 PNG.
# 18종(펫12+가디언6)에 매핑된 몬스터만 렌더 → assets/ui/creatures/<Monster>.png.
# 실행: bash render-creatures.sh
set -u
export MSYS_NO_PATHCONV=1

BL="/c/Program Files/Blender Foundation/Blender 4.2/blender.exe"
SCRIPT="D:/.CODE/AXdata/axdata_05/scripts/render_monster.py"
SRC="D:/.CODE/AXdata/렌더/Quaternius_CuteMonsters/glTF"
OUT="D:/.CODE/AXdata/axdata_01/axdata_01/assets/ui/creatures"
mkdir -p "$OUT"

# 매핑에 쓰인 몬스터(중복 없이)
MONSTERS=(Pig Yeti Chicken Deer Panda Crab YellowDragon Bat Bee Cthulhu GreenDemon Cyclops Demon Ghost Mushroom Alien_Tall Penguin Skull)

n=0
for M in "${MONSTERS[@]}"; do
  n=$((n+1)); echo "[$n/${#MONSTERS[@]}] $M"
  MON_FBX="$SRC/$M.gltf" MON_OUT="$OUT" MON_NAME="$M" MON_RES=256 \
    "$BL" --background --python "$SCRIPT" >/tmp/cre_"$M".log 2>&1 || echo "  [실패] /tmp/cre_$M.log"
done
echo "완료 → $OUT : $(ls "$OUT"/*.png 2>/dev/null | wc -l) 파일"
