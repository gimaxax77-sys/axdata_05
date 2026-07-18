#!/usr/bin/env bash
# 적 스프라이트 EEVEE 재렌더(16프레임) — idle+hit+attack, 왼쪽(파티 방향) 측면.
# 아군과 동일한 EEVEE 3점 조명으로 전투 화면 톤 통일.
# 적별 공격 클립이 달라 개별 매핑(기존 out_enemy_atk 파일명과 동일 규약).
# 출력: idle/hit → out_enemy16, attack → out_enemy_atk.  실행: bash render-enemy16-eevee.sh
set -u
export MSYS_NO_PATHCONV=1
export SPRITE_ENGINE=eevee

BL="/c/Program Files/Blender Foundation/Blender 4.2/blender.exe"
SCRIPT_WIN="D:/.CODE/AXdata/axdata_05/scripts/render_sprites.py"
FRAMES=16
DIR="-1,0,0"          # 왼쪽 측면(파티를 바라봄)

R="D:/.CODE/AXdata/렌더"
GENERAL="$R/KayKit_Adventurers_2.0_FREE/KayKit_Adventurers_2.0_FREE/Animations/gltf/Rig_Medium/Rig_Medium_General.glb"
MELEE="$R/KayKit_Character_Animations_1.1/KayKit_Character_Animations_1.1/Animations/gltf/Rig_Medium/Rig_Medium_CombatMelee.glb"
RANGED="$R/KayKit_Character_Animations_1.1/KayKit_Character_Animations_1.1/Animations/gltf/Rig_Medium/Rig_Medium_CombatRanged.glb"
SKEL="$R/KayKit_Complete_v6/The Complete KayKit Collection v6/KayKit Skeletons 1.1/characters/gltf"
WERE="$R/KayKit_Complete_v6/The Complete KayKit Collection v6/KayKit Mystery Monthly Series 4/4 - October 2023 - Werewolf/characters/gltf"

render() { # $1 chardir  $2 body  $3 anim  $4 clip  $5 outdir
  SPRITE_CHARDIR="$1" SPRITE_BODIES="$2" SPRITE_ANIM_PATH="$3" \
  SPRITE_ACTIONS="$4" SPRITE_FRAMES="$FRAMES" SPRITE_DIR="$DIR" SPRITE_OUT="$5" \
  "$BL" --background --python "$SCRIPT_WIN" >/tmp/en_"$2"_"$4".log 2>&1
}

# id  chardir  body  attack_anim  attack_clip
enemy() { # $1 body_dir $2 body $3 anim $4 clip
  echo "  $2 — idle/hit/attack($4)"
  render "$1" "$2" "$GENERAL" "Idle_A" "D:/.CODE/AXdata/axdata_05/out_enemy16"
  render "$1" "$2" "$GENERAL" "Hit_A"  "D:/.CODE/AXdata/axdata_05/out_enemy16"
  render "$1" "$2" "$3"       "$4"     "D:/.CODE/AXdata/axdata_05/out_enemy_atk"
}

echo "[1/5] skeleton_golem";   enemy "$SKEL" "Skeleton_Golem"   "$MELEE"  "Melee_2H_Attack_Chop"
echo "[2/5] skeleton_mage";    enemy "$SKEL" "Skeleton_Mage"    "$RANGED" "Ranged_Magic_Shoot"
echo "[3/5] skeleton_minion";  enemy "$SKEL" "Skeleton_Minion"  "$MELEE"  "Melee_1H_Attack_Slice_Diagonal"
echo "[4/5] skeleton_warrior"; enemy "$SKEL" "Skeleton_Warrior" "$MELEE"  "Melee_1H_Attack_Slice_Diagonal"
echo "[5/5] werewolf_wolf";    enemy "$WERE" "Werewolf_Wolf"    "$MELEE"  "Melee_Unarmed_Attack_Kick"
echo "완료 → out_enemy16: $(ls out_enemy16/*.png 2>/dev/null | wc -l) / out_enemy_atk: $(ls out_enemy_atk/*.png 2>/dev/null | wc -l)"
