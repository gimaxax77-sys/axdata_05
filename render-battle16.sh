#!/usr/bin/env bash
# 전투 스프라이트 재렌더(16프레임) 드라이버 — idle + 원형별 attack, 오른쪽 측면.
#
# 배경: 전투 애니를 더 부드럽게(8→16프레임) 하려고 재렌더. 각 동작의 Blender
#       타임라인을 16개 균등 샘플 → 진짜 3D 중간 동작(보간 아님).
# 입력: battle_render_map.tsv (id · archetype · body_glb 절대경로).
# 엔진: scripts/render_sprites.py (env로 제어). 카메라 SPRITE_DIR="1,0,0"(오른쪽 측면,
#       기존 out_roster_full 과 동일 방향으로 검증됨).
# 출력: out_battle16/<id>_<clip>_NN.png  (예: knight_idle_a_00.png,
#       knight_melee_1h_attack_slice_diagonal_15.png). 기존 파일명 규약과 동일.
# 조립: axdata_01 쪽 assemble_strips.py(NFR=16)로 가로 스트립 조립 → assets/units.
#
# 실행:  bash render-battle16.sh
# 소요:  21종 × (idle+attack) × 16프레임, 대략 8~15분.
set -u
export MSYS_NO_PATHCONV=1

BL="/c/Program Files/Blender Foundation/Blender 4.2/blender.exe"
ROOT="/d/.CODE/AXdata/axdata_05"
SCRIPT_WIN="D:/.CODE/AXdata/axdata_05/scripts/render_sprites.py"  # blender엔 Windows 경로로
MAP="$ROOT/battle_render_map.tsv"
OUT_WIN="D:/.CODE/AXdata/axdata_05/out_battle16"
FRAMES=16
DIR="1,0,0"          # 오른쪽 측면(적 방향) — 기존과 동일

R="D:/.CODE/AXdata/렌더"
GENERAL="$R/KayKit_Adventurers_2.0_FREE/KayKit_Adventurers_2.0_FREE/Animations/gltf/Rig_Medium/Rig_Medium_General.glb"
MELEE="$R/KayKit_Character_Animations_1.1/KayKit_Character_Animations_1.1/Animations/gltf/Rig_Medium/Rig_Medium_CombatMelee.glb"
RANGED="$R/KayKit_Character_Animations_1.1/KayKit_Character_Animations_1.1/Animations/gltf/Rig_Medium/Rig_Medium_CombatRanged.glb"

# 원형 → 공격 애니파일 · 클립 키워드
attack_anim() { case "$1" in
  VANGUARD|STRIKER|ROGUE) echo "$MELEE" ;;
  ARCHER|MAGE|SUPPORT)    echo "$RANGED" ;;
esac; }
attack_clip() { case "$1" in
  VANGUARD) echo "Melee_1H_Attack_Slice_Diagonal" ;;
  STRIKER)  echo "Melee_2H_Attack_Chop" ;;
  ROGUE)    echo "Melee_1H_Attack_Stab" ;;
  ARCHER)   echo "Ranged_Bow_Release" ;;
  MAGE)     echo "Ranged_Magic_Shoot" ;;
  SUPPORT)  echo "Ranged_Magic_Spellcasting" ;;
esac; }

# 한 번 렌더 호출(공통 env → render_sprites.py)
render() { # $1 chardir_win  $2 body  $3 anim_win  $4 clip
  SPRITE_CHARDIR="$1" SPRITE_BODIES="$2" SPRITE_ANIM_PATH="$3" \
  SPRITE_ACTIONS="$4" SPRITE_FRAMES="$FRAMES" SPRITE_DIR="$DIR" \
  SPRITE_OUT="$OUT_WIN" \
  "$BL" --background --python "$SCRIPT_WIN" \
    >/tmp/bl_"$2"_"$4".log 2>&1
}

n=0
# TSV 헤더 스킵, 탭 구분
tail -n +2 "$MAP" | while IFS=$'\t' read -r id arch body_glb; do
  [ -z "$id" ] && continue
  chardir_win="${body_glb%/*}"                 # 폴더(Windows 정방향 경로)
  body="${body_glb##*/}"; body="${body%.glb}"  # 몸 basename
  n=$((n+1))
  echo "[$n/21] $id ($arch) — idle"
  render "$chardir_win" "$body" "$GENERAL" "Idle_A"
  echo "        $id — attack: $(attack_clip "$arch")"
  render "$chardir_win" "$body" "$(attack_anim "$arch")" "$(attack_clip "$arch")"
done
echo "완료 → out_battle16 : $(ls "$ROOT/out_battle16" 2>/dev/null | wc -l) 파일"
