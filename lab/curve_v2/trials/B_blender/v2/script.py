"""B_blender v2: procedural hypercar explainer shots: fan suction + skirts, two COPVs, 10 cold-gas nozzles.

Built in Python on Blender 5.2 EEVEE: no downloaded models or textures. Reflections and fill come from the Poly Haven
CC0 HDRI studio_small_09 (assets/polyhaven/CREDITS.txt) under coloured key lights; the camera sees a generated dark
studio. Mechanism follows lab/research/TESLA_ROADSTER_FACTS.md s2-s4: fans pull air from under the floor while skirts
seal the gap; COPVs 200 L (boot) + 400 L (passenger seat); 10 nozzles = 4 rear + 4 corner (down) + 2 front (yaw).

Shots (each a standalone clip from frame 1, 30 fps by default):
  hang  6 s  car pinned upside down under a slab, x-ray: fans pull air out, skirts seal, pressure arrows push in
  xray  6 s  x-ray build: tanks, then the 10 nozzles light in order (4 rear, 4 corner-down, 2 front)
  drop  5 s  nozzles fire, car drops from the slab, rolls upright, landing cushion (Mach-diamond jets, Mantaflow smoke)

Run:
  blender -b -P script.py -- --shot hang --aspect v --mode sheet --frames 1,90,160 --pct 50
  blender -b -P script.py -- --shot hang --aspect v --mode anim
"""
import bpy, bmesh, math, os, sys, time, argparse
from math import sin, cos, pi, sqrt, exp, radians, acos, atan2, tan
from mathutils import Vector, Matrix, Euler, Quaternion
from mathutils import noise as mnoise
import numpy as np
import bpy_extras.anim_utils as au

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--mode', default='sheet')
ap.add_argument('--shot', default='hang')
ap.add_argument('--aspect', default='v')
ap.add_argument('--fps', type=int, default=30)
ap.add_argument('--frames', default='1,90,160')
ap.add_argument('--pct', type=int, default=100)
ap.add_argument('--samples', type=int, default=24)
ap.add_argument('--out', default=os.path.join(HERE, 'frames'))
ap.add_argument('--hdri', default=os.path.expanduser('~/Bernard/lab/curve_v2/assets/polyhaven/studio_small_09_4k.exr'))
ap.add_argument('--hdri_strength', type=float, default=0.30)
ap.add_argument('--nosmoke', action='store_true')
ap.add_argument('--start', type=int, default=1)
ap.add_argument('--end', type=int, default=100000)
ap.add_argument('--save', default='')
A = ap.parse_args(argv)

SHOT = A.shot
VERT = A.aspect == 'v'
FPS = A.fps
F_END = int(round({'hang': 6.0, 'xray': 6.0, 'drop': 5.0, 'gauge': 2.0, 'refill': 8.0}.get(SHOT, 6.0) * FPS))
CUTS = []
T0 = time.time()

# =====================================================================================================
# helpers
# =====================================================================================================
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def smoothstep(a, b, x):
    t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

class Spline:
    """Natural cubic spline (C2) through (x, y) keys; clamps outside the key range."""
    def __init__(self, pts):
        pts = sorted(pts)
        x = [p[0] for p in pts]; y = [p[1] for p in pts]; n = len(x)
        h = [x[i + 1] - x[i] for i in range(n - 1)]
        al = [0.0] * n
        for i in range(1, n - 1):
            al[i] = 3 / h[i] * (y[i + 1] - y[i]) - 3 / h[i - 1] * (y[i] - y[i - 1])
        l = [1.0] + [0.0] * (n - 1); mu = [0.0] * n; z = [0.0] * n
        for i in range(1, n - 1):
            l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * mu[i - 1]
            mu[i] = h[i] / l[i]
            z[i] = (al[i] - h[i - 1] * z[i - 1]) / l[i]
        c = [0.0] * n; b = [0.0] * (n - 1); d = [0.0] * (n - 1)
        for j in range(n - 2, -1, -1):
            c[j] = z[j] - mu[j] * c[j + 1]
            b[j] = (y[j + 1] - y[j]) / h[j] - h[j] * (c[j + 1] + 2 * c[j]) / 3
            d[j] = (c[j + 1] - c[j]) / (3 * h[j])
        self.x, self.y, self.b, self.c, self.d = x, y, b, c, d

    def __call__(self, t):
        x = self.x
        t = min(max(t, x[0]), x[-1])
        lo, hi = 0, len(x) - 1
        while hi - lo > 1:
            m = (lo + hi) // 2
            if x[m] <= t: lo = m
            else: hi = m
        dx = t - x[lo]
        return self.y[lo] + self.b[lo] * dx + self.c[lo] * dx * dx + self.d[lo] * dx ** 3


def link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob)
    return ob

def mesh_obj(name, bm, mats=(), smooth=True, parent=None):
    me = bpy.data.meshes.new(name)
    bm.normal_update()
    bm.to_mesh(me); bm.free()
    for m in mats: me.materials.append(m)
    if smooth: me.shade_smooth()
    ob = link(bpy.data.objects.new(name, me))
    if parent: set_parent(ob, parent)
    return ob

def empty(name, loc=(0, 0, 0), parent=None):
    ob = link(bpy.data.objects.new(name, None))
    ob.empty_display_size = 0.3
    ob.location = loc
    if parent: set_parent(ob, parent)
    return ob

def set_parent(child, parent):
    bpy.context.view_layer.update()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()

def apply_mods(ob):
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg), preserve_all_data_layers=True, depsgraph=dg)
    old = ob.data
    ob.modifiers.clear()
    ob.data = me
    me.name = old.name
    bpy.data.meshes.remove(old)

def add_bevel(ob, width, segs=2, angle=35, harden=True):
    m = ob.modifiers.new('bevel', 'BEVEL')
    m.width = width; m.segments = segs; m.limit_method = 'ANGLE'; m.angle_limit = radians(angle)
    m.harden_normals = harden; m.use_clamp_overlap = True
    return m

def lathe(profile, seg=96, closed=False, a0=0.0, a1=2 * pi):
    """Revolve a (r, y) profile around the Y axis."""
    bm = bmesh.new()
    full = abs((a1 - a0) - 2 * pi) < 1e-6
    nring = seg if full else seg + 1
    rings = []
    for k in range(nring):
        a = a0 + (a1 - a0) * k / seg
        ca, sa = cos(a), sin(a)
        rings.append([bm.verts.new((r * ca, y, r * sa)) for (r, y) in profile])
    P = len(profile)
    for k in range(seg):
        Aa = rings[k]; Bb = rings[(k + 1) % nring]
        for j in (range(P) if closed else range(P - 1)):
            j2 = (j + 1) % P
            bm.faces.new((Aa[j], Aa[j2], Bb[j2], Bb[j]))
    return bm

def recalc(bm):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bm

# --- materials -----------------------------------------------------------------------------------------
def new_mat(name):
    m = bpy.data.materials.new(name)
    if m.node_tree is None:
        m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    return m, nt, out

def node(nt, typ, inputs=None, **props):
    n = nt.nodes.new(typ)
    for k, v in props.items(): setattr(n, k, v)
    for k, v in (inputs or {}).items():
        n.inputs[k].default_value = v
    return n

def lk(nt, a, b):
    nt.links.new(a, b)

def math_node(nt, op, a=None, b=None, clamp_=False):
    n = nt.nodes.new('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp_
    for i, v in enumerate((a, b)):
        if v is None: continue
        if isinstance(v, (int, float)): n.inputs[i].default_value = v
        else: nt.links.new(v, n.inputs[i])
    return n.outputs[0]

def principled(nt, **kw):
    p = nt.nodes.new('ShaderNodeBsdfPrincipled')
    for k, v in kw.items(): p.inputs[k].default_value = v
    return p

def rgba(c, a=1.0):
    return (c[0], c[1], c[2], a)

# --- animation -----------------------------------------------------------------------------------------
def channelbag(id_):
    if id_.animation_data is None: id_.animation_data_create()
    ad = id_.animation_data
    if ad.action is None:
        ad.action = bpy.data.actions.new(id_.name + 'Action')
    act = ad.action
    if ad.action_slot is None:
        slot = act.slots.new(id_type=id_.id_type, name=id_.name)
        ad.action_slot = slot
    return au.action_ensure_channelbag_for_slot(act, ad.action_slot)

def bake(id_, path, index, frames, values, interp='LINEAR', const_frames=()):
    cb = channelbag(id_)
    fc = cb.fcurves.find(path, index=index)
    if fc is None: fc = cb.fcurves.new(path, index=index)
    fc.keyframe_points.clear()
    fc.keyframe_points.add(len(frames))
    co = []
    for f, v in zip(frames, values): co += [float(f), float(v)]
    fc.keyframe_points.foreach_set('co', co)
    cset = set(const_frames)
    for kp, f in zip(fc.keyframe_points, frames):
        kp.interpolation = 'CONSTANT' if f in cset else interp
        kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    fc.update()
    return fc

def bake_fn(id_, path, index, fn, f0=-4, f1=None, pad=0):
    """Per-frame linear keys; a constant step half a frame before every hard cut (no motion blur across cuts)."""
    f1 = (F_END + 4) if f1 is None else f1
    frames, vals, const = [], [], set()
    for f in range(f0 - pad, f1 + pad + 1):
        frames.append(float(f)); vals.append(fn(f))
        if (f + 1) in CUTS:
            frames.append(f + 0.5); vals.append(fn(f + 1)); const |= {float(f), f + 0.5}
    bake(id_, path, index, frames, vals, 'LINEAR', const)

# --- easing / springs ----------------------------------------------------------------------------------
def cubic_bezier(p1x, p1y, p2x, p2y):
    """CSS-style cubic-bezier easing function t->y."""
    def bx(s): return 3 * (1 - s) ** 2 * s * p1x + 3 * (1 - s) * s * s * p2x + s ** 3
    def by(s): return 3 * (1 - s) ** 2 * s * p1y + 3 * (1 - s) * s * s * p2y + s ** 3
    def f(t):
        t = clamp(t)
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if bx(mid) < t: lo = mid
            else: hi = mid
        return by((lo + hi) / 2)
    return f

EASE_IO = cubic_bezier(0.65, 0.0, 0.35, 1.0)
EASE_OUT = cubic_bezier(0.16, 1.0, 0.3, 1.0)
EASE_IN = cubic_bezier(0.55, 0.0, 0.85, 0.35)
EASE_SOFT = cubic_bezier(0.45, 0.05, 0.25, 1.0)

def keys_fn(keys):
    """keys: [(frame, value, ease)] -> function(frame). ease applies to the segment ending at that key."""
    def f(fr):
        if fr <= keys[0][0]: return keys[0][1]
        for (fa, va, _), (fb, vb, e) in zip(keys, keys[1:]):
            if fr <= fb:
                t = (fr - fa) / (fb - fa)
                return va + (vb - va) * (e(t) if e else t)
        return keys[-1][1]
    return f

def spring(t, freq=2.2, damp=0.38):
    """Damped spring step response 0->1 (t in seconds, t<0 -> 0)."""
    if t <= 0: return 0.0
    w = 2 * pi * freq; wd = w * sqrt(1 - damp * damp)
    return 1 - exp(-damp * w * t) * (cos(wd * t) + damp * w / wd * sin(wd * t))

def sec(fr):
    return (fr - 1) / FPS


# =====================================================================================================
# scene reset + render settings
# =====================================================================================================
bpy.ops.wm.read_factory_settings(use_empty=True)
SC = bpy.context.scene
SC.render.engine = 'BLENDER_EEVEE'
SC.render.fps = FPS
SC.frame_start, SC.frame_end = 1, F_END
EE = SC.eevee
EE.taa_render_samples = A.samples
EE.use_raytracing = True
EE.ray_tracing_method = 'SCREEN'
EE.ray_tracing_options.resolution_scale = '1'
EE.ray_tracing_options.trace_max_roughness = 0.6
EE.ray_tracing_options.screen_trace_quality = 0.5
EE.ray_tracing_options.use_denoise = True
EE.use_fast_gi = True
EE.fast_gi_method = 'GLOBAL_ILLUMINATION'
EE.use_shadows = True
EE.shadow_ray_count = 1
EE.shadow_step_count = 6
EE.volumetric_tile_size = '4'
EE.volumetric_samples = 48
EE.volumetric_start = 0.5
EE.volumetric_end = 40.0
EE.use_volumetric_shadows = True
EE.clamp_surface_indirect = 10.0
SC.render.use_motion_blur = True
SC.render.motion_blur_shutter = 0.5
EE.motion_blur_steps = 1
SC.view_settings.view_transform = 'AgX'
SC.view_settings.look = 'AgX - Punchy'
SC.view_settings.exposure = 0.0
SC.render.film_transparent = False
SC.render.image_settings.file_format = 'PNG'
SC.render.image_settings.color_depth = '8'


# =====================================================================================================
# CAR BODY (lofted sections, nose +X, ground z=0)
# =====================================================================================================
XN, XT = 2.36, -2.18
LNP, PN = 0.52, 2.4      # nose plan rounding length / exponent
LNS_T, QN_T = 0.17, 1.3  # nose side rounding above the tip (crisp leading edge)
LNS_B, QN_B = 0.44, 2.0  # raked front fascia below the tip
LTP, PT = 0.15, 4.0      # tail plan rounding (squared-off Kamm tail)
LTS_T, QT_T = 0.07, 3.5  # tail deck edge (crisp)
LTS_B, QT_B = 0.10, 3.0
ZTIP_N, ZTIP_T = 0.33, 0.62
DIPW = 0.46
NB, NT = 6.0, 5.0
FRONT_AX, REAR_AX = 1.43, -1.395    # 2,825 mm wheelbase (facts s3)

fW = Spline([(-2.18, 0.935), (-1.95, 1.005), (-1.40, 1.055), (-0.90, 1.01), (-0.25, 0.955), (0.35, 0.96),
             (0.95, 0.995), (1.43, 1.015), (1.90, 0.99), (2.36, 0.90)])
fZB = Spline([(-2.18, 0.31), (-1.95, 0.21), (-1.65, 0.135), (-1.2, 0.115), (0.0, 0.11), (1.5, 0.11),
              (1.95, 0.115), (2.36, 0.12)])
fZS = Spline([(-2.18, 0.64), (-1.75, 0.63), (-1.40, 0.60), (-0.7, 0.53), (0.2, 0.49), (0.9, 0.48),
              (1.43, 0.46), (1.95, 0.39), (2.36, 0.33)])
fZF = Spline([(-2.18, 0.90), (-1.95, 0.94), (-1.40, 0.975), (-0.9, 0.935), (-0.3, 0.855), (0.3, 0.80),
              (0.9, 0.78), (1.43, 0.765), (1.90, 0.61), (2.36, 0.40)])
fZC = Spline([(-2.18, 0.885), (-1.95, 0.91), (-1.40, 0.92), (-0.9, 0.89), (-0.3, 0.815), (0.3, 0.755),
              (0.9, 0.69), (1.43, 0.625), (1.90, 0.53), (2.36, 0.38)])

def _sfac(x, L, q, nose):
    if nose:
        if x <= XN - L: return 1.0
        u = clamp((x - (XN - L)) / L)
    else:
        if x >= XT + L: return 1.0
        u = clamp(((XT + L) - x) / L)
    return (1 - u ** q) ** (1 / q)

def end_fac(x):
    ep = 1.0
    if x > XN - LNP:
        u = clamp((x - (XN - LNP)) / LNP); ep = (1 - u ** PN) ** (1 / PN)
    if x < XT + LTP:
        u = clamp(((XT + LTP) - x) / LTP); ep = (1 - u ** PT) ** (1 / PT)
    if x > 0:
        return ep, _sfac(x, LNS_T, QN_T, True), _sfac(x, LNS_B, QN_B, True)
    return ep, _sfac(x, LTS_T, QT_T, False), _sfac(x, LTS_B, QT_B, False)

def cove(x):
    return 0.085 * smoothstep(-0.88, -0.45, x) * smoothstep(0.95, 0.50, x)

def sec_params(x):
    ep, et, eb = end_fac(x)
    zt = ZTIP_N if x > 0 else ZTIP_T
    f = lambda z: zt + (z - zt) * (et if z > zt else eb)
    return (fW(x) * ep, f(fZB(x)), f(fZS(x)), f(fZF(x)), f(fZC(x)), cove(x))

def sec_point(P, phi):
    W, zb, zs, zf, zc, cv = P
    if phi <= 0:
        c = max(0.0, cos(phi)); s = max(0.0, -sin(phi))
        z = zs - (zs - zb) * s ** (2 / NB)
        hz = clamp((zs - z) / max(1e-6, zs - zb))
        return W * c ** (2 / NB) * (1 - cv * sin(pi * hz ** 0.8) ** 2), z
    c = max(0.0, cos(phi)); s = max(0.0, sin(phi))
    y = W * c ** (2 / NT)
    zenv = zs + (zf - zs) * s ** (2 / NT)
    t = (y / W) if W > 1e-9 else 0.0
    return y, zenv - (zf - zc) * exp(-(t / DIPW) ** 4)

def body_top_z(x, y):
    P = sec_params(x); W, zc = P[0], P[4]
    if W < 1e-6: return zc
    c = clamp(abs(y) / W) ** (NT / 2)
    phi = acos(min(1.0, c))
    return sec_point(P, phi)[1]

SEGS = [(-pi / 2, radians(-30), 16), (radians(-30), 0.0, 10), (0.0, radians(42), 12), (radians(42), pi / 2, 18)]
MTOT = sum(s[2] for s in SEGS)

def resample(fn, t0, t1, count, dense=160, kw=0.05):
    pts = [fn(t0 + (t1 - t0) * i / dense) for i in range(dense + 1)]
    w = [0.0]
    for i in range(1, len(pts)):
        dy = pts[i][0] - pts[i - 1][0]; dz = pts[i][1] - pts[i - 1][1]
        ds = sqrt(dy * dy + dz * dz)
        turn = 0.0
        if 1 < i:
            ay = pts[i - 1][0] - pts[i - 2][0]; az = pts[i - 1][1] - pts[i - 2][1]
            la = sqrt(ay * ay + az * az)
            if la > 1e-9 and ds > 1e-9:
                cr = (ay * dz - az * dy) / (la * ds); dt = (ay * dy + az * dz) / (la * ds)
                turn = abs(atan2(cr, dt))
        w.append(w[-1] + ds + kw * turn)
    tot = w[-1]
    if tot < 1e-9: return [pts[0]] * count
    out = []; j = 0
    for k in range(count):
        target = tot * k / count
        while j < len(w) - 2 and w[j + 1] < target: j += 1
        seg = w[j + 1] - w[j]
        t = 0.0 if seg < 1e-12 else (target - w[j]) / seg
        out.append((lerp(pts[j][0], pts[j + 1][0], t), lerp(pts[j][1], pts[j + 1][1], t)))
    return out

def half_section(x):
    P = sec_params(x)
    half = []
    for (a, b, cnt) in SEGS:
        half += resample(lambda ph: sec_point(P, ph), a, b, cnt)
    half.append(sec_point(P, pi / 2))
    half[0] = (0.0, half[0][1]); half[-1] = (0.0, half[-1][1])
    return half

def end_dense(a, b, n, at_b=True):
    """n samples in [a, b) clustered towards b (if at_b) using a sine map."""
    out = []
    for i in range(n):
        th = (pi / 2) * i / n
        u = sin(th)
        out.append(a + (b - a) * u if at_b else b - (b - a) * u)
    return out

def stations(xt, xn, lt, ln, nt_, nn, step):
    xs = sorted(end_dense(xt + lt, xt, nt_, True))           # tail zone, dense at the tail tip
    mid0, mid1 = xt + lt, xn - ln
    m = max(2, int((mid1 - mid0) / step))
    xs += [mid0 + (mid1 - mid0) * i / m for i in range(m)]
    xs += end_dense(xn - ln, xn, nn, True)
    xs = sorted(set([round(v, 6) for v in xs] + [xt, xn]))
    return xs

def loft(xs, sect_fn, name, mat_fn=None):
    """xs: station positions (first/last are poles). sect_fn(x) -> half section list (y,z) bottom->top."""
    bm = bmesh.new()
    rings = []
    halves = [sect_fn(x) for x in xs]
    M = len(halves[0]) - 1
    for i, x in enumerate(xs):
        if i == 0 or i == len(xs) - 1:
            h = halves[i]
            z = sum(p[1] for p in h) / len(h)
            rings.append(bm.verts.new((x, 0.0, z)))
            continue
        h = halves[i]
        ring = [(x, y, z) for (y, z) in h] + [(x, -y, z) for (y, z) in reversed(h[1:-1])]
        rings.append([bm.verts.new(p) for p in ring])
    R = 2 * M
    faces_meta = []
    for i in range(len(xs) - 1):
        A0, B0 = rings[i], rings[i + 1]
        for k in range(R):
            k2 = (k + 1) % R
            row = k if k <= M else 2 * M - k
            if i == 0:
                f = bm.faces.new((A0, B0[k], B0[k2]))
            elif i == len(xs) - 2:
                f = bm.faces.new((A0[k], B0, A0[k2]))
            else:
                f = bm.faces.new((A0[k], B0[k], B0[k2], A0[k2]))
            if mat_fn: f.material_index = mat_fn(i, row, xs[i], k)
    recalc(bm)
    return bm

def body_mat_index(i, row, x, k):
    if row < SEGS[0][2] - 3: return 1                      # carbon lower band below the sill line
    if x > 2.14 and row < SEGS[0][2] + SEGS[1][2] - 1: return 3   # front intake (raked fascia)
    if x < XT + 0.085 and row < SEGS[0][2] + SEGS[1][2] + 2: return 3  # black rear mesh fascia
    return 0

def section_crossings(x, h, side=1):
    """outermost y of the body at height h for station x (None if no crossing)."""
    half = half_section(x)
    best = None
    for (y0, z0), (y1, z1) in zip(half, half[1:]):
        if (z0 - h) * (z1 - h) <= 0 and abs(z1 - z0) > 1e-9:
            t = (h - z0) / (z1 - z0); y = lerp(y0, y1, t)
            best = y if best is None else max(best, y)
    return best


# =====================================================================================================
# MATERIALS
# =====================================================================================================
CAR_PAINT = (0.62, 0.006, 0.016)   # candy red

def scanmask_group(body_ob):
    g = bpy.data.node_groups.new('SCANMASK', 'ShaderNodeTree')
    g.interface.new_socket('Mask', in_out='OUTPUT', socket_type='NodeSocketFloat')
    g.interface.new_socket('Band', in_out='OUTPUT', socket_type='NodeSocketFloat')
    nt = g
    gout = nt.nodes.new('NodeGroupOutput')
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.object = body_ob
    sx = nt.nodes.new('ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
    thr = nt.nodes.new('ShaderNodeValue'); thr.name = 'thr'; thr.outputs[0].default_value = 3.0
    lo = math_node(nt, 'SUBTRACT', thr.outputs[0], 0.06)
    hi = math_node(nt, 'ADD', thr.outputs[0], 0.06)
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.interpolation_type = 'SMOOTHSTEP'
    lk(nt, sx.outputs[0], mr.inputs['Value']); lk(nt, lo, mr.inputs['From Min']); lk(nt, hi, mr.inputs['From Max'])
    lk(nt, mr.outputs[0], gout.inputs['Mask'])
    d = math_node(nt, 'ABSOLUTE', math_node(nt, 'SUBTRACT', sx.outputs[0], thr.outputs[0]))
    band = nt.nodes.new('ShaderNodeMapRange'); band.interpolation_type = 'SMOOTHSTEP'
    band.inputs['From Min'].default_value = 0.0; band.inputs['From Max'].default_value = 0.035
    band.inputs['To Min'].default_value = 1.0; band.inputs['To Max'].default_value = 0.0
    lk(nt, d, band.inputs['Value'])
    lk(nt, band.outputs[0], gout.inputs['Band'])
    return g

def xray_group(scan_g):
    g = bpy.data.node_groups.new('XRAY', 'ShaderNodeTree')
    g.interface.new_socket('Surface', in_out='INPUT', socket_type='NodeSocketShader')
    g.interface.new_socket('Shader', in_out='OUTPUT', socket_type='NodeSocketShader')
    nt = g
    gin = nt.nodes.new('NodeGroupInput'); gout = nt.nodes.new('NodeGroupOutput')
    sm = nt.nodes.new('ShaderNodeGroup'); sm.node_tree = scan_g
    lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.35
    fres = math_node(nt, 'POWER', lw.outputs['Facing'], 2.2)
    stren = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', fres, 2.4), 0.05)
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.05, 0.75, 0.9, 1)
    lk(nt, stren, em.inputs['Strength'])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    holo = nt.nodes.new('ShaderNodeAddShader'); lk(nt, tr.outputs[0], holo.inputs[0]); lk(nt, em.outputs[0], holo.inputs[1])
    mix = nt.nodes.new('ShaderNodeMixShader')
    lk(nt, sm.outputs['Mask'], mix.inputs[0]); lk(nt, gin.outputs['Surface'], mix.inputs[1]); lk(nt, holo.outputs[0], mix.inputs[2])
    sem = nt.nodes.new('ShaderNodeEmission'); sem.inputs['Color'].default_value = (0.25, 1.0, 0.92, 1)
    lk(nt, math_node(nt, 'MULTIPLY', sm.outputs['Band'], 18.0), sem.inputs['Strength'])
    add = nt.nodes.new('ShaderNodeAddShader'); lk(nt, mix.outputs[0], add.inputs[0]); lk(nt, sem.outputs[0], add.inputs[1])
    lk(nt, add.outputs[0], gout.inputs['Shader'])
    return g

def wrap_xray(mat, nt, out, shader_socket, xg):
    gn = nt.nodes.new('ShaderNodeGroup'); gn.node_tree = xg
    lk(nt, shader_socket, gn.inputs['Surface'])
    lk(nt, gn.outputs['Shader'], out.inputs['Surface'])
    mat.use_transparent_shadow = True

def mat_paint(xg):
    m, nt, out = new_mat('paint')
    p = principled(nt, **{'Base Color': (0.80, 0.81, 0.83, 1), 'Metallic': 0.25, 'Roughness': 0.28,
                          'Coat Weight': 1.0, 'Coat Roughness': 0.02, 'Coat IOR': 1.52,
                          'Thin Film Thickness': 320.0, 'Thin Film IOR': 1.35})
    tc = node(nt, 'ShaderNodeTexCoord')
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 900.0, 'Detail': 1.0})
    lk(nt, tc.outputs['Object'], nz.inputs['Vector'])
    bump = node(nt, 'ShaderNodeBump', {'Strength': 0.05, 'Distance': 0.001})
    lk(nt, nz.outputs['Fac'], bump.inputs['Height'])
    lk(nt, bump.outputs['Normal'], p.inputs['Normal'])
    wrap_xray(m, nt, out, p.outputs[0], xg)
    return m

