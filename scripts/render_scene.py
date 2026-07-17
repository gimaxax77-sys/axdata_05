# KayKit 던전 모듈 → 전투 배경 씬 렌더 (Blender 헤드리스)
"""
바닥 타일 격자 + 뒷벽 + 기둥을 배치해 넓은 전투 배경을 굽는다(투명 PNG).
실행: blender --background --python scripts/render_scene.py
env:
  SCENE_DIR  : 던전 gltf 폴더(필수)
  SCENE_OUT  : 결과 폴더
  SCENE_NAME : 파일명
  SCENE_FLOOR/SCENE_WALL/SCENE_COL : 각 gltf 파일명(확장자 제외)
  SCENE_RES_W/H : 해상도(기본 1024x576)
"""
import bpy, os, math
from mathutils import Vector

DIR   = os.environ["SCENE_DIR"]
OUT   = os.environ.get("SCENE_OUT", os.path.join(os.getcwd(), "out_scene"))
NAME  = os.environ.get("SCENE_NAME", "bg")
FLOOR = os.environ.get("SCENE_FLOOR", "floor_tile_large")
WALL  = os.environ.get("SCENE_WALL", "wall")
COL   = os.environ.get("SCENE_COL", "column")
RW    = int(os.environ.get("SCENE_RES_W", "1024"))
RH    = int(os.environ.get("SCENE_RES_H", "576"))

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    for c in (bpy.data.meshes, bpy.data.images, bpy.data.materials, bpy.data.cameras, bpy.data.objects):
        for d in list(c):
            if getattr(d, 'users', 0) == 0:
                try: c.remove(d)
                except Exception: pass

def imp(name):
    path = os.path.join(DIR, name + ".gltf")
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]

def footprint(objs):
    mn = Vector((1e9, 1e9, 1e9)); mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        if o.type != 'MESH': continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector((min(mn.x, w.x), min(mn.y, w.y), min(mn.z, w.z)))
            mx = Vector((max(mx.x, w.x), max(mx.y, w.y), max(mx.z, w.z)))
    return mn, mx

def move(objs, dx, dy, dz=0.0):
    for o in objs:
        if o.parent is None:
            o.location.x += dx; o.location.y += dy; o.location.z += dz

def main():
    os.makedirs(OUT, exist_ok=True)
    clear()
    # 1) 바닥 한 장으로 크기 측정
    f0 = imp(FLOOR); mn, mx = footprint(f0)
    tw = (mx.x - mn.x) or 4.0; td = (mx.y - mn.y) or 4.0
    # 2) 바닥 격자 5x4 (원점 중심)
    NX, NY = 5, 4
    for iy in range(NY):
        for ix in range(NX):
            if ix == 0 and iy == 0: objs = f0
            else: objs = imp(FLOOR)
            move(objs, (ix - (NX-1)/2) * tw, (iy - (NY-1)/2) * td)
    # 3) 뒷벽 한 줄(맨 뒤 = +Y)
    backY = ((NY-1)/2) * td + td/2
    try:
        for ix in range(NX):
            w = imp(WALL); wmn, wmx = footprint(w); ww = (wmx.x - wmn.x) or tw
            move(w, (ix - (NX-1)/2) * tw, backY)
    except Exception as e:
        print("[벽 생략]", e)
    # 4) 기둥 뒤 양 코너
    try:
        for sx in (-1, 1):
            c = imp(COL); move(c, sx * ((NX-1)/2) * tw, backY - td*0.3)
    except Exception as e:
        print("[기둥 생략]", e)

    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_WORKBENCH'
    sc.display.shading.light = 'STUDIO'
    sc.display.shading.color_type = 'TEXTURE'
    sc.render.film_transparent = True
    sc.render.resolution_x = RW; sc.render.resolution_y = RH
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

    # 카메라 — 앞(+Y 아님, -Y쪽)에서 위로 살짝 내려다보며 무대를 담는다
    allobjs = [o for o in bpy.data.objects if o.type == 'MESH']
    mn, mx = footprint(allobjs); center = (mn + mx) * 0.5
    span = max(mx.x - mn.x, mx.y - mn.y, mx.z - mn.z)
    cam_data = bpy.data.cameras.new("C"); cam_data.type = 'PERSP'; cam_data.lens = 40
    cam = bpy.data.objects.new("C", cam_data); bpy.context.collection.objects.link(cam)
    # 앞(-Y) + 위(+Z)에서 중심 바라봄
    cam.location = Vector((center.x, mn.y - span*0.7, center.z + span*0.6))
    cam.rotation_euler = (center - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.camera = cam

    sc.render.filepath = os.path.join(OUT, NAME + ".png")
    bpy.ops.render.render(write_still=True)
    print("[씬]", NAME + ".png")

main()
