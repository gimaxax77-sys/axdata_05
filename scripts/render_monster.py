# Monster Pack(FBX) → EEVEE 아이콘 렌더 — 펫·가디언 이모지 대체용 정사각 PNG
"""
실행: blender --background --python scripts/render_monster.py
env: MON_FBX(필수) · MON_OUT · MON_NAME · MON_RES(기본 256) · MON_TINT("r,g,b" 색조, 선택)
카메라 3/4 정면, EEVEE 3점 조명(캐릭터와 톤 통일), 투명 배경.
"""
import bpy, os, math
from mathutils import Vector

FBX  = os.environ["MON_FBX"]
OUT  = os.environ.get("MON_OUT", os.path.join(os.getcwd(), "out_monster"))
NAME = os.environ.get("MON_NAME", "monster")
RES  = int(os.environ.get("MON_RES", "256"))
TINT = os.environ.get("MON_TINT")  # "1,0.6,0.6" 처럼 곱색조(선택)
CAM_DIR = (0.55, 0.8, 0.0)
TILT = 10.0
PAD = 1.3


def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    for c in (bpy.data.meshes, bpy.data.armatures, bpy.data.actions, bpy.data.cameras,
              bpy.data.images, bpy.data.lights, bpy.data.materials, bpy.data.objects):
        for d in list(c):
            if getattr(d, 'users', 0) == 0:
                try: c.remove(d)
                except Exception: pass


def bbox(meshes):
    mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
    for m in meshes:
        for c in m.bound_box:
            w = m.matrix_world @ Vector(c)
            mn = Vector((min(mn.x,w.x),min(mn.y,w.y),min(mn.z,w.z)))
            mx = Vector((max(mx.x,w.x),max(mx.y,w.y),max(mx.z,w.z)))
    return mn, mx


def add_sun(name, d, energy, color):
    ld = bpy.data.lights.new(name, 'SUN'); ld.energy=energy; ld.angle=0.25; ld.color=color
    lo = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(lo)
    lo.rotation_euler = Vector(d).normalized().to_track_quat('-Z','Y').to_euler()


def main():
    os.makedirs(OUT, exist_ok=True)
    clear()
    before = set(bpy.data.objects)
    ext = os.path.splitext(FBX)[1].lower()
    if ext == '.obj':
        bpy.ops.wm.obj_import(filepath=FBX)  # .mtl 색상 반영
    elif ext in ('.gltf', '.glb'):
        bpy.ops.import_scene.gltf(filepath=FBX)  # 임베드 지오메트리·재질색
    else:
        bpy.ops.import_scene.fbx(filepath=FBX)
    objs = [o for o in bpy.data.objects if o not in before]
    meshes = [o for o in objs if o.type == 'MESH']
    if not meshes:
        print("[경고] 메시 없음:", FBX); return
    # 첫 프레임(기본 포즈) 고정 — 애니 FBX는 재생 안 함
    bpy.context.scene.frame_set(1)

    # 색조(선택) — 모든 재질 Base Color를 곱색조로(변형 아이콘용)
    if TINT:
        r, g, b = (float(x) for x in TINT.split(","))
        for mat in bpy.data.materials:
            if not mat.use_nodes: continue
            bsdf = mat.node_tree.nodes.get('Principled BSDF')
            if bsdf:
                col = bsdf.inputs['Base Color'].default_value
                bsdf.inputs['Base Color'].default_value = (col[0]*r, col[1]*g, col[2]*b, col[3])

    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    try: sc.eevee.use_raytracing = True
    except Exception: pass
    sc.eevee.use_shadows = True
    sc.eevee.taa_render_samples = 64
    sc.view_settings.view_transform = 'Standard'
    sc.render.film_transparent = True
    sc.render.resolution_x = RES; sc.render.resolution_y = RES
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

    world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs[0].default_value = (0.42, 0.45, 0.52, 1.0); bg.inputs[1].default_value = 0.35
    add_sun("Key",  (-0.6, -0.7, -0.9), 4.2, (1.0, 0.96, 0.9))
    add_sun("Fill", ( 0.8, -0.4, -0.3), 1.2, (0.85, 0.9, 1.0))
    add_sun("Rim",  ( 0.3,  0.9,  0.2), 4.5, (1.0, 0.98, 0.95))

    mn, mx = bbox(meshes); center = (mn+mx)*0.5
    size = max((mx-mn).x,(mx-mn).y,(mx-mn).z) or 1.0
    cd = bpy.data.cameras.new("C"); cd.type='ORTHO'; cd.ortho_scale=size*PAD
    cam = bpy.data.objects.new("C", cd); bpy.context.collection.objects.link(cam)
    d = Vector(CAM_DIR).normalized(); dist=size*3
    up = Vector((0,0,math.tan(math.radians(TILT))*dist))
    cam.location = center - d*dist + up
    cam.rotation_euler = (center-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.camera = cam

    sc.render.filepath = os.path.join(OUT, NAME + ".png")
    bpy.ops.render.render(write_still=True)
    print("[몬스터]", NAME + ".png")


main()
