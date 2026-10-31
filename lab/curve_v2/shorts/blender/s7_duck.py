"""Curve Short 7 (Microduck): our own 3D "sim duck" (not Pollen's meshes, which are CC BY-NC-SA).

Proportions come from the Apache-2.0 MJCF in pollen-robotics/microduck_rl (robot_walk.xml, forward kinematics at the
HOME pose): hips at 10 cm, neck base at 15 cm, head top at about 27 cm, head about 12 cm long with the camera "eye" at
the front, reverse-bending knees. Everything is in millimetres, then scaled by S (1 Blender unit = 10 cm).

Shots (each its own frame range and camera):
  poses    one still per pose, for checking the design
  grid     64 x 64 ducks on a simulator floor (4,096: the num-envs in Pollen's training command), poses flicking,
           falls getting rarer; drift, then crane up to the whole grid                                  frames 1-130
  tripod   one duck propped on its head and both feet (the "head-tripod" loophole in Pollen's AGENTS.md); slow orbit
                                                                                                         frames 1-150
  lineup   five "wrong bodies" in a row: heavier, off balance, slippery, low battery, shoved; camera trucks along
                                                                                                         frames 1-220
Usage: blender -b -P s7_duck.py -- --shot grid --out DIR [--frames 1,60] [--scale 100] [--samples 16]
"""
import argparse
import json
import math
import os
import sys
from math import radians as rad

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--out", required=True)
ap.add_argument("--shot", default="poses")
ap.add_argument("--frames", default="")
ap.add_argument("--scale", type=int, default=100)
ap.add_argument("--samples", type=int, default=16)
ap.add_argument("--cam", default="6.2,-6.8,3.0")      # poses shot only
ap.add_argument("--yaw", type=float, default=-30)     # poses shot only
ap.add_argument("--only", default="")                 # poses shot only: comma list of pose names
A = ap.parse_args(argv)

S = 0.01            # mm -> Blender units
N, SPACING = 64, 3.4
FPS = 30
BG = (0.004, 0.012, 0.035)

bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene
SC.render.engine = "BLENDER_EEVEE"
SC.render.fps = FPS
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


# ------------------------------------------------------------------------------------------------ materials
def new_mat(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    return m


FOG = {"grid": (60.0, 520.0, 0.9)}.get(A.shot, (24.0, 160.0, 0.88))


def fogged(m, build, near=FOG[0], far=FOG[1], top=FOG[2]):
    """Shader faded into the background colour with view distance: depth haze over the big grid."""
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    shader = build(nt)
    cam = nt.nodes.new("ShaderNodeCameraData")
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.inputs["From Min"].default_value = near
    mr.inputs["From Max"].default_value = far
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = top
    nt.links.new(cam.outputs["View Distance"], mr.inputs["Value"])
    fog = nt.nodes.new("ShaderNodeEmission")
    fog.inputs["Color"].default_value = (*BG, 1)
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mr.outputs["Result"], mix.inputs["Fac"])
    nt.links.new(shader, mix.inputs[1])
    nt.links.new(fog.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def principled(name, color, rough, metal=0.0, coat=0.0, emit=None, emit_strength=0.0):
    m = new_mat(name)

    def build(nt):
        p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        p.inputs["Base Color"].default_value = (*color, 1)
        p.inputs["Roughness"].default_value = rough
        p.inputs["Metallic"].default_value = metal
        p.inputs["Coat Weight"].default_value = coat
        if emit:
            p.inputs["Emission Color"].default_value = (*emit, 1)
            p.inputs["Emission Strength"].default_value = emit_strength
        return p.outputs["BSDF"]
    fogged(m, build)
    return m


M_SHELL = principled("shell", (0.88, 0.89, 0.9), 0.38, coat=0.5)
M_DARK = principled("servo", (0.035, 0.038, 0.045), 0.5, metal=0.2)
M_ORANGE = principled("beak", (1.0, 0.36, 0.05), 0.42, coat=0.3)
M_LENS = principled("lens", (0.005, 0.005, 0.008), 0.08, coat=1.0)
M_RING = principled("eye_ring", (0.85, 1.0, 0.0), 0.35, emit=(0.85, 1.0, 0.0), emit_strength=1.2)
M_TRUNK = principled("trunk_shell", (0.88, 0.89, 0.9), 0.38, coat=0.5)     # same look as the shell; its own slot so one shot can x-ray it
MATS = (M_SHELL, M_DARK, M_ORANGE, M_LENS, M_RING, M_TRUNK)
WHITE, DARK, ORANGE, LENS, RING, TRUNK = range(6)


# ------------------------------------------------------------------------------------------------ geometry helpers
def _tag(bm, n0, res, mat, part, parts):
    """Material on the new faces; the part keeps an index range (Blender 5 BMesh may move elements, so no refs)."""
    for v in res["verts"]:
        for f in v.link_faces:
            f.material_index = mat
    parts.setdefault(part, []).append((n0, len(bm.verts)))


def capsule(bm, a, b, r, mat, part, parts, seg=14):
    a, b = Vector(a), Vector(b)
    d = b - a
    q = Vector((0, 0, 1)).rotation_difference(d.normalized())
    M = Matrix.Translation((a + b) / 2) @ q.to_matrix().to_4x4()
    n0 = len(bm.verts)
    _tag(bm, n0, bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r, depth=d.length, matrix=M), mat, part, parts)
    n0 = len(bm.verts)
    _tag(bm, n0, bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=8, radius=r, matrix=Matrix.Translation(a)), mat, part, parts)
    n0 = len(bm.verts)
    _tag(bm, n0, bmesh.ops.create_uvsphere(bm, u_segments=seg, v_segments=8, radius=r, matrix=Matrix.Translation(b)), mat, part, parts)


def ball(bm, c, r, mat, part, parts, u=14, v=9):
    n0 = len(bm.verts)
    _tag(bm, n0, bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=r, matrix=Matrix.Translation(Vector(c))), mat, part, parts)


def rbox(bm, c, size, mat, part, parts, R=None, round_=0.35):
    """A rounded box: an icosphere mapped onto a superellipsoid (round_ 1 = ellipsoid, towards 0 = sharper box)."""
    M = Matrix.Translation(Vector(c)) @ (R.to_4x4() if R is not None else Matrix.Identity(4))
    e = 0.22 + 0.78 * round_ * round_
    n0 = len(bm.verts)
    res = bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    sx, sy, sz = size
    for v in res["verts"]:
        p = v.co
        q = Vector([math.copysign(abs(a) ** e, a) for a in p])
        v.co = M @ Vector((q.x * sx / 2, q.y * sy / 2, q.z * sz / 2))
    _tag(bm, n0, res, mat, part, parts)


def disc(bm, c, normal, r, depth, mat, part, parts, seg=28):
    q = Vector((0, 0, 1)).rotation_difference(Vector(normal).normalized())
    M = Matrix.Translation(Vector(c)) @ q.to_matrix().to_4x4()
    n0 = len(bm.verts)
    _tag(bm, n0, bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=seg, radius1=r, radius2=r, depth=depth, matrix=M), mat, part, parts)


# ------------------------------------------------------------------------------------------------ the duck
HOME = dict(thigh_L=-32, bend_L=56, foot_L=0, hipab_L=0, thigh_R=-32, bend_R=56, foot_R=0, hipab_R=0,
            neck=-20, head=20, head_yaw=0, jaw=0, whole=(0, 0, 0), roll_fix=0.0)
L1, L2, L3 = 42.0, 46.0, 21.0     # thigh, shank, ankle-to-sole (mm)


def Ry(deg):
    return Matrix.Rotation(rad(deg), 3, "Y")


