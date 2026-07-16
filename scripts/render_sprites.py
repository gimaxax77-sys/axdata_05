# KayKit 3D 캐릭터 → 2D 스프라이트 배치 렌더 (Blender 헤드리스)
"""
GUI 클릭 없이 캐릭터×동작을 한 번에 2D PNG로 굽는 스크립트.

실행:
  blender --background --python scripts/render_sprites.py

먼저 아래 CONFIG의 경로를 본인 PC에 맞게 수정하세요.
이 스크립트는 GPU/Blender가 있는 PC에서만 돕니다(클라우드 불가).
첫 실행에서 카메라 방향·액션 이름 등을 1~2번 조정할 수 있습니다.
"""
import bpy
import os
import math
from mathutils import Vector

# ===================== CONFIG (본인 PC에 맞게 수정) =====================
# KayKit Adventurers 압축 푼 폴더(캐릭터 몸 + 애니메이션 모두 여기에 있음)
KAYKIT   = r"D:\.CODE\AXdata\렌더\KayKit_Adventurers_2.0_FREE\KayKit_Adventurers_2.0_FREE"
CHAR_DIR = KAYKIT + r"\Characters\gltf"
ANIM_FILE = KAYKIT + r"\Animations\gltf\Rig_Medium\Rig_Medium_General.glb"
OUT_DIR  = r"D:\.CODE\AXdata\axdata_05\out"          # 결과 저장 폴더

BODIES   = ["Knight"]                       # 확장 예: ["Knight","Barbarian","Mage","Rogue","Rogue_Hooded","Ranger"]
ACTIONS  = ["Idle"]                         # 액션 이름에 포함되는 키워드. 확장 예: ["Idle","Attack","Hit","Death"]
FRAMES_PER_ACTION = 1                       # 1 = 대표 한 장(포트레이트). N = N프레임 개별 저장(간이 시트용)

RESOLUTION   = 512                          # 출력 정사각 크기(px)
CAMERA_DIR   = (0.0, 1.0, 0.0)             # 카메라가 바라보는 방향(월드). 앞모습. 옆모습은 (-1,0,0) 등
CAMERA_TILT_DEG = 10.0                      # 살짝 위에서 내려다보는 각도(0=정측면)
PADDING      = 1.15                         # 캐릭터 여백(클수록 작게 잡힘)
# ======================================================================

# 폴링 자동화에서 명령으로 넘길 수 있도록 환경변수로 BODIES/ACTIONS 덮어쓰기(있을 때만)
_env_bodies = os.environ.get("SPRITE_BODIES")
if _env_bodies:
    BODIES = [b.strip() for b in _env_bodies.split(",") if b.strip()]
_env_actions = os.environ.get("SPRITE_ACTIONS")
if _env_actions:
    ACTIONS = [a.strip() for a in _env_actions.split(",") if a.strip()]
# 걷기/달리기 등은 다른 애니 파일(MovementBasic)·다프레임·측면이 필요 → env 로 덮어씀
_env_anim = os.environ.get("SPRITE_ANIM")          # 예: MovementBasic
if _env_anim:
    ANIM_FILE = KAYKIT + r"\Animations\gltf\Rig_Medium\Rig_Medium_" + _env_anim + ".glb"
_env_anim_path = os.environ.get("SPRITE_ANIM_PATH")  # 다른 팩의 애니 glb 전체 경로
if _env_anim_path:
    ANIM_FILE = _env_anim_path
_env_frames = os.environ.get("SPRITE_FRAMES")
if _env_frames:
    FRAMES_PER_ACTION = max(1, int(_env_frames))
_env_camdir = os.environ.get("SPRITE_DIR")         # 예: "1,0,0" (측면)
if _env_camdir:
    try:
        CAMERA_DIR = tuple(float(x) for x in _env_camdir.split(","))
    except Exception:
        pass
_env_out = os.environ.get("SPRITE_OUT")            # 결과 폴더 덮어쓰기
if _env_out:
    OUT_DIR = _env_out


def clear_scene():
    """장면의 모든 오브젝트 + 미사용 데이터 정리."""
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.armatures, bpy.data.actions,
                 bpy.data.cameras, bpy.data.images):
        for d in list(coll):
            if d.users == 0:
                coll.remove(d)


