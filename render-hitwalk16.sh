#!/usr/bin/env bash
# 전투 보조 모션 재렌더(16프레임) — hit(피격) + walk(걷기), 오른쪽 측면.
# hit=General/Hit_A, walk=MovementBasic/Walking_A (둘 다 공유 리그라 원형 무관).
# 매핑: battle_render_map.tsv(id·body_glb). 출력: out_battle16/<id>_<clip>_NN.png.
# 실행: bash render-hitwalk16.sh
set -u
export MSYS_NO_PATHCONV=1

BL="/c/Program Files/Blender Foundation/Blender 4.2/blender.exe"
ROOT="/d/.CODE/AXdata/axdata_05"
SCRIPT_WIN="D:/.CODE/AXdata/axdata_05/scripts/render_sprites.py"
MAP="$ROOT/battle_render_map.tsv"
OUT_WIN="D:/.CODE/AXdata/axdata_05/out_battle16"
FRAMES=16
DIR="1,0,0"

R="D:/.CODE/AXdata/렌더"
GENERAL="$R/KayKit_Adventurers_2.0_FREE/KayKit_Adventurers_2.0_FREE/Animations/gltf/Rig_Medium/Rig_Medium_General.glb"
MOVE="$R/KayKit_Adventurers_2.0_FREE/KayKit_Adventurers_2.0_FREE/Animations/gltf/Rig_Medium/Rig_Medium_MovementBasic.glb"

render() { # $1 chardir  $2 body  $3 anim  $4 clip
  SPRITE_CHARDIR="$1" SPRITE_BODIES="$2" SPRITE_ANIM_PATH="$3" \
  SPRITE_ACTIONS="$4" SPRITE_FRAMES="$FRAMES" SPRITE_DIR="$DIR" SPRITE_OUT="$OUT_WIN" \
  "$BL" --background --python "$SCRIPT_WIN" >/tmp/hw_"$2"_"$4".log 2>&1
}

n=0
tail -n +2 "$MAP" | while IFS=$'\t' read -r id arch body_glb; do
  [ -z "$id" ] && continue
  chardir_win="${body_glb%/*}"
  body="${body_glb##*/}"; body="${body%.glb}"
  n=$((n+1))
  echo "[$n/21] $id — hit + walk"
  render "$chardir_win" "$body" "$GENERAL" "Hit_A"
  render "$chardir_win" "$body" "$MOVE" "Walking_A"
done
echo "완료 → out_battle16 hit/walk: $(ls "$ROOT/out_battle16"/*_hit_a_*.png "$ROOT/out_battle16"/*_walking_a_*.png 2>/dev/null | wc -l) 파일"