def Rx(deg):
    return Matrix.Rotation(rad(deg), 3, "X")


def build_duck(P0):
    """Returns (bmesh, parts dict of verts by part). Frame: x forward, y left, z up, mm; trunk origin at (0,0,120)."""
    P = dict(HOME)
    P.update(P0)
    bm = bmesh.new()
    parts = {}
    # trunk
    rbox(bm, (-2, 0, 124), (78, 66, 58), TRUNK, "trunk", parts, round_=0.55)
    rbox(bm, (-4, 0, 99), (52, 46, 14), DARK, "trunk", parts, round_=0.4)            # belly plate between the hips
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        H = Vector((4, 40 * s, 102))
        ab = Rx(P[f"hipab_{side}"] * s)      # + splays the leg outward
        t1 = P[f"thigh_{side}"]
        t2 = t1 + P[f"bend_{side}"]
        dthigh = ab @ Vector((math.sin(rad(t1)), 0, -math.cos(rad(t1))))
        dshank = ab @ Vector((math.sin(rad(t2)), 0, -math.cos(rad(t2))))
        K = H + dthigh * L1
        An = K + dshank * L2
        rbox(bm, H + Vector((0, -4 * s, 2)), (30, 22, 34), DARK, f"hip{side}", parts, round_=0.4)    # hip servo block
        capsule(bm, H, K, 12.5, WHITE, f"leg{side}", parts)
        ball(bm, K, 10.5, DARK, f"leg{side}", parts)
        capsule(bm, K, An, 8.5, DARK, f"leg{side}", parts)
        # foot: plate pitch is set in the trunk frame (0 = level with the trunk)
        fp = Ry(-P[f"foot_{side}"])   # + toes up
        sole = An + fp @ Vector((0, 0, -L3))
        ball(bm, An, 9.0, DARK, f"foot{side}", parts)
        capsule(bm, An, sole + fp @ Vector((0, 0, 6)), 7.0, DARK, f"foot{side}", parts)
        rbox(bm, sole + fp @ Vector((10, 0, 4.5)), (68, 36, 9), ORANGE, f"foot{side}", parts, R=fp, round_=0.5)
    # neck and head
    N0 = Vector((26, 0, 152))
    Rn = Ry(P["neck"])                      # + leans the neck forward
    N1 = N0 + Rn @ Vector((0, 0, 50))
    capsule(bm, N0, N1, 8.5, DARK, "neck", parts)
    ball(bm, N0, 12, DARK, "neck", parts)
    Rh = Rn @ Ry(P["head"]) @ Matrix.Rotation(rad(P["head_yaw"]), 3, "Z")   # head pitch (+ nose down), then yaw

    def hp(x, y, z):
        return N1 + Rh @ Vector((x, y, z))
    capsule(bm, N1, hp(0, 0, 18), 9.5, DARK, "head", parts)                                    # yaw/roll joint stub
    rbox(bm, hp(-4, 0, 42), (124, 70, 58), WHITE, "head", parts, R=Rh, round_=0.6)
    rbox(bm, hp(-14, 0, 70), (84, 56, 8), ORANGE, "head", parts, R=Rh, round_=0.6)             # cap stripe
    eye_n = Rh @ Vector((1, 0, 0))
    disc(bm, hp(58.5, 0, 50), eye_n, 19.0, 5.0, RING, "head", parts)
    disc(bm, hp(61.5, 0, 50), eye_n, 13.0, 3.0, LENS, "head", parts)
    ball(bm, hp(62.0, 4.5, 54.5), 3.2, WHITE, "head", parts, u=8, v=6)                        # glint
    # beak: upper half fixed, lower jaw hinged at the back of the beak
    rbox(bm, hp(52, 0, 25), (46, 44, 10), ORANGE, "head", parts, R=Rh, round_=0.6)
    Rj = Rh @ Ry(P["jaw"])
    jh = hp(32, 0, 20)
    rbox(bm, jh + Rj @ Vector((20, 0, -2)), (42, 40, 7), ORANGE, "head", parts, R=Rj, round_=0.6)
    ball(bm, hp(-10, 37, 30), 9, DARK, "head", parts)       # head servo horns
    ball(bm, hp(-10, -37, 30), 9, DARK, "head", parts)
    return bm, parts, P


def pose_points(bm, parts, M):
    bm.verts.ensure_lookup_table()
    return {k: [M @ bm.verts[i].co for a, b in rs for i in range(a, b)] for k, rs in parts.items()}


CONTACTS = {}
TOPS = {}


def solve_pitch(bm, parts, P, solve):
    """Extra forward pitch (deg) at which the lowest points of two contact groups sit at the same height."""
    base = Euler([rad(x) for x in P.get("whole", (0, 0, 0))]).to_matrix()
    pivot = Vector((0, 0, 120))
    ga, gb = solve
    best = None
    for i in range(0, 1201):
        ang = i * 0.1
        Mt = Matrix.Translation(pivot) @ (Ry(ang) @ base).to_4x4() @ Matrix.Translation(-pivot)
        pts = pose_points(bm, parts, Mt)
        za = min(p.z for p in pts[ga])
        zb = max(min(p.z for p in pts[g]) for g in gb)
        if best is None or abs(za - zb) < best[0]:
            best = (abs(za - zb), ang)
    return best[1]


def finish(name, bm, parts, P, coll):
    """Rotate the whole duck about the trunk origin, drop it to z=0, scale to scene units; record each part's lowest point."""
    base = Euler([rad(x) for x in P.get("whole", (0, 0, 0))]).to_matrix()
    pivot = Vector((0, 0, 120))
    M = Matrix.Translation(pivot) @ base.to_4x4() @ Matrix.Translation(-pivot)
    bmesh.ops.transform(bm, matrix=M, verts=bm.verts)
    zmin = min(v.co.z for v in bm.verts)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, -zmin)), verts=bm.verts)
    bmesh.ops.scale(bm, vec=(S, S, S), verts=bm.verts)
    pts = pose_points(bm, parts, Matrix.Identity(4))
    CONTACTS[name] = {k: min(v, key=lambda q: q.z).copy() for k, v in pts.items()}
    TOPS[name] = {k: max(v, key=lambda q: q.z).copy() for k, v in pts.items()}
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    for m in MATS:
        me.materials.append(m)
    ob = bpy.data.objects.new(name, me)
    coll.objects.link(ob)
    return ob


POSES = [
    ("p0_stand", dict(), None),
    ("p1_step_l", dict(thigh_L=-12, bend_L=50, foot_L=-6, thigh_R=-44, bend_R=60, foot_R=6, whole=(0, 4, 0)), None),
    ("p2_step_r", dict(thigh_R=-12, bend_R=50, foot_R=-6, thigh_L=-44, bend_L=60, foot_L=6, whole=(0, 4, 0)), None),
    ("p3_crouch", dict(thigh_L=-62, bend_L=110, thigh_R=-58, bend_R=106, foot_L=-4, foot_R=-4, neck=10, head=-6, whole=(0, 10, 0)), None),
    ("p4_face_down", dict(thigh_L=-10, bend_L=30, thigh_R=4, bend_R=20, neck=30, head=10, jaw=18, whole=(0, 88, 8)), None),
    ("p5_on_back", dict(thigh_L=30, bend_L=60, thigh_R=50, bend_R=40, foot_L=30, foot_R=20, neck=-40, head=-10, whole=(0, -95, -10)), None),
    ("p6_on_side", dict(thigh_L=-20, bend_L=70, thigh_R=10, bend_R=40, hipab_R=20, neck=-10, head=10, whole=(84, 0, 20)), None),
    ("p7_crash_sit", dict(thigh_L=70, bend_L=-20, thigh_R=74, bend_R=-26, foot_L=40, foot_R=36, neck=-10, head=12, whole=(0, -18, 0)), None),
    ("p8_head_tripod", dict(thigh_L=34, bend_L=24, thigh_R=34, bend_R=24, foot_L=-40, foot_R=-40, hipab_L=10, hipab_R=10,
                            neck=70, head=36, head_yaw=-90, whole=(0, 0, 0)), ("head", ("footL", "footR"))),
    ("p9_split", dict(thigh_L=-14, bend_L=26, thigh_R=-14, bend_R=26, hipab_L=24, hipab_R=24, foot_L=0, foot_R=0, neck=-6, head=8), None),
]