def mat_simple(name, color, rough, metal=0.0, coat=0.0, xg=None, emission=None, estr=0.0, spec=0.5):
    m, nt, out = new_mat(name)
    kw = {'Base Color': rgba(color), 'Roughness': rough, 'Metallic': metal, 'Coat Weight': coat,
          'Coat Roughness': 0.04, 'Specular IOR Level': spec}
    if emission is not None:
        kw['Emission Color'] = rgba(emission); kw['Emission Strength'] = estr
    p = principled(nt, **kw)
    if xg: wrap_xray(m, nt, out, p.outputs[0], xg)
    else: lk(nt, p.outputs[0], out.inputs['Surface'])
    return m

def mat_emit(name, color, strength):
    m, nt, out = new_mat(name)
    e = node(nt, 'ShaderNodeEmission', {'Color': rgba(color), 'Strength': strength})
    lk(nt, e.outputs[0], out.inputs['Surface'])
    return m

def mat_glass(xg):
    m, nt, out = new_mat('glass')
    p = principled(nt, **{'Base Color': (0.004, 0.005, 0.008, 1), 'Roughness': 0.015, 'Specular IOR Level': 0.75,
                          'Coat Weight': 0.0})
    wrap_xray(m, nt, out, p.outputs[0], xg)
    return m

def mat_glass_clear(xg):
    m, nt, out = new_mat('glass')
    tr = node(nt, 'ShaderNodeBsdfTransparent', {'Color': (0.52, 0.56, 0.60, 1)})
    p = principled(nt, **{'Base Color': (0.0, 0.0, 0.0, 1), 'Roughness': 0.02, 'Specular IOR Level': 0.65})
    ad = node(nt, 'ShaderNodeAddShader'); lk(nt, tr.outputs[0], ad.inputs[0]); lk(nt, p.outputs[0], ad.inputs[1])
    wrap_xray(m, nt, out, ad.outputs[0], xg)
    m.use_transparent_shadow = True
    return m

def mat_grille(xg):
    m, nt, out = new_mat('grille')
    p = principled(nt, **{'Base Color': (0.004, 0.004, 0.005, 1), 'Roughness': 0.3, 'Metallic': 0.0,
                          'Specular IOR Level': 0.18})
    tc = node(nt, 'ShaderNodeTexCoord')
    wv = node(nt, 'ShaderNodeTexWave', {'Scale': 14.0, 'Distortion': 0.0}, wave_type='BANDS', bands_direction='Z')
    lk(nt, tc.outputs['Object'], wv.inputs['Vector'])
    rr = node(nt, 'ShaderNodeMapRange', {'From Min': 0.35, 'From Max': 0.65, 'To Min': 0.35, 'To Max': 0.9})
    lk(nt, wv.outputs['Fac'], rr.inputs['Value']); lk(nt, rr.outputs[0], p.inputs['Roughness'])
    wrap_xray(m, nt, out, p.outputs[0], xg)
    return m


# =====================================================================================================
# BUILD CAR
# =====================================================================================================
ROOT = empty('car_root')
ROLL = empty('car_roll', (0, 0, 0.55), ROOT)
SUSP = empty('car_susp', (0, 0, 0.55), ROLL)

# body first (texture coordinate reference for every x-ray material)
xs_body = stations(XT, XN, LTP, LNP, 22, 34, 0.032)
bm = loft(xs_body, half_section, 'body', body_mat_index)
BODY = mesh_obj('body', bm, smooth=True)
SCAN_G = scanmask_group(BODY)
XRAY_G = xray_group(SCAN_G)

M_PAINT = mat_paint(XRAY_G)
M_CARBON = mat_simple('carbon', (0.012, 0.012, 0.014), 0.22, metal=0.2, coat=1.0, xg=XRAY_G)
M_WELL = mat_simple('well', (0.006, 0.006, 0.007), 0.7, xg=XRAY_G)
M_GLASS = mat_glass_clear(XRAY_G)
M_GRILLE = mat_grille(XRAY_G)
M_FASCIA = mat_simple('fascia', (0.005, 0.005, 0.006), 0.55, xg=XRAY_G, spec=0.25)
M_VENT = mat_simple('vent', (0.003, 0.003, 0.004), 0.18, coat=0.0, xg=XRAY_G, spec=0.6)
M_CHROME_DK = mat_simple('chrome_dark', (0.30, 0.31, 0.33), 0.12, metal=1.0, xg=XRAY_G)
M_INTERIOR = mat_simple('interior', (0.018, 0.018, 0.020), 0.8, xg=XRAY_G, spec=0.25)
M_LEATHER = mat_simple('leather', (0.03, 0.026, 0.026), 0.55, xg=XRAY_G, spec=0.35)
M_ACCENT = mat_simple('seat_accent', (0.55, 0.03, 0.02), 0.45, xg=XRAY_G)
M_TRIM = mat_simple('interior_trim', (0.012, 0.012, 0.014), 0.6, xg=XRAY_G, spec=0.3)
M_AMBIENT = mat_emit('ambient_strip', (0.25, 0.8, 1.0), 3.0)
M_LIGHT_F = mat_emit('light_front', (0.85, 0.93, 1.0), 15.0)
M_LIGHT_R = mat_emit('light_rear', (1.0, 0.02, 0.03), 16.0)
for mm in (M_PAINT, M_CARBON, M_WELL, M_GRILLE, M_FASCIA):
    BODY.data.materials.append(mm)

sub = BODY.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; sub.render_levels = 1

WHEELS = [(FRONT_AX, 0.862, 0.37, 1.0), (FRONT_AX, -0.862, 0.37, 1.0), (REAR_AX, 0.885, 0.37, 1.10), (REAR_AX, -0.885, 0.37, 1.10)]

# canopy footprint (glass greenhouse, roadster-like: wide, low, raked)
CXF, CXR = 0.98, -1.32
WCMAX = 0.745
fZR = Spline([(0.98, 0.69), (0.80, 0.80), (0.55, 0.925), (0.25, 1.005), (-0.1, 1.05), (-0.4, 1.055), (-0.7, 1.03),
              (-1.0, 0.985), (-1.32, 0.93)])

def canopy_w(x):
    u = clamp((CXF - x) / (CXF - CXR))
    front = sin(pi / 2 * min(1.0, u / 0.17)) ** 0.7
    rear = 1.0 if u < 0.52 else max(0.0, 1 - ((u - 0.52) / 0.48) ** 2.2) ** 0.55
    return WCMAX * front * rear * (1.0 - 0.05 * (2 * u - 0.7) ** 2)

def resample_poly(pts, n):
    P = [Vector((p[0], p[1])) for p in pts]
    L = [0.0]
    for i in range(1, len(P)): L.append(L[-1] + (P[i] - P[i - 1]).length)
    out = []; j = 0
    for k in range(n + 1):
        t = L[-1] * k / n
        while j < len(P) - 2 and L[j + 1] < t: j += 1
        seg = L[j + 1] - L[j]
        a = 0.0 if seg < 1e-12 else (t - L[j]) / seg
        q = P[j].lerp(P[j + 1], a); out.append((q.x, q.y))
    out[0] = (0.0, out[0][1]); out[-1] = (0.0, out[-1][1])
    return out

def cockpit_half(x):
    cw = max(0.002, canopy_w(x) - 0.065)
    zf_, zt_ = 0.17, 1.6
    r = min(0.08, cw * 0.5)
    pts = [(0.0, zf_), (max(0.0, cw - r), zf_)]
    for k in range(1, 7):
        a = -pi / 2 + (pi / 2) * k / 6
        pts.append((cw - r + r * cos(a), zf_ + r + r * sin(a)))
    pts += [(cw, zt_), (0.0, zt_)]
    return resample_poly(pts, 40)

cutters = []
def add_cutter(cbm, mat):
    cob = mesh_obj('cutter', cbm, mats=[mat], smooth=True); cob.hide_render = True
    cutters.append(cob)
    bo = BODY.modifiers.new('cut', 'BOOLEAN'); bo.object = cob; bo.operation = 'DIFFERENCE'; bo.solver = 'EXACT'
    bo.material_mode = 'TRANSFER'
