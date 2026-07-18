#!/usr/bin/env bash
# 전투 배경 10종 EEVEE 일괄 렌더 — 층·난이도별로 바닥·벽·기둥·색조 무드 변화.
# render_scene_eevee.py 사용. 결과 → _bg10, 전부 성공 시 assets/pixel/bg-battle-N.png 덮어씀.
# 실행: bash render-bg10-eevee.sh
set -u
export MSYS_NO_PATHCONV=1

BL="/c/Program Files/Blender Foundation/Blender 4.2/blender.exe"
SCRIPT="D:/.CODE/AXdata/axdata_05/scripts/render_scene_eevee.py"
SDIR="D:/.CODE/AXdata/렌더/KayKit_Complete_v6/The Complete KayKit Collection v6/KayKit Dungeon Remastered 1.1/Assets/gltf"
OUT="D:/.CODE/AXdata/axdata_05/_bg10"
ASSETS="D:/.CODE/AXdata/axdata_01/axdata_01/assets/pixel"
mkdir -p "$OUT"

# N : floor | wall | col | tint(r,g,b)  — 10개 무드
CFG=(
  "floor_dirt_large|wall|pillar_decorated|0.03,0.04,0.08"        # 0 푸른 밤
  "floor_tile_large|wall_cracked|pillar|0.06,0.045,0.03"         # 1 따뜻한 동굴
  "floor_dirt_large_rocky|wall_broken|column|0.03,0.06,0.045"    # 2 초록 늪
  "floor_tile_large_rocks|wall|pillar_decorated|0.055,0.03,0.08" # 3 보라 심연
  "floor_dirt_large|wall_cracked|pillar|0.09,0.03,0.03"          # 4 붉은 지옥
  "floor_tile_large|wall|column|0.03,0.06,0.07"                  # 5 청록 지하묘
  "floor_wood_large|wall_broken|pillar_decorated|0.07,0.05,0.03" # 6 호박빛
  "floor_tile_large_rocks|wall_cracked|pillar|0.03,0.03,0.09"    # 7 남색
  "floor_dirt_large_rocky|wall_broken|column|0.04,0.055,0.05"    # 8 무덤
  "floor_wood_large_dark|wall|pillar_decorated|0.08,0.025,0.045" # 9 진홍
)

ok=0
for i in "${!CFG[@]}"; do
  IFS='|' read -r FLOOR WALL COL TINT <<< "${CFG[$i]}"
  echo "[$((i+1))/10] bg-battle-$i : $FLOOR / $WALL / tint $TINT"
  SCENE_DIR="$SDIR" SCENE_OUT="$OUT" SCENE_NAME="bg-battle-$i" \
  SCENE_FLOOR="$FLOOR" SCENE_WALL="$WALL" SCENE_COL="$COL" SCENE_TINT="$TINT" \
  SCENE_RES_W=1024 SCENE_RES_H=576 \
  "$BL" --background --python "$SCRIPT" >/tmp/bg_"$i".log 2>&1 \
    && ok=$((ok+1)) || echo "  [실패] 로그: /tmp/bg_$i.log"
done

echo "렌더 성공 $ok/10"
if [ "$ok" -eq 10 ]; then
  for i in 0 1 2 3 4 5 6 7 8 9; do cp "$OUT/bg-battle-$i.png" "$ASSETS/bg-battle-$i.png"; done
  echo "assets/pixel 반영 완료 → $ASSETS"
else
  echo "일부 실패 → assets 미반영(수동 확인 필요)"
fi
