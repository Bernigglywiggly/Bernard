"""A01 v5 — "One line, many worlds".

Every palette is a room on the same amber drift line. The rooms change with the
script's register (see shots.py); the line, the type, the finishing pass and the
frame furniture never change. That is what keeps the variety on-brand.

Render a shot (Blender 4.2+ or the `bpy` module; tested on 4.5 LTS):
    python3 worlds.py S07                    # -> $A01_BUILD/frames/S07/0001.png ...
    python3 worlds.py S07 --still 30         # one frame -> $A01_BUILD/stills/S07_0030.png
    blender -b -P worlds.py -- S07 --res 1920x1080 --samples 32      # final quality
"""
import json
import math
import os
import random
import sys

import bpy
import bmesh  # after bpy: the bpy module puts bmesh on the path
import numpy as np
from mathutils import Euler, Quaternion, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import BUILD, FONTS, FPS, OUTRO, SHOTS, TEX, frames, lf  # noqa: E402

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def opt(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default


RES = tuple(int(v) for v in opt("--res", "960x540").split("x"))
SAMPLES = int(opt("--samples", "8"))
STILL = opt("--still")
LAYOUT = json.load(open(os.path.join(TEX, "layout.json")))


# ---------------------------------------------------------------- brand
def lin(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


AMBER, GROUND, IMPERIAL, PHOS = lin("FFB23F"), lin("07080B"), lin("0B2A6B"), lin("5CFF9D")
BONE, INK, WHITE, CONCRETE, STEEL = lin("ECE6DA"), lin("0B0B0C"), lin("ECEDEF"), lin("56524C"), lin("8A90A0")
AMBER_L = (1.0, 0.62, 0.22)          # light colour that reads as the brand amber


# ---------------------------------------------------------------- scene
def safe(obj, **kw):
    for k, v in kw.items():
        try:
            setattr(obj, k, v)
        except (AttributeError, TypeError, ValueError):
            pass


def reset(samples=None, blur=False, raytrace=False, res=None, engine="EEVEE"):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.fps = FPS
    sc.render.resolution_x, sc.render.resolution_y = res or RES
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGB"
    if engine == "CYCLES":
        sc.render.engine = "CYCLES"
        use_gpu(sc)
        safe(sc.cycles, samples=(samples or SAMPLES) * 2, adaptive_threshold=0.02, use_denoising=True,
             max_bounces=6, glossy_bounces=4, diffuse_bounces=2, transmission_bounces=2, volume_bounces=0)
        sc.render.use_persistent_data = True
    for eng in (() if engine == "CYCLES" else ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE")):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    safe(sc.eevee, taa_render_samples=samples or SAMPLES, use_shadows=True, volumetric_tile_size="8",
         volumetric_samples=48, use_volumetric_shadows=False, use_gtao=True, use_raytracing=raytrace)
    if raytrace:
        safe(sc.eevee, ray_tracing_method="SCREEN")
    safe(sc.render, use_motion_blur=blur, motion_blur_shutter=0.6)
    safe(sc.view_settings, view_transform="Standard")   # AgX drifts the brand amber to salmon
    safe(sc.view_settings, look="None")
    w = bpy.data.worlds.new("W")
    sc.world = w
    w.use_nodes = True
    w.node_tree.nodes["Background"].inputs[0].default_value = GROUND
    return sc


def use_gpu(sc):
    """Cycles on the GPU when there is one (Metal on the Mac), else CPU."""
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        for kind in ("METAL", "OPTIX", "CUDA", "HIP", "ONEAPI"):
            try:
                prefs.compute_device_type = kind
            except TypeError:
                continue
            prefs.get_devices()
            gpus = [d for d in prefs.devices if d.type != "CPU"]
            if gpus:
                for d in prefs.devices:
                    d.use = True
                sc.cycles.device = "GPU"
                return
    except Exception:
        pass
    sc.cycles.device = "CPU"


def link(o):
    bpy.context.scene.collection.objects.link(o)
    return o


def key(target, attr, pairs):
    for f, v in pairs:
        setattr(target, attr, v)
        target.keyframe_insert(attr, frame=f)


# ---------------------------------------------------------------- materials
def mat_emit(name, col, strength):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs[0].default_value = col
    e.inputs[1].default_value = strength
    nt.links.new(e.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs[0])
    return m


def mat_pbr(name, col, rough=0.5, metal=0.0, emit=None, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes["Principled BSDF"]
    p.inputs["Base Color"].default_value = col
    p.inputs["Roughness"].default_value = rough
    p.inputs["Metallic"].default_value = metal
    if emit:
        p.inputs["Emission Color"].default_value = emit
        p.inputs["Emission Strength"].default_value = es
    return m


def mat_tex(name, img, rough=0.85, es=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes["Principled BSDF"]
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(os.path.join(TEX, img))
    t.interpolation = "Cubic"
    nt.links.new(t.outputs["Color"], p.inputs["Base Color"])
    p.inputs["Roughness"].default_value = rough
    if es:
        nt.links.new(t.outputs["Color"], p.inputs["Emission Color"])
        p.inputs["Emission Strength"].default_value = es
    return m


def emission_socket(m):
    n = m.node_tree.nodes
    return n["Principled BSDF"].inputs["Emission Strength"] if "Principled BSDF" in n else n["Emission"].inputs[1]


# ---------------------------------------------------------------- geometry
def boxes(name, items, mat):
    bm = bmesh.new()
    for c, s in items:
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=s, verts=r["verts"])
        bmesh.ops.translate(bm, vec=c, verts=r["verts"])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    return link(bpy.data.objects.new(name, me))


def plane(name, w, h, mat, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (w, h, 1)
    o.rotation_euler = [math.radians(a) for a in rot]
    o.data.materials.append(mat)
    return o


def sphere(r, loc, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=24, ring_count=12)
    o = bpy.context.object
    o.data.materials.append(mat)
    for poly in o.data.polygons:
        poly.use_smooth = True
    return o


_FONTS = {}


def text(body, fnt="Unbounded-900", size=1.0, ext=0.05, bev=0.0, loc=(0, 0, 0), rot=(0, 0, 0), mat=None,
         ax="CENTER", ay="CENTER"):
    if fnt not in _FONTS:
        flat = os.path.join(FONTS, fnt + "-flat.ttf")      # overlaps removed (posters.py makes these)
        _FONTS[fnt] = bpy.data.fonts.load(flat if os.path.exists(flat) else os.path.join(FONTS, fnt + ".ttf"))
    cu = bpy.data.curves.new("TXT", "FONT")
    cu.body, cu.font, cu.size = body, _FONTS[fnt], size
    cu.extrude, cu.bevel_depth, cu.bevel_resolution = ext, bev, 3
    cu.align_x, cu.align_y = ax, ay
    if mat:
        cu.materials.append(mat)
    o = link(bpy.data.objects.new("T_" + body[:10], cu))
    o.location = loc
    o.rotation_euler = [math.radians(a) for a in rot]
    return o


def light(kind, loc, energy, col=(1, 1, 1), size=1.0, rot=(0, 0, 0), shadow=True, spot=None, aim_at=None):
    ld = bpy.data.lights.new("L", kind)
    ld.energy, ld.color = energy, col
    if kind == "AREA":
        ld.size = size
    else:
        ld.shadow_soft_size = size
    if kind == "SPOT":
        ld.spot_size, ld.spot_blend = math.radians(spot or 45), 0.6
    ld.use_shadow = shadow
    o = link(bpy.data.objects.new("L", ld))
    o.location = loc
    o.rotation_euler = aim(loc, aim_at) if aim_at else Euler([math.radians(a) for a in rot])
    return o


def fog(density=0.02, size=(40, 60, 30), loc=(0, 10, 8), col=(0.85, 0.85, 0.9, 1), anis=0.35):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.object
    o.name, o.scale = "FOG", size
    m = bpy.data.materials.new("FOG")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    v = nt.nodes.new("ShaderNodeVolumePrincipled")
    v.inputs["Density"].default_value = density
    v.inputs["Color"].default_value = col
    v.inputs["Anisotropy"].default_value = anis
    nt.links.new(v.outputs[0], nt.nodes.new("ShaderNodeOutputMaterial").inputs["Volume"])
    o.data.materials.append(m)
    return o


def points(P, r=0.01, mat=None, name="PTS"):
    """Vertex-only mesh rendered as a point cloud (Geometry Nodes: Mesh to Points)."""
    me = bpy.data.meshes.new(name)
    me.vertices.add(len(P))
    me.vertices.foreach_set("co", np.asarray(P, np.float32).ravel())
    me.update()
    o = link(bpy.data.objects.new(name, me))
    ng = bpy.data.node_groups.new(name, "GeometryNodeTree")
    ng.interface.new_socket("Geometry", in_out="INPUT", socket_type="NodeSocketGeometry")
    ng.interface.new_socket("Geometry", in_out="OUTPUT", socket_type="NodeSocketGeometry")
    gi, go = ng.nodes.new("NodeGroupInput"), ng.nodes.new("NodeGroupOutput")
    mp = ng.nodes.new("GeometryNodeMeshToPoints")
    mp.inputs["Radius"].default_value = r
    sm = ng.nodes.new("GeometryNodeSetMaterial")
    sm.inputs["Material"].default_value = mat
    ng.links.new(gi.outputs[0], mp.inputs["Mesh"])
    ng.links.new(mp.outputs["Points"], sm.inputs["Geometry"])
    ng.links.new(sm.outputs["Geometry"], go.inputs[0])
    o.modifiers.new("GN", "NODES").node_group = ng
    return o


def shape(o, name, P):
    if not o.data.shape_keys:
        o.shape_key_add(name="Basis", from_mix=False)
    k = o.shape_key_add(name=name, from_mix=False)
    k.data.foreach_set("co", np.asarray(P, np.float32).ravel())
    return k


def text_points(body, n, size=2.0, ext=0.2, fnt="Unbounded-900", seed=3):
    """Sample n points on the surface of extruded text, stood upright facing -Y."""
    o = text(body, fnt, size, ext)
    me = bpy.data.meshes.new_from_object(o.evaluated_get(bpy.context.evaluated_depsgraph_get()))
    me.calc_loop_triangles()
    V = np.array([v.co[:] for v in me.vertices])
    T = np.array([t.vertices[:] for t in me.loop_triangles])
    A, B, C = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
    area = 0.5 * np.linalg.norm(np.cross(B - A, C - A), axis=1)
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(T), n, p=area / area.sum())
    u, v = rng.random(n), rng.random(n)
    flip = u + v > 1
    u[flip], v[flip] = 1 - u[flip], 1 - v[flip]
    P = A[idx] + (B[idx] - A[idx]) * u[:, None] + (C[idx] - A[idx]) * v[:, None]
    bpy.data.objects.remove(o)
    bpy.data.meshes.remove(me)
    P = np.column_stack([P[:, 0], -P[:, 2], P[:, 1]])       # stand up, front faces -Y
    return P - P.mean(axis=0)


def dust(n, box, r=0.009, strength=0.85, seed=5):
    rng = np.random.default_rng(seed)
    P = np.column_stack([rng.uniform(*box[i], n) for i in range(3)])
    return points(P, r, mat_emit("dust", (1, 0.95, 0.88, 1), strength), "DUST")


# ---------------------------------------------------------------- the drift line (the constant)
def smooth(pts, n=240):
    """Catmull-Rom through control points -> dense polyline."""
    P = np.array(pts, float)
    P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out, segs = [], len(P) - 3
    for i in range(segs):
        p0, p1, p2, p3 = P[i:i + 4]
        for t in np.linspace(0, 1, max(2, n // segs), endpoint=False):
            out.append(0.5 * (2 * p1 + (p2 - p0) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (3 * p1 - p0 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return np.array(out)


def line(pts, r=0.025, strength=1.0, col=AMBER, lights=0, energy=60, draw=None, mat=None, name="DRIFT"):
    """The amber drift line. draw=(f0, f1, a, b) animates it drawing itself, lights follow the tip."""
    S = smooth(pts)
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions, cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = "3D", r, 4, True
    sp = cu.splines.new("POLY")
    sp.points.add(len(S) - 1)
    for i, p in enumerate(S):
        sp.points[i].co = (p[0], p[1], p[2], 1)
    cu.materials.append(mat or mat_emit(name, col, strength))
    o = link(bpy.data.objects.new(name, cu))
    if draw:
        f0, f1, a, b = draw
        safe(cu, bevel_factor_mapping_end="SPLINE")
        key(cu, "bevel_factor_end", [(f0, a), (f1, b)])
    for k in range(lights):
        u = (k + 0.5) / lights
        p = S[int(u * (len(S) - 1))]
        L = light("POINT", (p[0], p[1], p[2] + 0.18), energy, AMBER_L, 0.25, shadow=False)
        if draw:
            f0, f1, a, b = draw
            if u > a:
                fon = f0 + (f1 - f0) * min(1.0, (u - a) / max(b - a, 1e-3))
                key(L.data, "energy", [(max(1, int(fon) - 1), 0.0), (int(fon) + 3, energy)])
    return o, S


def at(S, u):
    return Vector(S[int(min(max(u, 0), 1) * (len(S) - 1))])


# ---------------------------------------------------------------- camera grammar
def cam(lens=35, fstop=None, name="CAM"):
    cd = bpy.data.cameras.new(name)
    cd.lens, cd.clip_start, cd.clip_end, cd.sensor_width = lens, 0.02, 500, 36
    if fstop:
        cd.dof.use_dof, cd.dof.aperture_fstop = True, fstop
    o = link(bpy.data.objects.new(name, cd))
    if bpy.context.scene.camera is None:
        bpy.context.scene.camera = o
    return o


def aim(loc, tgt, roll=0.0, prev=None):
    q = (Vector(tgt) - Vector(loc)).to_track_quat("-Z", "Y")
    if roll:
        q = q @ Quaternion((0, 0, 1), math.radians(roll))
    return q.to_euler("XYZ", prev) if prev is not None else q.to_euler("XYZ")


def ease(t, k="io"):
    t = min(max(t, 0.0), 1.0)
    if k == "io":
        return t * t * t * (t * (t * 6 - 15) + 10)
    if k == "o":
        return 1 - (1 - t) ** 3
    if k == "i":
        return t ** 3
    if k == "xo":
        return 1.0 if t >= 1 else 1 - 2 ** (-10 * t)
    return t


def mix(a, b, t):
    if isinstance(a, (int, float)):
        return a + (b - a) * t
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(len(a)))


def seg(f, f0, f1):
    return min(max((f - f0) / max(f1 - f0, 1e-6), 0.0), 1.0)


def shake(f, amp, seed=0, speed=1.0):
    r = random.Random(seed)
    out = []
    for _ in range(3):
        v = 0.0
        for k in range(3):
            v += math.sin(f * (0.11 + r.random() * 0.2) * (k + 1) * speed + r.random() * 6.28) / (k + 1)
        out.append(v * amp)
    return Vector(out)


def animate(c, f0, f1, fn):
    """Key the camera on every frame from fn(t, f) -> dict(loc, tgt, lens?, roll?, focus?, jitter?)."""
    prev = None
    for f in range(f0, f1 + 1):
        s = fn(seg(f, f0, f1), f)
        loc = Vector(s["loc"]) + (s["jitter"] if "jitter" in s else Vector())
        c.location = loc
        e = aim(loc, s["tgt"], s.get("roll", 0.0), prev)
        c.rotation_euler = e
        prev = e.copy()
        c.keyframe_insert("location", frame=f)
        c.keyframe_insert("rotation_euler", frame=f)
        if "lens" in s:
            c.data.lens = s["lens"]
            c.data.keyframe_insert("lens", frame=f)
        if "focus" in s and c.data.dof.use_dof:
            c.data.dof.focus_distance = s["focus"]
            c.data.dof.keyframe_insert("focus_distance", frame=f)


def dist(a, b):
    return (Vector(a) - Vector(b)).length


def bind(c, frame):
    m = bpy.context.scene.timeline_markers.new(c.name, frame=frame)
    m.camera = c


# ---------------------------------------------------------------- worlds
def world_color(sc, col=GROUND):
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = col


def world_gradient(sc, top=IMPERIAL, horizon=GROUND, strength=1.0):
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    tc, sep, ramp = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ"), nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.0, horizon
    e[1].position, e[1].color = 0.5, top
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = strength


def world_studio(sc, strength=2.6):
    """Softbox bands for chrome to reflect; the camera itself only ever sees the black ground."""
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    tc, sep, mr = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ"), nt.nodes.new("ShaderNodeMapRange")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    cr = ramp.color_ramp
    cr.interpolation = "EASE"
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], mr.inputs["Value"])
    mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = -1, 1
    nt.links.new(mr.outputs["Result"], ramp.inputs[0])
    blk = (0.0, 0.0, 0.0, 1)
    stops = [(0.0, blk), (0.40, (0.01, 0.012, 0.018, 1)), (0.47, (0.35, 0.40, 0.55, 1)), (0.52, blk),
             (0.575, AMBER), (0.61, blk), (0.80, blk), (0.86, (1, 1, 1, 1)), (0.93, (1, 1, 1, 1)), (0.975, blk)]
    cr.elements[0].position, cr.elements[0].color = stops[0]
    cr.elements[1].position, cr.elements[1].color = stops[-1]
    for p, c in stops[1:-1]:
        cr.elements.new(p).color = c
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    bg.inputs[1].default_value = strength
    black = nt.nodes.new("ShaderNodeBackground")
    black.inputs[0].default_value = GROUND
    lp, mx = nt.nodes.new("ShaderNodeLightPath"), nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lp.outputs["Is Camera Ray"], mx.inputs[0])
    nt.links.new(bg.outputs[0], mx.inputs[1])
    nt.links.new(black.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], nt.nodes["World Output"].inputs["Surface"])


def floor(rough=0.35, col="09090B", size=80):
    return plane("FLOOR", size, size, mat_pbr("floor", lin(col), rough))


STAIR = dict(W=7.0, d=0.62, h=0.34, n=26)


def stair_world(fogd=0.026):
    W, d, h, n = STAIR["W"], STAIR["d"], STAIR["h"], STAIR["n"]
    boxes("STAIRS", [((0, i * d + d / 2, (i + 1) * h / 2), (W, d, (i + 1) * h)) for i in range(n)]
          + [((0, -9, -0.05), (W, 18, 0.1))], mat_pbr("concrete", CONCRETE, 0.9))
    boxes("WALLS", [((-W / 2 - 0.3, 5, 7), (0.6, 44, 16)), ((W / 2 + 0.3, 5, 7), (0.6, 44, 16))],
          mat_pbr("wall", lin("141417"), 0.93))
    light("AREA", (0, n * d + 1.5, n * h + 6.5), 2600, (1, 0.93, 0.84), 6, rot=(-40, 0, 0))
    fog(fogd, (W + 1, 46, 26), (0, 6, 10))
    dust(1400, ((-W / 2, W / 2), (-6, n * d), (0, n * h + 4)))
    pts = [(1.3, -4.5, 0.06), (0.5, -1.8, 0.06), (0.1, -0.5, 0.22)]
    for i in range(1, n, 2):
        y = i * d + d / 2
        pts.append((math.sin(y * 0.52) * 1.7 + 0.3, y, y * h / d + h + 0.1))
    return pts


def press_world(poster, size=(6, 4)):
    floor(0.6, "0A0A0C")
    plane("POSTER", size[0], size[1], mat_tex("poster", poster, 0.8, es=0.62), loc=(0, 0, 0.002))
    light("AREA", (0.4, -1.2, 6.0), 380, (1, 0.96, 0.9), 5, rot=(12, 0, 0))


def billboard_world(poster, zc=2.1):
    floor(0.16, "08080A")
    plane("POSTER", 6, 4, mat_tex("poster", poster, 0.85, es=0.62), loc=(0, 0, zc), rot=(90, 0, 0))
    light("AREA", (0.5, -4.6, 5.6), 420, (1, 0.96, 0.9), 4.5, rot=(52, 0, 0))
    return zc


def phone(loc, rotz, img, name="PHONE"):
    body = boxes(name, [((0, 0, 0.76), (0.72, 0.08, 1.48))], mat_pbr("phone", lin("1C1D22"), 0.28, metal=0.6))
    bv = body.modifiers.new("B", "BEVEL")
    bv.width, bv.segments = 0.05, 4
    m = mat_tex("scr", img, 0.3, es=0.9)
    scr = plane(name + "S", 0.62, 1.34, m, loc=(0, -0.042, 0.76), rot=(90, 0, 0))
    scr.parent = body
    body.location, body.rotation_euler = loc, (0, 0, math.radians(rotz))
    return body, m


def signal_world():
    floor(0.22, "0B0B0D")
    for x in (-1.2, 1.2):
        light("SPOT", (x, -1.2, 3.4), 520, (1, 1, 1), 0.3, spot=42, aim_at=(x * 0.8, 0, 0.7))


def void_world():
    floor(0.12, "060607")


# ---------------------------------------------------------------- shots
def s01(s):
    sc = reset()
    ln, S = line(stair_world(), r=0.03, strength=1.0, lights=7, energy=75, draw=(1, 52, 0.0, 0.62))
    d, h = STAIR["d"], STAIR["h"]
    text("22.09", "Unbounded-900", 0.85, 0.12, 0.0, loc=(-1.75, 5 * d + 0.25, 6 * h), rot=(90, 0, 0),
         mat=mat_pbr("date", WHITE, 0.55, emit=WHITE, es=0.3), ay="BOTTOM")
    c = cam(20, fstop=2.8)
    animate(c, 1, frames(s), lambda t, f: dict(
        loc=mix((1.5, -3.3, 0.22), (0.3, -0.7, 2.7), ease(t)), tgt=mix((0.0, 6.0, 2.2), (-0.4, 9.0, 5.0), ease(t)),
        lens=mix(18, 24, ease(t)), focus=mix(7.6, 4.6, ease(t))))
    return sc


def s02(s):
    sc = reset()
    ln, S = line(stair_world(), r=0.03, strength=1.0, lights=7, energy=75, draw=(1, 40, 0.62, 1.0))
    for u, fd in ((0.40, lf(s, 3.60)), (0.60, lf(s, 3.78))):
        p = at(S, u)
        orb = sphere(0.24, (p.x, p.y, p.z + 15), mat_emit("orb", (1, 0.93, 0.8, 1), 1.0))
        L = light("POINT", (p.x, p.y, p.z + 0.5), 0, AMBER_L, 0.3, shadow=False)
        for f in range(1, frames(s) + 1):
            g = seg(f, fd, fd + 8)
            hover = 0.25 * math.sin(f * 0.2 + u * 9) if g == 0 else 0.0
            orb.location = (p.x, p.y, p.z + 0.26 + (15 + hover) * (1 - g * g))
            orb.keyframe_insert("location", frame=f)
        key(L.data, "energy", [(fd + 7, 0.0), (fd + 9, 1100.0), (fd + 20, 260.0)])
        lab = text("DROP 01" if u < 0.5 else "DROP 02 · +90 MIN", "PlexMono-600", 0.42, 0.0,
                   loc=(p.x + 0.45, p.y - 0.05, p.z + 0.02), mat=mat_emit("lab", WHITE, 1.0), ax="LEFT")
        key(lab, "scale", [(fd + 8, (0, 0, 0)), (fd + 11, (1, 1, 1))])
    c = cam(35, fstop=4.0)
    animate(c, 1, frames(s), lambda t, f: dict(
        loc=mix((0.4, 8.6, 23.0), (0.0, 8.0, 20.5), ease(t)), tgt=mix((0.4, 8.63, 0.0), (0.0, 8.03, 0.0), ease(t)),
        roll=mix(0, -14, ease(t)), lens=mix(33, 38, ease(t)), focus=mix(18.5, 16.0, ease(t))))
    return sc


def s03(s):
    sc = reset()
    press_world("P90.png")
    L = LAYOUT["p90"]
    text("90", "Unbounded-900", L["size"], 0.004, loc=(L["x"], L["base"], 0.012), mat=mat_pbr("ink", INK, 0.9),
         ax="LEFT", ay="BOTTOM_BASELINE")
    line([(x, L["tl_y"] + 0.05, 0.03) for x in (-2.75, -1.3, 0.2, 1.6, 2.75)], r=0.012, strength=1.0)
    c = cam(40)
    animate(c, 1, frames(s), lambda t, f: dict(
        loc=mix((0.35, -0.3, 7.9), (0.05, -0.1, 6.4), ease(t, "o")), tgt=mix((0.35, -0.25, 0.0), (0.05, -0.05, 0.0), ease(t, "o")),
        roll=mix(4, 0, ease(t)), focus=7.0))
    return sc


def s04(s):
    sc = reset(blur=True)
    press_world("P90.png")
    L = LAYOUT["p90"]
    n90 = text("90", "Unbounded-900", L["size"], 0.004, loc=(L["x"], L["base"], 0.012), mat=mat_pbr("ink", INK, 0.4),
               ax="LEFT", ay="BOTTOM_BASELINE")
    f0, f1 = lf(s, 6.28), lf(s, 6.95)
    for f in range(1, frames(s) + 1):
        g = ease(seg(f, f0, f1), "o")
        n90.rotation_euler = (math.radians(92 * g - 2 * g * g), 0, 0)
        n90.keyframe_insert("rotation_euler", frame=f)
        n90.data.extrude = 0.004 + 0.2 * g
        n90.data.keyframe_insert("extrude", frame=f)
    xc = L["x"] + L["w"] / 2
    light("SPOT", (xc + 0.4, L["base"] + 2.6, 2.9), 3400, AMBER_L, 0.5, spot=60, aim_at=(xc, L["base"], 0.7))
    light("AREA", (xc - 2.6, L["base"] - 2.4, 0.9), 260, (1, 0.97, 0.92), 1.6, aim_at=(xc, L["base"], 0.7))
    line([(x, L["tl_y"] + 0.05, 0.03) for x in (-2.75, -1.3, 0.2, 1.6, 2.75)], r=0.012, strength=1.0)
    c = cam(50, fstop=2.8)
    tgt1 = (xc - 0.1, L["base"] + 0.05, 0.7)
    animate(c, 1, frames(s), lambda t, f: dict(
        loc=mix((0.05, -0.1, 6.4), (xc - 1.3, -4.9, 0.32), ease(t)), tgt=mix((0.05, -0.05, 0.0), tgt1, ease(t)),
        lens=mix(40, 20, ease(t)), roll=mix(0, -6, ease(t)), focus=mix(6.4, dist((xc - 1.3, -4.9, 0.32), tgt1), ease(t))))
    return sc


def s05(s):
    sc = reset(res=(RES[0] // 2, RES[1] // 2))
    signal_world()
    A, mA = phone((-0.95, 0, 0), 45, "SCREEN_A.png", "PA")
    B, mB = phone((0.95, 0, 0), -45, "SCREEN_B.png", "PB")
    line([(-3, 0.8, 0.02), (-0.95, -0.35, 0.02), (0, 0.35, 0.02), (0.95, -0.35, 0.02), (3, 0.8, 0.02)], r=0.02,
         strength=1.0, lights=3, energy=40)
    for m, flashes in ((mA, (47, 83, 96)), (mB, (71, 89, 96))):
        sock = emission_socket(m)
        pairs = [(1, 0.9)]
        for fl in flashes:
            pairs += [(fl - 1, 0.9), (fl, 3.0), (fl + 6, 0.9)]
        key(sock, "default_value", pairs)
    N = frames(s)
    sA, sB = Vector((-0.92, -0.03, 0.8)), Vector((0.92, -0.03, 0.8))
    shots = {
        "c1": lambda t, f: dict(loc=mix((0.45, -4.3, 0.55), (0.3, -3.6, 0.6), t), tgt=(0, 0, 0.8), lens=28, roll=12),
        "c2": lambda t, f: dict(loc=(-0.05, -0.95, 0.9), tgt=sA, lens=mix(30, 62, ease(seg(f, 47, 52), "xo")), roll=-18),
        "c3": lambda t, f: dict(loc=(0.05, -0.95, 0.9), tgt=sB, lens=mix(30, 62, ease(seg(f, 71, 76), "xo")), roll=18),
        "c4": lambda t, f: dict(loc=(0.1, -1.7, 3.2), tgt=(0, 0, 0.6), lens=22, roll=-25),
        "c5": lambda t, f: dict(loc=(0, -1.35, 0.09), tgt=(0, 0, 1.05), lens=17, roll=8),
        "c6": lambda t, f: dict(loc=(-3.9, -0.7, 0.9), tgt=(0, 0, 0.8), lens=35, roll=0),
    }
    cams = {}
    for i, (name, fn) in enumerate(shots.items()):
        c = cam(30, name=name)
        cams[name] = c
        animate(c, 1, N, lambda t, f, fn=fn, i=i: dict(fn(t, f), jitter=shake(f, 0.012, seed=i)))
    for f, name in ((1, "c1"), (47, "c2"), (71, "c3"), (83, "c4"), (87, "c2"), (91, "c5"), (95, "c3"), (99, "c6"),
                    (103, "c4"), (107, "c2"), (111, "c5"), (115, "c1")):
        bind(cams[name], f)
    return sc


def s06(s):
    sc = reset()
    world_gradient(sc)
    fl = floor(0.28, "050608")
    m = fl.data.materials[0]
    nt = m.node_tree
    tc, mp, t = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeMapping"), nt.nodes.new("ShaderNodeTexImage")
    mp.inputs["Scale"].default_value = (20, 20, 1)
    t.image = bpy.data.images.load(os.path.join(TEX, "GRID.png"))
    nt.links.new(tc.outputs["UV"], mp.inputs[0])
    nt.links.new(mp.outputs[0], t.inputs[0])
    nt.links.new(t.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Emission Color"])
    nt.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.1
    fog(0.012, (80, 80, 20), (0, 20, 8), col=(0.7, 0.76, 0.95, 1))
    dust(1600, ((-10, 10), (-6, 20), (0, 8)), strength=0.8)
    light("AREA", (0, -3, 7), 700, (0.8, 0.86, 1.0), 6, rot=(25, 0, 0))
    hA, hB = 52.3 / 20, 66.4 / 20
    A = boxes("BAR_A", [((0, 0, 0.5), (1.1, 1.1, 1.0))], mat_pbr("barA", lin("3A4050"), 0.45))
    A.location, A.scale = (-0.95, 0, 0), (1, 1, hA)
    B = boxes("BAR_B", [((0, 0, 0.5), (1.1, 1.1, 1.0))], mat_pbr("barB", WHITE, 0.35))
    B.location = (0.95, 0, 0)
    fr, fu = lf(s, 13.3), lf(s, 13.95)
    key(B, "scale", [(1, (1, 1, hA)), (fr, (1, 1, hA)), (fu, (1, 1, hB))])
    cap = boxes("CAP", [((0, 0, 0), (1.12, 1.12, 0.04))], mat_emit("cap", AMBER, 1.0))
    cap.location = (0.95, 0, hA + 0.02)
    key(cap, "location", [(fr, (0.95, 0, hA + 0.02)), (fu, (0.95, 0, hB + 0.02))])
    c = cam(28, fstop=2.8)
    lA = text("52.3", "Unbounded-800", 0.42, 0.02, loc=(-0.95, 0, hA + 0.55), mat=mat_emit("lA", STEEL, 1.0))
    lB = text("66.4", "Unbounded-800", 0.42, 0.02, loc=(0.95, 0, hA + 0.55), mat=mat_emit("lB", WHITE, 1.0))
    key(lB, "location", [(fr, (0.95, 0, hA + 0.55)), (fu, (0.95, 0, hB + 0.55))])
    d14 = text("+14", "Unbounded-900", 0.75, 0.06, loc=(0.0, -0.4, hB + 0.78), mat=mat_emit("d14", AMBER, 1.0))
    key(d14, "scale", [(lf(s, 13.6) - 1, (0, 0, 0)), (lf(s, 13.6) + 4, (1.15, 1.15, 1.15)), (lf(s, 13.6) + 8, (1, 1, 1))])
    for o in (lA, lB, d14):
        con = o.constraints.new("TRACK_TO")
        con.target, con.track_axis, con.up_axis = c, "TRACK_Z", "UP_Y"
    line([(-0.95, 0.0, hA + 0.06), (-0.4, -0.25, hA + 0.5), (0.4, -0.25, hB + 0.45), (0.95, 0.0, hB + 0.08)],
         r=0.022, strength=1.0, lights=2, energy=40, draw=(fu, fu + 10, 0.0, 1.0))
    boxes("RULER", [((-1.85, 0, 1.75), (0.02, 0.02, 3.5))] + [((-1.8, 0, v / 20), (0.12, 0.02, 0.012)) for v in range(0, 71, 10)],
          mat_emit("ruler", STEEL, 0.8))
    for v in (0, 20, 40, 60):
        text(str(v), "PlexMono-600", 0.16, 0.0, loc=(-2.0, 0, v / 20), rot=(90, 0, 0), mat=mat_emit("rl", STEEL, 0.8), ax="RIGHT")
    ct = text("CODING TEST", "PlexMono-600", 0.3, 0.0, loc=(0, -1.5, 0.004), mat=mat_emit("ct", STEEL, 1.0))
    key(ct, "scale", [(lf(s, 16.45) - 1, (0, 0, 0)), (lf(s, 16.45) + 3, (1, 1, 1))])

    def mv(t, f):
        e = ease(t)
        a, R = math.radians(-62 + 88 * e), 7.4 - 1.3 * e
        loc = (R * math.sin(a), -R * math.cos(a), 0.55 + 1.9 * e)
        return dict(loc=loc, tgt=(0, 0, 2.05 + 0.75 * e), lens=26 + 7 * e, focus=dist(loc, (0, 0, 2.2)))
    animate(c, 1, frames(s), mv)
    return sc


def s07(s):
    sc = reset(blur=True, engine="CYCLES")        # real reflections: chrome is the one Cycles shot
    world_studio(sc, 1.6)
    chrome = mat_pbr("chrome", (0.95, 0.96, 0.98, 1), 0.035, metal=1.0)
    text("+14", "Unbounded-900", 2.3, 0.32, 0.045, rot=(90, 0, 0), mat=chrome)
    # softboxes: two cool strips and one amber kicker, so the chrome has something to mirror
    light("AREA", (-4.5, -3.5, 2.5), 2600, (0.9, 0.95, 1.0), 3.0, aim_at=(0, 0, 0))
    light("AREA", (4.8, -2.5, 3.5), 2000, (1.0, 1.0, 1.0), 2.5, aim_at=(0, 0, 0))
    light("AREA", (0.5, 3.5, 3.0), 1800, AMBER_L, 2.0, aim_at=(0, 0, 0))
    rng = random.Random(4)
    for k in range(3):
        R, ph, tilt = 3.6 + 0.8 * k, rng.random() * 6.28, 1.0 + 0.5 * k
        pts = []
        for a in np.linspace(0, 2 * math.pi, 13):
            front = math.sin(a) < -0.15            # the near side stays under the number
            z = -1.75 - 0.45 * abs(math.sin(2 * a + ph)) if front else tilt * math.sin(2 * a + ph)
            pts.append((R * math.cos(a), 0.9 * R * math.sin(a) + 1.6, z))
        line(pts, r=0.055, mat=chrome, name=f"TANGLE{k}")
    line([(-6, 1.5, -1.3), (-3, -0.9, -1.0), (-1, -0.8, -1.3), (1, -0.9, -1.25), (3, -0.6, -0.7), (6, 1.5, 0.4)],
         r=0.03, strength=1.0, lights=3, energy=50)
    c = cam(18, fstop=2.2)
    fl = lf(s, 19.15)

    def mv(t, f):
        g = ease(seg(f, 1, fl), "o")
        a = math.radians(mix(108, 0, g))
        R = mix(3.3, 6.3, g) + 0.25 * seg(f, fl, frames(s))
        loc = (R * math.sin(a), -R * math.cos(a), mix(0.1, 0.55, g))
        return dict(loc=loc, tgt=(0, 0, mix(-0.2, 0.05, g)), roll=mix(26, 0, g), lens=mix(18, 32, g), focus=R)
    animate(c, 1, frames(s), mv)
    return sc


def cloud_bg(seed=9):
    rng = np.random.default_rng(seed)
    P = np.column_stack([rng.uniform(-45, 45, 5000), rng.uniform(8, 70, 5000), rng.uniform(-25, 25, 5000)])
    points(P, 0.035, mat_emit("far", (0.8, 0.85, 1.0, 1), 0.8), "FAR")


def s08(s):
    sc = reset()
    P = text_points("+14", 32000, size=2.2, ext=0.25)
    rng = np.random.default_rng(8)
    dirn = P + rng.normal(0, 0.6, P.shape)
    dirn /= np.linalg.norm(dirn, axis=1)[:, None]
    dd = rng.gamma(2.0, 1.3, len(P))[:, None]
    D = P + dirn * dd + np.array([0, 0.4, 0.5]) * dd
    ang = 0.35 * dd[:, 0]
    D = np.column_stack([D[:, 0] * np.cos(ang) - D[:, 1] * np.sin(ang), D[:, 0] * np.sin(ang) + D[:, 1] * np.cos(ang), D[:, 2]])
    o = points(P, 0.0065, mat_emit("pts", (1, 1, 1, 1), 1.0), "CLOUD")
    k = shape(o, "Disp", D)
    f0 = lf(s, 20.25)
    for f in range(1, frames(s) + 1):
        k.value = ease(seg(f, f0, frames(s)), "i")
        k.keyframe_insert("value", frame=f)
    cloud_bg()
    dot = sphere(0.06, (0.0, -0.35, 0.0), mat_emit("dot", AMBER, 1.0))
    light("POINT", (0, -0.5, 0), 30, AMBER_L, 0.1, shadow=False)
    fp = lf(s, 21.8)
    key(dot, "scale", [(fp - 1, (1, 1, 1)), (fp + 3, (1.9, 1.9, 1.9)), (fp + 10, (1.2, 1.2, 1.2))])
    c = cam(28, fstop=1.8)

    def mv(t, f):
        lens = mix(28, 110, ease(t))
        d = 5.6 * lens / 28
        return dict(loc=(0, -d, 0.25), tgt=(0, 0, 0), lens=lens, focus=d)
    animate(c, 1, frames(s), mv)
    return sc


def s09(s):
    sc = reset()
    zc = billboard_world("P_UPDATE.png")
    line([(-5, -1.3, 0.03), (-2, -0.6, 0.03), (0, -1.0, 0.03), (2, -0.5, 0.03), (5, -1.4, 0.03)], r=0.02,
         strength=1.0, lights=3, energy=45)
    c = cam(30, fstop=2.0)

    def mv(t, f):
        e = ease(t)
        loc, tgt = mix((-4.2, -5.6, 1.5), (2.6, -4.6, 2.3), e), mix((-1.5, 0, 2.0), (0.6, 0, 2.05), e)
        return dict(loc=loc, tgt=tgt, lens=mix(30, 38, e), roll=mix(8, 3, e), focus=dist(loc, tgt))
    animate(c, 1, frames(s), mv)
    return sc


def s10(s):
    sc = reset(blur=True)
    zc = billboard_world("P_COOL.png")
    line([(-5, -1.3, 0.03), (-2, -0.7, 0.03), (0, -1.1, 0.03), (2, -0.6, 0.03), (5, -1.4, 0.03)], r=0.02,
         strength=1.0, lights=3, energy=45)
    st = (LAYOUT["cool"]["x"], 0.0, zc + LAYOUT["cool"]["y"])
    fs = lf(s, 28.3)
    c = cam(35, fstop=2.8)

    def mv(t, f):
        a, b = ease(seg(f, 1, fs)), ease(seg(f, fs, fs + 5), "xo")
        loc = mix(mix((0.2, -7.3, 2.1), (0.1, -6.0, 2.1), a), (st[0] + 0.12, -1.3, st[2] + 0.05), b)
        tgt = mix((0.0, 0.0, 2.1), st, b)
        j = shake(f, 0.01 * seg(f, fs + 4, fs + 6), seed=3, speed=2.5)
        return dict(loc=loc, tgt=tgt, lens=mix(35, 46, b), roll=mix(0, -10, b), focus=dist(loc, tgt), jitter=j)
    animate(c, 1, frames(s), mv)
    return sc


def s11(s):
    sc = reset(res=(RES[0] // 2, RES[1] // 2))
    signal_world()
    P, m = phone((0, 0, 0), 20, "SCREEN_DONE.png")
    key(P, "rotation_euler", [(1, (0, 0, math.radians(24))), (frames(s), (0, 0, math.radians(-22)))])
    ring = [(1.15 * math.cos(a), 1.15 * math.sin(a), 0.02) for a in np.linspace(0, 2 * math.pi, 13)]
    line(ring, r=0.02, strength=1.0, lights=3, energy=40)
    fn, fc = lf(s, 30.4), lf(s, 31.55)
    fn, fc = fn + (fn + 1) % 2, fc + (fc + 1) % 2          # odd frames: this shot renders on twos
    N = frames(s)
    c1, c2, c3 = cam(30, name="c1"), cam(50, name="c2"), cam(30, name="c3")
    animate(c1, 1, N, lambda t, f: dict(loc=mix((2.2, -3.2, 2.1), (1.9, -2.8, 1.9), t), tgt=(0, 0, 0.75), lens=30, roll=-10,
                                        jitter=shake(f, 0.01, 1)))
    animate(c2, 1, N, lambda t, f: dict(loc=(0.25, -1.25, 0.85), tgt=(0, 0, 0.8), lens=mix(35, 70, ease(seg(f, fn, fn + 5), "xo")),
                                        roll=15, jitter=shake(f, 0.012, 2)))
    animate(c3, 1, N, lambda t, f: dict(loc=(-0.15, -0.55, 1.55), tgt=(0, -0.05, 0.85), lens=mix(24, 40, ease(seg(f, fc, fc + 5), "xo")),
                                        roll=-28, jitter=shake(f, 0.012, 3)))
    for f, c in ((1, c1), (fn, c2), (fc, c3)):
        bind(c, f)
    return sc


def wrong(mat_strength=1.0, **kw):
    return text("WRONG", "Unbounded-900", 1.45, kw.pop("ext", 0.3), 0.02, mat=mat_emit("am", AMBER, mat_strength), **kw)


def s12(s):
    sc = reset(blur=True)
    void_world()
    wrong(rot=(90, 0, 0), ay="BOTTOM")
    c = cam(50)

    def mv(t, f):
        a = ease(seg(f, 1, 7), "xo")
        loc = mix(mix((0, -15, 0.9), (0, -8.2, 0.75), a), (0, -7.8, 0.72), seg(f, 7, frames(s)))
        return dict(loc=loc, tgt=(0, 0, 0.62), jitter=shake(f, 0.05 * max(0.0, 1 - seg(f, 6, 14)), 4, 3.0))
    animate(c, 1, frames(s), mv)
    return sc


def s13(s):
    sc = reset()
    void_world()
    text("NOT ONLY", "Unbounded-800", 0.5, 0.08, loc=(0, 0.25, 1.2), rot=(90, 0, 0), mat=mat_emit("w", WHITE, 1.0), ay="BOTTOM")
    wrong(rot=(90, 0, 0), ay="BOTTOM")
    c = cam(22)
    animate(c, 1, frames(s), lambda t, f: dict(loc=mix((-1.9, -4.3, 0.1), (-1.2, -3.6, 0.2), ease(t)),
                                              tgt=mix((0, 0, 0.9), (0, 0, 1.0), ease(t)), roll=mix(-24, -12, ease(t))))
    return sc


def s14(s):
    sc = reset(blur=True)
    for i in range(16):
        wrong(0.85 ** i, ext=0.05, loc=(0, 0, -i * 1.3), rot=(0, 0, i * 9))
    c = cam(35)

    def mv(t, f):
        z = mix(5.5, -6.5, ease(t, "i"))
        return dict(loc=(0, -0.05, z), tgt=(0, 0.0, z - 10), roll=mix(0, -75, ease(t)), lens=mix(35, 16, ease(t)))
    animate(c, 1, frames(s), mv)
    return sc


def s15(s):
    sc = reset()
    ctrl = [(-10, 2.5, -0.6), (-6, 0.5, 0.4), (-2, 1.5, -0.3), (2, -0.2, 0.3), (6, 1.0, -0.2), (10, -0.8, 0.5)]
    S = smooth(ctrl)
    n = 26000
    rng = np.random.default_rng(15)
    D = rng.normal(0, 1.0, (n, 3)) * np.array([3.4, 2.2, 1.8]) + np.array([0, 1.0, 0.2])
    Lp = S[(np.sort(rng.random(n)) * (len(S) - 1)).astype(int)] + rng.normal(0, 0.035, (n, 3))
    D = D[np.argsort(D[:, 0])]
    m = mat_emit("pts", (1, 1, 1, 1), 1.0)
    o = points(D, 0.0075, m, "CLOUD")
    k = shape(o, "Line", Lp)
    f0, f1 = lf(s, 37.2), lf(s, 40.1)
    for f in range(1, frames(s) + 1):
        k.value = ease(seg(f, f0, f1))
        k.keyframe_insert("value", frame=f)
    col = m.node_tree.nodes["Emission"].inputs[0]
    key(col, "default_value", [(lf(s, 39.9), (1, 1, 1, 1)), (lf(s, 40.6), AMBER)])
    line(ctrl, r=0.02, strength=1.0, lights=4, energy=45, draw=(lf(s, 40.3), lf(s, 41.4), 0.0, 1.0))
    cloud_bg(11)
    c = cam(70, fstop=2.2)

    def mv(t, f):
        e = ease(t)
        loc, tgt = mix((-5.5, -13, -0.6), (3.5, -12, 0.9), e), mix((-2.5, 0.8, 0.0), (2.5, 0.4, 0.1), e)
        return dict(loc=loc, tgt=tgt, lens=70, focus=dist(loc, tgt))
    animate(c, 1, frames(s), mv)
    return sc


def s16(s):
    sc = reset(blur=True)
    floor(0.18, "08080A")
    locA, rotA, locB, rotB = (-2.1, 0, 1.75), (90, 0, 24), (2.1, 0.6, 1.75), (90, 0, -24)
    plane("CARD_A", 2.4, 3.2, mat_tex("ca", "CARD_A.png", 0.85, es=0.55), loc=locA, rot=rotA)
    plane("CARD_B", 2.4, 3.2, mat_tex("cb", "CARD_B.png", 0.85, es=0.62), loc=locB, rot=rotB)
    light("AREA", (0, -5, 4.5), 420, (1, 0.96, 0.9), 5, rot=(48, 0, 0))
    light("SPOT", (2.6, 2.4, 3.6), 700, AMBER_L, 0.4, spot=50, aim_at=locB)

    def on_card(loc, rot, key_):
        e = Euler([math.radians(a) for a in rot])
        return Vector(loc) + e.to_matrix() @ Vector((LAYOUT[key_]["x"], LAYOUT[key_]["y"], 0.03))
    pA, pB = on_card(locA, rotA, "CARD_A"), on_card(locB, rotB, "CARD_B")
    line([tuple(pA), (pA.x + 0.9, pA.y - 1.1, pA.z + 0.4), (0.3, -1.4, 1.0), (pB.x - 1.0, pB.y - 1.2, pB.z + 0.3), tuple(pB)],
         r=0.02, strength=1.0, lights=3, energy=45, draw=(lf(s, 44.6), lf(s, 46.5), 0.0, 1.0))
    c = cam(38, fstop=2.0)
    w0, w1 = lf(s, 46.2), lf(s, 46.6)
    cA, cB = Vector(locA), Vector(locB)

    def mv(t, f):
        a, w, z = ease(seg(f, 1, w0)), ease(seg(f, w0, w1)), seg(f, w1, frames(s))
        loc = mix(mix((-3.6, -4.8, 1.8), (-1.4, -4.6, 1.8), a), mix((0.9, -4.3, 1.8), (1.25, -3.7, 1.8), z), w)
        tgt = mix(mix(tuple(cA), (-1.2, 0.1, 1.75), a), tuple(cB), w)
        return dict(loc=loc, tgt=tgt, roll=6 * math.sin(math.pi * w), focus=dist(loc, tgt))
    animate(c, 1, frames(s), mv)
    return sc


def s17(s):
    sc = reset(raytrace=True)
    world_studio(sc, 1.2)
    floor(0.5, "0B0B0D", 140)
    fog(0.01, (100, 100, 40), (0, 0, 10))
    dust(2200, ((-20, 20), (-12, 12), (0, 8)))
    d, h = 0.28, 0.16
    boxes("MINI_STAIRS", [((-12, -1.5 + i * d + d / 2, (i + 1) * h / 2), (2.2, d, (i + 1) * h)) for i in range(8)],
          mat_pbr("concrete", CONCRETE, 0.9))
    light("AREA", (-12, -0.5, 3.5), 120, (1, 0.93, 0.84), 2)
    tile = plane("MINI_LOBBY", 4, 4, mat_pbr("tile", lin("050608"), 0.3), loc=(-6, 2.8, 0.01))
    nt = tile.data.materials[0].node_tree
    t = nt.nodes.new("ShaderNodeTexImage")
    t.image = bpy.data.images.load(os.path.join(TEX, "GRID.png"))
    nt.links.new(t.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Emission Color"])
    nt.nodes["Principled BSDF"].inputs["Emission Strength"].default_value = 1.0
    boxes("MINI_BARS", [((-6.35, 2.8, 0.55), (0.4, 0.4, 1.1)), ((-5.65, 2.8, 0.7), (0.4, 0.4, 1.4))], mat_pbr("bar", WHITE, 0.4))
    light("POINT", (-6, 2.8, 2.2), 160, (0.5, 0.62, 1.0), 1, shadow=False)
    plane("MINI_PRESS", 3, 2, mat_tex("press", "P90.png", 0.8, es=0.55), loc=(-0.5, -2.8, 0.012), rot=(0, 0, 8))
    light("AREA", (-0.5, -2.8, 3), 140, (1, 0.96, 0.9), 2.5)
    text("+14", "Unbounded-900", 1.1, 0.16, 0.025, loc=(2.6, 1.6, 0.0), rot=(90, 0, 0), ay="BOTTOM",
         mat=mat_pbr("chrome", (0.92, 0.93, 0.96, 1), 0.08, metal=1.0))
    rng = np.random.default_rng(3)
    points(rng.normal(0, 1, (5000, 3)) * np.array([1.1, 0.8, 0.6]) + np.array([7, -2.2, 1.0]), 0.012,
           mat_emit("pts", (1, 1, 1, 1), 1.0), "MINI_CLOUD")
    text("WRONG", "Unbounded-900", 0.9, 0.06, loc=(12, 1.9, 0.05), rot=(0, 0, 14), mat=mat_emit("am", AMBER, 1.0))
    phone((-8.6, -4.4, 0.0), 30, "SCREEN_A.png", "MINI_PHONE")
    light("SPOT", (-8.6, -5.6, 2.2), 90, (0.4, 1.0, 0.6), 0.3, spot=40, aim_at=(-8.6, -4.4, 0.7))
    line([(-18, -3, 0.05), (-12.6, -2.1, 0.05), (-9, 0.6, 0.05), (-6, 1.9, 0.05), (-3, 0.2, 0.05), (-0.5, -1.6, 0.05),
          (1.4, -0.6, 0.05), (2.6, 0.9, 0.05), (4.6, 0.4, 0.05), (7, -0.8, 0.05), (9.6, -0.4, 0.05), (12, 1.0, 0.05), (17, 3, 0.05)],
         r=0.045, strength=1.0, lights=9, energy=110)
    for lab, x, y in (("W0 STAIR", -12, -2.5), ("W0 LOBBY", -6, 0.3), ("W1 PRESS", -0.5, -4.6), ("W4 SIGNAL", -8.6, -5.6),
                      ("W3 CHROME", 2.6, 0.5), ("W2 CLOUD", 7, -4.0), ("W0 VOID", 12, 0.6)):
        text(lab, "PlexMono-600", 0.34, 0.0, loc=(x, y, 0.02), mat=mat_emit("ml", WHITE, 0.75))
    c = cam(26, fstop=4.0)

    def mv(t, f):
        e = ease(t)
        loc, tgt = mix((2.9, -2.4, 0.75), (-1.0, -21.0, 25.0), e), mix((2.6, 1.6, 0.7), (-0.5, 0.0, 0.0), e)
        return dict(loc=loc, tgt=tgt, lens=mix(26, 30, e), roll=mix(0, -6, e), focus=dist(loc, tgt))
    animate(c, 1, frames(s), mv)
    return sc


def s18(s):
    """HOME: the ending ritual. Still water, fireflies, the line running to an amber dawn."""
    sc = reset(raytrace=True)
    nt = sc.world.node_tree
    bg = nt.nodes["Background"]
    tc, sep, ramp = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ"), nt.nodes.new("ShaderNodeValToRGB")
    nt.links.new(tc.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs[0])
    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.0, tuple(c * 0.95 for c in AMBER[:3]) + (1,)
    e[1].position, e[1].color = 0.55, lin("04050A")
    for p, c in ((0.035, lin("C8704A")), (0.12, lin("3A2448")), (0.28, lin("0B1A40"))):
        e.new(p).color = c
    nt.links.new(ramp.outputs[0], bg.inputs[0])
    # still water: dark, glossy, barely rippled, so it mirrors the dawn and the line
    water = plane("WATER", 600, 600, mat_pbr("water", lin("020305"), 0.05))
    wn = water.data.materials[0].node_tree
    nz, bump = wn.nodes.new("ShaderNodeTexNoise"), wn.nodes.new("ShaderNodeBump")
    nz.inputs["Scale"].default_value = 2.2
    bump.inputs["Strength"].default_value = 0.06
    wn.links.new(nz.outputs["Fac"], bump.inputs["Height"])
    wn.links.new(bump.outputs["Normal"], wn.nodes["Principled BSDF"].inputs["Normal"])
    ys = [-4, 2, 8, 15, 24, 36, 52, 75, 110, 160, 240, 330]
    line([(2.2 * math.sin(y * 0.09) * (1 - y / 360), y, 0.06) for y in ys], r=0.035, strength=1.0, lights=0)
    for y in (0, 5, 10, 16, 23, 31, 40, 52):
        x = 2.2 * math.sin(y * 0.09) * (1 - y / 360)
        lamp = light("POINT", (x, y, 0.35), 30, AMBER_L, 0.06, shadow=False)
        lamp.data.specular_factor = 0.12          # warm pools on the water, not white discs
    rng = np.random.default_rng(18)
    n = 900
    F0 = np.column_stack([rng.uniform(-12, 12, n), rng.uniform(-2, 60, n), rng.uniform(0.2, 4.0, n)])
    F1 = F0 + np.column_stack([rng.normal(0, 0.35, n), rng.normal(0, 0.35, n), rng.uniform(0.4, 1.3, n)])
    ff = points(F0, 0.022, mat_emit("firefly", AMBER, 1.0), "FIREFLIES")
    k = shape(ff, "Rise", F1)
    key(k, "value", [(1, 0.0), (frames(s), 1.0)])
    a, z = rng.uniform(0, 2 * math.pi, 2600), rng.uniform(0.06, 1.0, 2600)
    r = 320
    stars = np.column_stack([r * np.cos(a) * np.sqrt(1 - z ** 2), r * np.sin(a) * np.sqrt(1 - z ** 2) + 120, r * z])
    points(stars, 0.3, mat_emit("star", (0.9, 0.93, 1.0, 1), 0.9), "STARS")
    safe(sc.eevee, use_bokeh_jittered=True)     # round firefly bokeh
    c = cam(32, fstop=1.6)
    N = frames(s)

    def mv(t, f):
        g, up = ease(t), ease(seg(t, 0.6, 1.0))
        loc = mix((0.5, -3.0, 0.9), (0.2, 7.5, 1.15), g)
        return dict(loc=loc, tgt=mix((0.0, 40.0, 1.6), (0.0, 40.0, 13.0), up), focus=mix(7.0, 11.0, g),
                    lens=32, roll=mix(-1.5, 0.8, g), jitter=shake(f, 0.004, 18, 0.4))
    animate(c, 1, N, mv)
    return sc


BUILDERS = {k: v for k, v in globals().items() if k[:1] == "s" and k[1:].isdigit()}

if __name__ == "__main__":
    shot = next(s for s in SHOTS + [OUTRO] if s["id"] == ARGS[0])
    sc = BUILDERS["s" + shot["id"][1:]](shot)
    sc.frame_start, sc.frame_end, sc.frame_step = 1, frames(shot), shot.get("step", 1)
    if STILL:
        os.makedirs(os.path.join(BUILD, "stills"), exist_ok=True)
        sc.frame_set(int(STILL))
        sc.render.filepath = os.path.join(BUILD, "stills", f"{shot['id']}_{int(STILL):04d}.png")
        bpy.ops.render.render(write_still=True)
    else:
        out = os.path.join(BUILD, "frames", shot["id"])
        os.makedirs(out, exist_ok=True)
        sc.render.filepath = out + "/"
        bpy.ops.render.render(animation=True)
