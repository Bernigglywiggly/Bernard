"""Curve Short 4: "thousands of virtual copies practise in a simulator" (our 3D illustration, not Unitree footage).

A 64 x 64 grid (4,096, the default num_envs in Unitree's public unitree_rl_gym config) of stylised robots on a neon
simulator floor. Geometry Nodes pick each robot's pose every few frames; the share that has fallen over drops through
the shot, so the grid visibly "learns". Three shots on one timeline, rendered as separate frame ranges:
  C  glimpse   frames   1-70   close on one robot, quick pull back
  E  practise  frames 101-245  medium-high drift, poses flicking, falls getting rarer
  F  reveal    frames 301-436  crane up and back to the whole grid
Usage: blender -b -P s4_sim.py -- --out DIR [--frames 1,120] [--scale 100] [--samples 16]
"""
import argparse
import math
import sys
from math import radians as rad

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--frames", default="")
ap.add_argument("--scale", type=int, default=100)
ap.add_argument("--samples", type=int, default=16)
A = ap.parse_args(argv)

N, SPACING = 64, 1.7
FPS = 30

bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene
SC.render.engine = "BLENDER_EEVEE"
SC.render.fps = FPS
SC.frame_start, SC.frame_end = 1, 436
SC.render.resolution_x, SC.render.resolution_y = 1080, 1920
SC.render.resolution_percentage = A.scale
EE = SC.eevee
EE.taa_render_samples = A.samples
EE.use_raytracing = True
EE.ray_tracing_method = "SCREEN"
EE.ray_tracing_options.use_denoise = True
EE.use_fast_gi = True
EE.use_shadows = True
SC.render.use_motion_blur = True
SC.render.motion_blur_shutter = 0.5
SC.view_settings.view_transform = "AgX"
SC.view_settings.look = "AgX - Punchy"
SC.render.image_settings.file_format = "PNG"

BG = (0.012, 0.004, 0.03)


# ------------------------------------------------------------------------------------------------ materials
def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m


def fogged(m, base_socket_fn):
    """Principled (or emission) shader faded into the background colour with view distance: depth haze."""
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    shader = base_socket_fn(nt)
    cam = nt.nodes.new("ShaderNodeCameraData")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = 14.0
    mr.inputs["From Max"].default_value = 150.0
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = 0.85
    nt.links.new(cam.outputs["View Distance"], mr.inputs["Value"])
    fog = nt.nodes.new("ShaderNodeEmission")
    fog.inputs["Color"].default_value = (*BG, 1)
    fog.inputs["Strength"].default_value = 1.0
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mr.outputs["Result"], mix.inputs["Fac"])
    nt.links.new(shader, mix.inputs[1])
    nt.links.new(fog.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def principled_mat(name, color, rough, metal=0.0, coat=0.0):
    m = new_mat(name)

    def build(nt):
        p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        p.inputs["Base Color"].default_value = (*color, 1)
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = metal
        p.inputs["Coat Weight"].default_value = coat
        return p.outputs["BSDF"]
    fogged(m, build)
    return m


def emit_mat(name, color, strength):
    m = new_mat(name)

    def build(nt):
        for n in list(nt.nodes):
            if n.type == "BSDF_PRINCIPLED":
                nt.nodes.remove(n)
        e = nt.nodes.new("ShaderNodeEmission")
        e.inputs["Color"].default_value = (*color, 1)
        e.inputs["Strength"].default_value = strength
        return e.outputs["Emission"]
    fogged(m, build)
    return m


M_WHITE = principled_mat("robot_white", (0.86, 0.88, 0.92), 0.32, coat=0.4)
M_DARK = principled_mat("robot_dark", (0.03, 0.035, 0.05), 0.45, metal=0.3)
M_VISOR = emit_mat("robot_visor", (0.24, 1.0, 0.95), 7.0)


def floor_mat():
    m = new_mat("floor")

    def build(nt):
        p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        p.inputs["Base Color"].default_value = (0.02, 0.008, 0.05, 1)
        p.inputs["Roughness"].default_value = 0.55
        # grid lines halfway between robots: |fract(x / S + 0.5) - 0.5| small -> line
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])

        def line(axis):
            d = nt.nodes.new("ShaderNodeMath"); d.operation = "DIVIDE"; d.inputs[1].default_value = SPACING
            nt.links.new(sep.outputs[axis], d.inputs[0])
            fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"
            nt.links.new(d.outputs[0], fr.inputs[0])
            sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = 0.5
            nt.links.new(fr.outputs[0], sub.inputs[0])
            ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"
            nt.links.new(sub.outputs[0], ab.inputs[0])
            gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.488
            nt.links.new(ab.outputs[0], gt.inputs[0])
            return gt
        lx, ly = line("X"), line("Y")
        mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
        nt.links.new(lx.outputs[0], mx.inputs[0]); nt.links.new(ly.outputs[0], mx.inputs[1])
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (0.24, 1.0, 0.95, 1)
        em.inputs["Strength"].default_value = 1.6
        add = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(mx.outputs[0], add.inputs["Fac"])
        nt.links.new(p.outputs["BSDF"], add.inputs[1])
        nt.links.new(em.outputs["Emission"], add.inputs[2])
        return add.outputs["Shader"]
    fogged(m, build)
    return m