for (wx, wy, wz, ws) in WHEELS:
    r = 0.425 if wx > 0 else 0.432
    y0, y1 = (0.56, 1.30) if wy > 0 else (-1.30, -0.56)
    cbm = bmesh.new()
    bmesh.ops.create_cone(cbm, cap_ends=True, segments=96, radius1=r, radius2=r, depth=(y1 - y0))
    bmesh.ops.rotate(cbm, verts=cbm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
    bmesh.ops.translate(cbm, verts=cbm.verts, vec=(wx, (y0 + y1) / 2, wz + 0.018))
    add_cutter(cbm, M_WELL)
xs_ck = [x for x in stations(CXR + 0.16, CXF - 0.10, 0.25, 0.25, 10, 10, 0.05)]
add_cutter(loft(xs_ck, cockpit_half, 'cockpit'), M_INTERIOR)
apply_mods(BODY)
for c in cutters: bpy.data.objects.remove(c)
bm = bmesh.new(); bm.from_mesh(BODY.data)
dark_idx = [i for i, m in enumerate(BODY.data.materials) if m and (m.name.startswith('well') or m.name.startswith('interior'))]
for e in bm.edges:
    if len(e.link_faces) == 2:
        a, b = e.link_faces
        if (a.material_index in dark_idx) != (b.material_index in dark_idx):
            e.smooth = False
bm.to_mesh(BODY.data); bm.free()
set_parent(BODY, SUSP)

# ---------------- open glass canopy ----------------
def canopy_half_open(x):
    wc = canopy_w(x)
    zbase = body_top_z(x, wc) - 0.012
    zr = max(fZR(x), zbase + 0.002)
    nc = 3.0
    def up(ph):
        c = max(0.0, cos(ph)); s_ = max(0.0, sin(ph))
        return (wc * c ** (2 / nc), zbase + (zr - zbase) * s_ ** (2 / nc))
    return [(wc, zbase - 0.03)] + resample(up, 0.0, pi / 2, 28) + [(0.0, zr)]

def loft_open(xs, sect_fn):
    bm = bmesh.new(); rings = []
    for i, x in enumerate(xs):
        h = sect_fn(x)
        if i == 0 or i == len(xs) - 1:
            rings.append(bm.verts.new((x, 0.0, h[-1][1]))); continue
        ring = [(x, y, z) for (y, z) in h] + [(x, -y, z) for (y, z) in reversed(h[:-1])]
        rings.append([bm.verts.new(p) for p in ring])
    n = len(rings[1])
    for i in range(len(xs) - 1):
        A0, B0 = rings[i], rings[i + 1]
        for k in range(n - 1):
            if i == 0: bm.faces.new((A0, B0[k], B0[k + 1]))
            elif i == len(xs) - 2: bm.faces.new((A0[k], B0, A0[k + 1]))
            else: bm.faces.new((A0[k], B0[k], B0[k + 1], A0[k + 1]))
    bm.normal_update()
    for f in bm.faces:
        c = f.calc_center_median()
        if f.normal.dot(c - Vector((c.x, 0.0, 0.55))) < 0: f.normal_flip()
    bm.normal_update()
    return bm

xs_can = stations(CXR, CXF, 0.30, 0.22, 18, 22, 0.03)
CANOPY = mesh_obj('canopy', loft_open(xs_can, canopy_half_open), mats=[M_GLASS], smooth=True)
s2 = CANOPY.modifiers.new('sub', 'SUBSURF'); s2.levels = 1; s2.render_levels = 1
set_parent(CANOPY, SUSP)

# ---------------- interior: one seat (LHD), yoke (steer-by-wire), dash, console ----------------
def rbox(name, size, loc, rot=(0, 0, 0), mat=None, bevel=0.02, segs=3):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    ob = mesh_obj(name, bm, mats=[mat], smooth=False)
    ob.location = loc; ob.rotation_euler = rot
    if bevel: add_bevel(ob, bevel, segs, 30)
    set_parent(ob, SUSP)
    return ob

SEAT_Y = 0.36
rbox('seat_cushion', (0.50, 0.44, 0.10), (-0.30, SEAT_Y, 0.25), (0, radians(-7), 0), M_LEATHER, 0.035, 4)
rbox('seat_back', (0.11, 0.46, 0.70), (-0.62, SEAT_Y, 0.58), (0, radians(-21), 0), M_LEATHER, 0.04, 4)
rbox('seat_bolster_l', (0.46, 0.06, 0.15), (-0.32, SEAT_Y + 0.235, 0.31), (0, radians(-7), 0), M_ACCENT, 0.025, 3)
rbox('seat_bolster_r', (0.46, 0.06, 0.15), (-0.32, SEAT_Y - 0.235, 0.31), (0, radians(-7), 0), M_ACCENT, 0.025, 3)
rbox('dash', (0.22, 1.30, 0.12), (0.66, 0.0, 0.58), (0, radians(12), 0), M_TRIM, 0.03, 3)
rbox('console', (0.95, 0.15, 0.16), (-0.12, 0.0, 0.26), (0, 0, 0), M_CARBON, 0.02, 3)
_yk = lathe([(0.165 + 0.017 * cos(2 * pi * i / 12), 0.017 * sin(2 * pi * i / 12)) for i in range(12)], 40, closed=True,
            a0=radians(125), a1=radians(415))
bmesh.ops.rotate(_yk, verts=_yk.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-pi / 2, 3, 'Z'))
for v in _yk.verts: v.co.z *= 0.78
bmesh.ops.holes_fill(_yk, edges=[e for e in _yk.edges if e.is_boundary], sides=0)
recalc(_yk)
YOKE = mesh_obj('yoke', _yk, mats=[M_LEATHER]); YOKE.location = (0.30, SEAT_Y, 0.63); YOKE.rotation_euler = (0, radians(-22), 0)
set_parent(YOKE, SUSP)
rbox('yoke_hub', (0.035, 0.11, 0.07), (0.31, SEAT_Y, 0.63), (0, radians(-22), 0), M_TRIM, 0.01, 2)
curve_stub = None

# canopy seal (dark chrome bead along the base)
def curve_obj(name, pts, radius, mat, parent=None, cyclic=False, res=6):
    cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'
    cu.bevel_depth = radius; cu.bevel_resolution = res; cu.use_fill_caps = True
    sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts): p.co = (q[0], q[1], q[2], 1.0)
    sp.use_cyclic_u = cyclic
    cu.materials.append(mat)
    ob = link(bpy.data.objects.new(name, cu))
    if parent: set_parent(ob, parent)
    return ob

seal = []
for x in [CXF - (CXF - CXR) * i / 160 for i in range(161)]:
    wc = canopy_w(x)
    seal.append((x, wc, body_top_z(x, wc) - 0.004))
seal = seal + [(p[0], -p[1], p[2]) for p in reversed(seal[1:-1])]
curve_obj('canopy_seal', seal, 0.0065, M_CHROME_DK, SUSP, cyclic=True)
curve_obj('steering_column', [(0.33, SEAT_Y, 0.62), (0.58, SEAT_Y, 0.58)], 0.022, M_TRIM, SUSP)
curve_obj('ambient_strip', [(0.57, -0.60, 0.645), (0.57, 0.60, 0.645)], 0.0045, M_AMBIENT, SUSP)

# ---------------- light bars ----------------
def outline_at_height(h, x0, x1, n=120, grow=0.0):
    pts = []
    xs = [x0 + (x1 - x0) * (1 - cos(pi / 2 * i / n)) for i in range(n + 1)]  # dense toward x1
    for x in xs:
        y = section_crossings(x, h)
        if y is None or y < 0.004: break
        pts.append((x, y + grow))
    return pts

