# 입력 폴더(input)의 모든 3D 파일을 2D PNG로 렌더 (경로 지정 불필요)
"""
input 폴더에 넣은 .glb / .gltf 파일(하위 폴더 포함)을 전부 렌더해서
out 폴더에 <파일명>.png 로 저장한다. 경로는 render-folder.bat 가 넘겨준다.

- .glb : 자체 완결(그대로 넣으면 됨)
- .gltf: .bin·텍스처가 같이 있어야 하므로, 그 파일이 든 '폴더째' 넣기
- 애니메이션이 들어있으면 중간 프레임(자연스러운 포즈), 없으면 기본 포즈로 렌더
"""
import bpy
import os
import math
from mathutils import Vector

INPUT_DIR = os.environ.get("SPRITE_INPUT") or os.path.join(os.getcwd(), "input")
OUT_DIR = os.environ.get("SPRITE_OUT") or os.path.join(os.getcwd(), "out")
RESOLUTION = int(os.environ.get("SPRITE_RES", "512"))
# 카메라 방향: render-folder.bat 메뉴가 SPRITE_DIR="x,y,z" 로 넘김(없으면 앞모습 Y)
def _parse_dir(s, default=(0.0, 1.0, 0.0)):
    try:
        parts = [float(v) for v in s.split(",")]
        return tuple(parts) if len(parts) == 3 else default
    except Exception:
        return default
CAMERA_DIR = _parse_dir(os.environ.get("SPRITE_DIR", ""))
CAMERA_TILT_DEG = 10.0
PADDING = 1.15


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
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
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
    look = center - cam.location
    cam.rotation_euler = look.to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = cam


def render_file(path):
    clear_scene()
    objs = import_gltf(path)
    meshes = [o for o in objs if o.type == 'MESH']
    if not meshes:
        print(f"[건너뜀] 메시 없음: {path}")
        return
    setup_workbench()
    make_camera(meshes)
    # 애니메이션이 있으면 중간 프레임(자연스러운 포즈)
    arm = next((o for o in objs if o.type == 'ARMATURE'), None)
    if arm and bpy.data.actions:
        act = bpy.data.actions[0]
        if not arm.animation_data:
            arm.animation_data_create()
        arm.animation_data.action = act
        f0, f1 = act.frame_range
        bpy.context.scene.frame_set(int((f0 + f1) // 2))
    name = os.path.splitext(os.path.basename(path))[0].lower()
    bpy.context.scene.render.filepath = os.path.join(OUT_DIR, name + ".png")
    bpy.ops.render.render(write_still=True)
    print(f"[렌더] {name}.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    if not os.path.isdir(INPUT_DIR):
        print(f"[에러] 입력 폴더 없음: {INPUT_DIR}")
        return
    files = []
    for root, _dirs, fs in os.walk(INPUT_DIR):
        for f in sorted(fs):
            if f.lower().endswith((".glb", ".gltf")):
                files.append(os.path.join(root, f))
    if not files:
        print(f"입력 폴더에 3D 파일(.glb/.gltf)이 없습니다: {INPUT_DIR}")
        return
    print(f"{len(files)}개 파일 렌더 시작 →")
    for p in files:
        try:
            render_file(p)
        except Exception as e:
            print(f"[에러] {os.path.basename(p)}: {e}")
    print("완료. 결과:", OUT_DIR)


main()