# ------------------------------------------------------------------------------------------------ robot builder
def capsule(bm, a, b, r, mat, seg=10):
    a, b = Vector(a), Vector(b)
    d = b - a
    L = d.length
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    M = Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4()
    res = bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r * 0.92, depth=L, matrix=M)
    for v in res["verts"]:
        for f in v.link_faces:
            f.material_index = mat


def ball(bm, c, r, mat, u=10, v=6):
    res = bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r, matrix=Matrix.Translation(Vector(c)))
    for vt in res["verts"]:
        for f in vt.link_faces:
            f.material_index = mat


def box(bm, c, size, mat, rot=None):
    M = Matrix.Translation(Vector(c)) @ (rot.to_matrix().to_4x4() if rot else Matrix.Identity(4)) @ Matrix.Diagonal((*size, 1))
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=M)
    for vt in res["verts"]:
        for f in vt.link_faces:
            f.material_index = mat


def build_robot(name, P, coll):
    """P: pose dict of joint angles in degrees. Robot faces -Y; x is its left/right; z up."""
    bm = bmesh.new()
    pel = Vector((0, 0, P.get("pelvis_z", 0.95)))
    lean = Matrix.Rotation(rad(P.get("lean", 0)), 3, "X")          # + leans forward (towards -Y)
    spine_top = pel + lean @ Vector((0, 0, 0.5))
    # torso, pelvis, head
    box(bm, pel + lean @ Vector((0, 0, 0.27)), (0.32, 0.2, 0.4), 0, rot=Euler((rad(P.get("lean", 0)), 0, 0)))
    box(bm, pel + lean @ Vector((0, -0.102, 0.3)), (0.18, 0.02, 0.17), 1, rot=Euler((rad(P.get("lean", 0)), 0, 0)))
    box(bm, pel, (0.28, 0.18, 0.13), 1)
    neck = spine_top + lean @ Vector((0, 0, 0.06))
    capsule(bm, spine_top, neck + lean @ Vector((0, 0, 0.04)), 0.045, 1)
    head_c = neck + lean @ Vector((0, 0, 0.15))
    res = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=1.0,
                                    matrix=Matrix.Translation(head_c) @ Euler((rad(P.get("lean", 0)), 0, 0)).to_matrix().to_4x4() @ Matrix.Diagonal((0.105, 0.11, 0.125, 1)))
    for vt in res["verts"]:
        for f in vt.link_faces:
            f.material_index = 0
    box(bm, head_c + lean @ Vector((0, -0.098, 0.01)), (0.13, 0.03, 0.05), 2, rot=Euler((rad(P.get("lean", 0)), 0, 0)))

    def limb(root, ang_flex, ang_abd, ang_bend, l1, l2, r1, r2, side, leg):
        # flex: + swings forward (towards -Y); abd: + swings outward; bend: + folds the lower segment
        down = Vector((0, 0, -1)) if leg else Vector((0, 0, -1))
        R1 = Matrix.Rotation(rad(-ang_flex), 3, "X") @ Matrix.Rotation(rad(ang_abd * side), 3, "Y")
        R1 = lean @ R1 if not leg else R1
        knee = root + R1 @ (down * l1)
        bend = -ang_bend if leg else ang_bend      # knees fold back, elbows fold forward
        R2 = R1 @ Matrix.Rotation(rad(bend), 3, "X")
        end = knee + R2 @ (down * l2)
        capsule(bm, root, knee, r1, 0)
        capsule(bm, knee, end, r2, 0)
        ball(bm, root, r1 * 1.15, 1)
        ball(bm, knee, r2 * 1.2, 1)
        if leg:
            box(bm, end + R2 @ Vector((0, -0.05, -0.03)), (0.11, 0.24, 0.07), 1, rot=R2.to_euler())
        else:
            ball(bm, end, r2 * 1.25, 1)

    for side, s in (("L", 1), ("R", -1)):
        hip = pel + Vector((0.11 * s, 0, -0.04))
        limb(hip, P.get(f"hip_{side}", 0), P.get(f"hipab_{side}", 4), P.get(f"knee_{side}", 6), 0.42, 0.42, 0.065, 0.055, s, True)
        sh = spine_top + lean @ Vector((0.22 * s, 0, -0.06))
        limb(sh, P.get(f"sh_{side}", 8), P.get(f"shab_{side}", 10), P.get(f"elb_{side}", 15), 0.29, 0.27, 0.05, 0.043, s, False)

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    for m in (M_WHITE, M_DARK, M_VISOR):
        me.materials.append(m)
    whole = P.get("whole")
    if whole:
        ob.rotation_euler = Euler([rad(x) for x in whole])
        bpy.context.view_layer.update()
        me.transform(ob.matrix_basis)
        ob.rotation_euler = (0, 0, 0)
        me.update()
    zmin = min(v.co.z for v in me.vertices)
    me.transform(Matrix.Translation((0, 0, -zmin)))
    for p in me.polygons:
        p.use_smooth = True
    bv = ob.modifiers.new("bevel", "BEVEL")
    bv.width = 0.014
    bv.segments = 2
    bv.limit_method = "ANGLE"
    coll.objects.link(ob)
    return ob