def bar_curve(name, h, x0, x1, radius, mat, inset=0.004):
    o = outline_at_height(h, x0, x1)
    tip = (o[-1][0] + 0.004, 0.0)
    path = o + [tip] + [(x, -y) for (x, y) in reversed(o)]
    pts = []
    for i, (x, y) in enumerate(path):
        a = path[max(0, i - 1)]; b = path[min(len(path) - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = sqrt(tx * tx + ty * ty) or 1.0
        nx, ny = -ty / ln, tx / ln
        if nx * x + ny * y < 0: nx, ny = -nx, -ny
        pts.append((x - nx * inset, y - ny * inset, h))
    return curve_obj(name, pts, radius, mat, SUSP)

bar_curve('lightbar_front_housing', 0.345, 1.86, XN, 0.016, M_FASCIA, inset=0.008)
bar_curve('lightbar_front', 0.345, 1.88, XN, 0.0085, M_LIGHT_F, inset=-0.004)
bar_curve('lightbar_rear_housing', 0.715, -1.94, XT, 0.017, M_FASCIA, inset=0.008)
bar_curve('lightbar_rear', 0.715, -1.96, XT, 0.0095, M_LIGHT_R, inset=-0.004)

# ---------------- surface patches (vents, intakes) ----------------
def surface_point_side(x, z):
    y = section_crossings(x, z)
    return None if y is None else Vector((x, y, z))

def patch_side(name, x0, x1, zlo, zhi, mat, nx=40, nz=10, off=0.003):
    bm = bmesh.new(); grid = []
    for i in range(nx + 1):
        x = lerp(x0, x1, i / nx); row = []
        for j in range(nz + 1):
            z = lerp(zlo(x), zhi(x), j / nz)
            p = surface_point_side(x, z)
            row.append(p)
        grid.append(row)
    vs = [[None] * (nz + 1) for _ in range(nx + 1)]
    for i in range(nx + 1):
        for j in range(nz + 1):
            p = grid[i][j]
            # offset outward in +y (side patch)
            vs[i][j] = bm.verts.new((p.x, p.y + off, p.z))
    for i in range(nx):
        for j in range(nz):
            bm.faces.new((vs[i][j], vs[i + 1][j], vs[i + 1][j + 1], vs[i][j + 1]))
    recalc(bm)
    ob = mesh_obj(name, bm, mats=[mat])
    # mirror copy
    ob2 = link(bpy.data.objects.new(name + '_R', ob.data)); ob2.scale.y = -1
    set_parent(ob, SUSP); set_parent(ob2, SUSP)
    return ob

def patch_top(name, x0, x1, ylo, yhi, mat, nx=24, ny=12, off=0.0025, mirror=True):
    bm = bmesh.new(); vs = []
    for i in range(nx + 1):
        x = lerp(x0, x1, i / nx); row = []
        for j in range(ny + 1):
            y = lerp(ylo(x), yhi(x), j / ny)
            row.append(bm.verts.new((x, y, body_top_z(x, y) + off)))
        vs.append(row)
    for i in range(nx):
        for j in range(ny):
            bm.faces.new((vs[i][j], vs[i][j + 1], vs[i + 1][j + 1], vs[i + 1][j]))
    recalc(bm)
    ob = mesh_obj(name, bm, mats=[mat]); set_parent(ob, SUSP)
    if mirror:
        ob2 = link(bpy.data.objects.new(name + '_R', ob.data)); ob2.scale.y = -1; set_parent(ob2, SUSP)
    return ob

# side scoop ahead of the rear wheel (swept shape)
patch_side('side_scoop', -0.92, -0.18,
           lambda x: 0.30 + 0.10 * smoothstep(-0.18, -0.92, x),
           lambda x: 0.44 + 0.07 * smoothstep(-0.18, -0.92, x) - 0.10 * smoothstep(-0.55, -0.18, x) ** 1.5,
           M_GRILLE)
# hood vents
# rear deck louvres
pass  # deck louvre removed (fans exhaust at the rear and flanks)

# ---------------- door shut line ----------------
def door_line():
    loop = []
    for t in [i / 30 for i in range(31)]:                      # front edge, bottom -> top
        loop.append((lerp(0.86, 0.80, t), lerp(0.24, 0.70, t)))
    for t in [i / 40 for i in range(1, 41)]:                   # top edge under the canopy seal
        loop.append((lerp(0.80, -0.42, t), lerp(0.70, 0.735, t)))
    for t in [i / 30 for i in range(1, 31)]:                   # rear edge, curving forward at the bottom
        loop.append((-0.42 - 0.10 * sin(pi * t) * 0.6 + 0.12 * t, lerp(0.735, 0.24, t)))
    for t in [i / 30 for i in range(1, 30)]:                   # bottom edge
        loop.append((lerp(-0.30, 0.86, t), 0.24))
    pts = []
    for (x, z) in loop:
        y = section_crossings(x, z)
        if y is not None: pts.append((x, y - 0.0012, z))
    for side in (1, -1):
        curve_obj('door_line', [(p[0], side * p[1], p[2]) for p in pts], 0.0024, M_WELL, SUSP, cyclic=True, res=3)
door_line()

# ---------------- splitter, skirts, diffuser ----------------
def extrude_outline(name, pts2d, z0, z1, mat, bevel=0.006, parent=SUSP):
    bm = bmesh.new()
    bot = [bm.verts.new((x, y, z0)) for (x, y) in pts2d]
    top = [bm.verts.new((x, y, z1)) for (x, y) in pts2d]
    bm.faces.new(bot[::-1]); bm.faces.new(top)
    n = len(pts2d)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((bot[i], bot[j], top[j], top[i]))
    recalc(bm)
    ob = mesh_obj(name, bm, mats=[mat], smooth=False)
    if bevel: add_bevel(ob, bevel, 3, 30)
    if parent: set_parent(ob, parent)
    return ob

o = outline_at_height(0.15, 1.45, XN, n=80)
sp_r = [(x + 0.015, y + 0.018) for (x, y) in o]
tipx = sp_r[-1][0] + 0.02
splitter = sp_r + [(tipx, 0.0)] + [(x, -y) for (x, y) in reversed(sp_r)]
extrude_outline('splitter', splitter, 0.085, 0.108, M_CARBON)

for side in (1, -1):
    pts = []
    for i in range(40):
        x = lerp(-0.86, 0.92, i / 39)
        y = section_crossings(x, 0.15)
        pts.append((x, side * (y + 0.035)))
    inner = [(x, side * (abs(y) - 0.20)) for (x, y) in reversed(pts)]
    poly = pts + inner if side > 0 else list(reversed(pts + inner))
    extrude_outline('skirt', poly, 0.10, 0.12, M_CARBON, bevel=0.005)

for yf in (-0.62, -0.31, 0.0, 0.31, 0.62):
    prof = []
    for i in range(16):
        x = lerp(-1.62, XT + 0.03, i / 15)
        prof.append((x, sec_params(x)[1] + 0.02))
    bot = [(x, max(0.115, z - 0.02 - 0.09 * smoothstep(-1.62, XT, x))) for (x, z) in reversed(prof)]
    poly = [(x, z) for (x, z) in prof] + bot
    bm = bmesh.new()
    a = [bm.verts.new((x, yf - 0.007, z)) for (x, z) in poly]
    b = [bm.verts.new((x, yf + 0.007, z)) for (x, z) in poly]
    bm.faces.new(a[::-1]); bm.faces.new(b)
    for i in range(len(poly)):
        j = (i + 1) % len(poly); bm.faces.new((a[i], a[j], b[j], b[i]))
    recalc(bm)
    fin = mesh_obj('diffuser_fin', bm, mats=[M_CARBON], smooth=False); add_bevel(fin, 0.003, 2, 30)
    set_parent(fin, SUSP)

# =====================================================================================================
# WHEELS
# =====================================================================================================
M_TIRE = mat_simple('tire', (0.009, 0.009, 0.010), 0.86, spec=0.18)
M_RIM = mat_simple('rim', (0.33, 0.34, 0.36), 0.18, metal=1.0)
M_LIP = mat_simple('rim_lip', (0.85, 0.86, 0.88), 0.06, metal=1.0)
M_DISC = mat_simple('disc', (0.42, 0.42, 0.43), 0.32, metal=1.0)
M_HAT = mat_simple('disc_hat', (0.08, 0.08, 0.09), 0.4, metal=0.8)
M_CALIPER = mat_simple('caliper', (1.0, 0.70, 0.02), 0.28, coat=1.0)
M_HOLE = mat_simple('hole', (0.004, 0.004, 0.004), 0.9)

def build_wheel_parts():
    parts = []
    tire = [(0.285, 0.128), (0.298, 0.146), (0.318, 0.156), (0.340, 0.158), (0.357, 0.152), (0.366, 0.138),
            (0.370, 0.115), (0.371, 0.062), (0.365, 0.056), (0.365, 0.036), (0.371, 0.030), (0.371, -0.030),
            (0.365, -0.036), (0.365, -0.056), (0.371, -0.062), (0.370, -0.115), (0.366, -0.138), (0.356, -0.152),
            (0.340, -0.158), (0.318, -0.156), (0.298, -0.146), (0.285, -0.128), (0.281, -0.10), (0.281, 0.10)]
    parts.append(('tire', recalc(lathe(tire, 144, closed=True)), M_TIRE, None))
    rim = [(0.269, -0.128), (0.275, -0.134), (0.285, -0.128), (0.285, 0.116), (0.294, 0.124), (0.297, 0.132),
           (0.292, 0.139), (0.279, 0.138), (0.270, 0.130), (0.265, 0.112), (0.262, -0.12)]
    parts.append(('rim', recalc(lathe(rim, 144, closed=True)), M_LIP, None))
    # twin spokes
    bm = bmesh.new()
    NSP = 7
    for i in range(NSP):
        for tw in (-1, 1):
            vs = []
            for (r, dang, hw, yf) in ((0.078, 1.2, 0.0165, 0.100), (0.268, 4.1, 0.0140, 0.124)):
                th = 2 * pi * i / NSP + tw * radians(dang)
                ca, sa = cos(th), sin(th)
                tx, tz = -sa, ca
                for (s, yy, wmul) in ((-1, yf, 0.70), (1, yf, 0.70), (1, yf - 0.042, 1.0), (-1, yf - 0.042, 1.0)):
                    vs.append(bm.verts.new((r * ca + s * hw * wmul * tx, yy, r * sa + s * hw * wmul * tz)))
            a, b = vs[:4], vs[4:]
            bm.faces.new((a[0], a[1], a[2], a[3])[::-1]); bm.faces.new((b[0], b[1], b[2], b[3]))
            for k in range(4):
                k2 = (k + 1) % 4; bm.faces.new((a[k], a[k2], b[k2], b[k]))
    recalc(bm)
    parts.append(('spokes', bm, M_RIM, 0.0035))
    # hub + centre lock
    hub = [(0.03, 0.118), (0.085, 0.112), (0.092, 0.100), (0.092, 0.07), (0.03, 0.07)]
    parts.append(('hub', recalc(lathe(hub, 64, closed=True)), M_RIM, None))
    nut = bmesh.new()
    bmesh.ops.create_cone(nut, cap_ends=True, segments=6, radius1=0.03, radius2=0.03, depth=0.03)
    bmesh.ops.rotate(nut, verts=nut.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
    bmesh.ops.translate(nut, verts=nut.verts, vec=(0, 0.125, 0))
    parts.append(('nut', nut, M_LIP, 0.004))
    # disc + hat + holes
    disc = [(0.095, -0.052), (0.218, -0.052), (0.218, -0.022), (0.095, -0.022)]
    parts.append(('disc', recalc(lathe(disc, 96, closed=True)), M_DISC, None))
    hat = [(0.06, -0.06), (0.098, -0.06), (0.098, 0.068), (0.06, 0.068)]
    parts.append(('hat', recalc(lathe(hat, 64, closed=True)), M_HAT, None))
    holes = bmesh.new()
    for ring, (rr, n, off) in enumerate(((0.136, 20, 0.0), (0.162, 20, 0.5), (0.188, 20, 0.0))):
        for k in range(n):
            th = 2 * pi * (k + off) / n + ring * 0.12
            bmesh.ops.create_circle(holes, cap_ends=True, segments=10, radius=0.0062,
                                    matrix=Matrix.Translation((rr * cos(th), -0.0215, rr * sin(th))) @ Matrix.Rotation(-pi / 2, 4, 'X'))
    parts.append(('holes', holes, M_HOLE, None))
    # caliper (top-rear arc block)
    cal = [(0.160, -0.078), (0.240, -0.078), (0.240, 0.006), (0.160, 0.006)]
    cbm = lathe(cal, 18, closed=True, a0=radians(108), a1=radians(168))
    parts.append(('caliper', cbm, M_CALIPER, 0.010))
    return parts

def cap_open_ends(bm):
    # close the two open ends of an arc block
    edges = [e for e in bm.edges if e.is_boundary]
    bmesh.ops.holes_fill(bm, edges=edges, sides=0)
    return bm

WHEEL_MESHES = []
for (nm, bmw, mat, bev) in build_wheel_parts():
    if nm == 'caliper': recalc(cap_open_ends(bmw))
    ob = mesh_obj('w_' + nm, bmw, mats=[mat], smooth=True)
    if bev: add_bevel(ob, bev, 3, 30)
    apply_mods(ob)
    WHEEL_MESHES.append(ob)

WHEEL_OBJS = []
for wi, (wx, wy, wz, ws) in enumerate(WHEELS):
    we = empty('wheel_%d' % wi, (wx, wy, wz))
    we.scale = (1.0, ws if wy > 0 else -ws, 1.0)
    set_parent(we, ROLL)
    for src in WHEEL_MESHES:
        ob = link(bpy.data.objects.new(src.name + '_%d' % wi, src.data))
        ob.parent = we
    WHEEL_OBJS.append(we)
for src in WHEEL_MESHES:
    bpy.data.objects.remove(src)

print('car built %.1fs' % (time.time() - T0))


# =====================================================================================================
# STUDIO
# =====================================================================================================
def make_env(w=2048, h=1024):
    u = (np.arange(w) + 0.5) / w; v = (np.arange(h) + 0.5) / h
    U, V = np.meshgrid(u, v)
    th = pi - 2 * pi * U
    el = (V - 0.5) * pi
    dx = np.cos(el) * np.cos(th); dy = np.cos(el) * np.sin(th); dz = np.sin(el)
    img = np.zeros((h, w, 3), np.float32)

    def nrm(a):
        a = np.array(a, float); return a / np.linalg.norm(a)

    def box(cdir, ha, hb, color, inten, feather=0.25, up=(0, 0, 1), grad=0.35):
        c = nrm(cdir); upv = np.array(up, float)
        if abs(np.dot(c, upv)) > 0.95: upv = np.array((1.0, 0, 0))
        ua = nrm(np.cross(upv, c)); vb = np.cross(c, ua)
        dc = dx * c[0] + dy * c[1] + dz * c[2]
        da = dx * ua[0] + dy * ua[1] + dz * ua[2]
        db = dx * vb[0] + dy * vb[1] + dz * vb[2]
        ok = dc > 0.05
        a = np.where(ok, da / np.maximum(dc, 1e-3), 9.0); b = np.where(ok, db / np.maximum(dc, 1e-3), 9.0)
        ta, tb = tan(radians(ha)), tan(radians(hb))
        ma = np.clip((ta - np.abs(a)) / (ta * feather), 0, 1); mb = np.clip((tb - np.abs(b)) / (tb * feather), 0, 1)
        m = ma * ma * (3 - 2 * ma) * mb * mb * (3 - 2 * mb)
        hot = 1.0 - grad * (np.abs(a) / ta) ** 2   # gentle hotspot falloff inside the box
        img[...] += (m * hot)[..., None] * (np.array(color, np.float32) * inten)

    # base: near-black studio with a faint lift towards the horizon
    lift = 0.004 + 0.018 * np.exp(-((el - 0.02) / 0.22) ** 2)
    img += lift[..., None] * np.array((0.55, 0.6, 0.85), np.float32)
    # floor half: dark, slightly warm
    img[el < 0] = img[el < 0] * 0.5 + np.array((0.006, 0.005, 0.005), np.float32)
    # softboxes (world directions; car nose = +X, car left = +Y)
    box((0.15, 0.32, 1.0), 46, 4, (1.0, 0.96, 0.92), 1.6, feather=0.35)                # overhead strips
    box((0.15, -0.32, 1.0), 46, 4, (1.0, 0.96, 0.92), 1.6, feather=0.35)
    box((0.35, 1.0, 0.32), 22, 16, (1.0, 0.04, 0.55), 7.0)                            # hot magenta, car-left
    box((-0.25, -1.0, 0.30), 22, 16, (0.0, 0.62, 1.0), 7.0)                           # electric cyan, car-right
    box((-1.0, 0.25, 0.22), 26, 12, (0.80, 0.86, 1.0), 4.0)                           # cool white, behind
    box((1.0, -0.45, 0.12), 14, 6, (0.9, 0.95, 1.0), 1.6)                             # small front kicker
    # thin horizon line, colour drifting with azimuth
    hb = np.exp(-((el - 0.035) / 0.012) ** 2)
    hue = 0.5 + 0.5 * np.cos(th)
    hcol = np.stack([0.75 * hue + 0.05, 0.25 + 0.45 * (1 - hue), 0.95 - 0.1 * hue], -1).astype(np.float32)
    img += (hb * 0.9)[..., None] * hcol
    rgba_ = np.concatenate([img, np.ones((h, w, 1), np.float32)], -1)
    im = bpy.data.images.new('studio_env', w, h, alpha=True, float_buffer=True)
    im.pixels.foreach_set(rgba_.ravel())
    im.pack()
    return im

def build_world():
    w = bpy.data.worlds.new('studio'); SC.world = w
    if w.node_tree is None: w.use_nodes = True
    nt = w.node_tree
    for n in list(nt.nodes): nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputWorld')
    proc = nt.nodes.new('ShaderNodeTexEnvironment'); proc.image = make_env()
    refl = proc.outputs['Color']
    if A.hdri and os.path.exists(A.hdri):
        tc = nt.nodes.new('ShaderNodeTexCoord')
        mp = nt.nodes.new('ShaderNodeMapping'); mp.inputs['Rotation'].default_value = (0.0, 0.0, pi)
        lk(nt, tc.outputs['Generated'], mp.inputs['Vector'])
        hd = nt.nodes.new('ShaderNodeTexEnvironment'); hd.image = bpy.data.images.load(A.hdri)
        lk(nt, mp.outputs[0], hd.inputs['Vector'])
        sz = nt.nodes.new('ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Generated'], sz.inputs[0])
        low = node(nt, 'ShaderNodeMapRange', {'From Min': -0.12, 'From Max': 0.06, 'To Min': 0.06, 'To Max': 1.0})
        lk(nt, sz.outputs['Z'], low.inputs['Value'])
        k = math_node(nt, 'MULTIPLY', low.outputs[0], A.hdri_strength)
        hs = nt.nodes.new('ShaderNodeVectorMath'); hs.operation = 'SCALE'
        lk(nt, hd.outputs['Color'], hs.inputs[0]); lk(nt, k, hs.inputs['Scale'])
        ps = nt.nodes.new('ShaderNodeVectorMath'); ps.operation = 'SCALE'; ps.inputs['Scale'].default_value = 0.40
        lk(nt, proc.outputs['Color'], ps.inputs[0])
        ad = nt.nodes.new('ShaderNodeVectorMath'); ad.operation = 'ADD'
        lk(nt, hs.outputs[0], ad.inputs[0]); lk(nt, ps.outputs[0], ad.inputs[1])
        refl = ad.outputs[0]
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = 1.0
    lk(nt, refl, bg.inputs['Color'])
    bgc = nt.nodes.new('ShaderNodeBackground'); bgc.inputs['Strength'].default_value = 0.16
    navy = nt.nodes.new('ShaderNodeVectorMath'); navy.operation = 'MULTIPLY'; navy.inputs[1].default_value = (0.45, 0.62, 1.0)
    lk(nt, proc.outputs['Color'], navy.inputs[0]); lk(nt, navy.outputs[0], bgc.inputs['Color'])
    lp = nt.nodes.new('ShaderNodeLightPath')
    mix = nt.nodes.new('ShaderNodeMixShader')
    lk(nt, lp.outputs['Is Camera Ray'], mix.inputs[0]); lk(nt, bg.outputs[0], mix.inputs[1]); lk(nt, bgc.outputs[0], mix.inputs[2])
    lk(nt, mix.outputs[0], out.inputs['Surface'])
    vol = nt.nodes.new('ShaderNodeVolumePrincipled')
    vol.inputs['Density'].default_value = 0.0009
    vol.inputs['Anisotropy'].default_value = 0.55
    vol.inputs['Color'].default_value = (0.9, 0.92, 1.0, 1)
    lk(nt, vol.outputs[0], out.inputs['Volume'])
    try: w.probe_resolution = '2048'
    except Exception: pass
    w.sun_threshold = 50.0
    return w

def build_floor():
    m, nt, out = new_mat('floor')
    p = principled(nt, **{'Base Color': (0.010, 0.010, 0.012, 1), 'Roughness': 0.14, 'Specular IOR Level': 0.5})
    tc = node(nt, 'ShaderNodeTexCoord')
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 0.35, 'Detail': 6.0, 'Roughness': 0.6})
    lk(nt, tc.outputs['Object'], nz.inputs['Vector'])
    rr = node(nt, 'ShaderNodeMapRange', {'From Min': 0.3, 'From Max': 0.75, 'To Min': 0.09, 'To Max': 0.24})
    lk(nt, nz.outputs['Fac'], rr.inputs['Value'])
    # far floor gets rougher + darker to dissolve the horizon
    dist = node(nt, 'ShaderNodeVectorMath', operation='LENGTH'); lk(nt, tc.outputs['Object'], dist.inputs[0])
    far = node(nt, 'ShaderNodeMapRange', {'From Min': 9.0, 'From Max': 26.0, 'To Min': 0.0, 'To Max': 1.0})
    lk(nt, dist.outputs['Value'], far.inputs['Value'])
    rmix = node(nt, 'ShaderNodeMix', data_type='FLOAT')
    lk(nt, far.outputs[0], rmix.inputs[0]); lk(nt, rr.outputs[0], rmix.inputs[2]); rmix.inputs[3].default_value = 0.55
    lk(nt, rmix.outputs[0], p.inputs['Roughness'])
    lk(nt, p.outputs[0], out.inputs['Surface'])
    bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=128, radius=40.0)
    ob = mesh_obj('floor', bm, mats=[m], smooth=False)
    return ob

def area(name, loc, target, color, energy, sx, sy, spec=1.0, shadow=True):
    l = bpy.data.lights.new(name, 'AREA'); l.shape = 'RECTANGLE'; l.size = sx; l.size_y = sy
    l.color = color; l.energy = energy; l.specular_factor = spec; l.use_shadow = shadow
    ob = link(bpy.data.objects.new(name, l)); ob.location = loc
    d = (Vector(target) - Vector(loc)).normalized()
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

def spot(name, loc, target, color, energy, size_deg, blend=0.6, radius=0.3):
    l = bpy.data.lights.new(name, 'SPOT'); l.color = color; l.energy = energy
    l.spot_size = radians(size_deg); l.spot_blend = blend; l.shadow_soft_size = radius
    ob = link(bpy.data.objects.new(name, l)); ob.location = loc
    d = (Vector(target) - Vector(loc)).normalized()
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    return ob

build_world()
FLOOR = build_floor()
L_MAG = area('key_magenta', (2.0, 5.6, 3.6), (0, 0, 0.5), (1.0, 0.10, 0.62), 950, 4.5, 1.6, spec=0.6)
L_KEYW = area('key_white', (3.6, 3.4, 3.0), (0, 0, 0.6), (1.0, 0.98, 0.96), 1700, 4.0, 2.2, spec=0.55)
L_CYA = area('fill_cyan', (-1.6, -5.6, 3.2), (0, 0, 0.5), (0.05, 0.70, 1.0), 1150, 4.5, 1.6, spec=0.6)
L_ORA = area('rim_cool', (-6.0, 1.4, 2.6), (0, 0, 0.6), (0.70, 0.80, 1.0), 1600, 3.5, 1.4, spec=0.7)
L_TOP = area('top_soft', (0.2, 0.0, 5.0), (0, 0, 0), (1.0, 0.97, 0.94), 900, 6.0, 1.8, spec=0.08)
L_RIM = spot('rim_spot', (-7.2, -2.2, 2.1), (0, 0, 0.55), (0.85, 0.9, 1.0), 7000, 30, 0.7, 0.8)
L_RIM.data.volume_factor = 0.05
L_RIM.data.specular_factor = 0.5
try:   # rim light skips the floor (grazing spec on the glossy floor sparkles)
    _rc = bpy.data.collections.new('rim_receivers'); _rc.objects.link(FLOOR)
    L_RIM.light_linking.receiver_collection = _rc
    _rc.collection_objects[0].light_linking.link_state = 'EXCLUDE'   # only member: the floor
except Exception as _ex:
    print('light linking unavailable', _ex)
for _l in (L_MAG, L_CYA, L_ORA, L_TOP): _l.data.volume_factor = 0.6

# contact shadow (fake AO blob that follows the car)
def build_contact():
    m, nt, out = new_mat('contact')
    m.surface_render_method = 'BLENDED'
    tc = node(nt, 'ShaderNodeTexCoord')
    mp = node(nt, 'ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1 / 2.55, 1 / 1.22, 1)
    lk(nt, tc.outputs['Object'], mp.inputs['Vector'])
    ln = node(nt, 'ShaderNodeVectorMath', operation='LENGTH'); lk(nt, mp.outputs[0], ln.inputs[0])
    fall = node(nt, 'ShaderNodeMapRange', {'From Min': 0.55, 'From Max': 1.0, 'To Min': 1.0, 'To Max': 0.0},
                interpolation_type='SMOOTHERSTEP')
    lk(nt, ln.outputs['Value'], fall.inputs['Value'])
    at = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='opacity')
    a = math_node(nt, 'MULTIPLY', fall.outputs[0], at.outputs['Fac'])
    a = math_node(nt, 'MULTIPLY', a, 0.85)
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    blk = node(nt, 'ShaderNodeBsdfDiffuse', {'Color': (0, 0, 0, 1)})
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, a, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, blk.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=3.0)
    ob = mesh_obj('contact_shadow', bm, mats=[m], smooth=False)
    ob.location = (0, 0, 0.003)
    ob['opacity'] = 1.0
    ob.visible_shadow = False
    return ob

CONTACT = build_contact()

# tyres skip the saturated magenta/cyan keys (no colour spill on rubber)
try:
    _tc = bpy.data.collections.new('tyre_receivers')
    for o in [o for o in bpy.data.objects if o.name.startswith('w_tire_')]: _tc.objects.link(o)
    for L_ in (L_MAG, L_CYA): L_.light_linking.receiver_collection = _tc
    for co_ in _tc.collection_objects: co_.light_linking.link_state = 'EXCLUDE'
except Exception as _ex:
    print('tyre linking unavailable', _ex)