poses_coll = bpy.data.collections.new("DuckPoses")
SC.collection.children.link(poses_coll)
pose_objs = []
for name, P0, solve in POSES:
    if solve:
        # the feet must end up flat on the floor after the forward pitch, so iterate: pitch -> feet -> pitch
        pitch = 70.0
        for _ in range(4):
            P0 = dict(P0, foot_L=pitch, foot_R=pitch, whole=(0, 0, 0))
            bm, parts, P = build_duck(P0)
            pitch = solve_pitch(bm, parts, P, solve)
            bm.free()
        print(f"{name}: pitch {pitch:.1f} deg")
        P0 = dict(P0, foot_L=pitch, foot_R=pitch, whole=(0, pitch, 0))
    bm, parts, P = build_duck(P0)
    ob = finish(name, bm, parts, P, poses_coll)
    if solve:
        print(name, {k: tuple(round(x, 3) for x in CONTACTS[name][k]) for k in ("head", "footL", "footR")})
    sub = ob.modifiers.new("subd", "SUBSURF")
    sub.levels = 1
    sub.render_levels = 1
    pose_objs.append(ob)


# ------------------------------------------------------------------------------------------------ floor, world, lights
def floor_mat(gloss=False):
    m = new_mat("floor_gloss" if gloss else "floor")

    def build(nt):
        p = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        p.inputs["Roughness"].default_value = 0.06 if gloss else 0.5
        tc = nt.nodes.new("ShaderNodeTexCoord")
        ck = nt.nodes.new("ShaderNodeTexChecker")
        ck.inputs["Scale"].default_value = 1.0
        ck.inputs["Color1"].default_value = (0.03, 0.08, 0.2, 1) if not gloss else (0.25, 0.55, 0.75, 1)
        ck.inputs["Color2"].default_value = (0.012, 0.035, 0.1, 1) if not gloss else (0.12, 0.35, 0.55, 1)
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Scale"].default_value = (1 / (SPACING / 2),) * 3
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], ck.inputs["Vector"])
        nt.links.new(ck.outputs["Color"], p.inputs["Base Color"])
        # thin cyan lines on the tile edges
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(mp.outputs["Vector"], sep.inputs["Vector"])

        def line(axis):
            fr = nt.nodes.new("ShaderNodeMath"); fr.operation = "FRACT"
            nt.links.new(sep.outputs[axis], fr.inputs[0])
            sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"; sub.inputs[1].default_value = 0.5
            nt.links.new(fr.outputs[0], sub.inputs[0])
            ab = nt.nodes.new("ShaderNodeMath"); ab.operation = "ABSOLUTE"
            nt.links.new(sub.outputs[0], ab.inputs[0])
            gt = nt.nodes.new("ShaderNodeMath"); gt.operation = "GREATER_THAN"; gt.inputs[1].default_value = 0.493
            nt.links.new(ab.outputs[0], gt.inputs[0])
            return gt
        lx, ly = line("X"), line("Y")
        mx = nt.nodes.new("ShaderNodeMath"); mx.operation = "MAXIMUM"
        nt.links.new(lx.outputs[0], mx.inputs[0]); nt.links.new(ly.outputs[0], mx.inputs[1])
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (0.25, 0.9, 1.0, 1)
        em.inputs["Strength"].default_value = 0.9
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(mx.outputs[0], mix.inputs["Fac"])
        nt.links.new(p.outputs["BSDF"], mix.inputs[1])
        nt.links.new(em.outputs["Emission"], mix.inputs[2])
        return mix.outputs["Shader"]
    fogged(m, build)
    return m


def add_floor(size, loc=(0, 0, 0), gloss=False, name="Floor"):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=size)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    me.materials.append(floor_mat(gloss))
    SC.collection.objects.link(ob)
    return ob


world = bpy.data.worlds.new("w")
world.use_nodes = True
bgn = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
bgn.inputs["Color"].default_value = (*BG, 1)
SC.world = world


def light(name, typ, rot, energy, color, loc=(0, 0, 30), size=1.0):
    ld = bpy.data.lights.new(name, typ)
    ld.energy = energy
    ld.color = color
    if typ == "SUN":
        ld.angle = rad(5)
    else:
        ld.size = size
    ob = bpy.data.objects.new(name, ld)
    ob.location = loc
    ob.rotation_euler = Euler([rad(x) for x in rot])
    SC.collection.objects.link(ob)
    return ob


light("key", "SUN", (40, 0, -35), 3.4, (1.0, 0.96, 0.9))
light("rim", "SUN", (-62, 0, 165), 2.6, (0.35, 0.9, 1.0))
light("fill", "SUN", (60, 0, 120), 0.7, (0.6, 0.7, 1.0))

cam_d = bpy.data.cameras.new("cam")
cam_d.clip_start = 0.05
cam_d.clip_end = 600
cam = bpy.data.objects.new("Cam", cam_d)
SC.collection.objects.link(cam)
SC.camera = cam
tgt = bpy.data.objects.new("CamTarget", None)
SC.collection.objects.link(tgt)
tc = cam.constraints.new("TRACK_TO")
tc.target = tgt
tc.track_axis = "TRACK_NEGATIVE_Z"
tc.up_axis = "UP_Y"


def key(ob, frame, loc):
    ob.location = loc
    ob.keyframe_insert("location", frame=frame)


def all_fcurves(ob):
    ad = ob.animation_data
    act = ad.action if ad else None
    if act is None:
        return []
    if hasattr(act, "fcurves"):
        return list(act.fcurves)
    out = []
    for layer in act.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                out += list(bag.fcurves)
    return out


def interp(ob, mode="BEZIER"):
    for fc in all_fcurves(ob):
        for k in fc.keyframe_points:
            k.interpolation = mode