POSES = [
    ("p0_stand", dict()),
    ("p1_guard", dict(pelvis_z=0.86, lean=8, hip_L=28, knee_L=40, hip_R=-12, knee_R=30, sh_L=70, shab_L=18, elb_L=115, sh_R=55,
                      shab_R=22, elb_R=125)),
    ("p2_kick", dict(lean=-14, hip_R=98, knee_R=4, hipab_R=6, knee_L=14, sh_L=-20, shab_L=75, elb_L=20, sh_R=-35, shab_R=40, elb_R=40)),
    ("p3_sidekick", dict(lean=0, hip_R=10, hipab_R=78, knee_R=8, knee_L=18, shab_L=60, sh_L=20, elb_L=70, sh_R=30, shab_R=20, elb_R=110,
                         whole=(0, -14, 0))),
    ("p4_crouch", dict(pelvis_z=0.6, lean=20, hip_L=82, knee_L=118, hip_R=82, knee_R=118, sh_L=60, elb_L=40, sh_R=60, elb_R=40)),
    ("p5_fallen_back", dict(hipab_L=22, hipab_R=22, knee_L=30, shab_L=60, shab_R=40, elb_R=60, sh_L=40, whole=(-90, 0, 18))),
    ("p6_fallen_side", dict(hip_L=40, knee_L=60, hip_R=10, knee_R=20, sh_L=80, elb_L=30, shab_R=30, whole=(0, 88, -30))),
]

poses_coll = bpy.data.collections.new("RobotPoses")
SC.collection.children.link(poses_coll)
pose_objs = [build_robot(n, p, poses_coll) for n, p in POSES]
poses_coll.hide_render = True
poses_coll.hide_viewport = True

