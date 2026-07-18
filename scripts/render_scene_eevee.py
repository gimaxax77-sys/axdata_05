# KayKit 던전 → 분위기 있는 전투 배경(EEVEE) — 소품 + 횃불 점광 + 안개감 + 어두운 하늘
"""
기존 render_scene.py(Workbench 평면·빈 무대)의 개선판.
바닥격자+뒷벽+기둥에 더해 횃불(따뜻한 점광)·통·상자를 배치하고 EEVEE 조명으로 굽는다.
전사들이 서는 앞-중앙은 비우고 소품은 뒤·측면에만 둔다(겹침 방지).

실행: blender --background --python scripts/render_scene_eevee.py
env: SCENE_DIR(필수) · SCENE_OUT · SCENE_NAME · SCENE_FLOOR/WALL/COL · SCENE_RES_W/H
     SCENE_TINT = "r,g,b" 월드(하늘) 색 · SCENE_TORCH = "1"(따뜻)|"0"(끔)
"""
import bpy, os
from mathutils import Vector

DIR   = os.environ["SCENE_DIR"]
OUT   = os.environ.get("SCENE_OUT", os.path.join(os.getcwd(), "out_scene"))
NAME  = os.environ.get("SCENE_NAME", "bg")
FLOOR = os.environ.get("SCENE_FLOOR", "floor_dirt_large")
WALL  = os.environ.get("SCENE_WALL", "wall")
COL   = os.environ.get("SCENE_COL", "pillar_decorated")
RW    = int(os.environ.get("SCENE_RES_W", "1024"))
RH    = int(os.environ.get("SCENE_RES_H", "576"))
TINT  = tuple(float(x) for x in os.environ.get("SCENE_TINT", "0.03,0.04,0.08").split(","))
TORCH = os.environ.get("SCENE_TORCH", "1") == "1"


def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    for c in (bpy.data.meshes, bpy.data.images, bpy.data.materials, bpy.data.cameras, bpy.data.objects, bpy.data.lights):
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
    mn = Vector((1e9,)*3); mx = Vector((-1e9,)*3)
    for o in objs:
        if o.type != 'MESH': continue
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            mn = Vector((min(mn.x,w.x),min(mn.y,w.y),min(mn.z,w.z)))
            mx = Vector((max(mx.x,w.x),max(mx.y,w.y),max(mx.z,w.z)))
    return mn, mx


def move(objs, dx, dy, dz=0.0):
    for o in objs:
        if o.parent is None:
            o.location.x += dx; o.location.y += dy; o.location.z += dz


def try_prop(name, x, y, z=0.0):
    try:
        p = imp(name); move(p, x, y, z); return p
    except Exception as e:
        print(f"[소품 생략] {name}: {e}"); return None


def point_light(name, loc, energy, color):
    ld = bpy.data.lights.new(name, 'POINT'); ld.energy = energy; ld.color = color
    ld.shadow_soft_size = 0.4
    lo = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(lo)
    lo.location = Vector(loc)


def sun(name, direction, energy, color):
    ld = bpy.data.lights.new(name, 'SUN'); ld.energy = energy; ld.color = color; ld.angle = 0.3
    lo = bpy.data.objects.new(name, ld); bpy.context.collection.objects.link(lo)
    lo.rotation_euler = Vector(direction).normalized().to_track_quat('-Z','Y').to_euler()