# overhead slab (hang / drop shots): underside at SLAB_Z, on four steel columns
SLAB_Z = 3.6
def mat_concrete():
    m, nt, out = new_mat('concrete')
    tc = node(nt, 'ShaderNodeTexCoord')
    sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 1.2, 'Detail': 6.0, 'Roughness': 0.55}); lk(nt, tc.outputs['Object'], nz.inputs['Vector'])
    g = node(nt, 'ShaderNodeMapRange', {'From Min': 0.3, 'From Max': 0.7, 'To Min': 0.19, 'To Max': 0.24}); lk(nt, nz.outputs['Fac'], g.inputs['Value'])
    lane = node(nt, 'ShaderNodeMapRange', {'From Min': 0.045, 'From Max': 0.030, 'To Min': 0.0, 'To Max': 1.0})
    lk(nt, math_node(nt, 'ABSOLUTE', math_node(nt, 'SUBTRACT', math_node(nt, 'ABSOLUTE', sx.outputs['Y']), 1.32)), lane.inputs['Value'])
    col = node(nt, 'ShaderNodeMix', data_type='FLOAT'); lk(nt, lane.outputs[0], col.inputs[0]); lk(nt, g.outputs[0], col.inputs[2]); col.inputs[3].default_value = 0.78
    cc = node(nt, 'ShaderNodeCombineXYZ')
    for k in ('X', 'Y', 'Z'): lk(nt, col.outputs[0], cc.inputs[k])
    fine = node(nt, 'ShaderNodeTexNoise', {'Scale': 70.0, 'Detail': 4.0}); lk(nt, tc.outputs['Object'], fine.inputs['Vector'])
    bump = node(nt, 'ShaderNodeBump', {'Strength': 0.12, 'Distance': 0.002}); lk(nt, fine.outputs['Fac'], bump.inputs['Height'])
    p = principled(nt, **{'Roughness': 0.78, 'Specular IOR Level': 0.35})
    lk(nt, cc.outputs[0], p.inputs['Base Color']); lk(nt, bump.outputs['Normal'], p.inputs['Normal'])
    lk(nt, p.outputs[0], out.inputs['Surface'])
    return m
M_CONCRETE = mat_concrete()
M_STEEL = mat_simple('steel', (0.05, 0.05, 0.055), 0.35, metal=0.9)
SLAB_OBJS = []
_b = bmesh.new(); bmesh.ops.create_cube(_b, size=1.0)
for v in _b.verts: v.co = Vector((v.co.x * 16.0, v.co.y * 6.0, v.co.z * 0.4 + 0.2 + SLAB_Z))
_sl = mesh_obj('slab', _b, mats=[M_CONCRETE], smooth=False); add_bevel(_sl, 0.02, 2, 30); SLAB_OBJS.append(_sl)
M_LED_RED = mat_emit('led_red', (1.0, 0.0, 0.008), 2.6)
for sy_ in (1, -1):
    _b = bmesh.new(); bmesh.ops.create_cube(_b, size=1.0)
    for v in _b.verts: v.co = Vector((v.co.x * 16.0, v.co.y * 0.022 + sy_ * 2.99, v.co.z * 0.022 + SLAB_Z + 0.012))
    SLAB_OBJS.append(mesh_obj('slab_led', _b, mats=[M_LED_RED], smooth=False))
for (cx, cy) in ():
    _b = bmesh.new(); bmesh.ops.create_cube(_b, size=1.0)
    for v in _b.verts: v.co = Vector((v.co.x * 0.45 + cx, v.co.y * 0.45 + cy, (v.co.z + 0.5) * SLAB_Z))
    _co = mesh_obj('column', _b, mats=[M_STEEL], smooth=False); add_bevel(_co, 0.015, 2, 30); SLAB_OBJS.append(_co)
print('studio built %.1fs' % (time.time() - T0))


# =====================================================================================================
# camera helpers
# =====================================================================================================
def make_cam(name, lens, sensor=36.0):
    cd = bpy.data.cameras.new(name); cd.lens = lens; cd.sensor_width = sensor; cd.clip_start = 0.05; cd.clip_end = 200
    cd.dof.use_dof = True; cd.dof.aperture_fstop = 2.8; cd.dof.aperture_blades = 7
    ob = link(bpy.data.objects.new(name, cd))
    return ob

def look(ob, eye, target, roll=0.0, prev=None):
    eye = Vector(eye); target = Vector(target)
    q = (target - eye).normalized().to_track_quat('-Z', 'Y')
    if roll: q = q @ Quaternion((0, 0, 1), roll)
    e = q.to_euler('XYZ', prev) if prev is not None else q.to_euler('XYZ')
    return eye, e

def orbit_eye(az, el, dist, target):
    a, e = radians(az), radians(el)
    return (target[0] + dist * cos(e) * cos(a), target[1] + dist * cos(e) * sin(a), target[2] + dist * sin(e))


# =====================================================================================================
# modes
# =====================================================================================================
def set_res(w, h, pct):
    SC.render.resolution_x = w; SC.render.resolution_y = h; SC.render.resolution_percentage = pct

def render_still(path):
    SC.render.filepath = path
    bpy.ops.render.render(write_still=True)

if A.mode == 'cartest':
    os.makedirs(A.out, exist_ok=True)
    for o in SLAB_OBJS: o.hide_render = True
    set_res(1920, 1080, A.pct)
    SC.render.use_motion_blur = False
    cam = make_cam('testcam', 50); SC.camera = cam
    views = [(35, 7, 7.4, 50), (90, 4, 8.2, 50), (150, 9, 7.6, 50), (15, 34, 8.0, 50)]
    for i, (az, el, dist, lens) in enumerate(views):
        tgt = (0.0, 0.0, 0.52)
        eye, rot = look(cam, orbit_eye(az, el, dist, tgt), tgt)
        cam.location = eye; cam.rotation_euler = rot; cam.data.lens = lens
        cam.data.dof.focus_distance = dist
        render_still(os.path.join(A.out, 'cartest_%d.png' % i))
    print('cartest done %.1fs' % (time.time() - T0))
    if A.save: bpy.ops.wm.save_as_mainfile(filepath=A.save)
    sys.exit(0)




# =====================================================================================================
# CLOCK + BEATS (animated shader inputs shared by many materials)
# =====================================================================================================
def clock_group():
    g = bpy.data.node_groups.new('CLOCK', 'ShaderNodeTree')
    g.interface.new_socket('Time', in_out='OUTPUT', socket_type='NodeSocketFloat')
    gout = g.nodes.new('NodeGroupOutput')
    v = g.nodes.new('ShaderNodeValue'); v.name = 't'
    g.links.new(v.outputs[0], gout.inputs['Time'])
    bake(g, 'nodes["t"].outputs[0].default_value', 0, [-10, F_END + 20], [sec(-10), sec(F_END + 20)], interp='LINEAR')
    return g

CLOCK_G = clock_group()

def clock_out(nt):
    n = nt.nodes.new('ShaderNodeGroup'); n.node_tree = CLOCK_G
    return n.outputs['Time']

BEAT_NAMES = ('Fans', 'Skirts', 'Tanks', 'Nozzles', 'Flow', 'Phase')
def beats_group():
    g = bpy.data.node_groups.new('BEATS', 'ShaderNodeTree')
    for nm in BEAT_NAMES:
        g.interface.new_socket(nm, in_out='OUTPUT', socket_type='NodeSocketFloat')
    gout = g.nodes.new('NodeGroupOutput')
    for nm in BEAT_NAMES:
        v = g.nodes.new('ShaderNodeValue'); v.name = nm; v.outputs[0].default_value = 0.0
        g.links.new(v.outputs[0], gout.inputs[nm])
    return g

BEATS_G = beats_group()

def beat_out(nt, name):
    n = nt.nodes.new('ShaderNodeGroup'); n.node_tree = BEATS_G
    return n.outputs[name]


# =====================================================================================================
# MECHANISM (facts file s2-s4): fans + skirts, two COPVs (200 L boot, 400 L passenger seat), 10 nozzles
# =====================================================================================================
CYAN = (0.047, 1.0, 0.888)      # #3DFFF2
MAGENTA = (1.0, 0.024, 0.672)   # #FF2BD6
ACID = (0.79, 1.0, 0.027)       # #E6FF2E
AMBER = ACID; ICE = (0.10, 0.85, 0.95); WHITE_ICE = (0.85, 0.97, 1.0); ORANGE = MAGENTA

def mat_mech(name, beat, glow_col, glow_str, normal=None, kind=None):
    """Normal look outside the x-ray (or hidden if normal is None); in the x-ray: invisible until its beat,
    then emissive. SCANMASK says whether a point is currently x-rayed."""
    m, nt, out = new_mat(name)
    sm = nt.nodes.new('ShaderNodeGroup'); sm.node_tree = SCAN_G
    if beat == 'lit':
        b = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='lit').outputs['Fac']
    else:
        b = beat_out(nt, beat)
    base_sh = None
    if kind == 'tank':
        tc = node(nt, 'ShaderNodeTexCoord'); sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
        ang = math_node(nt, 'ARCTAN2', sx.outputs['Z'], sx.outputs['X'])
        u = math_node(nt, 'MULTIPLY', sx.outputs['Y'], 6.0)
        v = math_node(nt, 'MULTIPLY', ang, 4 / pi)
        h1 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'ADD', u, v), 2 * pi))
        h2 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'SUBTRACT', u, v), 2 * pi))
        bands = math_node(nt, 'POWER', math_node(nt, 'MAXIMUM', math_node(nt, 'MAXIMUM', h1, h2), 0.0), 8.0)
        # 'drain' (object property, 0 = full, 1 = empty) moves a fill front along the tank's length like a charging
        # bar (Generated Y runs 0-1 end to end); the empty part keeps a faint carbon wrap, the front is a bright band
        drain = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='drain').outputs['Fac']
        sg = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Generated'], sg.inputs[0]); gy = sg.outputs['Y']
        level = math_node(nt, 'SUBTRACT', 1.02, math_node(nt, 'MULTIPLY', drain, 1.04))
        fill = node(nt, 'ShaderNodeMapRange', {'To Min': 1.0, 'To Max': 0.0}, interpolation_type='SMOOTHSTEP')
        lk(nt, math_node(nt, 'SUBTRACT', level, 0.008), fill.inputs['From Min']); lk(nt, math_node(nt, 'ADD', level, 0.008), fill.inputs['From Max'])
        lk(nt, gy, fill.inputs['Value'])
        men = node(nt, 'ShaderNodeMapRange', {'From Min': 0.0, 'From Max': 0.025, 'To Min': 1.0, 'To Max': 0.0}, interpolation_type='SMOOTHSTEP')
        lk(nt, math_node(nt, 'ABSOLUTE', math_node(nt, 'SUBTRACT', gy, level)), men.inputs['Value'])
        st = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', bands, glow_str * 2.4), glow_str * 0.45)
        empty = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', bands, glow_str * 0.35), glow_str * 0.02)
        st = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', st, fill.outputs[0]),
                       math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', men.outputs[0], glow_str * 4.0),
                                 math_node(nt, 'MULTIPLY', empty, math_node(nt, 'SUBTRACT', 1.0, fill.outputs[0]))))
        base = principled(nt, **{'Base Color': (0.022, 0.022, 0.025, 1), 'Roughness': 0.38, 'Coat Weight': 1.0,
                                 'Coat Roughness': 0.06})
        bump = node(nt, 'ShaderNodeBump', {'Strength': 0.3, 'Distance': 0.002}); lk(nt, bands, bump.inputs['Height'])
        lk(nt, bump.outputs['Normal'], base.inputs['Normal'])
        base_sh = base.outputs[0]
    else:
        lw = node(nt, 'ShaderNodeLayerWeight', {'Blend': 0.4})
        st = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', lw.outputs['Facing'], glow_str * 1.4), glow_str * 0.45)
        if normal is not None:
            base_sh = principled(nt, **normal).outputs[0]
    if base_sh is None:
        base_sh = node(nt, 'ShaderNodeBsdfTransparent').outputs[0]
    em = node(nt, 'ShaderNodeEmission', {'Color': rgba(glow_col)}); lk(nt, st, em.inputs['Strength'])
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    xr = node(nt, 'ShaderNodeMixShader'); lk(nt, b, xr.inputs[0]); lk(nt, tr.outputs[0], xr.inputs[1]); lk(nt, em.outputs[0], xr.inputs[2])
    fin = node(nt, 'ShaderNodeMixShader'); lk(nt, sm.outputs['Mask'], fin.inputs[0]); lk(nt, base_sh, fin.inputs[1]); lk(nt, xr.outputs[0], fin.inputs[2])
    lk(nt, fin.outputs[0], out.inputs['Surface'])
    m.use_transparent_shadow = True
    return m

def capsule(R, L, seg=48, rings=12):
    prof = []
    for i in range(rings + 1):
        a = -pi / 2 + (pi / 2) * i / rings
        prof.append((max(1e-4, R * cos(a)), -L / 2 + R * sin(a)))
    for i in range(1, rings + 1):
        a = (pi / 2) * i / rings
        prof.append((max(1e-4, R * cos(a)), L / 2 + R * sin(a)))
    return lathe(prof, seg)

def catmull(pts, n=10):
    P = [Vector(p) for p in pts]
    P = [P[0] * 2 - P[1]] + P + [P[-1] * 2 - P[-2]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-2])
    return [tuple(v) for v in out]

def rotate_y_to_x(bm):
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-pi / 2, 3, 'Z'))

# ---------------- fans (two, flat, behind the rear axle): pull air up from under the floor, exhaust out the flanks
FAN_X, FAN_Y, FAN_Z = -1.75, 0.30, 0.20
M_FAN_SHROUD = mat_mech('fan_shroud', 'Fans', ACID, 2.6, normal={'Base Color': (0.05, 0.05, 0.055, 1), 'Roughness': 0.35, 'Metallic': 0.8})
M_FAN_BLADE = mat_mech('fan_blade', 'Fans', ACID, 3.6, normal={'Base Color': (0.34, 0.35, 0.37, 1), 'Roughness': 0.25, 'Metallic': 1.0})
M_DUCT = mat_mech('fan_duct', 'Fans', ICE, 1.0)
ROTORS = []; FAN_PARTS = []
def rotate_y_to_z(bm):
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
for sy in (1, -1):
    c = Vector((FAN_X, sy * FAN_Y, FAN_Z))
    sh = lathe([(0.150, -0.06), (0.172, -0.06), (0.172, 0.06), (0.150, 0.06)], 64, closed=True)
    rotate_y_to_z(sh); bmesh.ops.translate(sh, verts=sh.verts, vec=c); recalc(sh)
    so = mesh_obj('fan_shroud', sh, mats=[M_FAN_SHROUD]); set_parent(so, SUSP); FAN_PARTS.append(so)
    rot_e = empty('fan_rotor', tuple(c)); set_parent(rot_e, SUSP)
    bm = bmesh.new()
    for i in range(9):
        th = 2 * pi * i / 9
        er = Vector((cos(th), sin(th), 0)); et = Vector((-sin(th), cos(th), 0))
        pc, ps = cos(radians(34)), sin(radians(34))
        vs = []
        for r in (0.042, 0.146):
            for (cs, ts) in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                chord = 0.028 * cs * (1.0 if r < 0.1 else 0.8); thick = 0.004 * ts
                t_off = chord * pc - thick * ps; z_off = chord * ps + thick * pc
                vs.append(bm.verts.new(er * r + et * t_off + Vector((0, 0, z_off))))
        a_, b2 = vs[:4], vs[4:]
        bm.faces.new(a_[::-1]); bm.faces.new(b2)
        for k in range(4):
            k2 = (k + 1) % 4; bm.faces.new((a_[k], a_[k2], b2[k2], b2[k]))
    recalc(bm)
    bl = mesh_obj('fan_blades', bm, mats=[M_FAN_BLADE], smooth=False); add_bevel(bl, 0.002, 1, 30); bl.parent = rot_e
    hb = lathe([(0.001, -0.05), (0.045, -0.05), (0.045, 0.03), (0.03, 0.05), (0.001, 0.06)], 32)
    rotate_y_to_z(hb); recalc(hb)
    hub = mesh_obj('fan_hub', hb, mats=[M_FAN_SHROUD]); hub.parent = rot_e
    ROTORS.append(rot_e); FAN_PARTS += [bl, hub]
    duct = curve_obj('fan_duct', catmull([(FAN_X, sy * FAN_Y, 0.27), (FAN_X - 0.06, sy * 0.60, 0.34), (-1.98, sy * 0.93, 0.40)], 10),
                     0.085, M_DUCT, SUSP, res=6)
    FAN_PARTS.append(duct)