# ------------------------------------------------------------------------------------------------ the grid (Geometry Nodes)
grid_me = bpy.data.meshes.new("gridpts")
grid_ob = bpy.data.objects.new("RobotGrid", grid_me)
SC.collection.objects.link(grid_ob)
gn = grid_ob.modifiers.new("robots", "NODES")
ng = bpy.data.node_groups.new("RobotGridGN", "GeometryNodeTree")
gn.node_group = ng
ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
nn, ln = ng.nodes, ng.links
out = nn.new("NodeGroupOutput")
grid = nn.new("GeometryNodeMeshGrid")
grid.inputs["Size X"].default_value = SPACING * (N - 1)
grid.inputs["Size Y"].default_value = SPACING * (N - 1)
grid.inputs["Vertices X"].default_value = N
grid.inputs["Vertices Y"].default_value = N
pts = nn.new("GeometryNodeMeshToPoints")
ln.new(grid.outputs["Mesh"], pts.inputs["Mesh"])
# drop the centre point: the hero robot stands there
pos = nn.new("GeometryNodeInputPosition")
vlen = nn.new("ShaderNodeVectorMath"); vlen.operation = "LENGTH"
ln.new(pos.outputs["Position"], vlen.inputs[0])
near = nn.new("FunctionNodeCompare"); near.data_type = "FLOAT"; near.operation = "LESS_THAN"
near.inputs["B"].default_value = SPACING * 0.5
ln.new(vlen.outputs["Value"], near.inputs["A"])
dele = nn.new("GeometryNodeDeleteGeometry"); dele.domain = "POINT"
ln.new(pts.outputs["Points"], dele.inputs["Geometry"])
ln.new(near.outputs["Result"], dele.inputs["Selection"])

idx = nn.new("GeometryNodeInputIndex")
stime = nn.new("GeometryNodeInputSceneTime")
# per-robot phase so the grid doesn't switch in lockstep
ph = nn.new("FunctionNodeRandomValue"); ph.data_type = "FLOAT"
ph.inputs["Min"].default_value = 0.0; ph.inputs["Max"].default_value = 7.0
ln.new(idx.outputs["Index"], ph.inputs["ID"])
ph.inputs["Seed"].default_value = 3
addp = nn.new("ShaderNodeMath"); addp.operation = "ADD"
ln.new(stime.outputs["Frame"], addp.inputs[0]); ln.new(ph.outputs["Value"], addp.inputs[1])
dvp = nn.new("ShaderNodeMath"); dvp.operation = "DIVIDE"; dvp.inputs[1].default_value = 7.0
ln.new(addp.outputs[0], dvp.inputs[0])
epoch = nn.new("ShaderNodeMath"); epoch.operation = "FLOOR"
ln.new(dvp.outputs[0], epoch.inputs[0])
# id per (robot, epoch)
mul = nn.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 7919.0
ln.new(epoch.outputs[0], mul.inputs[0])
addid = nn.new("ShaderNodeMath"); addid.operation = "ADD"
ln.new(mul.outputs[0], addid.inputs[0]); ln.new(idx.outputs["Index"], addid.inputs[1])
toint = nn.new("FunctionNodeFloatToInt"); toint.rounding_mode = "ROUND"
ln.new(addid.outputs[0], toint.inputs[0])
r1 = nn.new("FunctionNodeRandomValue"); r1.data_type = "FLOAT"; r1.inputs["Seed"].default_value = 11
ln.new(toint.outputs[0], r1.inputs["ID"])
r2 = nn.new("FunctionNodeRandomValue"); r2.data_type = "FLOAT"; r2.inputs["Seed"].default_value = 29
ln.new(toint.outputs[0], r2.inputs["ID"])
# chance of being on the floor falls through the practise shot: 0.55 at frame 100 -> 0.05 at frame 250
pfall = nn.new("ShaderNodeMapRange")
pfall.inputs["From Min"].default_value = 100.0; pfall.inputs["From Max"].default_value = 250.0
pfall.inputs["To Min"].default_value = 0.55; pfall.inputs["To Max"].default_value = 0.05
ln.new(stime.outputs["Frame"], pfall.inputs["Value"])
isfall = nn.new("ShaderNodeMath"); isfall.operation = "LESS_THAN"
ln.new(r1.outputs["Value"], isfall.inputs[0]); ln.new(pfall.outputs["Result"], isfall.inputs[1])
# upright pose 0-4 from r2, fallen pose 5-6 from r2
up_f = nn.new("ShaderNodeMath"); up_f.operation = "MULTIPLY"; up_f.inputs[1].default_value = 4.999
ln.new(r2.outputs["Value"], up_f.inputs[0])
up_i = nn.new("ShaderNodeMath"); up_i.operation = "FLOOR"
ln.new(up_f.outputs[0], up_i.inputs[0])
fa_f = nn.new("ShaderNodeMath"); fa_f.operation = "MULTIPLY"; fa_f.inputs[1].default_value = 1.999
ln.new(r2.outputs["Value"], fa_f.inputs[0])
fa_i = nn.new("ShaderNodeMath"); fa_i.operation = "FLOOR"
ln.new(fa_f.outputs[0], fa_i.inputs[0])
fa_o = nn.new("ShaderNodeMath"); fa_o.operation = "ADD"; fa_o.inputs[1].default_value = 5.0
ln.new(fa_i.outputs[0], fa_o.inputs[0])
pick = nn.new("ShaderNodeMix"); pick.data_type = "FLOAT"
ln.new(isfall.outputs[0], pick.inputs["Factor"])
ln.new(up_i.outputs[0], pick.inputs["A"])
ln.new(fa_o.outputs[0], pick.inputs["B"])
pick_i = nn.new("FunctionNodeFloatToInt"); pick_i.rounding_mode = "ROUND"
ln.new(pick.outputs["Result"], pick_i.inputs[0])
# yaw: mostly facing the camera side, a little scatter
yaw = nn.new("FunctionNodeRandomValue"); yaw.data_type = "FLOAT"
yaw.inputs["Min"].default_value = rad(-35); yaw.inputs["Max"].default_value = rad(35)
yaw.inputs["Seed"].default_value = 5
ln.new(idx.outputs["Index"], yaw.inputs["ID"])
rot = nn.new("ShaderNodeCombineXYZ")
ln.new(yaw.outputs["Value"], rot.inputs["Z"])
ci = nn.new("GeometryNodeCollectionInfo")
ci.inputs["Collection"].default_value = poses_coll
ci.inputs["Separate Children"].default_value = True
ci.inputs["Reset Children"].default_value = True
inst = nn.new("GeometryNodeInstanceOnPoints")
ln.new(dele.outputs["Geometry"], inst.inputs["Points"])
ln.new(ci.outputs["Instances"], inst.inputs["Instance"])
inst.inputs["Pick Instance"].default_value = True
ln.new(pick_i.outputs[0], inst.inputs["Instance Index"])
ln.new(rot.outputs["Vector"], inst.inputs["Rotation"])
ln.new(inst.outputs["Instances"], out.inputs["Geometry"])

