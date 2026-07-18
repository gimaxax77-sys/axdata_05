#!/usr/bin/env bash
# Quaternius 몬스터 → 적 스프라이트(16f, 왼쪽 향) 렌더. idle/attack(Bite_Front)/hit(HitRecieve).
# 6종 추가로 적 다양화. 출력 → _qenemy/<key>_<state>_NN.png. 실행: bash render-enemies-q.sh
set -u
export MSYS_NO_PATHCONV=1

BL="/c/Program Files/Blender Foundation/Blender 4.2/blender.exe"
SCRIPT="D:/.CODE/AXdata/axdata_05/scripts/render_monster_sprite.py"
SRC="D:/.CODE/AXdata/렌더/Quaternius_CuteMonsters/glTF"
OUT="D:/.CODE/AXdata/axdata_05/_qenemy"
mkdir -p "$OUT"

# key : gltf파일명
declare -A M=( [demon]=Demon [greendemon]=GreenDemon [cthulhu]=Cthulhu [cyclops]=Cyclops [yeti]=Yeti [alien]=Alien )

render() { # $1 key $2 gltf $3 clip $4 state
  MSP_GLTF="$SRC/$2.gltf" MSP_OUT="$OUT" MSP_NAME="$1" MSP_CLIP="$3" MSP_STATE="$4" \
  MSP_FRAMES=16 MSP_RES=256 MSP_DIR="-1,0,0" \
  "$BL" --background --python "$SCRIPT" >/tmp/qen_"$1"_"$4".log 2>&1
}

n=0
for key in "${!M[@]}"; do
  n=$((n+1)); echo "[$n/${#M[@]}] $key (${M[$key]})"
  render "$key" "${M[$key]}" "Idle"       "idle"
  render "$key" "${M[$key]}" "Bite_Front" "attack"
  render "$key" "${M[$key]}" "HitRecieve" "hit"
done
echo "완료 → $OUT : $(ls "$OUT"/*.png 2>/dev/null | wc -l) 프레임"