# ---------------- deployable side skirts (seal the gap to the ground) ----------------
def mat_skirt():
    m, nt, out = new_mat('skirt')
    p = principled(nt, **{'Base Color': (0.012, 0.012, 0.014, 1), 'Roughness': 0.25, 'Metallic': 0.2, 'Coat Weight': 1.0})
    gx = nt.nodes.new('ShaderNodeGroup'); gx.node_tree = XRAY_G; lk(nt, p.outputs[0], gx.inputs['Surface'])
    sm = nt.nodes.new('ShaderNodeGroup'); sm.node_tree = SCAN_G
    b = beat_out(nt, 'Skirts')
    lw = node(nt, 'ShaderNodeLayerWeight', {'Blend': 0.3})
    st = math_node(nt, 'MULTIPLY', math_node(nt, 'MULTIPLY', sm.outputs['Mask'], b),
                   math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', lw.outputs['Facing'], 5.0), 4.0))
    em = node(nt, 'ShaderNodeEmission', {'Color': rgba(ORANGE)}); lk(nt, st, em.inputs['Strength'])
    ad = node(nt, 'ShaderNodeAddShader'); lk(nt, gx.outputs['Shader'], ad.inputs[0]); lk(nt, em.outputs[0], ad.inputs[1])
    lk(nt, ad.outputs[0], out.inputs['Surface'])
    m.use_transparent_shadow = True
    return m

M_SKIRT = mat_mech('skirt', 'Skirts', MAGENTA, 4.5, normal={'Base Color': (0.012, 0.012, 0.014, 1), 'Roughness': 0.25, 'Metallic': 0.2, 'Coat Weight': 1.0})
SKIRTS = []
for side in (1, -1):
    xs_ = [lerp(-0.90, 0.95, i / 40) for i in range(41)]
    ys_ = [0.93 * sec_params(x)[0] for x in xs_]
    bm = bmesh.new(); top = []; bot = []; top2 = []; bot2 = []
    for x, y in zip(xs_, ys_):
        top.append(bm.verts.new((x, side * y, 0.0))); bot.append(bm.verts.new((x, side * y, -0.26)))
        top2.append(bm.verts.new((x, side * (y - 0.02), 0.0))); bot2.append(bm.verts.new((x, side * (y - 0.02), -0.26)))
    for i in range(len(xs_) - 1):
        bm.faces.new((top[i], bot[i], bot[i + 1], top[i + 1]))
        bm.faces.new((top2[i + 1], bot2[i + 1], bot2[i], top2[i]))
        bm.faces.new((bot[i], bot2[i], bot2[i + 1], bot[i + 1]))
        bm.faces.new((top[i + 1], top2[i + 1], top2[i], top[i]))
    for (a_, b_, c_, d_) in ((top[0], top2[0], bot2[0], bot[0]), (top[-1], bot[-1], bot2[-1], top2[-1])):
        bm.faces.new((a_, b_, c_, d_))
    recalc(bm)
    sk = mesh_obj('skirt_deploy', bm, mats=[M_SKIRT], smooth=False); add_bevel(sk, 0.003, 2, 30)
    sk.location = (0, 0, 0.26)       # origin inside the lower body: scaling z extends it towards the ground
    set_parent(sk, SUSP)
    SKIRTS.append(sk)

# ---------------- COPV tanks ----------------
M_COPV = mat_mech('copv', 'lit', AMBER, 4.2, kind='tank')
M_BOSS = mat_mech('copv_boss', 'Tanks', (1.0, 0.85, 0.6), 5.0, normal={'Base Color': (0.6, 0.6, 0.62, 1), 'Roughness': 0.2, 'Metallic': 1.0})

def copv(name, R, Lc, loc, rot):
    bm = capsule(R, Lc); recalc(bm)
    ob = mesh_obj(name, bm, mats=[M_COPV]); ob.location = loc; ob.rotation_euler = rot; ob['lit'] = 0.0
    for s in (-1, 1):
        bb = lathe([(0.001, 0.0), (0.055, 0.0), (0.055, 0.05), (0.036, 0.085), (0.001, 0.085)], 24)
        if s < 0: bmesh.ops.rotate(bb, verts=bb.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi, 3, 'X'))
        bmesh.ops.translate(bb, verts=bb.verts, vec=(0, s * (Lc / 2 + R - 0.015), 0)); recalc(bb)
        boss = mesh_obj(name + '_boss', bb, mats=[M_BOSS]); boss.parent = ob; boss['lit'] = 0.0
    set_parent(ob, SUSP)
    return ob

TANK_P = copv('copv_400L', 0.29, 1.12, (-0.17, -0.37, 0.475), (0, 0, -pi / 2))   # in place of the passenger seat
TANK_B = copv('copv_200L', 0.26, 0.595, (-1.62, 0.0, 0.62), (0, 0, 0))          # transverse, in the boot

# ---------------- 10 nozzles: 4 rear (thrust), 4 corners down (lift), 2 front (yaw) ----------------
NOZ_DEF = [
    ('R1', (XT + 0.06, 0.10, 0.62), (-1, 0, 0), 'rear'), ('R2', (XT + 0.06, -0.10, 0.62), (-1, 0, 0), 'rear'),
    ('R3', (XT + 0.07, 0.66, 0.62), (-1, 0, 0), 'rear'), ('R4', (XT + 0.07, -0.66, 0.62), (-1, 0, 0), 'rear'),
    ('CFL', (1.92, 0.70, 0.17), (0, 0, -1), 'corner'), ('CFR', (1.92, -0.70, 0.17), (0, 0, -1), 'corner'),
    ('CRL', (-1.92, 0.74, 0.25), (0, 0, -1), 'corner'), ('CRR', (-1.92, -0.74, 0.25), (0, 0, -1), 'corner'),
    ('YL', (2.02, 0.74, 0.30), (0, 1, 0), 'yaw'), ('YR', (2.02, -0.74, 0.30), (0, -1, 0), 'yaw'),
]
M_NOZM = mat_mech('nozzle', 'lit', ACID, 7.0, normal={'Base Color': (0.50, 0.50, 0.53, 1), 'Roughness': 0.3, 'Metallic': 1.0})
M_FEED = mat_mech('feed_line', 'lit', CYAN, 2.2)
bell = lathe([(0.018, 0.0), (0.046, 0.10), (0.053, 0.10), (0.026, 0.0)], 24, closed=True)
bmesh.ops.rotate(bell, verts=bell.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
recalc(bell)
BELL_ME = bpy.data.meshes.new('bell'); bell.to_mesh(BELL_ME); bell.free(); BELL_ME.materials.append(M_NOZM); BELL_ME.shade_smooth()
NOZZLES = []    # (id, group, empty, pos, dir, bell)
for (nid, p, d, grp) in NOZ_DEF:
    p = Vector(p); d = Vector(d)
    e = empty('noz_' + nid, tuple(p))
    e.rotation_mode = 'QUATERNION'; e.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
    set_parent(e, SUSP)
    bo = link(bpy.data.objects.new('bell_' + nid, BELL_ME)); bo.parent = e; bo['lit'] = 0.0
    NOZZLES.append((nid, grp, e, p, d, bo))

P_FRONT = Vector((0.71, -0.37, 0.475)); B_BOT = Vector((-1.62, 0.0, 0.36))
FEEDS = []
for (nid, grp, e, p, d, bo) in NOZZLES:
    sy = 1 if p.y > 0 else -1
    if grp == 'corner' and p.x > 0:
        way = [P_FRONT, (1.15, sy * 0.25 - 0.1, 0.24), (1.70, sy * 0.55, 0.20), p]
    elif grp == 'yaw':
        way = [P_FRONT, (1.25, sy * 0.20 - 0.1, 0.34), (1.85, sy * 0.58, 0.31), p]
    elif grp == 'corner':
        way = [B_BOT, (-1.72, sy * 0.45, 0.34), (-1.86, sy * 0.68, 0.28), p]
    else:
        way = [B_BOT, (-1.80, p.y * 0.55, 0.45), (-2.00, p.y * 0.95, 0.58), p]
    cv = curve_obj('feed_' + nid, catmull(way, 12), 0.015, M_FEED, SUSP, res=4)
    cv['lit'] = 0.0; cv['nid'] = nid
    FEEDS.append(cv)

# ---------------- airflow streamlines + low-pressure sheet ----------------
def tube_mesh(name, pts, radius, seg=8):
    P = [Vector(p) for p in pts]
    s = [0.0]
    for i in range(1, len(P)): s.append(s[-1] + (P[i] - P[i - 1]).length)
    bm = bmesh.new(); uvl = bm.loops.layers.uv.new('UVMap')
    rings = []; prev_n = None
    for i, p in enumerate(P):
        t = (P[min(i + 1, len(P) - 1)] - P[max(i - 1, 0)]).normalized()
        if prev_n is None:
            a = Vector((0, 0, 1)) if abs(t.z) < 0.9 else Vector((1, 0, 0))
            n = t.cross(a).normalized()
        else:
            n = (prev_n - t * prev_n.dot(t)).normalized()
        b = t.cross(n); prev_n = n
        rings.append([bm.verts.new(p + (n * cos(2 * pi * k / seg) + b * sin(2 * pi * k / seg)) * radius) for k in range(seg)])
    for i in range(len(P) - 1):
        for k in range(seg):
            k2 = (k + 1) % seg
            f = bm.faces.new((rings[i][k], rings[i][k2], rings[i + 1][k2], rings[i + 1][k]))
            for loop, (ii, kk) in zip(f.loops, ((i, k), (i, k2), (i + 1, k2), (i + 1, k))):
                loop[uvl].uv = (s[ii], kk / seg)
    return bm, s[-1]

def mat_flow():
    m, nt, out = new_mat('flowline')
    m.surface_render_method = 'BLENDED'; m.show_transparent_back = False
    uv = node(nt, 'ShaderNodeUVMap'); sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, uv.outputs['UV'], sx.inputs[0])
    u = sx.outputs['X']
    d = math_node(nt, 'FRACT', math_node(nt, 'SUBTRACT', math_node(nt, 'MULTIPLY', u, 2.4), beat_out(nt, 'Phase')))
    streak = math_node(nt, 'POWER', math_node(nt, 'DIVIDE', math_node(nt, 'SUBTRACT', d, 0.40), 0.60, clamp_=True), 1.6)
    ln = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='len')
    e0 = node(nt, 'ShaderNodeMapRange', {'From Min': 0.0, 'From Max': 0.5}); lk(nt, u, e0.inputs['Value'])
    rem = math_node(nt, 'SUBTRACT', ln.outputs['Fac'], u)
    e1 = node(nt, 'ShaderNodeMapRange', {'From Min': 0.0, 'From Max': 0.6}); lk(nt, rem, e1.inputs['Value'])
    a = math_node(nt, 'MAXIMUM', streak, 0.24)
    a = math_node(nt, 'MULTIPLY', a, math_node(nt, 'MULTIPLY', e0.outputs[0], e1.outputs[0]))
    a = math_node(nt, 'MULTIPLY', a, beat_out(nt, 'Flow'), clamp_=True)
    em = node(nt, 'ShaderNodeEmission', {'Color': (0.62, 0.95, 1.0, 1)}); lk(nt, math_node(nt, 'MULTIPLY', a, 6.0), em.inputs['Strength'])
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, a, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

M_FLOW = mat_flow()
FLOW_PATHS = []
for (x0, y0, out_) in ((1.55, 0.22, 'rear'), (1.55, 0.62, 'flank'), (0.55, 0.80, 'flank'), (0.05, 0.36, 'rear'), (-0.75, 0.70, 'flank')):
    for sy in (1, -1):
        y = sy * y0
        wp = [(x0 + 0.55, y * 1.05, 0.03), (x0, y, 0.035), (-0.55, y * 0.75, 0.04), (-1.40, sy * 0.30, 0.05),
              (-1.72, sy * FAN_Y, 0.10), (FAN_X, sy * FAN_Y, 0.30)]
        if out_ == 'rear':
            wp += [(-1.98, sy * FAN_Y, 0.42), (-2.30, sy * (FAN_Y + 0.02), 0.44), (-2.75, sy * (FAN_Y + 0.04), 0.44), (-3.15, sy * (FAN_Y + 0.05), 0.44)]
        else:
            wp += [(-1.85, sy * 0.62, 0.42), (-1.97, sy * 0.95, 0.43), (-2.02, sy * 1.35, 0.43), (-2.06, sy * 1.75, 0.43)]
        FLOW_PATHS.append(wp)
FLOWS = []
for i, wp in enumerate(FLOW_PATHS):
    bm, L = tube_mesh('flow', catmull(wp, 10), 0.022)
    ob = mesh_obj('flowline_%d' % i, bm, mats=[M_FLOW]); ob['len'] = L; ob.visible_shadow = False
    set_parent(ob, SUSP); FLOWS.append(ob)

def mat_suction():
    m, nt, out = new_mat('suction')
    m.surface_render_method = 'BLENDED'
    tc = node(nt, 'ShaderNodeTexCoord'); sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
    ex = node(nt, 'ShaderNodeMapRange', {'From Min': 1.88, 'From Max': 1.4}); lk(nt, math_node(nt, 'ABSOLUTE', sx.outputs['X']), ex.inputs['Value'])
    ey = node(nt, 'ShaderNodeMapRange', {'From Min': 0.92, 'From Max': 0.55}); lk(nt, math_node(nt, 'ABSOLUTE', sx.outputs['Y']), ey.inputs['Value'])
    pulse = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', clock_out(nt), 7.0)), 0.25), 0.75)
    a = math_node(nt, 'MULTIPLY', math_node(nt, 'MULTIPLY', ex.outputs[0], ey.outputs[0]), pulse)
    a = math_node(nt, 'MULTIPLY', math_node(nt, 'MULTIPLY', a, math_node(nt, 'MULTIPLY', beat_out(nt, 'Flow'), beat_out(nt, 'Skirts'))), 0.34, clamp_=True)
    em = node(nt, 'ShaderNodeEmission', {'Color': (0.12, 0.42, 1.0, 1), 'Strength': 1.8})
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, a, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

bm = bmesh.new()
for (x, y) in ((-1.88, -0.92), (1.88, -0.92), (1.88, 0.92), (-1.88, 0.92)): bm.verts.new((x, y, 0.0))
bm.faces.new(bm.verts[:])
SUCTION = mesh_obj('suction_sheet', bm, mats=[mat_suction()], smooth=False); SUCTION.location = (0, 0, 0.04)
SUCTION.visible_shadow = False; set_parent(SUCTION, SUSP)

# ---------------- x-ray wireframe shell ----------------
SEGS_C = [(-pi / 2, radians(-30), 5), (radians(-30), 0.0, 4), (0.0, radians(42), 4), (radians(42), pi / 2, 7)]
def half_section_coarse(x):
    P = sec_params(x); half = []
    for (a, b, cnt) in SEGS_C:
        half += resample(lambda ph: sec_point(P, ph), a, b, cnt)
    half.append(sec_point(P, pi / 2)); half[0] = (0.0, half[0][1]); half[-1] = (0.0, half[-1][1])
    return half

def build_wire():
    m, nt, out = new_mat('xray_wire')
    sm = nt.nodes.new('ShaderNodeGroup'); sm.node_tree = SCAN_G
    em = node(nt, 'ShaderNodeEmission', {'Color': (0.25, 0.95, 1.0, 1), 'Strength': 1.3})
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, sm.outputs['Mask'], mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    xs = stations(XT, XN, LTP, LNP, 3, 5, 0.14)
    bm = loft(xs, half_section_coarse, 'wire')
    kill = []
    for f in bm.faces:
        c = f.calc_center_median()
        if c.z > 0.62 and abs(c.y) < max(0.0, canopy_w(c.x) - 0.04): kill.append(f); continue
        for (wx, wy, wz, ws) in WHEELS:
            if abs(c.y) > 0.45 and (c.x - wx) ** 2 + (c.z - wz) ** 2 < 0.47 ** 2: kill.append(f); break
    bmesh.ops.delete(bm, geom=list(set(kill)), context='FACES')
    bm.normal_update()
    for v in bm.verts: v.co += v.normal * 0.014
    ob = mesh_obj('xray_wire', bm, mats=[m], smooth=False)
    wm = ob.modifiers.new('wire', 'WIREFRAME'); wm.thickness = 0.0042; wm.use_even_offset = True; wm.use_replace = True
    set_parent(ob, SUSP)
    return ob

WIRE = build_wire()
print('mechanism built %.1fs' % (time.time() - T0))


# =====================================================================================================
# FX: cold-gas jets (frosty plume + Mach-diamond core)
# =====================================================================================================
def cone_mesh(name, r0, r1, rings=18, seg=28, pw=0.8):
    bm = bmesh.new(); vs = []
    for i in range(rings + 1):
        z = i / rings; r = r0 + (r1 - r0) * z ** pw
        vs.append([bm.verts.new((r * cos(2 * pi * k / seg), r * sin(2 * pi * k / seg), z)) for k in range(seg)])
    for i in range(rings):
        for k in range(seg):
            k2 = (k + 1) % seg
            bm.faces.new((vs[i][k], vs[i][k2], vs[i + 1][k2], vs[i + 1][k]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.shade_smooth()
    return me

def diamond_mesh(name, r0, nd=5, rings=90, seg=18):
    bm = bmesh.new(); vs = []
    for i in range(rings + 1):
        z = i / rings
        r = r0 * (0.28 + 0.72 * abs(sin(pi * z * nd)) ** 0.85) * (1.0 - 0.35 * z) + 0.002
        vs.append([bm.verts.new((r * cos(2 * pi * k / seg), r * sin(2 * pi * k / seg), z)) for k in range(seg)])
    for i in range(rings):
        for k in range(seg):
            k2 = (k + 1) % seg
            bm.faces.new((vs[i][k], vs[i][k2], vs[i + 1][k2], vs[i + 1][k]))
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.shade_smooth()
    return me

def mat_jet(name, core=False):
    m, nt, out = new_mat(name)
    m.surface_render_method = 'BLENDED'; m.show_transparent_back = True; m.use_transparency_overlap = True
    tc = node(nt, 'ShaderNodeTexCoord')
    sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
    z = sx.outputs['Z']
    zf = math_node(nt, 'POWER', math_node(nt, 'SUBTRACT', 1.0, math_node(nt, 'MINIMUM', z, 1.0)), 1.5 if core else 1.9)
    zin = node(nt, 'ShaderNodeMapRange', {'From Min': 0.0, 'From Max': 0.04}); lk(nt, z, zin.inputs['Value'])
    lw = node(nt, 'ShaderNodeLayerWeight', {'Blend': 0.5})
    edge = math_node(nt, 'POWER', math_node(nt, 'SUBTRACT', 1.0, lw.outputs['Facing']), 1.4 if core else 1.6)
    clk = clock_out(nt)
    mp = node(nt, 'ShaderNodeMapping'); lk(nt, tc.outputs['Object'], mp.inputs['Vector'])
    mp.inputs['Scale'].default_value = (5.0, 5.0, 2.2)
    off = node(nt, 'ShaderNodeCombineXYZ'); lk(nt, math_node(nt, 'MULTIPLY', clk, -7.0), off.inputs['Z'])
    vadd = node(nt, 'ShaderNodeVectorMath', operation='ADD'); lk(nt, mp.outputs[0], vadd.inputs[0]); lk(nt, off.outputs[0], vadd.inputs[1])
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 1.6, 'Detail': 5.0, 'Roughness': 0.62}, noise_dimensions='4D')
    lk(nt, vadd.outputs[0], nz.inputs['Vector']); lk(nt, math_node(nt, 'MULTIPLY', clk, 1.3), nz.inputs['W'])
    nzr = node(nt, 'ShaderNodeMapRange', {'From Min': 0.32, 'From Max': 0.74, 'To Min': 0.0, 'To Max': 1.5})
    lk(nt, nz.outputs['Fac'], nzr.inputs['Value'])
    at = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='fire')
    a = math_node(nt, 'MULTIPLY', zf, zin.outputs[0])
    a = math_node(nt, 'MULTIPLY', a, edge)
    if not core: a = math_node(nt, 'MULTIPLY', a, nzr.outputs[0])
    a = math_node(nt, 'MULTIPLY', a, at.outputs['Fac'])
    a = math_node(nt, 'MULTIPLY', a, 1.4 if core else 0.95, clamp_=True)
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    if core:
        sh = node(nt, 'ShaderNodeEmission', {'Color': (0.72, 0.92, 1.0, 1), 'Strength': 14.0}); so = sh.outputs[0]
    else:
        frost = principled(nt, **{'Base Color': (0.22, 0.25, 0.28, 1), 'Roughness': 1.0, 'Specular IOR Level': 0.0})
        em = node(nt, 'ShaderNodeEmission', {'Color': (0.78, 0.93, 1.0, 1)})
        lk(nt, math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', math_node(nt, 'POWER', math_node(nt, 'SUBTRACT', 1.0, math_node(nt, 'MINIMUM', z, 1.0)), 3.0), 2.4), 0.85), em.inputs['Strength'])
        ad = node(nt, 'ShaderNodeAddShader'); lk(nt, frost.outputs[0], ad.inputs[0]); lk(nt, em.outputs[0], ad.inputs[1])
        so = ad.outputs[0]
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, a, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, so, mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

M_JET = mat_jet('jet_plume'); M_JETCORE = mat_jet('jet_core', core=True)
ME_PLUME = cone_mesh('plume', 0.040, 0.42, pw=0.62); ME_PLUME.materials.append(M_JET)
ME_CORE = diamond_mesh('mach_core', 0.045); ME_CORE.materials.append(M_JETCORE)
JETS = []   # (nid, grp, plume, core, pos, dir)
for (nid, grp, e, p, d, bo) in NOZZLES:
    po = link(bpy.data.objects.new('jet_' + nid, ME_PLUME)); po.parent = e; po['fire'] = 0.0
    co = link(bpy.data.objects.new('mach_' + nid, ME_CORE)); co.parent = e; co['fire'] = 0.0
    for o_ in (po, co): o_.visible_shadow = False; o_.location = (0, 0, 0.10)
    JETS.append((nid, grp, po, co, p, d))
print('fx built %.1fs' % (time.time() - T0))




# =====================================================================================================
# PRESSURE ARROWS (hang shot): ambient air pushing the car up against the slab
# =====================================================================================================
def mat_arrow():
    m, nt, out = new_mat('pressure_arrow')
    m.surface_render_method = 'BLENDED'
    at = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='fade')
    em = node(nt, 'ShaderNodeEmission', {'Color': rgba(CYAN), 'Strength': 1.9})
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    a = math_node(nt, 'MULTIPLY', at.outputs['Fac'], 1.0, clamp_=True)
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, a, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