# ------------------------------------------------------------------------------------------------ hero robot (centre)
hero_seq = [(1, 2), (40, 1), (58, 0)]      # (frame, pose index): kick, then guard, then stand
hero_objs = []
for i, src in enumerate(pose_objs):
    ob = src.copy()
    ob.data = src.data
    ob.name = f"hero_{i}"
    SC.collection.objects.link(ob)
    hero_objs.append(ob)
for i, ob in enumerate(hero_objs):
    ob.rotation_euler = (0, 0, rad(-12))
    for f in range(1, 437):
        cur = max([p for fr, p in hero_seq if fr <= f] or [2])
        cur = [p for fr, p in hero_seq if fr <= f][-1]
        # in the later shots the hero joins the grid's flicker
        if f > 100:
            cur = (i == ((f // 7 + 3) % 5))
            vis = cur
        else:
            vis = (i == cur)
        ob.hide_render = not vis
        ob.keyframe_insert("hide_render", frame=f)
for ob in hero_objs:
    for fc in (ob.animation_data.action.fcurves if hasattr(ob.animation_data.action, "fcurves") else []):
        for k in fc.keyframe_points:
            k.interpolation = "CONSTANT"

# ------------------------------------------------------------------------------------------------ floor, world, lights
fl_me = bpy.data.meshes.new("floor")
bm = bmesh.new()
bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=SPACING * N * 0.85)
bm.to_mesh(fl_me); bm.free()
floor = bpy.data.objects.new("Floor", fl_me)
fl_me.materials.append(floor_mat())
SC.collection.objects.link(floor)

world = bpy.data.worlds.new("w")
world.use_nodes = True
bgn = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
bgn.inputs["Color"].default_value = (*BG, 1)
bgn.inputs["Strength"].default_value = 1.0
SC.world = world


def light(name, typ, loc, rot, energy, color, size=1.0):
    ld = bpy.data.lights.new(name, typ)
    ld.energy = energy
    ld.color = color
    if typ == "AREA":
        ld.size = size
    if typ == "SUN":
        ld.angle = rad(6)
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = Euler([rad(x) for x in rot])
    SC.collection.objects.link(ob)
    return ob


light("sun", "SUN", (0, 0, 30), (38, 0, -28), 3.2, (1.0, 0.96, 0.92))
light("rim_cyan", "SUN", (0, 0, 30), (-60, 0, 160), 2.2, (0.3, 1.0, 0.95))
light("fill_mag", "SUN", (0, 0, 30), (55, 0, 110), 1.1, (1.0, 0.25, 0.85))

# ------------------------------------------------------------------------------------------------ camera
cam_d = bpy.data.cameras.new("cam")
cam_d.lens = 32
cam_d.clip_end = 400
cam = bpy.data.objects.new("Cam", cam_d)
SC.collection.objects.link(cam)
SC.camera = cam
tgt = bpy.data.objects.new("CamTarget", None)
SC.collection.objects.link(tgt)
tc = cam.constraints.new("TRACK_TO")
tc.target = tgt
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"


def key(ob, frame, loc, interp="BEZIER"):
    ob.location = loc
    ob.keyframe_insert("location", frame=frame)


# C glimpse: from the hero's chest height, pull back and up fast
key(cam, 1, (0.9, -2.6, 1.3)); key(tgt, 1, (0, 0, 1.15))
key(cam, 70, (5.0, -11.0, 5.2)); key(tgt, 70, (0, 0, 0.9))
# E practise: medium-high drift across the grid
key(cam, 100, (5.0, -11.0, 5.2)); key(tgt, 100, (0, 0, 0.9))
key(cam, 101, (-9.0, -16.0, 9.0)); key(tgt, 101, (-1.0, 0.0, 0.5))
key(cam, 245, (-3.0, -15.0, 8.0)); key(tgt, 245, (2.0, 1.0, 0.5))
# F reveal: crane up and back until the whole grid shows
key(cam, 300, (-3.0, -15.0, 8.0)); key(tgt, 300, (2.0, 1.0, 0.5))
key(cam, 301, (0.0, -14.0, 7.0)); key(tgt, 301, (0.0, 2.0, 0.5))
key(cam, 436, (0.0, -46.0, 36.0)); key(tgt, 436, (0.0, 10.0, 0.0))


def set_interp(ob):
    ad = ob.animation_data
    act = ad.action if ad else None
    curves = []
    if act is not None:
        if hasattr(act, "fcurves"):
            curves = list(act.fcurves)
        else:  # Blender 5 layered actions
            for layer in act.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        curves += list(bag.fcurves)
    for fc in curves:
        kps = fc.keyframe_points
        for k in kps:
            k.interpolation = "BEZIER"
            k.easing = "AUTO"
        # hard cuts between shots: constant across each gap
        for k in kps:
            if int(k.co[0]) in (70, 100, 245, 300):
                k.interpolation = "CONSTANT"


set_interp(cam)
set_interp(tgt)
for ob in hero_objs:
    ad = ob.animation_data
    act = ad.action if ad else None
    if act is not None and not hasattr(act, "fcurves"):
        for layer in act.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:
                            k.interpolation = "CONSTANT"

# ------------------------------------------------------------------------------------------------ render
import os  # noqa: E402

os.makedirs(A.out, exist_ok=True)
frames = [int(x) for x in A.frames.split(",") if x] if A.frames else list(range(1, 71)) + list(range(101, 246)) + list(range(301, 437))
for f in frames:
    SC.frame_set(f)
    SC.render.filepath = os.path.join(A.out, f"f_{f:04d}.png")
    bpy.ops.render.render(write_still=True)
print("rendered", len(frames))
