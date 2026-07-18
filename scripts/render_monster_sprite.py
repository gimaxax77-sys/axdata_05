# Quaternius 몬스터(glTF, 애니 내장) → 적 스프라이트 프레임 렌더(EEVEE, 왼쪽 향, 16프레임)
"""
실행: blender --background --python scripts/render_monster_sprite.py
env: MSP_GLTF(필수) · MSP_OUT · MSP_NAME(적 key) · MSP_CLIP(애니 클립 키워드) ·
     MSP_STATE(idle|hit|attack 파일접미) · MSP_FRAMES(기본16) · MSP_RES(기본256) · MSP_DIR("-1,0,0")
출력: <MSP_OUT>/<name>_<state>_NN.png
"""
import bpy, os, math
from mathutils import Vector

GLTF  = os.environ["MSP_GLTF"]
OUT   = os.environ.get("MSP_OUT", os.path.join(os.getcwd(), "out_mon_sprite"))
NAME  = os.environ.get("MSP_NAME", "mon")
CLIP  = os.environ.get("MSP_CLIP", "Idle")
STATE = os.environ.get("MSP_STATE", "idle")
FRAMES = int(os.environ.get("MSP_FRAMES", "16"))
RES   = int(os.environ.get("MSP_RES", "256"))
DIR   = tuple(float(x) for x in os.environ.get("MSP_DIR", "-1,0,0").split(","))
TILT  = 8.0
PAD   = 1.25


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
    bpy.ops.import_scene.gltf(filepath=GLTF)
    objs = list(bpy.data.objects)
    meshes = [o for o in objs if o.type == 'MESH']
    arm = next((o for o in objs if o.type == 'ARMATURE'), None)

    # 애니 클립 적용
    action = next((a for a in bpy.data.actions if CLIP.lower() in a.name.lower()), None)
    if arm and action:
        if not arm.animation_data: arm.animation_data_create()
        arm.animation_data.action = action
        f0, f1 = int(action.frame_range[0]), int(action.frame_range[1])
    else:
        f0 = f1 = 1
        print("[경고] 클립 못 찾음:", CLIP)

    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    try: sc.eevee.use_raytracing = True
    except Exception: pass
    sc.eevee.use_shadows = True
    sc.eevee.taa_render_samples = 48
    sc.view_settings.view_transform = 'Standard'
    sc.render.film_transparent = True
    sc.render.resolution_x = RES; sc.render.resolution_y = RES
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
    world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg: bg.inputs[0].default_value=(0.42,0.45,0.52,1.0); bg.inputs[1].default_value=0.32
    add_sun("Key",(-0.6,-0.7,-0.9),4.2,(1.0,0.96,0.9))
    add_sun("Fill",(0.8,-0.4,-0.3),1.2,(0.85,0.9,1.0))
    add_sun("Rim",(0.3,0.9,0.2),4.5,(1.0,0.98,0.95))

    # 카메라 — 전 프레임 공통 바운딩(첫 프레임 기준)으로 고정(흔들림 방지)
    bpy.context.scene.frame_set(f0)
    mn, mx = bbox(meshes); center=(mn+mx)*0.5
    size = max((mx-mn).x,(mx-mn).y,(mx-mn).z) or 1.0
    cd = bpy.data.cameras.new("C"); cd.type='ORTHO'; cd.ortho_scale=size*PAD
    cam = bpy.data.objects.new("C", cd); bpy.context.collection.objects.link(cam)
    d = Vector(DIR).normalized(); dist=size*3
    up = Vector((0,0,math.tan(math.radians(TILT))*dist))
    cam.location = center - d*dist + up
    cam.rotation_euler = (center-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.camera = cam

    frames = [int(f0 + (f1-f0)*i/(FRAMES-1)) for i in range(FRAMES)] if FRAMES>1 and f1>f0 else [f0]*FRAMES
    for idx, f in enumerate(frames):
        sc.frame_set(f)
        sc.render.filepath = os.path.join(OUT, f"{NAME}_{STATE}_{idx:02d}.png")
        bpy.ops.render.render(write_still=True)
    print(f"[적스프] {NAME}_{STATE} x{FRAMES}")


main()