def render(frames):
    os.makedirs(A.out, exist_ok=True)
    for f in frames:
        SC.frame_set(f)
        SC.render.filepath = os.path.join(A.out, f"f_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
    print("rendered", len(frames))


def frames_arg(default):
    return [int(x) for x in A.frames.split(",") if x] if A.frames else default


# ------------------------------------------------------------------------------------------------ shot: poses (design check)
if A.shot == "poses":
    add_floor(40)
    SC.render.resolution_x, SC.render.resolution_y = 900, 900
    SC.render.use_motion_blur = False
    cam_d.lens = 50
    for i, ob in enumerate(pose_objs):
        ob.location = (0, 0, 0)
        ob.rotation_euler = (0, 0, rad(A.yaw))
    poses_coll.hide_render = False
    only = [x for x in A.only.split(",") if x]
    for i, ob in enumerate(pose_objs):
        if only and ob.name not in only:
            continue
        for j, o2 in enumerate(pose_objs):
            o2.hide_render = j != i
        key(cam, 1, tuple(float(x) for x in A.cam.split(",")))
        key(tgt, 1, (0, 0, 1.0))
        SC.frame_set(1)
        os.makedirs(A.out, exist_ok=True)
        SC.render.filepath = os.path.join(A.out, f"{ob.name}.png")
        bpy.ops.render.render(write_still=True)
    sys.exit(0)

poses_coll.hide_render = True
poses_coll.hide_viewport = True


# ------------------------------------------------------------------------------------------------ the grid (Geometry Nodes)
def build_grid(hole=0.0, seed_shift=0, fall_from=(1, 110), fall_p=(0.6, 0.12), n=N):
    grid_ob = bpy.data.objects.new("DuckGrid", bpy.data.meshes.new("gridpts"))
    SC.collection.objects.link(grid_ob)
    ng = bpy.data.node_groups.new("DuckGridGN", "GeometryNodeTree")
    grid_ob.modifiers.new("ducks", "NODES").node_group = ng
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    nn, ln = ng.nodes, ng.links

    def mnode(op, a=None, b=None, va=None, vb=None):
        n = nn.new("ShaderNodeMath")
        n.operation = op
        if a is not None:
            ln.new(a, n.inputs[0])
        elif va is not None:
            n.inputs[0].default_value = va
        if b is not None:
            ln.new(b, n.inputs[1])
        elif vb is not None:
            n.inputs[1].default_value = vb
        return n.outputs[0]

    out = nn.new("NodeGroupOutput")
    grid = nn.new("GeometryNodeMeshGrid")
    grid.inputs["Size X"].default_value = SPACING * (n - 1)
    grid.inputs["Size Y"].default_value = SPACING * (n - 1)
    grid.inputs["Vertices X"].default_value = n
    grid.inputs["Vertices Y"].default_value = n
    pts = nn.new("GeometryNodeMeshToPoints")
    ln.new(grid.outputs["Mesh"], pts.inputs["Mesh"])
    geo = pts.outputs["Points"]
    if hole > 0:
        pos = nn.new("GeometryNodeInputPosition")
        vlen = nn.new("ShaderNodeVectorMath"); vlen.operation = "LENGTH"
        ln.new(pos.outputs["Position"], vlen.inputs[0])
        lt = mnode("LESS_THAN", vlen.outputs["Value"], vb=hole)
        dele = nn.new("GeometryNodeDeleteGeometry"); dele.domain = "POINT"
        ln.new(geo, dele.inputs["Geometry"]); ln.new(lt, dele.inputs["Selection"])
        geo = dele.outputs["Geometry"]
    idx = nn.new("GeometryNodeInputIndex").outputs["Index"]
    frame = nn.new("GeometryNodeInputSceneTime").outputs["Frame"]
    ph = nn.new("FunctionNodeRandomValue"); ph.data_type = "FLOAT"
    ph.inputs["Min"].default_value = 0.0; ph.inputs["Max"].default_value = 6.0
    ph.inputs["Seed"].default_value = 3 + seed_shift
    ln.new(idx, ph.inputs["ID"])
    epoch = mnode("FLOOR", mnode("DIVIDE", mnode("ADD", frame, ph.outputs["Value"]), vb=6.0))
    eid = mnode("ADD", mnode("MULTIPLY", epoch, vb=7919.0), idx)
    eid_i = nn.new("FunctionNodeFloatToInt"); eid_i.rounding_mode = "ROUND"
    ln.new(eid, eid_i.inputs[0])

    def rnd(seed):
        r = nn.new("FunctionNodeRandomValue"); r.data_type = "FLOAT"
        r.inputs["Seed"].default_value = seed + seed_shift
        ln.new(eid_i.outputs[0], r.inputs["ID"])
        return r.outputs["Value"]
    r1, r2 = rnd(11), rnd(29)
    pf = nn.new("ShaderNodeMapRange")
    pf.inputs["From Min"].default_value, pf.inputs["From Max"].default_value = fall_from
    pf.inputs["To Min"].default_value, pf.inputs["To Max"].default_value = fall_p
    ln.new(frame, pf.inputs["Value"])
    isfall = mnode("LESS_THAN", r1, pf.outputs["Result"])
    # upright: stand / step L / step R / crouch (0-3); down: face down / back / side / crash-sit / tripod (4-8)
    up_i = mnode("FLOOR", mnode("MULTIPLY", r2, vb=3.999))
    down_i = mnode("ADD", mnode("FLOOR", mnode("MULTIPLY", r2, vb=4.999)), vb=4.0)
    pick = nn.new("ShaderNodeMix"); pick.data_type = "FLOAT"
    ln.new(isfall, pick.inputs["Factor"])
    ln.new(up_i, pick.inputs["A"]); ln.new(down_i, pick.inputs["B"])
    pick_i = nn.new("FunctionNodeFloatToInt"); pick_i.rounding_mode = "ROUND"
    ln.new(pick.outputs["Result"], pick_i.inputs[0])
    yaw = nn.new("FunctionNodeRandomValue"); yaw.data_type = "FLOAT"
    yaw.inputs["Min"].default_value = rad(-150); yaw.inputs["Max"].default_value = rad(-30)
    yaw.inputs["Seed"].default_value = 5
    ln.new(idx, yaw.inputs["ID"])
    rot = nn.new("ShaderNodeCombineXYZ")
    ln.new(yaw.outputs["Value"], rot.inputs["Z"])
    ci = nn.new("GeometryNodeCollectionInfo")
    ci.inputs["Collection"].default_value = poses_coll
    ci.inputs["Separate Children"].default_value = True
    ci.inputs["Reset Children"].default_value = True
    inst = nn.new("GeometryNodeInstanceOnPoints")
    ln.new(geo, inst.inputs["Points"])
    ln.new(ci.outputs["Instances"], inst.inputs["Instance"])
    inst.inputs["Pick Instance"].default_value = True
    ln.new(pick_i.outputs[0], inst.inputs["Instance Index"])
    ln.new(rot.outputs["Vector"], inst.inputs["Rotation"])
    ln.new(inst.outputs["Instances"], out.inputs["Geometry"])
    return grid_ob


def hero(pose_name, loc=(0, 0, 0), yaw=0.0, name=None):
    src = next(o for o in pose_objs if o.name == pose_name)
    ob = src.copy()
    ob.data = src.data
    ob.name = name or f"hero_{pose_name}"
    ob.location = loc
    ob.rotation_euler = (0, 0, rad(yaw))
    SC.collection.objects.link(ob)
    return ob


# ------------------------------------------------------------------------------------------------ shot: grid
if A.shot == "grid":
    SC.frame_start, SC.frame_end = 1, 130
    build_grid()
    add_floor(SPACING * N * 0.8)
    cam_d.lens = 30
    # start low among the ducks, drift sideways, then crane up and back to the whole grid
    key(cam, 1, (-6.0, -16.0, 4.0)); key(tgt, 1, (2.0, 2.0, 0.8))
    key(cam, 55, (4.0, -18.0, 7.0)); key(tgt, 55, (5.0, 4.0, 0.6))
    key(cam, 130, (0.0, -150.0, 120.0)); key(tgt, 130, (0.0, 18.0, 0.0))
    interp(cam); interp(tgt)
    render(frames_arg(list(range(1, 131))))

# ------------------------------------------------------------------------------------------------ shot: tripod
if A.shot == "tripod":
    SC.frame_start, SC.frame_end = 1, 150
    build_grid(hole=SPACING * 2.2, seed_shift=7, fall_from=(1, 150), fall_p=(0.35, 0.35), n=20)
    add_floor(SPACING * N * 0.8)
    duck = hero("p8_head_tripod", yaw=0)
    cam_d.lens = 58
    cam_d.dof.use_dof = True
    cam_d.dof.focus_object = duck
    cam_d.dof.aperture_fstop = 1.4
    from bpy_extras.object_utils import world_to_camera_view
    C = CONTACTS["p8_head_tripod"]
    tri = [C["head"], C["footL"], C["footR"]]
    cen = sum(tri, Vector()) / 3
    # slow orbit, low, from the duck's face side round towards its flank; the triangle stays readable on the floor
    for f in range(1, 151):
        a = rad(-118 + 40 * (f - 1) / 149)
        r = 6.4 - 0.7 * (f - 1) / 149
        key(cam, f, (cen.x + r * math.cos(a), cen.y + r * math.sin(a), 2.1 - 0.25 * (f - 1) / 149))
    aim = cen.lerp(tri[0], 0.42)          # pulls the head towards the middle of the frame
    key(tgt, 1, (aim.x, aim.y, 0.75))
    key(tgt, 150, (aim.x, aim.y, 0.7))
    interp(tgt)
    track = []
    for f in range(1, 151):
        SC.frame_set(f)
        row = []
        for P in tri + [TOPS["p8_head_tripod"]["trunk"]]:
            v = world_to_camera_view(SC, cam, Vector((P.x, P.y, max(P.z, 0.0))))
            row.append([round(v.x * 1080, 1), round((1 - v.y) * 1920, 1)])
        track.append(row)
    os.makedirs(A.out, exist_ok=True)
    json.dump({"order": ["head", "footL", "footR", "trunk_top"], "track": track}, open(os.path.join(A.out, "tripod.json"), "w"))
    render(frames_arg(list(range(1, 151))))

# ------------------------------------------------------------------------------------------------ shot: variants
# Five deliberately wrong bodies in a diagonal row (fits the vertical frame), each with its own close camera segment:
#   W wide 1-60 | V1 heavier 61-120 | V2 off balance 121-180 | V3 slippery 181-240 | V4 low battery 241-300 | V5 shoved 301-360
# Label anchors (above each duck) and the centre-of-mass marker are projected per frame into variants.json for Remotion.
if A.shot == "variants":
    from bpy_extras.object_utils import world_to_camera_view

    SC.frame_start, SC.frame_end = 1, 360
    add_floor(90)
    SEG = {"W": 1, "V1": 61, "V2": 121, "V3": 181, "V4": 241, "V5": 301}
    rowp = [Vector((i * 3.4, i * 1.4, 0.0)) for i in range(5)]     # sideways row: no duck sits in another's camera line
    cam_off = Vector((-1.6, -4.8, 0.0))
    face = math.degrees(math.atan2(cam_off.y, cam_off.x)) + 8      # ducks turn to the camera side
    dview = (-cam_off).normalized()                                 # camera look direction on the floor
    right = Vector((dview.y, -dview.x, 0.0))                        # screen right on the floor

    def place(ob, p, yaw_deg, tip_deg=0.0, axis=None, lift=0.0):
        M = Matrix.Translation(p + Vector((0, 0, lift)))
        if tip_deg:
            M = M @ Matrix.Rotation(rad(tip_deg), 4, axis)
        M = M @ Matrix.Rotation(rad(yaw_deg), 4, "Z")
        ob.matrix_world = M

    d1 = hero("p3_crouch", name="d_heavy")
    d2 = hero("p0_stand", name="d_offbal")
    d3 = hero("p9_split", name="d_slip")
    d4 = hero("p3_crouch", name="d_batt")
    d5 = hero("p0_stand", name="d_shove")
    yaw_of = {"d_heavy": face + 72}       # the heavy one turns its back a little so the weight shows
    for ob, p in zip((d1, d2, d3, d4, d5), rowp):
        place(ob, p, yaw_of.get(ob.name, face))

    def mesh_obj(name, build, mat):
        ob = bpy.data.objects.new(name, bpy.data.meshes.new(name))
        bm = bmesh.new()
        build(bm)
        bm.to_mesh(ob.data)
        bm.free()
        for pg in ob.data.polygons:
            pg.use_smooth = True
        ob.data.materials.append(mat)
        SC.collection.objects.link(ob)
        return ob

    # 1 heavier: a lead weight strapped behind the neck
    top1 = TOPS["p3_crouch"]["trunk"]
    lead = mesh_obj("lead", lambda bm: bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.44, 0.5, 0.3, 1))),
                    principled("lead_mat", (0.16, 0.17, 0.19), 0.28, metal=1.0))
    bv = lead.modifiers.new("bevel", "BEVEL"); bv.width = 0.05; bv.segments = 3
    lead.parent = d1
    lead.location = (top1.x + 0.06, 0.0, top1.z + 0.14)
    for pg in lead.data.polygons:
        pg.use_smooth = False
    # 2 off balance: a centre-of-mass marker pushed out to the side; the duck leans after it
    cm = new_mat("com_mat")
    pb = next(n for n in cm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    ckn = cm.node_tree.nodes.new("ShaderNodeTexChecker"); ckn.inputs["Scale"].default_value = 2.0
    ckn.inputs["Color1"].default_value = (0.85, 1.0, 0.0, 1); ckn.inputs["Color2"].default_value = (0.01, 0.01, 0.01, 1)
    cm.node_tree.links.new(ckn.outputs["Color"], pb.inputs["Base Color"])
    com = mesh_obj("com", lambda bm: bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=0.17), cm)
    # 3 slippery: a glossy ice tile under the splits
    ice = add_floor(1.7, loc=(rowp[2].x, rowp[2].y, 0.004), gloss=True, name="ice")
    # 4 low battery: battery with one blinking red bar, turned to the camera
    batt = mesh_obj("batt", lambda bm: (bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.9, 0.08, 0.42, 1))),
                                        bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0.5, 0, 0)) @ Matrix.Diagonal((0.08, 0.08, 0.2, 1)))),
                    principled("batt_shell", (0.9, 0.92, 0.95), 0.3, emit=(0.9, 0.92, 0.95), emit_strength=0.5))
    bar = mesh_obj("bar", lambda bm: bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((-0.3, -0.05, 0)) @ Matrix.Diagonal((0.18, 0.04, 0.3, 1))),
                   principled("bar_red", (1.0, 0.08, 0.05), 0.4, emit=(1.0, 0.08, 0.05), emit_strength=8.0))
    byaw = math.degrees(math.atan2(-dview.x, dview.y)) if False else math.degrees(math.atan2(cam_off.x, -cam_off.y))
    # 5 shoved: a pusher slams in from screen right
    arrow = mesh_obj("pusher", lambda bm: (
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.14, radius2=0.14, depth=1.3,
                              matrix=Matrix.Translation((-0.85, 0, 0)) @ Euler((0, rad(90), 0)).to_matrix().to_4x4()),
        bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.36, radius2=0.0, depth=0.55,
                              matrix=Matrix.Translation((0.07, 0, 0)) @ Euler((0, rad(90), 0)).to_matrix().to_4x4())),
        principled("arrow_mat", (0.85, 1.0, 0.0), 0.35, emit=(0.85, 1.0, 0.0), emit_strength=3.0))
    ayaw = math.degrees(math.atan2(-right.y, -right.x))
    tip_axis = dview.copy()

    track = []
    for f in range(1, 361):
        t = (f - 1) / FPS
        # heavy: slow sag under the weight
        place(d1, rowp[0], face + 72, lift=-0.035 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.55 * t)))
        # off balance: lean towards the shifted mass (screen left/right)
        lean = 13 + 4 * math.sin(2 * math.pi * 0.7 * t)
        place(d2, rowp[1], face, tip_deg=-lean, axis=tip_axis)
        com_p = rowp[1] + right * (0.62 + 0.04 * math.sin(2 * math.pi * 0.7 * t)) + Vector((0, 0, 1.3))
        com.location = com_p
        # slippery: slides across the ice and wobbles
        slide = 0.32 * math.sin(2 * math.pi * 0.45 * t)
        place(d3, rowp[2] + right * slide, face + 9 * math.sin(2 * math.pi * 0.6 * t), tip_deg=5 * math.sin(2 * math.pi * 1.2 * t), axis=tip_axis)
        # low battery: sag, battery bobs, red bar blinks
        place(d4, rowp[3], face, lift=-0.02 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.4 * t)))
        bz = 2.95 + 0.05 * math.sin(2 * math.pi * 0.8 * t)
        batt.location = rowp[3] + Vector((0, 0, bz))
        batt.rotation_euler = (0, 0, rad(byaw))
        bar.location = batt.location
        bar.rotation_euler = batt.rotation_euler
        bar.hide_render = (f // 8) % 2 == 1
        # shoved: in the V5 segment the hit lands at frame 312; elsewhere the cycle repeats every 60 frames
        ph = (f - 301) % 60
        hit = 11
        if ph < hit:
            ax = 2.7 - ph / hit * 2.1
        elif ph < 26:
            ax = 0.6
        else:
            ax = 0.6 + (ph - 26) / 34 * 2.4
        arrow.location = rowp[4] + right * ax + Vector((0, 0, 1.2))
        arrow.rotation_euler = (0, 0, rad(ayaw))
        tip = 0.0
        if ph >= hit:
            u = (ph - hit) / FPS
            tip = 26 * math.exp(-u * 4.0) * math.sin(u * 8.5 + 0.35)
        place(d5, rowp[4], face, tip_deg=-tip, axis=tip_axis)
        arrow.hide_render = not (f <= 60 or f >= 301)       # the pusher belongs to the wide shot and V5 only
        arrow.keyframe_insert("hide_render", frame=f)
        for ob in (d1, d2, d3, d4, d5, com, batt, bar, arrow):
            ob.keyframe_insert("location", frame=f)
            ob.keyframe_insert("rotation_euler", frame=f)
        bar.keyframe_insert("hide_render", frame=f)
    interp(bar, "CONSTANT")
    interp(arrow, "LINEAR")
    for fc in all_fcurves(arrow):
        if fc.data_path == "hide_render":
            for k in fc.keyframe_points:
                k.interpolation = "CONSTANT"

    cam_d.lens = 42
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 2.0
    foc = bpy.data.objects.new("focus", None)
    SC.collection.objects.link(foc)
    cam_d.dof.focus_object = foc

    def seg_keys(f0, f1, cam_a, cam_b, tg, focus):
        key(cam, f0, cam_a); key(cam, f1, cam_b)
        key(tgt, f0, tg); key(tgt, f1, tg)
        key(foc, f0, focus); key(foc, f1, focus)

    mid = rowp[2]
    seg_keys(1, 60, rowp[0] + Vector((-4.6, -10.4, 4.0)), rowp[0] + Vector((-4.0, -9.2, 3.6)), mid + Vector((0.0, 0.0, 0.9)), mid + Vector((0, 0, 1.0)))
    for i, name in enumerate(("V1", "V2", "V3", "V4", "V5")):
        f0 = SEG[name]
        p = rowp[i]
        up = 1.0 if name != "V4" else 1.7
        lift = 0.45 if name == "V4" else 0.0
        shift = right * (0.62 if name == "V1" else 0.0)
        far = 1.3 if name == "V1" else 1.0      # the heavy one is side-on and longer: pull back
        seg_keys(f0, f0 + 59, p + shift + cam_off * 1.04 * far + Vector((0, 0, 1.6 + lift)), p + shift + cam_off * 0.9 * far + Vector((0, 0, 1.5 + lift)),
                 p + shift + Vector((0, 0, up)), p + Vector((0, 0, 1.0)))
    for ob in (cam, tgt, foc):
        interp(ob, "LINEAR")
        for fc in all_fcurves(ob):
            for k in fc.keyframe_points:
                if int(k.co[0]) in (60, 120, 180, 240, 300):
                    k.interpolation = "CONSTANT"

    # per-frame label anchors: above each duck's head, and the CoM marker with its floor point
    for f in range(1, 361):
        SC.frame_set(f)

        def pj(P):
            v = world_to_camera_view(SC, cam, P)
            return [round(v.x * 1080, 1), round((1 - v.y) * 1920, 1)]
        heads = [pj(p + Vector((0, 0, 3.0))) for p in rowp]
        track.append({"heads": heads, "com": pj(com.matrix_world.translation), "com_floor": pj(Vector((com.matrix_world.translation.x, com.matrix_world.translation.y, 0.0))),
                      "batt": pj(batt.matrix_world.translation)})
    os.makedirs(A.out, exist_ok=True)
    json.dump({"segments": SEG, "track": track}, open(os.path.join(A.out, "variants.json"), "w"))
    render(frames_arg(list(range(1, 361))))


# ------------------------------------------------------------------------------------------------ shot: crowd (v2)
# ~50 visibly different ducks (size, bulk, lean, tint) toppling over and resetting like simulator episodes; the camera
# drifts, then pushes into the one in the middle. Critic round 1: no counter, no far-off carpet of tiny ducks.
SHELLS = [(0.88, 0.89, 0.9), (0.93, 0.86, 0.74), (0.74, 0.8, 0.88), (0.86, 0.9, 0.8), (0.95, 0.8, 0.82)]


def tinted_shell(i, rgb):
    return principled(f"shell_{i}", rgb, 0.38, coat=0.5)


def override(ob, slot, mat):
    ob.material_slots[slot].link = "OBJECT"
    ob.material_slots[slot].material = mat


if A.shot == "crowd":
    import random
    rng = random.Random(7)
    SC.frame_start, SC.frame_end = 1, 152
    add_floor(80)
    tints = [tinted_shell(i, c) for i, c in enumerate(SHELLS)]
    src = next(o for o in pose_objs if o.name == "p0_stand")
    G = 3.2
    for gi in range(7):
        for gj in range(7):
            k = gi * 7 + gj
            base = Vector(((gi - 3) * G + rng.uniform(-0.4, 0.4), (gj - 3) * G + rng.uniform(-0.4, 0.4), 0.0))
            ob = src.copy()
            ob.data = src.data
            ob.name = f"crowd_{k}"
            SC.collection.objects.link(ob)
            hero_duck = (gi, gj) == (3, 3)
            sc = 1.0 if hero_duck else rng.uniform(0.86, 1.14)
            bulk = 1.0 if hero_duck else rng.uniform(1.0, 1.1)
            tint = tints[0] if hero_duck else tints[rng.randrange(len(tints))]
            override(ob, WHITE, tint)
            override(ob, TRUNK, tint)
            yaw = rad(rng.uniform(-125, -65))
            lean = 0.0 if hero_duck else rng.uniform(-5, 5)
            piv = bpy.data.objects.new(f"piv_{k}", None)
            SC.collection.objects.link(piv)
            ob.parent = piv
            ob.scale = (sc * bulk, sc * bulk, sc)
            ob.rotation_euler = (0, rad(lean), yaw)
            if hero_duck:
                piv.location = base
                for f in (1, 152):
                    sway = 1.5 * math.sin(f / 14.0)
                    piv.rotation_euler = (rad(sway * 0.5), rad(sway), 0)
                    piv.keyframe_insert("rotation_euler", frame=f)
                continue
            # episode loop: stand, topple, lie, reset
            ang = rng.uniform(0, 2 * math.pi)
            fall_dir = Vector((math.cos(ang), math.sin(ang), 0))
            axis = Vector((-fall_dir.y, fall_dir.x, 0))
            edge = 0.42 * sc
            piv.location = base + fall_dir * edge
            ob.location = -fall_dir * edge
            f = 1 - rng.randint(0, 40)
            events = []
            while f < 160:
                stand = rng.randint(16, 56)
                events.append(("stand", f, f + stand))
                f += stand
                fall = rng.randint(8, 12)
                events.append(("fall", f, f + fall))
                f += fall
                lie = rng.randint(10, 22)
                events.append(("lie", f, f + lie))
                f += lie
                events.append(("reset", f, f + 4))
                f += 4
                # the share that falls drops as they "learn": later episodes stand longer
                if f > 70 and rng.random() < 0.5:
                    events.append(("stand", f, f + 200))
                    break
            for fr in range(1, 153):
                ev = next((e for e in events if e[1] <= fr < e[2]), ("stand", fr, fr + 1))
                kind, a, b = ev
                u = (fr - a) / max(1, (b - a))
                tilt = 0.0
                s_pop = 1.0
                if kind == "fall":
                    tilt = 92 * (u ** 2.2)
                elif kind == "lie":
                    tilt = 92 - 6 * math.exp(-u * 6) * math.sin(u * 14)
                elif kind == "reset":
                    tilt = 0.0
                    s_pop = 0.15 + 0.85 * (u ** 0.6)
                else:
                    tilt = 1.2 * math.sin((fr + k * 7) / 9.0)
                q = Matrix.Rotation(rad(tilt), 3, axis).to_euler()
                piv.rotation_euler = q
                piv.scale = (s_pop, s_pop, s_pop)
                piv.keyframe_insert("rotation_euler", frame=fr)
                piv.keyframe_insert("scale", frame=fr)
    cam_d.lens = 34
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 2.8
    foc = bpy.data.objects.new("focus", None)
    SC.collection.objects.link(foc)
    cam_d.dof.focus_object = foc
    key(cam, 1, (-7.5, -21.0, 7.6)); key(tgt, 1, (0.0, 0.0, 0.6)); key(foc, 1, (0.0, 0.0, 1.0))
    key(cam, 108, (-4.5, -19.0, 6.4)); key(tgt, 108, (0.0, 0.0, 0.8)); key(foc, 108, (0.0, 0.0, 1.0))
    key(cam, 152, (-1.0, -6.6, 2.1)); key(tgt, 152, (0.0, 0.0, 1.35)); key(foc, 152, (0.0, 0.0, 1.2))
    for ob in (cam, tgt, foc):
        interp(ob)
    render(frames_arg(list(range(1, 153))))

# ------------------------------------------------------------------------------------------------ shot: wrong (v2)
# One duck, one continuous take (251 frames = the m5 line). The wrong-body changes land on the spoken words and stay:
# heavier (t=102), off balance (t=123), slippery (t=152), low battery (t=177), shoved (t=209, hit t=215).
if A.shot == "wrong":
    SC.frame_start, SC.frame_end = 1, 251
    T_HEAVY, T_OFF, T_SLIP, T_BATT, T_SHOVE = 102, 123, 152, 177, 209
    HIT = T_SHOVE + 6
    add_floor(80)
    src = next(o for o in pose_objs if o.name == "p0_stand")
    piv = bpy.data.objects.new("piv", None)
    SC.collection.objects.link(piv)
    duck = src.copy()
    duck.data = src.data
    duck.name = "wrong_duck"
    SC.collection.objects.link(duck)
    duck.parent = piv
    cam_dir = Vector((0.36, -0.93, 0.0)).normalized()             # floor direction from the duck to the camera
    yaw = math.degrees(math.atan2(cam_dir.y, cam_dir.x)) + 14
    duck.rotation_euler = (0, 0, rad(yaw))
    right = Vector((-cam_dir.y, cam_dir.x, 0.0)) * -1             # screen right on the floor
    right = Vector((cam_dir.y * -1, cam_dir.x, 0)) if False else Vector((-cam_dir.y, cam_dir.x, 0)) * -1
    view_axis = (-cam_dir).normalized()
    # background copies, soft focus, so "every copy" has copies
    tints = [tinted_shell(i, c) for i, c in enumerate(SHELLS)]
    for i in range(7):
        b = src.copy()
        b.data = src.data
        b.name = f"bg_{i}"
        SC.collection.objects.link(b)
        b.location = (-7.5 + i * 2.6 + (i % 2) * 0.6, 7.0 + (i % 3) * 2.2, 0)
        b.rotation_euler = (0, 0, rad(-100 + i * 9))
        s_ = 0.9 + 0.04 * (i % 4)
        b.scale = (s_, s_, s_)
        override(b, WHITE, tints[i % len(tints)])
        override(b, TRUNK, tints[i % len(tints)])
    # trunk x-ray from "off balance": the torso fades to glass so the balance point inside shows
    nt = M_TRUNK.node_tree
    outn = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    prev = outn.inputs["Surface"].links[0].from_socket
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(prev, mx.inputs[1])
    nt.links.new(tr.outputs["BSDF"], mx.inputs[2])
    nt.links.new(mx.outputs["Shader"], outn.inputs["Surface"])
    try:
        M_TRUNK.surface_render_method = "BLENDED"
    except Exception:
        pass
    fac = mx.inputs["Fac"]
    fac.default_value = 0.0
    fac.keyframe_insert("default_value", frame=T_OFF)
    fac.default_value = 0.62
    fac.keyframe_insert("default_value", frame=T_OFF + 8)
    # centre-of-mass marker inside the torso (shift exaggerated, labelled so in the edit)
    TB, TT = CONTACTS["p0_stand"]["trunk"], TOPS["p0_stand"]["trunk"]
    tc_local = Vector(((TB.x + TT.x) / 2, 0.0, (TB.z + TT.z) / 2))
    cmm = new_mat("com_mat")
    pb = next(n for n in cmm.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    ckn = cmm.node_tree.nodes.new("ShaderNodeTexChecker"); ckn.inputs["Scale"].default_value = 2.0
    ckn.inputs["Color1"].default_value = (0.85, 1.0, 0.0, 1); ckn.inputs["Color2"].default_value = (0.01, 0.01, 0.01, 1)
    cmm.node_tree.links.new(ckn.outputs["Color"], pb.inputs["Base Color"])
    pb.inputs["Emission Color"].default_value = (0.85, 1.0, 0.0, 1)
    pb.inputs["Emission Strength"].default_value = 0.6
    com = bpy.data.objects.new("com", bpy.data.meshes.new("com"))
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=24, v_segments=16, radius=0.085); bm.to_mesh(com.data); bm.free()
    for pg in com.data.polygons:
        pg.use_smooth = True
    com.data.materials.append(cmm)
    SC.collection.objects.link(com)
    com.parent = duck
    # battery gauge on the torso's front face
    front_x = TT.x + 0.0
    gauge = bpy.data.objects.new("gauge", bpy.data.meshes.new("gauge"))
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Diagonal((0.03, 0.42, 0.2, 1)))
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0, 0.235, 0)) @ Matrix.Diagonal((0.03, 0.05, 0.1, 1)))
    bm.to_mesh(gauge.data); bm.free()
    gauge.data.materials.append(principled("gauge_shell", (0.04, 0.045, 0.05), 0.4))
    SC.collection.objects.link(gauge)
    gauge.parent = duck
    gx = 0.38       # trunk front (x) in the duck's local frame, scaled
    gauge.location = (gx + 0.02, 0.0, tc_local.z + 0.02)
    bar = bpy.data.objects.new("bar", bpy.data.meshes.new("bar"))
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix.Translation((0, 0.18, 0)) @ Matrix.Diagonal((0.035, 0.36, 0.14, 1)))
    bm.to_mesh(bar.data); bar.data.materials.clear(); bm.free()
    bar_mat = new_mat("bar_mat")
    bp = next(n for n in bar_mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bp.inputs["Base Color"].default_value = (0.2, 1.0, 0.3, 1)
    bp.inputs["Emission Color"].default_value = (0.2, 1.0, 0.3, 1)
    bp.inputs["Emission Strength"].default_value = 4.0
    bar.data.materials.append(bar_mat)
    SC.collection.objects.link(bar)
    bar.parent = duck
    bar.location = (gx + 0.03, -0.18, tc_local.z + 0.02)
    for fr, w, col in ((T_BATT, 1.0, (0.2, 1.0, 0.3)), (T_BATT + 22, 0.18, (1.0, 0.1, 0.05))):
        bar.scale = (1, w, 1)
        bar.keyframe_insert("scale", frame=fr)
        bp.inputs["Base Color"].default_value = (*col, 1)
        bp.inputs["Emission Color"].default_value = (*col, 1)
        bp.inputs["Base Color"].keyframe_insert("default_value", frame=fr)
        bp.inputs["Emission Color"].keyframe_insert("default_value", frame=fr)
    gauge.hide_render = True
    bar.hide_render = True
    gauge.keyframe_insert("hide_render", frame=1)
    bar.keyframe_insert("hide_render", frame=1)
    gauge.hide_render = False
    bar.hide_render = False
    gauge.keyframe_insert("hide_render", frame=T_BATT - 2)
    bar.keyframe_insert("hide_render", frame=T_BATT - 2)
    # ice under the feet from "slippery"
    ice = add_floor(1.25, loc=(0, 0, 0.004), gloss=True, name="ice")
    im = ice.data.materials[0]
    o2 = next(n for n in im.node_tree.nodes if n.type == "OUTPUT_MATERIAL")
    pv = o2.inputs["Surface"].links[0].from_socket
    tr2 = im.node_tree.nodes.new("ShaderNodeBsdfTransparent")
    mx2 = im.node_tree.nodes.new("ShaderNodeMixShader")
    im.node_tree.links.new(tr2.outputs["BSDF"], mx2.inputs[1])
    im.node_tree.links.new(pv, mx2.inputs[2])
    im.node_tree.links.new(mx2.outputs["Shader"], o2.inputs["Surface"])
    try:
        im.surface_render_method = "BLENDED"
    except Exception:
        pass
    f2 = mx2.inputs["Fac"]
    f2.default_value = 0.0
    f2.keyframe_insert("default_value", frame=T_SLIP - 2)
    f2.default_value = 0.9
    f2.keyframe_insert("default_value", frame=T_SLIP + 6)
    # the pusher
    arrow = bpy.data.objects.new("pusher", bpy.data.meshes.new("pusher"))
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.12, radius2=0.12, depth=1.2,
                          matrix=Matrix.Translation((-0.8, 0, 0)) @ Euler((0, rad(90), 0)).to_matrix().to_4x4())
    bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.3, radius2=0.0, depth=0.5,
                          matrix=Matrix.Translation((0.05, 0, 0)) @ Euler((0, rad(90), 0)).to_matrix().to_4x4())
    bm.to_mesh(arrow.data); bm.free()
    arrow.data.materials.append(principled("arrow_mat", (0.85, 1.0, 0.0), 0.35, emit=(0.85, 1.0, 0.0), emit_strength=3.0))
    SC.collection.objects.link(arrow)
    ayaw = math.degrees(math.atan2(-right.y, -right.x))
    for fr in range(1, 252):
        t = fr
        # heavier: squash, then 5% bigger for the rest of the shot
        if t < T_HEAVY:
            sc = 1.0
            sz = 1.0
        else:
            u = (t - T_HEAVY) / 12.0
            sc = 1.0 + 0.05 * min(1.0, u)
            sz = sc * (1 - 0.07 * math.exp(-u * 3) * math.sin(min(u, 1.2) * math.pi))
        duck.scale = (sc, sc, sz)
        duck.keyframe_insert("scale", frame=fr)
        # off balance: the marker slides off-centre, the duck leans after it
        off = 0.0 if t < T_OFF else min(1.0, (t - T_OFF) / 10.0)
        com.location = tc_local + Vector((0.0, 0.17 * off, 0.0))
        com.keyframe_insert("location", frame=fr)
        lean = 6.0 * off + (1.2 * math.sin(t / 7.0) if t >= T_OFF else 0.0)
        # slippery: a skid to one side and back
        slip = 0.0 if t < T_SLIP else 0.3 * math.sin(min(math.pi, (t - T_SLIP) / 22.0 * math.pi)) * math.exp(-max(0, t - T_SLIP - 22) / 20)
        wob = 0.0 if t < T_SLIP else 5.0 * math.exp(-(t - T_SLIP) / 18.0) * math.sin((t - T_SLIP) / 2.6)
        # low battery: a slow sag
        sag = 0.0 if t < T_BATT else -0.05 * min(1.0, (t - T_BATT) / 24.0)
        # shoved: damped stagger after the hit
        tip = 0.0
        if t >= HIT:
            v = (t - HIT) / FPS
            tip = 24 * math.exp(-v * 3.6) * math.sin(v * 8.0 + 0.3)
        M = Matrix.Translation(right * slip + Vector((0, 0, sag))) @ Matrix.Rotation(rad(lean + wob - tip), 4, view_axis)
        piv.matrix_world = M
        piv.keyframe_insert("location", frame=fr)
        piv.keyframe_insert("rotation_euler", frame=fr)
        # the pusher comes in from screen right, hits, pulls back
        if t < T_SHOVE:
            ax = 4.0
        elif t < HIT:
            ax = 2.6 - (t - T_SHOVE) / (HIT - T_SHOVE) * 1.95
        elif t < HIT + 14:
            ax = 0.65
        else:
            ax = 0.65 + (t - HIT - 14) / 20.0 * 2.5
        arrow.location = right * ax + Vector((0, 0, 1.2))
        arrow.rotation_euler = (0, 0, rad(ayaw))
        arrow.hide_render = t < T_SHOVE - 1
        arrow.keyframe_insert("location", frame=fr)
        arrow.keyframe_insert("rotation_euler", frame=fr)
        arrow.keyframe_insert("hide_render", frame=fr)
    for ob in (gauge, bar, arrow):
        for fc in all_fcurves(ob):
            if fc.data_path == "hide_render":
                for k in fc.keyframe_points:
                    k.interpolation = "CONSTANT"
    # camera: duck ~40% of the frame height, head at ~36%, slow 4% push
    cam_d.lens = 45
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 2.0
    cam_d.dof.focus_object = duck
    T = Vector((0.0, 0.0, 1.72))
    for fr, dist in ((1, 8.25), (251, 7.92)):
        key(cam, fr, T + cam_dir * dist + Vector((0, 0, 0.55)))
        key(tgt, fr, T)
    interp(cam, "LINEAR"); interp(tgt, "LINEAR")
    from bpy_extras.object_utils import world_to_camera_view
    track = []
    for fr in range(1, 252):
        SC.frame_set(fr)

        def pj(P):
            v = world_to_camera_view(SC, cam, P)
            return [round(v.x * 1080, 1), round((1 - v.y) * 1920, 1)]
        cw = com.matrix_world.translation
        track.append({"com": pj(cw), "floor": pj(Vector((cw.x, cw.y, 0.0))), "head": pj(duck.matrix_world @ (TOPS["p0_stand"]["head"])),
                      "feet": pj(duck.matrix_world @ CONTACTS["p0_stand"]["footL"])})
    os.makedirs(A.out, exist_ok=True)
    json.dump({"cues": {"heavy": T_HEAVY, "off": T_OFF, "slip": T_SLIP, "batt": T_BATT, "shove": T_SHOVE, "hit": HIT}, "track": track},
              open(os.path.join(A.out, "wrong.json"), "w"))
    render(frames_arg(list(range(1, 252))))
