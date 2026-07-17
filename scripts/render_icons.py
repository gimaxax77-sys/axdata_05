# KayKit 아이템 gltf → 2D 아이콘 렌더 (Blender 헤드리스, 아마추어 불필요)
"""
자원/장비 등 정적 아이템 gltf를 3/4 각도 2D PNG 아이콘으로 굽는다.
실행: blender --background --python scripts/render_icons.py
env:
  ICON_MODEL  : gltf 전체 경로(필수)
  ICON_OUT    : 결과 폴더
  ICON_NAME   : 저장 파일명(확장자 제외)
  ICON_TINT   : "r,g,b" 텍스처 곱색(옵션, 색 구분용)
  ICON_DIR    : 카메라 방향 "x,y,z"(기본 0.5,1,0.55 = 정면-우-상 3/4)
  ICON_RES    : 해상도(기본 512)
"""
import bpy, os, math
from mathutils import Vector

MODEL = os.environ.get("ICON_MODEL")
OUT   = os.environ.get("ICON_OUT", os.path.join(os.getcwd(), "out_icons"))
NAME  = os.environ.get("ICON_NAME", "icon")
RES   = int(os.environ.get("ICON_RES", "512"))
TILT  = 8.0
PAD   = 1.25
CAM   = tuple(float(x) for x in os.environ.get("ICON_DIR", "0.5,1,0.55").split(","))
TINT  = os.environ.get("ICON_TINT")

def clear():
    bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
    for c in (bpy.data.meshes, bpy.data.images, bpy.data.materials, bpy.data.cameras):
        for d in list(c):
            if d.users == 0: c.remove(d)

def bbox(meshes):
    mn=Vector((1e9,)*3); mx=Vector((-1e9,)*3)
    for m in meshes:
        for cn in m.bound_box:
            w=m.matrix_world@Vector(cn)
            mn=Vector((min(mn.x,w.x),min(mn.y,w.y),min(mn.z,w.z)))
            mx=Vector((max(mx.x,w.x),max(mx.y,w.y),max(mx.z,w.z)))
    return mn,mx

def tint(mult):
    import numpy as np
    for img in bpy.data.images:
        n=len(img.pixels)
        if n==0: continue
        a=np.empty(n,dtype=np.float32); img.pixels.foreach_get(a)
        a[0::4]*=mult[0]; a[1::4]*=mult[1]; a[2::4]*=mult[2]
        img.pixels.foreach_set(a); img.update()

def main():
    os.makedirs(OUT, exist_ok=True)
    clear()
    bpy.ops.import_scene.gltf(filepath=MODEL)
    meshes=[o for o in bpy.data.objects if o.type=='MESH']
    if not meshes:
        print("[경고] 메시 없음:", MODEL); return
    sc=bpy.context.scene
    sc.render.engine='BLENDER_WORKBENCH'
    sc.display.shading.light='STUDIO'
    sc.display.shading.color_type='TEXTURE'
    sc.render.film_transparent=True
    sc.render.resolution_x=RES; sc.render.resolution_y=RES
    sc.render.image_settings.file_format='PNG'; sc.render.image_settings.color_mode='RGBA'
    mn,mx=bbox(meshes); center=(mn+mx)*0.5
    size=max((mx-mn).x,(mx-mn).y,(mx-mn).z) or 1.0
    cd=bpy.data.cameras.new("C"); cd.type='ORTHO'; cd.ortho_scale=size*PAD
    cam=bpy.data.objects.new("C",cd); bpy.context.collection.objects.link(cam)
    d=Vector(CAM).normalized(); dist=size*3.0
    up=Vector((0,0,math.tan(math.radians(TILT))*dist))
    cam.location=center-d*dist+up
    cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.camera=cam
    if TINT:
        try: tint(tuple(float(x) for x in TINT.split(",")))
        except Exception as e: print("[틴트 실패]", e)
    sc.render.filepath=os.path.join(OUT, NAME+".png")
    bpy.ops.render.render(write_still=True)
    print("[아이콘]", NAME+".png")

main()
