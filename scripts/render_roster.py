# 매핑(character_map.csv) 기반: 게임 캐릭터 이름·속성색으로 초상 배치 렌더
"""
게임팩의 character_map.csv 를 읽어, 각 캐릭터를 매핑된 KayKit 몸으로 렌더하고
속성 색을 입혀 <id>.png (게임 캐릭터 이름)으로 저장한다.

CSV 컬럼: ID,이름,칭호,속성,원형,등급,3D몸(KayKit),색상,비고
사용: render-roster.bat (아래 CONFIG 경로 수정)
"""
import bpy
import os
import csv
import math
import numpy as np
from mathutils import Vector

# ===================== CONFIG (KayKit 경로만 필요시 수정) =====================
KAYKIT  = r"D:\.CODE\AXdata\렌더\KayKit_Adventurers_2.0_FREE\KayKit_Adventurers_2.0_FREE"
# MAP_CSV·OUT_DIR 은 이 저장소 폴더 기준 자동. character_map.csv 를 폴더에 넣으면 됨.
_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_CSV = os.path.join(_REPO, "character_map.csv")
OUT_DIR = os.path.join(_REPO, "out_roster")
# =========================================================================
KAYKIT  = os.environ.get("SPRITE_KAYKIT", KAYKIT)
MAP_CSV = os.environ.get("SPRITE_MAP", MAP_CSV)
OUT_DIR = os.environ.get("SPRITE_OUT", OUT_DIR)
CHAR_DIR = KAYKIT + r"\Characters\gltf"
ANIM_FILE = KAYKIT + r"\Animations\gltf\Rig_Medium\Rig_Medium_General.glb"

RESOLUTION = 512
CAMERA_DIR = (0.0, 1.0, 0.0)     # 앞모습
CAMERA_TILT_DEG = 10.0
PADDING = 1.15
TINT = os.environ.get("SPRITE_TINT", "1") != "0"   # 0이면 색 입히기 끔

# 속성 → 텍스처 곱 색(은은한 틴트, 디테일 유지)
ELEMENT_MULT = {
    "FIRE":  (1.00, 0.60, 0.50),
    "WATER": (0.60, 0.75, 1.00),
    "WOOD":  (0.60, 0.90, 0.60),
    "LIGHT": (1.00, 0.98, 0.85),
    "DARK":  (0.75, 0.60, 0.85),
}


def clear_scene():
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
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def mesh_bbox(meshes):
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for m in meshes:
        for corner in m.bound_box:
            w = m.matrix_world @ Vector(corner)
            mn = Vector((min(mn.x, w.x), min(mn.y, w.y), min(mn.z, w.z)))
            mx = Vector((max(mx.x, w.x), max(mx.y, w.y), max(mx.z, w.z)))
    return mn, mx


def setup_workbench():
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
    cam.rotation_euler = (center - cam.location).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam


def tint_images(mult):
    """불러온 텍스처 이미지에 속성 색을 곱해 캐릭터를 물들인다(알파 유지)."""
    for img in bpy.data.images:
        n = len(img.pixels)
        if n == 0:
            continue
        arr = np.empty(n, dtype=np.float32)
        img.pixels.foreach_get(arr)
        arr[0::4] *= mult[0]
        arr[1::4] *= mult[1]
        arr[2::4] *= mult[2]
        img.pixels.foreach_set(arr)
        img.update()


def render_char(cid, body, element):
    clear_scene()
    body_path = os.path.join(CHAR_DIR, body + ".gltf")
    if not os.path.exists(body_path):
        body_path = os.path.join(CHAR_DIR, body + ".glb")
    if not os.path.exists(body_path):
        print(f"[건너뜀] {cid}: 몸 파일 없음 ({body})")
        return
    objs = import_gltf(body_path)
    arm = next((o for o in objs if o.type == 'ARMATURE'), None)
    meshes = [o for o in objs if o.type == 'MESH']
    anim = import_gltf(ANIM_FILE)
    for o in anim:
        o.hide_render = True; o.hide_viewport = True
    setup_workbench()
    make_camera(meshes)
    if arm:
        act = next((a for a in bpy.data.actions if 'idle' in a.name.lower()), None)
        if act:
            if not arm.animation_data:
                arm.animation_data_create()
            arm.animation_data.action = act
            f0, f1 = act.frame_range
            bpy.context.scene.frame_set(int((f0 + f1) // 2))
    if TINT:
        mult = ELEMENT_MULT.get((element or '').upper())
        if mult:
            tint_images(mult)
    bpy.context.scene.render.filepath = os.path.join(OUT_DIR, cid + ".png")
    bpy.ops.render.render(write_still=True)
    print(f"[렌더] {cid}.png  ({body}/{element})")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.exists(MAP_CSV):
        print(f"[에러] 매핑 파일 없음: {MAP_CSV}")
        return
    with open(MAP_CSV, encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        rows = list(reader)
    header = rows[0]
    print(f"{len(rows) - 1}명 렌더 시작 →")
    for r in rows[1:]:
        if len(r) < 7 or not r[0].strip():
            continue
        cid, element, body = r[0].strip(), r[3].strip(), r[6].strip()
        try:
            render_char(cid, body, element)
        except Exception as e:
            print(f"[에러] {cid}: {e}")
    print("완료. 결과:", OUT_DIR)


main()