def fog_domain(center, span):
    """씬을 감싸는 볼륨 큐브 → EEVEE 볼류메트릭 안개(공기감)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(center.x, center.y, span*0.35))
    cube = bpy.context.object
    cube.scale = (span*1.4, span*1.4, span*0.9)
    cube.name = "FogDomain"; cube.hide_render = False
    mat = bpy.data.materials.new("Fog"); mat.use_nodes = True
    nt = mat.node_tree; nt.nodes.clear()
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Density'].default_value = 0.018
    vol.inputs['Color'].default_value = (0.5, 0.55, 0.7, 1.0)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(vol.outputs['Volume'], out.inputs['Volume'])
    cube.data.materials.append(mat)


def main():
    os.makedirs(OUT, exist_ok=True)
    clear()
    f0 = imp(FLOOR); mn, mx = footprint(f0)
    tw = (mx.x - mn.x) or 4.0; td = (mx.y - mn.y) or 4.0
    NX, NY = 5, 3  # 앞 깊이 축소(빈 앞바닥 줄임)
    for iy in range(NY):
        for ix in range(NX):
            objs = f0 if (ix == 0 and iy == 0) else imp(FLOOR)
            move(objs, (ix - (NX-1)/2) * tw, (iy - (NY-1)/2) * td)
    backY = ((NY-1)/2) * td + td/2
    try:
        for ix in range(NX):
            w = imp(WALL); move(w, (ix - (NX-1)/2) * tw, backY)
    except Exception as e:
        print("[벽 생략]", e)
    for sx in (-1, 1):
        try_prop(COL, sx * ((NX-1)/2) * tw, backY - td*0.3)

    # 소품 — 뒤·측면에만(앞-중앙 전투 공간은 비움)
    try_prop("barrel_large", -((NX-1)/2)*tw + tw*0.4, backY - td*0.7)
    try_prop("barrel_small", -((NX-1)/2)*tw + tw*0.9, backY - td*0.7)
    try_prop("box_stacked",   ((NX-1)/2)*tw - tw*0.5, backY - td*0.7)
    try_prop("chest",         ((NX-1)/2)*tw - tw*1.1, backY - td*0.8)

    # 횃불 3개(뒤) + 따뜻한 점광 → 분위기의 핵심
    torch_xs = [-tw*1.3, 0.0, tw*1.3]
    for i, tx in enumerate(torch_xs):
        ty = backY - td*0.15
        if TORCH:
            try_prop("torch", tx, ty)
            point_light(f"Torch{i}", (tx, ty, 1.4), 170, (1.0, 0.5, 0.18))  # 균일·강화·따뜻

    sc = bpy.context.scene
    sc.render.engine = 'BLENDER_EEVEE_NEXT'
    try: sc.eevee.use_raytracing = True
    except Exception: pass
    sc.eevee.use_shadows = True
    sc.eevee.taa_render_samples = 96
    sc.view_settings.view_transform = 'Standard'
    sc.view_settings.look = 'Medium High Contrast'
    sc.render.film_transparent = False  # 어두운 하늘로 분위기(투명 아님)
    sc.render.resolution_x = RW; sc.render.resolution_y = RH
    sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'

    world = bpy.data.worlds.new("W"); sc.world = world; world.use_nodes = True
    bg = world.node_tree.nodes.get('Background')
    if bg:
        bg.inputs[0].default_value = (*TINT, 1.0); bg.inputs[1].default_value = 1.0
    # 차가운 달빛(약) — 전체 형태 + 그림자
    sun("Moon", (-0.3, 0.6, -1.0), 1.2, (0.55, 0.65, 1.0))
    # 앞바닥 필라이트 — 전사 서는 앞-중앙을 은은히 밝혀 캐릭터가 묻히지 않게
    point_light("FrontFill", (0.0, -td*0.3, 3.2), 90, (1.0, 0.92, 0.82))

    allobjs = [o for o in bpy.data.objects if o.type == 'MESH']
    mn, mx = footprint(allobjs); center = (mn + mx) * 0.5
    span = max(mx.x - mn.x, mx.y - mn.y, mx.z - mn.z)
    # 안개 도메인(공기감) — 조명 후, 카메라 전에 추가
    fog_domain(center, span)
    cam_data = bpy.data.cameras.new("C"); cam_data.type = 'PERSP'; cam_data.lens = 45
    cam = bpy.data.objects.new("C", cam_data); bpy.context.collection.objects.link(cam)
    # 카메라 타이트 — 더 가깝고 낮게(빈 앞바닥 축소, 무대를 꽉)
    cam.location = Vector((center.x, mn.y - span*0.5, center.z + span*0.42))
    cam.rotation_euler = (center - cam.location).to_track_quat('-Z','Y').to_euler()
    sc.camera = cam

    sc.render.filepath = os.path.join(OUT, NAME + ".png")
    bpy.ops.render.render(write_still=True)
    print("[씬]", NAME + ".png")


main()