def mat_outline():
    m, nt, out = new_mat('arrow_outline')
    m.surface_render_method = 'BLENDED'; m.use_backface_culling = True
    at = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='fade')
    em = node(nt, 'ShaderNodeEmission', {'Color': (0.0, 0.01, 0.02, 1), 'Strength': 1.0})
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, at.outputs['Fac'], mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

def arrow_mesh(length=0.72, shaft_r=0.045, head_r=0.125, head_l=0.24):
    bm = lathe([(0.001, 0.0), (shaft_r, 0.0), (shaft_r, length - head_l), (head_r, length - head_l), (0.001, length)], 24)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))   # along +Z
    recalc(bm)
    me = bpy.data.meshes.new('arrow'); bm.to_mesh(me); bm.free(); me.shade_smooth()
    me.materials.append(mat_arrow()); me.materials.append(mat_outline())
    return me

def add_outline(ob, width=0.014):
    so = ob.modifiers.new('outline', 'SOLIDIFY'); so.thickness = width; so.offset = 1.0
    so.use_flip_normals = True; so.use_rim = False; so.material_offset = 1

ARROWS = []   # (object, base position, direction)


# =====================================================================================================
# SHOTS (each a standalone clip starting at frame 1)
# =====================================================================================================
HANG_Z = SLAB_Z - 1.10 - 0.012
EASE_FALL = cubic_bezier(0.42, 0.0, 0.85, 0.45)
EASE_CUSH = cubic_bezier(0.2, 0.55, 0.45, 1.0)
EASE_WHIP = cubic_bezier(0.7, 0.0, 0.15, 1.0)
const = lambda v: (lambda f: v)

def ramp(f0, n=6):
    return lambda f: EASE_OUT(clamp((f - f0) / float(n)))

def pop(f0, f):
    return max(0.001, spring(sec(f) - sec(f0), 2.6, 0.42)) if f >= f0 - 1 else 0.001

def pulse_env(f, a, b, rise=3, fall=5):
    if f <= a or f >= b + fall: return 0.0
    if f < a + rise: return EASE_OUT((f - a) / rise)
    if f <= b: return 1.0
    return 1.0 - EASE_IO((f - b) / fall)

S = {}   # per-shot functions / keys
if SHOT == 'hang':
    F_SCAN = (10, 30); F_FANS = 26; F_FLOW = 32; F_SKIRT = 78; F_ARROWS = 112
    S['root_z'] = keys_fn([(1, HANG_Z, None), (F_ARROWS + 6, HANG_Z, None), (F_ARROWS + 22, HANG_Z + 0.018, EASE_IO), (F_END + 9, HANG_Z + 0.018, None)])
    S['roll'] = const(180.0); S['pitch'] = const(0.0)
    S['susp'] = keys_fn([(1, -0.006, None), (F_ARROWS + 6, -0.006, None), (F_ARROWS + 22, -0.034, EASE_IO), (F_END + 9, -0.034, None)])
    S['thr'] = keys_fn([(1, 2.8, None), (F_SCAN[0], 2.8, None), (F_SCAN[1], -2.8, EASE_IO), (F_END + 9, -2.8, None)])
    S['Fans'] = ramp(F_FANS); S['Skirts'] = ramp(F_SKIRT, 8); S['Tanks'] = const(0.0); S['Nozzles'] = const(0.0)
    S['flow'] = lambda f: 0.9 * EASE_OUT(clamp((f - F_FLOW) / 14.0)) + 0.1 * EASE_OUT(clamp((f - F_SKIRT - 6) / 12.0))
    S['speed'] = lambda f: lerp(1.6, 3.4, EASE_IO(clamp((f - F_FLOW) / 30.0)))
    S['fan_rps'] = lambda f: lerp(0.0, 5.5, EASE_IO(clamp((f - F_FANS) / 40.0)))
    S['skirt'] = lambda f: lerp(0.08, 1.0, clamp(spring(sec(f) - sec(F_SKIRT), 2.4, 0.55)))
    S['slab'] = True; S['smoke'] = False
    S['cam'] = dict(az=[(1, 24, None), (F_END, 36, EASE_SOFT)], el=[(1, -26.0, None), (F_END, -22.0, EASE_SOFT)],
                    dist=[(1, 5.0, None), (F_END, 4.55, EASE_SOFT)], tx=[(1, -0.25, None), (F_END, -0.20, EASE_SOFT)],
                    tz=[(1, 2.80, None), (F_END, 2.84, EASE_SOFT)], lens=[(1, 36, None), (F_END, 37, EASE_SOFT)],
                    roll=[(1, 0.0, None), (F_END, 0.0, None)], fstop=[(1, 7.0, None), (F_END, 7.0, None)],
                    shy=[(1, 0.0, None), (F_END, 0.0, None)])
elif SHOT == 'xray':
    F_SCAN = (6, 24)
    LIT = {'copv_400L': 30, 'copv_200L': 42,
           'R1': 70, 'R2': 75, 'R3': 80, 'R4': 85, 'CRL': 102, 'CRR': 107, 'CFL': 112, 'CFR': 117, 'YL': 134, 'YR': 139}
    S['root_z'] = const(0.0); S['roll'] = const(0.0); S['pitch'] = const(0.0); S['susp'] = const(0.0)
    S['thr'] = keys_fn([(1, 2.8, None), (F_SCAN[0], 2.8, None), (F_SCAN[1], -2.8, EASE_IO), (F_END + 9, -2.8, None)])
    S['Fans'] = const(0.0); S['Skirts'] = const(0.0); S['Tanks'] = ramp(LIT['copv_400L']); S['Nozzles'] = ramp(LIT['R1'])
    S['flow'] = const(0.0); S['speed'] = const(1.0); S['fan_rps'] = const(0.0); S['skirt'] = const(0.18)
    S['slab'] = False; S['smoke'] = False
    S['cam'] = dict(az=[(1, 168, None), (F_END, 153, EASE_SOFT)], el=[(1, 43.0, None), (F_END, 39.0, EASE_SOFT)],
                    dist=[(1, 5.45, None), (F_END, 4.95, EASE_SOFT)], tx=[(1, -0.10, None), (F_END, -0.05, EASE_SOFT)],
                    tz=[(1, 0.38, None), (F_END, 0.40, None)], lens=[(1, 42, None), (F_END, 43, EASE_SOFT)],
                    roll=[(1, 0.0, None), (F_END, 0.0, None)], fstop=[(1, 8.0, None), (F_END, 8.0, None)],
                    shy=[(1, -0.10, None), (F_END, -0.10, None)])
elif SHOT in ('gauge', 'refill'):   # gauge: rear jets empty the tanks in ~1.6 s; refill: no jets, the tanks fill slowly
    F_DRAIN = (3, 51) if SHOT == 'gauge' else (8, F_END - 10)
    S['root_z'] = const(0.0); S['roll'] = const(0.0); S['pitch'] = const(0.0); S['susp'] = const(0.0)
    S['thr'] = const(-2.8)
    S['Fans'] = const(0.0); S['Skirts'] = const(0.0); S['Tanks'] = const(1.0); S['Nozzles'] = const(1.0)
    S['flow'] = const(0.0); S['speed'] = const(1.0); S['fan_rps'] = const(0.0); S['skirt'] = const(0.08)
    S['slab'] = False; S['smoke'] = False
    S['cam'] = dict(az=[(1, 122, None), (F_END, 116, EASE_SOFT)], el=[(1, 44.0, None), (F_END, 41.0, EASE_SOFT)],
                    dist=[(1, 3.6, None), (F_END, 3.3, EASE_SOFT)], tx=[(1, -1.15, None), (F_END, -1.15, None)],
                    tz=[(1, 0.45, None), (F_END, 0.45, None)], lens=[(1, 36, None), (F_END, 37, EASE_SOFT)],
                    roll=[(1, 0.0, None), (F_END, 0.0, None)], fstop=[(1, 6.3, None), (F_END, 6.3, None)],
                    shy=[(1, -0.06, None), (F_END, -0.06, None)])
    if SHOT == 'refill':   # tighter on the two tanks (critic: the gauge fills 60% of the frame or more), slow push
        S['cam'] = dict(az=[(1, 120, None), (F_END, 113, EASE_SOFT)], el=[(1, 47.0, None), (F_END, 43.0, EASE_SOFT)],
                        dist=[(1, 2.75, None), (F_END, 2.45, EASE_SOFT)], tx=[(1, -0.92, None), (F_END, -0.92, None)],
                        tz=[(1, 0.52, None), (F_END, 0.52, None)], lens=[(1, 38, None), (F_END, 39, EASE_SOFT)],
                        roll=[(1, 0.0, None), (F_END, 0.0, None)], fstop=[(1, 6.3, None), (F_END, 6.3, None)],
                        shy=[(1, -0.04, None), (F_END, -0.04, None)])
else:   # drop
    F_PUSH, F_DETACH, F_ROLL, F_CUSH, F_LAND = 14, 19, (23, 43), (34, 53), 52
    S['root_z'] = keys_fn([(1, HANG_Z + 0.018, None), (F_PUSH, HANG_Z + 0.018, None), (F_DETACH, HANG_Z, EASE_IO),
                           (45, 0.40, EASE_FALL), (F_LAND, 0.0, EASE_CUSH), (F_LAND + 6, 0.035, EASE_OUT), (F_LAND + 12, 0.0, EASE_IN),
                           (F_END + 9, 0.0, None)])
    S['roll'] = keys_fn([(1, 180.0, None), (F_ROLL[0], 180.0, None), (F_ROLL[1], 360.0, cubic_bezier(0.55, 0.0, 0.3, 1.0)), (F_END + 9, 360.0, None)])
    S['pitch'] = keys_fn([(1, 0.0, None), (F_DETACH, 0.0, None), (F_DETACH + 7, 3.0, EASE_OUT), (F_ROLL[1], 0.0, EASE_IO),
                          (F_LAND + 1, 0.0, None), (F_LAND + 4, -2.2, EASE_OUT), (F_LAND + 11, 0.9, EASE_IO), (F_LAND + 18, 0.0, EASE_IO),
                          (F_END + 9, 0.0, None)])
    S['susp'] = keys_fn([(1, -0.034, None), (F_PUSH, -0.034, None), (F_DETACH + 3, 0.02, EASE_OUT), (F_DETACH + 11, 0.0, EASE_IO),
                         (F_LAND, 0.0, None), (F_LAND + 4, -0.07, EASE_OUT), (F_LAND + 10, 0.022, EASE_IO), (F_LAND + 16, -0.006, EASE_IO),
                         (F_LAND + 22, 0.0, EASE_IO), (F_END + 9, 0.0, None)])
    S['thr'] = const(2.8)
    S['Fans'] = const(0.0); S['Skirts'] = const(0.0); S['Tanks'] = const(0.0); S['Nozzles'] = const(0.0)
    S['flow'] = const(0.0); S['speed'] = const(1.0)
    S['fan_rps'] = lambda f: lerp(5.5, 0.8, EASE_IO(clamp((f - F_PUSH) / 30.0)))
    S['skirt'] = const(1.0)
    S['slab'] = True; S['smoke'] = True
    S['cam'] = dict(az=[(1, 34, None), (F_END, 26, EASE_SOFT)], el=[(1, 2.0, None), (F_DETACH, 2.0, None), (60, 5.0, EASE_IO), (F_END, 5.5, EASE_SOFT)],
                    dist=[(1, 7.4, None), (F_END, 6.7, EASE_SOFT)], tx=[(1, 0.15, None), (F_END, 0.1, EASE_SOFT)],
                    tz=[(1, 1.55, None), (F_END, 1.45, EASE_SOFT)], lens=[(1, 50, None), (F_END, 52, EASE_SOFT)],
                    roll=[(1, 0.0, None), (F_ROLL[0], 0.0, None), (F_ROLL[0] + 8, -4.0, EASE_OUT), (F_ROLL[1] + 4, 2.0, EASE_IO), (F_LAND + 8, 0.0, EASE_IO), (F_END, 0.0, None)],
                    fstop=[(1, 7.0, None), (F_END, 7.0, None)],
                    shy=[(1, -0.04, None), (F_END, -0.04, None)])

root_z = S['root_z']; roll_deg = S['roll']; pitch_deg = S['pitch']; susp_dz = S['susp']
bake_fn(ROOT, 'location', 2, root_z)
bake_fn(ROLL, 'rotation_euler', 0, lambda f: radians(roll_deg(f)))
bake_fn(ROLL, 'rotation_euler', 1, lambda f: radians(-pitch_deg(f)))
bake_fn(SUSP, 'location', 2, lambda f: 0.55 + susp_dz(f))
bake_fn(CONTACT, '["opacity"]', 0, lambda f: clamp(1.0 - root_z(f) / 1.4) ** 1.5)
for o in SLAB_OBJS:
    o.hide_render = not S['slab']
if S['slab']:   # neutral bounce under the slab so the ramp concrete reads grey
    L_SLABFILL = area('slab_fill', (0.0, 0.0, 0.9), (0.0, 0.0, SLAB_Z), (0.92, 0.95, 1.0), 380, 7.0, 4.5, spec=0.15, shadow=False)
    L_SLABFILL.data.volume_factor = 0.0
bake_fn(SCAN_G, 'nodes["thr"].outputs[0].default_value', 0, S['thr'])
for nm in ('Fans', 'Skirts', 'Tanks', 'Nozzles'):
    bake_fn(BEATS_G, 'nodes["%s"].outputs[0].default_value' % nm, 0, S[nm])
bake_fn(BEATS_G, 'nodes["Flow"].outputs[0].default_value', 0, S['flow'])
_ph = {}; acc = 0.0
for f in range(-10, F_END + 12):
    _ph[f] = acc; acc += S['speed'](f) * 2.4 / FPS
bake_fn(BEATS_G, 'nodes["Phase"].outputs[0].default_value', 0, lambda f: _ph.get(int(f), 0.0))
_ang = {}; acc = 0.0
for f in range(-10, F_END + 12):
    _ang[f] = acc; acc += 2 * pi * S['fan_rps'](f) / FPS
for r_ in ROTORS:
    bake_fn(r_, 'rotation_euler', 2, lambda f: _ang.get(int(f), 0.0))
for sk in SKIRTS:
    bake_fn(sk, 'scale', 2, S['skirt'])