def import_gltf(path):
    """glTF/glb 를 불러오고 새로 생긴 오브젝트 목록을 반환."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def find_armature(objs):
    for o in objs:
        if o.type == 'ARMATURE':
            return o
    return None


def mesh_bbox(meshes):
    """메시들의 월드 바운딩 박스(min, max)."""
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for m in meshes:
        for corner in m.bound_box:
            w = m.matrix_world @ Vector(corner)
            mn = Vector((min(mn.x, w.x), min(mn.y, w.y), min(mn.z, w.z)))
            mx = Vector((max(mx.x, w.x), max(mx.y, w.y), max(mx.z, w.z)))
    return mn, mx


def setup_workbench():
    """스프라이트에 적합한 균일 조명(Workbench Flat + 텍스처 + 투명 배경)."""
    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'FLAT'
    sc.display.shading.color_type = 'TEXTURE'
    sc.render.film_transparent = True
    sc.render.resolution_x = RESOLUTION
    sc.render.resolution_y = RESOLUTION
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode = 'RGBA'


def make_camera(meshes):
    """메시를 꽉 채우는 정사영(orthographic) 카메라 생성·배치."""
    mn, mx = mesh_bbox(meshes)
    center = (mn + mx) * 0.5
    size = max((mx - mn).x, (mx - mn).y, (mx - mn).z) or 1.0
    cam_data = bpy.data.cameras.new("SpriteCam")
    cam_data.type = 'ORTHO'
    cam_data.ortho_scale = size * PADDING
    cam = bpy.data.objects.new("SpriteCam", cam_data)
    bpy.context.collection.objects.link(cam)
    d = Vector(CAMERA_DIR).normalized()
    dist = size * 3.0
    up = Vector((0, 0, math.tan(math.radians(CAMERA_TILT_DEG)) * dist))
    cam.location = center - d * dist + up
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam
    return cam


def find_action(keyword):
    for a in bpy.data.actions:
        if keyword.lower() in a.name.lower():
            return a
    return None


def render_body(body):
    clear_scene()

    # 1) 몸(텍스처 있음) 불러오기 — .gltf 우선, 없으면 .glb
    body_path = os.path.join(CHAR_DIR, body + ".gltf")
    if not os.path.exists(body_path):
        body_path = os.path.join(CHAR_DIR, body + ".glb")
    if not os.path.exists(body_path):
        print(f"[경고] 몸 파일 없음: {body_path} — 건너뜀")
        return
    body_objs = import_gltf(body_path)
    body_arm = find_armature(body_objs)
    body_meshes = [o for o in body_objs if o.type == 'MESH']
    if not body_arm:
        print(f"[경고] {body}: 뼈대(armature) 못 찾음 — 건너뜀")
        return

    # 2) 애니메이션 불러오기(액션 확보). 딸려온 회색 밑몸은 렌더에서 제외
    anim_objs = import_gltf(ANIM_FILE)
    for o in anim_objs:
        o.hide_render = True
        o.hide_viewport = True

    setup_workbench()
    make_camera(body_meshes)

    if not body_arm.animation_data:
        body_arm.animation_data_create()

    # 3) 액션별로 씌워서 렌더
    for kw in ACTIONS:
        action = find_action(kw)
        if not action:
            print(f"[경고] 액션 '{kw}' 못 찾음 — 건너뜀 (bpy.data.actions 이름 확인)")
            continue
        body_arm.animation_data.action = action
        f0, f1 = int(action.frame_range[0]), int(action.frame_range[1])
        if FRAMES_PER_ACTION <= 1:
            frames = [(f0 + f1) // 2]
        else:
            frames = [int(f0 + (f1 - f0) * i / (FRAMES_PER_ACTION - 1))
                      for i in range(FRAMES_PER_ACTION)]
        for idx, f in enumerate(frames):
            bpy.context.scene.frame_set(f)
            suffix = "" if FRAMES_PER_ACTION <= 1 else f"_{idx:02d}"
            name = f"{body.lower()}_{kw.lower()}{suffix}"
            bpy.context.scene.render.filepath = os.path.join(OUT_DIR, name + ".png")
            bpy.ops.render.render(write_still=True)
            print(f"[렌더] {name}.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for b in BODIES:
        try:
            render_body(b)
        except Exception as e:
            print(f"[에러] {b}: {e}")
    print("완료. 결과 폴더:", OUT_DIR)


main()
