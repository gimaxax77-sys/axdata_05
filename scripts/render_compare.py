# 렌더 품질 비교 — 같은 캐릭터를 Workbench(현재) vs EEVEE(개선)로 나란히 굽는다
"""
목적: 조명·그림자·림라이트만 바꿨을 때 체감 차이를 증명.
같은 카메라·같은 프레임으로 엔진/조명만 바꿔 변수를 하나로 고정한다.

실행:
  blender --background --python scripts/render_compare.py

환경변수(선택):
  CMP_BODY_GLB  캐릭터 glb 전체경로
  CMP_ANIM      애니 glb 전체경로(Idle 액션 포함)
  CMP_OUT       출력 폴더
"""
import bpy, os, math
from mathutils import Vector

BODY_GLB = os.environ.get("CMP_BODY_GLB",
    r"D:\.CODE\AXdata\렌더\KayKit_Adventurers_2.0_FREE\KayKit_Adventurers_2.0_FREE\Characters\gltf\Barbarian.glb")
ANIM_GLB = os.environ.get("CMP_ANIM",
    r"D:\.CODE\AXdata\렌더\KayKit_Adventurers_2.0_FREE\KayKit_Adventurers_2.0_FREE\Animations\gltf\Rig_Medium\Rig_Medium_General.glb")
OUT_DIR  = os.environ.get("CMP_OUT", r"D:\.CODE\AXdata\axdata_05\_cmp")
RES = 640
# 입체감이 잘 보이는 3/4 정면(월드 방향). 캐릭터가 +X를 보므로 살짝 앞·옆.
CAM_DIR = (0.65, 0.75, 0.0)
CAM_TILT_DEG = 12.0
PADDING = 1.25


def clear():
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.armatures, bpy.data.actions,
                 bpy.data.cameras, bpy.data.images, bpy.data.lights):
        for d in list(coll):
            if d.users == 0:
                coll.remove(d)


def import_glb(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    return [o for o in bpy.data.objects if o not in before]


def bbox(meshes):
    mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
    for m in meshes:
        for c in m.bound_box:
            w = m.matrix_world @ Vector(c)
            mn = Vector((min(mn.x,w.x),min(mn.y,w.y),min(mn.z,w.z)))
            mx = Vector((max(mx.x,w.x),max(mx.y,w.y),max(mx.z,w.z)))
    return mn, mx


def make_camera(meshes):
    mn, mx = bbox(meshes)
    center = (mn+mx)*0.5
    size = max((mx-mn).x,(mx-mn).y,(mx-mn).z) or 1.0
    cd = bpy.data.cameras.new("Cam"); cd.type='ORTHO'; cd.ortho_scale=size*PADDING
    cam = bpy.data.objects.new("Cam", cd); bpy.context.collection.objects.link(cam)
    d = Vector(CAM_DIR).normalized(); dist=size*3.0
    up = Vector((0,0,math.tan(math.radians(CAM_TILT_DEG))*dist))
    cam.location = center - d*dist + up
    cam.rotation_euler = (center-cam.location).to_track_quat('-Z','Y').to_euler()
    bpy.context.scene.camera = cam
    return center, size


def add_sun(name, direction, energy, angle=0.15, color=(1,1,1)):
    ld = bpy.data.lights.new(name, 'SUN'); ld.energy=energy; ld.angle=angle
    ld.color = color
    lo = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(lo)
    lo.rotation_euler = Vector(direction).normalized().to_track_quat('-Z','Y').to_euler()
    return lo


def apply_idle(arm):
    if not arm.animation_data:
        arm.animation_data_create()
    act = next((a for a in bpy.data.actions if 'idle' in a.name.lower()), None)
    if act:
        arm.animation_data.action = act
        f0,f1 = int(act.frame_range[0]), int(act.frame_range[1])
        bpy.context.scene.frame_set((f0+f1)//2)


def common_render(meshes):
    sc = bpy.context.scene
    sc.render.film_transparent = True
    sc.render.resolution_x = RES; sc.render.resolution_y = RES
    sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'


def render_workbench(path):
    sc = bpy.context.scene
    sc.render.engine='BLENDER_WORKBENCH'
    sc.display.shading.light='FLAT'
    sc.display.shading.color_type='TEXTURE'
    common_render(None)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("[WB]", path)


def render_eevee(center, size, path):
    sc = bpy.context.scene
    sc.render.engine='BLENDER_EEVEE_NEXT'
    # 부드러운 그림자 + 은은한 환경광
    try:
        sc.eevee.use_raytracing = True
    except Exception:
        pass
    sc.eevee.use_shadows = True
    sc.eevee.taa_render_samples = 64
    # 색보정: AgX(채도 죽음) → Standard(게임 아트용 선명)로. 핵심 채도 복구.
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'None'
    # 월드 환경광(그림자만 안 새까맣게 — 색 안 빠지게 낮춤)
    world = bpy.data.worlds.new("W"); sc.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs[0].default_value = (0.42, 0.45, 0.52, 1.0)  # 살짝 차가운 회청
        bg.inputs[1].default_value = 0.18
    # 3점 조명: 키(따뜻·강) / 필(약·차가움·반대) / 림(뒤에서 윤곽)
    add_sun("Key",  (-0.6, -0.7, -0.9), 4.5, angle=0.25, color=(1.0, 0.96, 0.88))
    add_sun("Fill", ( 0.8, -0.4, -0.3), 1.1, angle=0.40, color=(0.85, 0.90, 1.0))
    add_sun("Rim",  ( 0.3,  0.9,  0.2), 5.5, angle=0.15, color=(1.0, 0.98, 0.95))
    common_render(None)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("[EEVEE]", path)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    clear()
    objs = import_glb(BODY_GLB)
    meshes = [o for o in objs if o.type=='MESH']
    arm = next((o for o in objs if o.type=='ARMATURE'), None)
    anim = import_glb(ANIM_GLB)
    for o in anim:
        o.hide_render = True; o.hide_viewport = True
    if arm:
        apply_idle(arm)
    center, size = make_camera(meshes)
    # 1) 현재(Workbench)
    render_workbench(os.path.join(OUT_DIR, "barbarian_A_workbench.png"))
    # 2) 개선(EEVEE)
    render_eevee(center, size, os.path.join(OUT_DIR, "barbarian_B_eevee.png"))
    print("완료:", OUT_DIR)


main()