# per-part lighting (x-ray build) and scale pops
if SHOT == 'xray':
    for tk in (TANK_P, TANK_B):
        f0 = LIT[tk.name]
        bake_fn(tk, '["lit"]', 0, ramp(f0, 5))
        for i in range(3): bake_fn(tk, 'scale', i, lambda f, f0=f0: pop(f0, f) if f >= f0 - 1 else 0.001)
    for (nid, grp, e, p, d, bo) in NOZZLES:
        f0 = LIT[nid]
        bake_fn(bo, '["lit"]', 0, lambda f, f0=f0: 0.0 if f < f0 else EASE_OUT(clamp((f - f0) / 3.0)) * (1.0 + 1.1 * exp(-(f - f0) / 5.0)))
        for i in range(3): bake_fn(bo, 'scale', i, lambda f, f0=f0: 1.5 * pop(f0, f) if f >= f0 - 1 else 0.001)
    for cv in FEEDS:
        f0 = LIT[cv['nid']]
        bake_fn(cv, '["lit"]', 0, ramp(f0 - 6, 4))
        bake_fn(cv.data, 'bevel_factor_end', 0, lambda f, f0=f0: max(0.0001, EASE_IO(clamp((f - (f0 - 8)) / 9.0))))
    for o in FAN_PARTS + SKIRTS + FLOWS + [SUCTION]:
        o.hide_render = True
elif SHOT == 'hang':
    for o in (TANK_P, TANK_B) + tuple(n[5] for n in NOZZLES) + tuple(FEEDS):
        o.hide_render = True
    for ch in TANK_P.children + TANK_B.children: ch.hide_render = True
    # pressure arrows: below the hanging car (pointing up) and at both flanks (pointing in)
    AR_ME = arrow_mesh()
    bases = []
    for x in (-1.25, 0.05, 1.30):
        for y in (-0.42, 0.42):
            bases.append(((x, y, HANG_Z + 1.10 - 1.28 - 1.15), (0, 0, 1)))
    for x in (-1.0, 0.55):
        for sy in (1, -1):
            bases.append(((x, sy * 2.2, HANG_Z + 0.62), (0, -sy, 0)))
    for k, (bp, dv) in enumerate(bases):
        ob = link(bpy.data.objects.new('arrow_%d' % k, AR_ME)); ob['fade'] = 0.0; ob.visible_shadow = False; add_outline(ob)
        ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector(dv))
        bp = Vector(bp); dv = Vector(dv)
        f0 = F_ARROWS + (k % 6) * 2
        period = 0.9 * FPS
        def ph(f, f0=f0, period=period, k=k): return ((f - f0) / period + 0.17 * k) % 1.0
        def fade(f, f0=f0, ph=ph):
            if f < f0: return 0.0
            return EASE_OUT(clamp((f - f0) / 8.0)) * sin(pi * ph(f)) ** 0.7
        bake_fn(ob, '["fade"]', 0, fade)
        for i in range(3):
            bake_fn(ob, 'location', i, lambda f, i=i, bp=bp, dv=dv, ph=ph, f0=f0: (bp + dv * (0.42 * (EASE_IO(ph(f)) if f >= f0 else 0.0)))[i])
        ARROWS.append(ob)
elif SHOT in ('gauge', 'refill'):
    for tk in (TANK_P, TANK_B):
        tk['lit'] = 1.0
        tk['drain'] = 0.0   # the custom property must exist before its keys can drive the shader
        if SHOT == 'gauge':
            bake_fn(tk, '["drain"]', 0, lambda f: clamp((f - F_DRAIN[0]) / float(F_DRAIN[1] - F_DRAIN[0])))
        else:
            bake_fn(tk, '["drain"]', 0, lambda f: 1.0 - EASE_IO(clamp((f - F_DRAIN[0]) / float(F_DRAIN[1] - F_DRAIN[0]))))
    for (nid, grp, e, p, d, bo) in NOZZLES:
        bo['lit'] = 1.0 if (grp == 'rear' and SHOT == 'gauge') else 0.3
    for cv in FEEDS: cv['lit'] = 1.0
    for o in FAN_PARTS + SKIRTS + FLOWS + [SUCTION]:
        o.hide_render = True
else:   # drop: opaque car, no x-ray parts
    for o in FAN_PARTS + FLOWS + [SUCTION, WIRE]:
        o.hide_render = True

# ---------------- jets (drop shot) ----------------
def jet_fire(nid, grp, f):
    if SHOT == 'gauge':
        if grp != 'rear': return 0.0
        v = (1.0 - EASE_IO(clamp((f - (F_DRAIN[1] - 6)) / 8.0))) * (1.0 - 0.35 * clamp((f - F_DRAIN[0]) / float(F_DRAIN[1] - F_DRAIN[0])))
        return v * (0.9 + 0.1 * mnoise.noise(Vector((f * 0.4, (sum(map(ord, nid)) % 97) * 0.37, 0.0))))
    if SHOT != 'drop': return 0.0
    v = 0.0
    if grp == 'corner':
        v = max(v, pulse_env(f, F_PUSH, F_ROLL[0] + 2, 2, 5))
        if nid.endswith('R'): v = max(v, pulse_env(f, F_ROLL[0], F_ROLL[0] + 10, 2, 5))
        v = max(v, pulse_env(f, F_CUSH[0], F_CUSH[1], 2, 8))
    elif grp == 'yaw':
        a0 = 31 if nid == 'YL' else 35
        v = max(v, 0.8 * pulse_env(f, a0, a0 + 3, 1, 4))
    flick = 0.88 + 0.12 * mnoise.noise(Vector((f * 0.28, (sum(map(ord, nid)) % 97) * 0.37, 0.0)))
    return v * flick

NOZ_LOCAL_Z = {n[0]: n[3].z for n in NOZZLES}
def jet_len(nid, grp, f, fire):
    if SHOT == 'gauge':
        return max(0.05, fire * 1.75)
    if grp == 'corner' and f >= F_CUSH[0] - 2:
        return max(0.05, fire * min(2.1, max(0.6, 0.35 + root_z(f) + 0.35)))
    if grp == 'corner' and f < F_ROLL[0] + 3:      # inverted: jet column up to the slab underside
        gap = SLAB_Z - (root_z(f) + 1.1 - NOZ_LOCAL_Z[nid]) - 0.10
        return max(0.05, fire * max(0.15, gap + 0.06))
    return max(0.05, fire * (1.45 if grp == 'corner' else 1.1))

for (nid, grp, po, co, p, d) in JETS:
    if SHOT not in ('drop', 'gauge') or (SHOT == 'gauge' and grp != 'rear'):
        po.hide_render = co.hide_render = True
        continue
    fire = lambda f, nid=nid, grp=grp: jet_fire(nid, grp, f)
    bake_fn(po, '["fire"]', 0, fire); bake_fn(co, '["fire"]', 0, fire)
    bake_fn(po, 'scale', 2, lambda f, nid=nid, grp=grp: jet_len(nid, grp, f, jet_fire(nid, grp, f)))
    bake_fn(co, 'scale', 2, lambda f, nid=nid, grp=grp: 0.78 * jet_len(nid, grp, f, jet_fire(nid, grp, f)))
    for i in (0, 1):
        bake_fn(po, 'scale', i, lambda f, nid=nid, grp=grp: 0.8 + 0.5 * jet_fire(nid, grp, f))
        bake_fn(co, 'scale', i, lambda f, nid=nid, grp=grp: 1.0 + 0.3 * jet_fire(nid, grp, f))
print('animation baked %.1fs' % (time.time() - T0))


# =====================================================================================================
# SMOKE (drop shot): Mantaflow gas sim, jets against the slab, roll burst, landing cushion cloud
# =====================================================================================================
SMOKE_DIR = os.path.join(HERE, 'cache_smoke_' + SHOT)

def rig_rot(f):
    return Euler((radians(roll_deg(f)), radians(-pitch_deg(f)), 0.0), 'XYZ').to_matrix()

def build_smoke():
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    dom = mesh_obj('smoke_domain', bm, smooth=False)
    dom.scale = (7.2, 6.0, SLAB_Z); dom.location = (0.0, 0.0, SLAB_Z / 2)
    md = dom.modifiers.new('Fluid', 'FLUID'); md.fluid_type = 'DOMAIN'; ds = md.domain_settings
    ds.domain_type = 'GAS'; ds.resolution_max = 112
    ds.cache_directory = SMOKE_DIR; ds.cache_type = 'ALL'
    ds.cache_frame_start = 1; ds.cache_frame_end = F_END
    ds.use_collision_border_top = True; ds.use_collision_border_bottom = True
    ds.alpha = -0.12; ds.beta = 0.0; ds.vorticity = 0.45
    ds.use_dissolve_smoke = True; ds.dissolve_speed = int(4.5 * FPS); ds.use_dissolve_smoke_log = True
    m, nt, out = new_mat('smoke')
    tc = node(nt, 'ShaderNodeTexCoord')
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 6.0, 'Detail': 6.0, 'Roughness': 0.6}, noise_dimensions='4D')
    lk(nt, tc.outputs['Object'], nz.inputs['Vector']); lk(nt, math_node(nt, 'MULTIPLY', clock_out(nt), 0.5), nz.inputs['W'])
    dn = math_node(nt, 'MULTIPLY', math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', nz.outputs['Fac'], 1.1), 0.25), 16.0)
    vol = node(nt, 'ShaderNodeVolumePrincipled', {'Color': (0.86, 0.92, 1.0, 1), 'Anisotropy': 0.3,
                                                 'Emission Color': (0.55, 0.85, 1.0, 1), 'Emission Strength': 0.02})
    lk(nt, dn, vol.inputs['Density'])
    lk(nt, vol.outputs[0], out.inputs['Volume'])
    dom.data.materials.append(m)
    em_me = bpy.data.meshes.new('smoke_em'); b2 = bmesh.new(); bmesh.ops.create_icosphere(b2, subdivisions=2, radius=0.14)
    b2.to_mesh(em_me); b2.free()
    for (nid, grp, po, co, p, d) in JETS:
        if grp not in ('corner', 'yaw'): continue
        e = [n for n in NOZZLES if n[0] == nid][0][2]
        eo = link(bpy.data.objects.new('smoke_em_' + nid, em_me)); eo.parent = e; eo.location = (0, 0, 0.22); eo.hide_render = True
        fm = eo.modifiers.new('Fluid', 'FLUID'); fm.fluid_type = 'FLOW'; fs = fm.flow_settings
        fs.flow_type = 'SMOKE'; fs.flow_behavior = 'INFLOW'; fs.flow_source = 'MESH'; fs.surface_distance = 0.12
        fs.smoke_color = (0.92, 0.96, 1.0); fs.density = 1.0; fs.use_initial_velocity = True; fs.velocity_factor = 0.0
        dloc = Vector(d)
        bake_fn(eo, 'modifiers["Fluid"].flow_settings.use_inflow', 0, lambda f, nid=nid, grp=grp: 1.0 if jet_fire(nid, grp, f) > 0.3 else 0.0)
        for i in range(3):
            bake_fn(eo, 'modifiers["Fluid"].flow_settings.velocity_coord', i, lambda f, i=i, dloc=dloc: (rig_rot(f) @ dloc)[i] * 10.0)
        for fc in channelbag(eo).fcurves:
            if fc.data_path.endswith('use_inflow'):
                for kp in fc.keyframe_points: kp.interpolation = 'CONSTANT'
    xs = stations(XT, XN, LTP, LNP, 3, 5, 0.14)
    pb = loft(xs, half_section_coarse, 'proxy')
    px = mesh_obj('smoke_proxy', pb, smooth=False); px.hide_render = True; set_parent(px, SUSP)   # (no effector: faster bake)
    return dom

SMOKE = build_smoke() if (S['smoke'] and not A.nosmoke) else None

def bake_smoke():
    if SMOKE is None: return
    t = time.time()
    SC.frame_start, SC.frame_end = 1, F_END
    with bpy.context.temp_override(scene=SC, active_object=SMOKE, object=SMOKE):
        bpy.ops.fluid.free_all()
        r = bpy.ops.fluid.bake_all()
    print('smoke bake', r, '%.1fs' % (time.time() - t))


# =====================================================================================================
# CAMERA (baked per frame, handheld noise, push-off + landing shake)
# =====================================================================================================
def car_center(f):
    return Vector((0.0, 0.0, 0.55 + root_z(f)))

def bake_camera(name):
    cam = make_cam(name, 50)
    if VERT: cam.data.sensor_fit = 'HORIZONTAL'
    K = {k: keys_fn(v) for k, v in S['cam'].items()}
    vals = {}; prev = [None]
    for f in range(-4, F_END + 5):
        t = sec(f)
        tz = K['tz'](f) if SHOT != 'drop' else K['tz'](f) + 0.45 * (root_z(f - 2) - root_z(1)) * 0.0 + 0.0
        tgt = Vector((K['tx'](f), 0.0, tz))
        eye = Vector(orbit_eye(K['az'](f), K['el'](f), K['dist'](f), tgt))
        eye += Vector((mnoise.noise(Vector((t * 0.42, 1.3, 0.0))), mnoise.noise(Vector((t * 0.42, 7.1, 2.0))),
                       mnoise.noise(Vector((t * 0.42, 3.7, 5.0))))) * 0.012
        q = (tgt - eye).normalized().to_track_quat('-Z', 'Y')
        hp = 0.2 * mnoise.noise(Vector((t * 0.55, 11.0, 0.0))); hy = 0.2 * mnoise.noise(Vector((t * 0.55, 17.0, 0.0)))
        hr = 0.1 * mnoise.noise(Vector((t * 0.5, 23.0, 0.0)))
        sk = 0.0
        if SHOT == 'drop':
            if f > F_LAND: sk += 1.1 * exp(-(f - F_LAND) / (0.19 * FPS)) * sin(2 * pi * (f - F_LAND) / (0.18 * FPS))
            if F_PUSH <= f <= F_PUSH + 12: sk += 0.5 * exp(-(f - F_PUSH) / (0.12 * FPS)) * sin(2 * pi * (f - F_PUSH) / (0.13 * FPS))
        q = q @ Euler((radians(hp + sk), radians(hy), radians(K['roll'](f) + hr + 0.4 * sk)), 'XYZ').to_quaternion()
        e = q.to_euler('XYZ', prev[0]) if prev[0] is not None else q.to_euler('XYZ'); prev[0] = e
        vals[f] = dict(loc=eye, rot=e, foc=(car_center(f) - eye).length - 0.5, lens=K['lens'](f), fst=K['fstop'](f), shy=K['shy'](f))
    get = lambda key, i=None: (lambda f: vals[int(f)][key][i] if i is not None else vals[int(f)][key])
    for i in range(3):
        bake_fn(cam, 'location', i, get('loc', i), -4, F_END + 4)
        bake_fn(cam, 'rotation_euler', i, get('rot', i), -4, F_END + 4)
    bake_fn(cam.data, 'lens', 0, get('lens'), -4, F_END + 4)
    bake_fn(cam.data, 'shift_y', 0, get('shy'), -4, F_END + 4)
    bake_fn(cam.data, 'dof.focus_distance', 0, get('foc'), -4, F_END + 4)
    bake_fn(cam.data, 'dof.aperture_fstop', 0, get('fst'), -4, F_END + 4)
    return cam

CAM = bake_camera('CAM')
SC.camera = CAM
print('camera baked %.1fs' % (time.time() - T0))


# =====================================================================================================
# COMPOSITOR
# =====================================================================================================
def build_compositor():
    ng = bpy.data.node_groups.new('Comp', 'CompositorNodeTree')
    SC.compositing_node_group = ng
    ng.interface.new_socket('Image', in_out='OUTPUT', socket_type='NodeSocketColor')
    rl = ng.nodes.new('CompositorNodeRLayers')
    gl = ng.nodes.new('CompositorNodeGlare')
    for k, v in (('Type', 'Bloom'), ('Quality', 'High'), ('Threshold', 1.6), ('Smoothness', 0.4), ('Strength', 0.26),
                 ('Size', 0.55), ('Saturation', 1.0)):
        try: gl.inputs[k].default_value = v
        except Exception as ex: print('glare opt', k, ex)
    ld = ng.nodes.new('CompositorNodeLensdist')
    ld.inputs['Dispersion'].default_value = 0.0045
    out = ng.nodes.new('NodeGroupOutput')
    ng.links.new(rl.outputs['Image'], gl.inputs['Image'])
    ng.links.new(gl.outputs['Image'], ld.inputs['Image'])
    ng.links.new(ld.outputs['Image'], out.inputs['Image'])
    SC.render.use_compositing = True

build_compositor()
print('scene ready %.1fs' % (time.time() - T0))


# =====================================================================================================
# RENDER
# =====================================================================================================
if VERT: set_res(1080, 1920, A.pct)
else: set_res(1920, 1080, A.pct)
SC.frame_start, SC.frame_end = 1, F_END
tag = '%s_%s' % (SHOT, 'v' if VERT else 'h')
if A.mode == 'sheet':
    frames = [int(v) for v in A.frames.split(',')]
    if SMOKE is not None: bake_smoke()
    if A.save: bpy.ops.wm.save_as_mainfile(filepath=A.save)
    os.makedirs(A.out, exist_ok=True)
    for f in frames:
        SC.frame_set(f)
        t = time.time()
        render_still(os.path.join(A.out, 'sheet_%s_%04d.png' % (tag, f)))
        print('frame %d %.1fs' % (f, time.time() - t))
elif A.mode == 'anim':
    if SMOKE is not None: bake_smoke()
    if A.save: bpy.ops.wm.save_as_mainfile(filepath=A.save)
    od = os.path.join(A.out, tag)
    os.makedirs(od, exist_ok=True)
    SC.frame_start, SC.frame_end = A.start, min(A.end, F_END)
    SC.render.filepath = os.path.join(od, '')
    t = time.time()
    bpy.ops.render.render(animation=True)
    print('anim %s frames %d-%d in %.1fs' % (tag, SC.frame_start, SC.frame_end, time.time() - t))
elif A.save:
    bpy.ops.wm.save_as_mainfile(filepath=A.save)
print('total %.1fs' % (time.time() - T0))
