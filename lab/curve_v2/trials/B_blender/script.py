"""B_blender style trial: procedural electric hypercar, cold-gas thruster reveal.

Everything is generated in Python (no downloaded models, textures or HDRIs). Optional --hdri PATH swaps the
procedural studio environment for an image (e.g. a Poly Haven CC0 studio HDRI) if one is approved later.

Run (Blender 5.2, EEVEE):
  blender -b -P script.py -- --mode cartest              # 4 static views of the car
  blender -b -P script.py -- --mode sheet --pct 50       # 6 representative frames -> frames/sheet_*.png
  blender -b -P script.py -- --mode anim --cam h         # 1920x1080 frames -> frames/h/
  blender -b -P script.py -- --mode anim --cam v         # 1080x1920 frames -> frames/v/
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
ap.add_argument('--cam', default='h')
ap.add_argument('--frames', default='1,60,100,150,165,232')
ap.add_argument('--pct', type=int, default=100)
ap.add_argument('--samples', type=int, default=32)
ap.add_argument('--out', default=os.path.join(HERE, 'frames'))
ap.add_argument('--hdri', default='')
ap.add_argument('--start', type=int, default=1)
ap.add_argument('--end', type=int, default=240)
ap.add_argument('--save', default='')
A = ap.parse_args(argv)

FPS = 24
F_END = 240
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

def bake(id_, path, index, frames, values, interp='BEZIER'):
    cb = channelbag(id_)
    fc = cb.fcurves.find(path, index=index)
    if fc is None: fc = cb.fcurves.new(path, index=index)
    fc.keyframe_points.clear()
    fc.keyframe_points.add(len(frames))
    co = []
    for f, v in zip(frames, values): co += [float(f), float(v)]
    fc.keyframe_points.foreach_set('co', co)
    for kp in fc.keyframe_points:
        kp.interpolation = interp
        kp.handle_left_type = kp.handle_right_type = 'AUTO_CLAMPED'
    fc.update()
    return fc

def bake_fn(id_, path, index, fn, f0=1, f1=F_END, pad=2):
    frames = list(range(f0 - pad, f1 + pad + 1))
    bake(id_, path, index, frames, [fn(f) for f in frames])

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
XN, XT = 2.34, -2.20
LNP, PN = 0.55, 2.1      # nose plan rounding length / exponent
LNS_T, QN_T = 0.22, 1.45  # nose side rounding above the tip (hood leading edge, fairly sharp)
LNS_B, QN_B = 0.46, 2.0  # nose side rounding below the tip (raked front fascia)
LTP, PT = 0.15, 4.0      # tail plan rounding (squared-off Kamm tail)
LTS_T, QT_T = 0.07, 3.5  # tail deck edge (crisp)
LTS_B, QT_B = 0.10, 3.0
ZTIP_N, ZTIP_T = 0.355, 0.62
DIPW = 0.50
NB, NT = 6.0, 5.0

fW = Spline([(-2.20, 0.935), (-1.95, 1.005), (-1.35, 1.055), (-0.85, 1.01), (-0.25, 0.955), (0.35, 0.96),
             (0.90, 0.995), (1.38, 1.015), (1.85, 0.995), (2.34, 0.94)])
fZB = Spline([(-2.20, 0.31), (-1.95, 0.21), (-1.65, 0.135), (-1.2, 0.115), (0.0, 0.11), (1.5, 0.11),
              (1.95, 0.115), (2.34, 0.12)])
fZS = Spline([(-2.20, 0.64), (-1.75, 0.63), (-1.33, 0.60), (-0.7, 0.53), (0.2, 0.49), (0.9, 0.48),
              (1.38, 0.46), (1.9, 0.40), (2.34, 0.34)])
fZF = Spline([(-2.20, 0.90), (-1.95, 0.94), (-1.33, 0.975), (-0.85, 0.935), (-0.3, 0.855), (0.3, 0.80),
              (0.85, 0.79), (1.38, 0.80), (1.85, 0.66), (2.34, 0.43)])
fZC = Spline([(-2.20, 0.885), (-1.95, 0.91), (-1.33, 0.92), (-0.85, 0.89), (-0.3, 0.815), (0.3, 0.755),
              (0.85, 0.695), (1.38, 0.635), (1.85, 0.55), (2.34, 0.415)])

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
    if x > 2.06 and row < SEGS[0][2] + SEGS[1][2] - 1: return 3   # front intake (raked fascia)
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
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = (0.10, 0.62, 1.0, 1)
    lk(nt, stren, em.inputs['Strength'])
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    holo = nt.nodes.new('ShaderNodeAddShader'); lk(nt, tr.outputs[0], holo.inputs[0]); lk(nt, em.outputs[0], holo.inputs[1])
    mix = nt.nodes.new('ShaderNodeMixShader')
    lk(nt, sm.outputs['Mask'], mix.inputs[0]); lk(nt, gin.outputs['Surface'], mix.inputs[1]); lk(nt, holo.outputs[0], mix.inputs[2])
    sem = nt.nodes.new('ShaderNodeEmission'); sem.inputs['Color'].default_value = (0.45, 0.92, 1.0, 1)
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
    p = principled(nt, **{'Base Color': rgba(CAR_PAINT), 'Metallic': 1.0, 'Roughness': 0.30,
                          'Specular Tint': (1.0, 0.42, 0.36, 1), 'Coat Weight': 1.0, 'Coat Roughness': 0.025,
                          'Coat IOR': 1.52})
    # metallic flake: fine noise into base normal only (coat stays mirror-smooth)
    tc = node(nt, 'ShaderNodeTexCoord')
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 900.0, 'Detail': 1.0})
    lk(nt, tc.outputs['Object'], nz.inputs['Vector'])
    bump = node(nt, 'ShaderNodeBump', {'Strength': 0.08, 'Distance': 0.001})
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
M_GLASS = mat_glass(XRAY_G)
M_GRILLE = mat_grille(XRAY_G)
M_FASCIA = mat_simple('fascia', (0.005, 0.005, 0.006), 0.55, xg=XRAY_G, spec=0.25)
M_VENT = mat_simple('vent', (0.003, 0.003, 0.004), 0.18, coat=0.0, xg=XRAY_G, spec=0.6)
M_CHROME_DK = mat_simple('chrome_dark', (0.30, 0.31, 0.33), 0.12, metal=1.0, xg=XRAY_G)
M_LIGHT_F = mat_emit('light_front', (0.85, 0.93, 1.0), 15.0)
M_LIGHT_R = mat_emit('light_rear', (1.0, 0.02, 0.03), 16.0)
for mm in (M_PAINT, M_CARBON, M_WELL, M_GRILLE, M_FASCIA):
    BODY.data.materials.append(mm)

sub = BODY.modifiers.new('sub', 'SUBSURF'); sub.levels = 1; sub.render_levels = 1

WHEELS = [(1.38, 0.862, 0.37, 1.0), (1.38, -0.862, 0.37, 1.0), (-1.33, 0.885, 0.37, 1.10), (-1.33, -0.885, 0.37, 1.10)]
cutters = []
for (wx, wy, wz, ws) in WHEELS:
    r = 0.425 if wx > 0 else 0.432
    y0, y1 = (0.56, 1.30) if wy > 0 else (-1.30, -0.56)
    cbm = bmesh.new()
    bmesh.ops.create_cone(cbm, cap_ends=True, segments=96, radius1=r, radius2=r, depth=(y1 - y0))
    bmesh.ops.rotate(cbm, verts=cbm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
    bmesh.ops.translate(cbm, verts=cbm.verts, vec=(wx, (y0 + y1) / 2, wz + 0.018))
    cob = mesh_obj('cutter', cbm, mats=[M_WELL], smooth=True)
    cob.hide_render = True
    cutters.append(cob)
    bo = BODY.modifiers.new('arch', 'BOOLEAN'); bo.object = cob; bo.operation = 'DIFFERENCE'; bo.solver = 'EXACT'
    bo.material_mode = 'TRANSFER'
apply_mods(BODY)
for c in cutters: bpy.data.objects.remove(c)
# sharp edge between paint and wheel well
bm = bmesh.new(); bm.from_mesh(BODY.data)
well_idx = [i for i, m in enumerate(BODY.data.materials) if m and m.name.startswith('well')]
for e in bm.edges:
    if len(e.link_faces) == 2:
        a, b = e.link_faces
        if (a.material_index in well_idx) != (b.material_index in well_idx):
            e.smooth = False
bm.to_mesh(BODY.data); bm.free()
set_parent(BODY, SUSP)

# ---------------- canopy ----------------
CXF, CXR = 1.02, -1.42
WCMAX = 0.655
fZR = Spline([(1.02, 0.69), (0.85, 0.80), (0.6, 0.93), (0.3, 1.035), (0.0, 1.095), (-0.3, 1.115), (-0.6, 1.10),
              (-0.95, 1.035), (-1.2, 0.97), (-1.42, 0.925)])
_um = 0.5 / (0.5 + 0.85); _fm = _um ** 0.5 * (1 - _um) ** 0.85

def canopy_w(x):
    u = clamp((CXF - x) / (CXF - CXR))
    return WCMAX * (u ** 0.5) * ((1 - u) ** 0.85) / _fm

def canopy_half(x):
    wc = canopy_w(x)
    zbase = body_top_z(x, wc) - 0.012
    zr = max(fZR(x), zbase + 0.002)
    nc = 2.5
    def up(ph):
        c = max(0.0, cos(ph)); s = max(0.0, sin(ph))
        return (wc * c ** (2 / nc), zbase + (zr - zbase) * s ** (2 / nc))
    zbur = zbase - 0.09
    half = resample(lambda t: (wc * 0.97 * t, zbur), 0.0, 1.0, 3)
    half += resample(lambda t: (lerp(wc * 0.97, wc, t), lerp(zbur, zbase, t)), 0.0, 1.0, 3)
    half += resample(up, 0.0, pi / 2, 26)
    half.append((0.0, zr))
    half[0] = (0.0, half[0][1])
    return half

xs_can = stations(CXR, CXF, 0.30, 0.22, 18, 22, 0.03)
bm = loft(xs_can, canopy_half, 'canopy')
CANOPY = mesh_obj('canopy', bm, mats=[M_GLASS], smooth=True)
s2 = CANOPY.modifiers.new('sub', 'SUBSURF'); s2.levels = 1; s2.render_levels = 1
set_parent(CANOPY, SUSP)

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

bar_curve('lightbar_front_housing', 0.372, 1.84, XN, 0.016, M_FASCIA, inset=0.008)
bar_curve('lightbar_front', 0.372, 1.86, XN, 0.0085, M_LIGHT_F, inset=-0.004)
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
patch_top('deck_louvre', -2.04, -1.64, lambda x: -0.44, lambda x: 0.44, M_GRILLE, mirror=False)

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
    box((-1.0, 0.25, 0.22), 26, 12, (1.0, 0.33, 0.02), 6.0)                           # warm orange, behind
    box((1.0, -0.45, 0.12), 14, 6, (0.9, 0.95, 1.0), 1.6)                             # small front kicker
    # thin horizon line, colour drifting with azimuth
    hb = np.exp(-((el - 0.035) / 0.012) ** 2)
    hue = 0.5 + 0.5 * np.cos(th)
    hcol = np.stack([0.9 * hue + 0.2, 0.35 + 0.3 * (1 - hue), 0.9 - 0.4 * hue], -1).astype(np.float32)
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
    env = nt.nodes.new('ShaderNodeTexEnvironment')
    if A.hdri and os.path.exists(A.hdri):
        env.image = bpy.data.images.load(A.hdri)
        mult = 1.0
    else:
        env.image = make_env()
        mult = 1.0
    bg = nt.nodes.new('ShaderNodeBackground'); bg.inputs['Strength'].default_value = mult
    lk(nt, env.outputs['Color'], bg.inputs['Color'])
    # what the camera sees directly: a much darker version (studio walls), lights stay in reflections
    bgc = nt.nodes.new('ShaderNodeBackground'); bgc.inputs['Strength'].default_value = 0.16
    lk(nt, env.outputs['Color'], bgc.inputs['Color'])
    lp = nt.nodes.new('ShaderNodeLightPath')
    mix = nt.nodes.new('ShaderNodeMixShader')
    lk(nt, lp.outputs['Is Camera Ray'], mix.inputs[0]); lk(nt, bg.outputs[0], mix.inputs[1]); lk(nt, bgc.outputs[0], mix.inputs[2])
    lk(nt, mix.outputs[0], out.inputs['Surface'])
    # haze
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
L_MAG = area('key_magenta', (2.0, 5.6, 3.6), (0, 0, 0.5), (1.0, 0.10, 0.62), 2600, 4.5, 1.6, spec=0.7)
L_CYA = area('fill_cyan', (-1.6, -5.6, 3.2), (0, 0, 0.5), (0.05, 0.70, 1.0), 2400, 4.5, 1.6, spec=0.7)
L_ORA = area('rim_orange', (-6.0, 1.4, 2.6), (0, 0, 0.6), (1.0, 0.38, 0.05), 2000, 3.5, 1.4, spec=0.7)
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
# CLOCK (seconds) for procedural motion inside shaders
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


# =====================================================================================================
# INTERNALS (revealed by the x-ray scan): COPV tank, feed lines, thruster clusters
# =====================================================================================================
TANK_C = Vector((-0.90, 0.0, 0.60)); TANK_R = 0.165; TANK_L = 0.60
INT_CYAN = (0.20, 0.80, 1.0)

def mat_internal(name, color, strength, kind=None):
    m, nt, out = new_mat(name)
    sm = nt.nodes.new('ShaderNodeGroup'); sm.node_tree = SCAN_G
    mask = sm.outputs['Mask']
    tc = node(nt, 'ShaderNodeTexCoord'); tc.object = BODY
    if kind == 'tank':
        sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
        ang = math_node(nt, 'ARCTAN2', math_node(nt, 'SUBTRACT', sx.outputs['Z'], TANK_C.z), sx.outputs['Y'])
        u = math_node(nt, 'MULTIPLY', sx.outputs['X'], 6.0)
        v = math_node(nt, 'MULTIPLY', ang, 4 / pi)
        h1 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'ADD', u, v), 2 * pi))
        h2 = math_node(nt, 'SINE', math_node(nt, 'MULTIPLY', math_node(nt, 'SUBTRACT', u, v), 2 * pi))
        bands = math_node(nt, 'POWER', math_node(nt, 'MAXIMUM', math_node(nt, 'MAXIMUM', h1, h2), 0.0), 8.0)
        st = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', bands, strength * 2.6), strength * 0.45)
    elif kind == 'flow':
        d = node(nt, 'ShaderNodeVectorMath', operation='DISTANCE'); lk(nt, tc.outputs['Object'], d.inputs[0])
        d.inputs[1].default_value = tuple(TANK_C)
        ph = math_node(nt, 'FRACT', math_node(nt, 'SUBTRACT', math_node(nt, 'MULTIPLY', d.outputs['Value'], 2.4),
                                               math_node(nt, 'MULTIPLY', clock_out(nt), 1.8)))
        pulse = node(nt, 'ShaderNodeMapRange', {'From Min': 0.0, 'From Max': 0.16, 'To Min': 1.0, 'To Max': 0.0},
                     interpolation_type='SMOOTHSTEP')
        lk(nt, ph, pulse.inputs['Value'])
        st = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', pulse.outputs[0], strength * 3.0), strength * 0.35)
    else:
        lw = node(nt, 'ShaderNodeLayerWeight', {'Blend': 0.4})
        st = math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', lw.outputs['Facing'], strength * 1.5), strength * 0.4)
    em = node(nt, 'ShaderNodeEmission', {'Color': rgba(color)}); lk(nt, st, em.inputs['Strength'])
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, mask, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

M_TANK = mat_internal('int_tank', (1.0, 0.40, 0.05), 4.0, 'tank')
M_PIPE = mat_internal('int_pipe', INT_CYAN, 3.2, 'flow')
M_NOZ = mat_internal('int_nozzle', (0.85, 0.97, 1.0), 6.0)
M_MANI = mat_internal('int_manifold', (0.18, 0.55, 1.0), 3.4)

def capsule(R, L, seg=48, rings=12):
    prof = []
    for i in range(rings + 1):
        a = -pi / 2 + (pi / 2) * i / rings
        prof.append((max(1e-4, R * cos(a)), -L / 2 + R * sin(a)))
    for i in range(1, rings + 1):
        a = (pi / 2) * i / rings
        prof.append((max(1e-4, R * cos(a)), L / 2 + R * sin(a)))
    return lathe(prof, seg)

bm = capsule(TANK_R, TANK_L)
bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-pi / 2, 3, 'Z'))
bmesh.ops.translate(bm, verts=bm.verts, vec=TANK_C)
recalc(bm)
TANK = mesh_obj('copv_tank', bm, mats=[M_TANK]); set_parent(TANK, SUSP)
for sx_ in (-1, 1):
    bm = lathe([(0.001, 0.0), (0.045, 0.0), (0.045, 0.05), (0.03, 0.08), (0.001, 0.08)], 32, closed=False)
    bmesh.ops.rotate(bm, verts=bm.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(-sx_ * pi / 2, 3, 'Z'))
    bmesh.ops.translate(bm, verts=bm.verts, vec=TANK_C + Vector((sx_ * (TANK_L / 2 + TANK_R - 0.01), 0, 0)))
    ob = mesh_obj('copv_valve', bm, mats=[M_NOZ]); set_parent(ob, SUSP)

CLUSTERS = [
    ('FL', (1.86, 0.70, 0.22), [(0, 0, -1), (0, 1, 0), (1, 0, 0)]),
    ('FR', (1.86, -0.70, 0.22), [(0, 0, -1), (0, -1, 0), (1, 0, 0)]),
    ('ML', (0.05, 0.84, 0.20), [(0, 0, -1), (0, 1, 0)]),
    ('MR', (0.05, -0.84, 0.20), [(0, 0, -1), (0, -1, 0)]),
    ('RL', (-1.86, 0.80, 0.30), [(0, 0, -1), (0, 1, 0), (-1, 0, 0)]),
    ('RR', (-1.86, -0.80, 0.30), [(0, 0, -1), (0, -1, 0), (-1, 0, 0)]),
]

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

NOZZLES = []   # (cluster, kind, empty)
bell = lathe([(0.018, 0.0), (0.046, 0.10), (0.053, 0.10), (0.026, 0.0)], 24, closed=True)
bmesh.ops.rotate(bell, verts=bell.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
recalc(bell)
BELL_ME = bpy.data.meshes.new('bell'); bell.to_mesh(BELL_ME); bell.free(); BELL_ME.materials.append(M_NOZ); BELL_ME.shade_smooth()
for (cid, c, dirs) in CLUSTERS:
    c = Vector(c)
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * 0.14, v.co.y * 0.11, v.co.z * 0.09)) + c
    mob = mesh_obj('manifold_' + cid, bm, mats=[M_MANI], smooth=False); add_bevel(mob, 0.012, 3, 30); set_parent(mob, SUSP)
    for d in dirs:
        d = Vector(d)
        kind = 'down' if d.z < -0.5 else ('out' if abs(d.y) > 0.5 else ('fore' if d.x > 0 else 'aft'))
        e = empty('noz_%s_%s' % (cid, kind), c + d * 0.05)
        e.rotation_mode = 'QUATERNION'; e.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d)
        set_parent(e, SUSP)
        bo = link(bpy.data.objects.new('bell_%s_%s' % (cid, kind), BELL_ME)); bo.parent = e
        NOZZLES.append((cid, kind, e, c, d))
    # feed line from the tank
    sgn = 1 if c.y > 0 else -1
    if c.x > 1.0:
        way = [(TANK_C.x + 0.48, 0, TANK_C.z), (-0.2, 0.05 * sgn, 0.30), (1.15, 0.26 * sgn, 0.22), (1.72, 0.52 * sgn, 0.22), (c.x - 0.06, c.y - 0.06 * sgn, c.z)]
    elif c.x > -1.0:
        way = [(TANK_C.x + 0.2, 0, TANK_C.z - 0.15), (-0.5, 0.30 * sgn, 0.24), (-0.05, 0.68 * sgn, 0.20), (c.x, c.y - 0.07 * sgn, c.z)]
    else:
        way = [(TANK_C.x - 0.48, 0, TANK_C.z), (-1.58, 0.30 * sgn, 0.42), (-1.78, 0.64 * sgn, 0.32), (c.x + 0.02, c.y - 0.07 * sgn, c.z)]
    curve_obj('feed_' + cid, catmull(way, 12), 0.017, M_PIPE, SUSP, res=4)

# x-ray wireframe shell (coarse loft, wheel openings removed)
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
    em = node(nt, 'ShaderNodeEmission', {'Color': (0.45, 0.88, 1.0, 1), 'Strength': 1.5})
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, sm.outputs['Mask'], mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, em.outputs[0], mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    xs = stations(XT, XN, LTP, LNP, 3, 5, 0.14)
    bm = loft(xs, half_section_coarse, 'wire')
    kill = []
    for f in bm.faces:
        c = f.calc_center_median()
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
print('internals built %.1fs' % (time.time() - T0))


# =====================================================================================================
# FX: cold-gas jets, frost mist
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

def mat_jet(name, core=False):
    m, nt, out = new_mat(name)
    m.surface_render_method = 'BLENDED'; m.show_transparent_back = True; m.use_transparency_overlap = True
    tc = node(nt, 'ShaderNodeTexCoord')
    sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
    z = sx.outputs['Z']
    zf = math_node(nt, 'POWER', math_node(nt, 'SUBTRACT', 1.0, math_node(nt, 'MINIMUM', z, 1.0)), 2.2 if core else 1.9)
    zin = node(nt, 'ShaderNodeMapRange', {'From Min': 0.0, 'From Max': 0.05}); lk(nt, z, zin.inputs['Value'])
    lw = node(nt, 'ShaderNodeLayerWeight', {'Blend': 0.5})
    edge = math_node(nt, 'POWER', math_node(nt, 'SUBTRACT', 1.0, lw.outputs['Facing']), 2.2 if core else 1.6)
    # turbulence scrolling downstream
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
    a = math_node(nt, 'MULTIPLY', a, nzr.outputs[0] if not core else 1.0)
    a = math_node(nt, 'MULTIPLY', a, at.outputs['Fac'])
    a = math_node(nt, 'MULTIPLY', a, 1.25 if core else 0.95, clamp_=True)
    tr = node(nt, 'ShaderNodeBsdfTransparent')
    if core:
        sh = node(nt, 'ShaderNodeEmission', {'Color': (0.75, 0.95, 1.0, 1), 'Strength': 7.0})
        so = sh.outputs[0]
    else:
        frost = principled(nt, **{'Base Color': (0.22, 0.25, 0.28, 1), 'Roughness': 1.0, 'Specular IOR Level': 0.0})
        em = node(nt, 'ShaderNodeEmission', {'Color': (0.78, 0.93, 1.0, 1)})
        lk(nt, math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', math_node(nt, 'POWER', math_node(nt, 'SUBTRACT', 1.0, math_node(nt, 'MINIMUM', z, 1.0)), 3.0), 2.4), 0.85), em.inputs['Strength'])
        ad = node(nt, 'ShaderNodeAddShader'); lk(nt, frost.outputs[0], ad.inputs[0]); lk(nt, em.outputs[0], ad.inputs[1])
        so = ad.outputs[0]
    mx = node(nt, 'ShaderNodeMixShader'); lk(nt, a, mx.inputs[0]); lk(nt, tr.outputs[0], mx.inputs[1]); lk(nt, so, mx.inputs[2])
    lk(nt, mx.outputs[0], out.inputs['Surface'])
    return m

def mat_mist(ring=False):
    m, nt, out = new_mat('mist_ring' if ring else 'mist')
    tc = node(nt, 'ShaderNodeTexCoord')
    if ring:
        sx = node(nt, 'ShaderNodeSeparateXYZ'); lk(nt, tc.outputs['Object'], sx.inputs[0])
        rxy = math_node(nt, 'SQRT', math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', sx.outputs['X'], sx.outputs['X']),
                                              math_node(nt, 'MULTIPLY', sx.outputs['Y'], sx.outputs['Y'])))
        dr = math_node(nt, 'SUBTRACT', rxy, 1.0)
        dz = math_node(nt, 'DIVIDE', sx.outputs['Z'], 0.9)
        d = math_node(nt, 'SQRT', math_node(nt, 'ADD', math_node(nt, 'MULTIPLY', dr, dr), math_node(nt, 'MULTIPLY', dz, dz)))
        fall = node(nt, 'ShaderNodeMapRange', {'From Min': 0.27, 'From Max': 0.04}, interpolation_type='SMOOTHSTEP')
    else:
        d = node(nt, 'ShaderNodeVectorMath', operation='LENGTH'); lk(nt, tc.outputs['Object'], d.inputs[0]); d = d.outputs['Value']
        fall = node(nt, 'ShaderNodeMapRange', {'From Min': 1.0, 'From Max': 0.15}, interpolation_type='SMOOTHSTEP')
    lk(nt, d, fall.inputs['Value'])
    clk = clock_out(nt)
    mp = node(nt, 'ShaderNodeMapping'); lk(nt, tc.outputs['Object'], mp.inputs['Vector'])
    mp.inputs['Scale'].default_value = (1.6, 1.6, 1.6) if not ring else (1.2, 1.2, 2.4)
    nz = node(nt, 'ShaderNodeTexNoise', {'Scale': 1.3, 'Detail': 3.0, 'Roughness': 0.55}, noise_dimensions='4D')
    lk(nt, mp.outputs[0], nz.inputs['Vector']); lk(nt, math_node(nt, 'MULTIPLY', clk, 0.45), nz.inputs['W'])
    nzr = node(nt, 'ShaderNodeMapRange', {'From Min': 0.3, 'From Max': 0.72, 'To Min': 0.05, 'To Max': 1.0})
    lk(nt, nz.outputs['Fac'], nzr.inputs['Value'])
    at = node(nt, 'ShaderNodeAttribute', attribute_type='OBJECT', attribute_name='fade')
    dens = math_node(nt, 'MULTIPLY', math_node(nt, 'MULTIPLY', fall.outputs[0], nzr.outputs[0]), at.outputs['Fac'])
    dens = math_node(nt, 'MULTIPLY', dens, 7.0 if not ring else 9.0)
    vol = node(nt, 'ShaderNodeVolumePrincipled', {'Color': (0.86, 0.94, 1.0, 1), 'Anisotropy': 0.25,
                                                 'Emission Color': (0.55, 0.85, 1.0, 1)})
    lk(nt, dens, vol.inputs['Density'])
    lk(nt, math_node(nt, 'MULTIPLY', dens, 0.035), vol.inputs['Emission Strength'])
    lk(nt, vol.outputs[0], out.inputs['Volume'])
    return m

M_JET = mat_jet('jet_plume'); M_JETCORE = mat_jet('jet_core', core=True); M_MIST = mat_mist(); M_MIST_RING = mat_mist(ring=True)
ME_PLUME = cone_mesh('plume', 0.034, 0.40, pw=0.62); ME_PLUME.materials.append(M_JET)
ME_CORE = cone_mesh('core', 0.020, 0.075, rings=12, seg=20); ME_CORE.materials.append(M_JETCORE)
JETS = []   # (kind, cid, plume_obj, core_obj)
for (cid, kind, e, c, d) in NOZZLES:
    po = link(bpy.data.objects.new('jet_%s_%s' % (cid, kind), ME_PLUME)); po.parent = e; po['fire'] = 0.0
    co = link(bpy.data.objects.new('jetcore_%s_%s' % (cid, kind), ME_CORE)); co.parent = e; co['fire'] = 0.0
    for o_ in (po, co): o_.visible_shadow = False; o_.location = (0, 0, 0.03)
    JETS.append((kind, cid, po, co, c, d))

def ico(name, subdiv=3):
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=1.0)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); me.shade_smooth(); me.materials.append(M_MIST)
    return me

ME_PUFF = ico('puff')
ringp = [(1.0 + 0.30 * cos(2 * pi * i / 16), 0.30 * sin(2 * pi * i / 16)) for i in range(16)]
bmr = lathe(ringp, 48, closed=True); bmesh.ops.rotate(bmr, verts=bmr.verts, cent=(0, 0, 0), matrix=Matrix.Rotation(pi / 2, 3, 'X'))
ME_RING = bpy.data.meshes.new('frost_ring'); recalc(bmr).to_mesh(ME_RING); bmr.free(); ME_RING.shade_smooth(); ME_RING.materials.append(M_MIST_RING)

def puff(name, me=ME_PUFF):
    ob = link(bpy.data.objects.new(name, me)); ob['fade'] = 0.0; ob.visible_shadow = False
    return ob
print('fx built %.1fs' % (time.time() - T0))


# =====================================================================================================
# ANIMATION: rig (hop, half-roll to inverted, roll-out, landing squash), x-ray scan
# =====================================================================================================
EASE_FALL = cubic_bezier(0.45, 0.0, 0.9, 0.45)
EASE_POP = cubic_bezier(0.2, 0.9, 0.3, 1.0)
F_FIRE, F_LIFT, F_APEX, F_LAND = 136, 140, 166, 184

root_z = keys_fn([(1, 0.0, None), (F_LIFT, 0.0, None), (158, 1.72, EASE_OUT), (F_APEX, 1.90, EASE_IO),
                  (F_LAND, 0.0, EASE_FALL), (189, 0.045, EASE_OUT), (194, 0.0, EASE_IN), (240, 0.0, None)])
roll_deg = keys_fn([(1, 0.0, None), (146, 0.0, None), (157, 180.0, cubic_bezier(0.55, 0.0, 0.2, 1.0)),
                    (166, 196.0, EASE_SOFT), (179, 360.0, cubic_bezier(0.5, 0.0, 0.3, 1.0)), (240, 360.0, None)])
pitch_deg = keys_fn([(1, 0.0, None), (138, 0.0, None), (144, 3.5, EASE_OUT), (156, 0.0, EASE_IO),
                     (F_LAND + 1, 0.0, None), (F_LAND + 3, -2.2, EASE_OUT), (192, 0.9, EASE_IO), (199, 0.0, EASE_IO)])
susp_dz = keys_fn([(1, 0.0, None), (133, 0.0, None), (137, -0.035, EASE_IO), (141, 0.018, EASE_OUT), (147, 0.0, EASE_IO),
                   (F_LAND, 0.0, None), (F_LAND + 3, -0.075, EASE_OUT), (192, 0.024, EASE_IO), (197, -0.008, EASE_IO),
                   (203, 0.0, EASE_IO)])
squash = keys_fn([(1, 0.0, None), (F_LAND, 0.0, None), (F_LAND + 2, 1.0, EASE_OUT), (193, 0.0, EASE_IO)])

bake_fn(ROOT, 'location', 2, root_z, -10, F_END + 10)
bake_fn(ROLL, 'rotation_euler', 0, lambda f: radians(roll_deg(f)), -10, F_END + 10)
bake_fn(ROLL, 'rotation_euler', 1, lambda f: radians(-pitch_deg(f)), -10, F_END + 10)
bake_fn(SUSP, 'location', 2, lambda f: 0.55 + susp_dz(f), -10, F_END + 10)
bake_fn(SUSP, 'scale', 2, lambda f: 1.0 - 0.016 * squash(f), -10, F_END + 10)
bake_fn(SUSP, 'scale', 0, lambda f: 1.0 + 0.006 * squash(f), -10, F_END + 10)
bake_fn(SUSP, 'scale', 1, lambda f: 1.0 + 0.006 * squash(f), -10, F_END + 10)
bake_fn(CONTACT, '["opacity"]', 0, lambda f: clamp(1.0 - root_z(f) / 1.4) ** 1.5, -10, F_END + 10)

SCAN_IN, SCAN_OUT = (76, 93), (121, 134)
thr = keys_fn([(1, 2.8, None), (SCAN_IN[0], 2.8, None), (SCAN_IN[1], -2.8, EASE_IO), (SCAN_OUT[0], -2.8, None),
               (SCAN_OUT[1], 2.8, EASE_IO), (240, 2.8, None)])
bake_fn(SCAN_G, 'nodes["thr"].outputs[0].default_value', 0, thr, -10, F_END + 10)

# ---------------- jets timeline ----------------
def pulse_env(f, a, b, rise=3, fall=5):
    if f <= a or f >= b + fall: return 0.0
    if f < a + rise: return EASE_OUT((f - a) / rise)
    if f <= b: return 1.0
    return 1.0 - EASE_IO((f - b) / fall)

def jet_fire(kind, cid, f):
    side = 1 if cid[1] == 'L' else -1
    v = 0.0
    if kind == 'down':
        v = max(v, pulse_env(f, F_FIRE, 149, 3, 5))
        v = max(v, 0.75 * pulse_env(f, 176, 183, 2, 5))
    elif kind == 'out':
        if side < 0: v = max(v, pulse_env(f, 144, 151, 2, 4))
        else: v = max(v, pulse_env(f, 165, 172, 2, 4))
    elif kind in ('fore', 'aft'):
        v = max(v, 0.7 * pulse_env(f, 145, 150, 2, 4))
        v = max(v, 0.6 * pulse_env(f, 166, 170, 2, 4))
    flick = 0.88 + 0.12 * mnoise.noise(Vector((f * 0.35, hash(cid + kind) % 97 * 0.37, 0.0)))
    return v * flick

def jet_len(kind, f, fire):
    if kind == 'down':
        reach = 0.32 + root_z(f) + 0.25
        return max(0.05, fire * min(1.9, max(0.6, reach)))
    return max(0.05, fire * (0.95 if kind == 'out' else 0.7))

for (kind, cid, po, co, c, d) in JETS:
    fr = list(range(-2, F_END + 4))
    fires = [jet_fire(kind, cid, f) for f in fr]
    lens_ = [jet_len(kind, f, fv) for f, fv in zip(fr, fires)]
    bake(po, '["fire"]', 0, fr, fires); bake(co, '["fire"]', 0, fr, fires)
    bake(po, 'scale', 2, fr, lens_); bake(co, 'scale', 2, fr, [l * 0.55 for l in lens_])
    widen = [0.75 + 0.35 * fv for fv in fires]
    for i in (0, 1):
        bake(po, 'scale', i, fr, widen); bake(co, 'scale', i, fr, widen)

# ---------------- frost: floor rings + puffs ----------------
def ring_anim(ob, f0, f1, r0, r1, peak, rise=4):
    fr = list(range(-2, F_END + 4))
    def k(f):
        t = clamp((f - f0) / (f1 - f0)); return t
    bake(ob, 'scale', 0, fr, [lerp(r0, r1, EASE_OUT(k(f))) if f >= f0 else 0.001 for f in fr])
    bake(ob, 'scale', 1, fr, [lerp(r0, r1, EASE_OUT(k(f))) if f >= f0 else 0.001 for f in fr])
    bake(ob, 'scale', 2, fr, [lerp(0.5, 1.6, EASE_OUT(k(f))) * (lerp(r0, r1, EASE_OUT(k(f))) ** 0.5) if f >= f0 else 0.001 for f in fr])
    bake(ob, '["fade"]', 0, fr, [0.0 if f < f0 else peak * min(1.0, (f - f0) / rise) * (1 - EASE_IO(k(f))) for f in fr])

R1 = puff('frost_ring_launch', ME_RING); R1.location = (0, 0, 0.06); ring_anim(R1, F_FIRE + 2, 182, 0.55, 3.4, 0.95)
R2 = puff('frost_ring_land', ME_RING); R2.location = (0, 0, 0.05); ring_anim(R2, F_LAND - 2, 236, 0.9, 3.0, 0.75)

def puff_anim(ob, base, f0, f1, s0, s1, peak, drift=(0, 0, 0.25), hold=1.0):
    fr = list(range(-2, F_END + 4))
    def t(f): return clamp((f - f0) / (f1 - f0))
    for i in range(3):
        bake(ob, 'location', i, fr, [base[i] + drift[i] * EASE_OUT(t(f)) for f in fr])
        bake(ob, 'scale', i, fr, [lerp(s0, s1, EASE_OUT(t(f))) * (1.0 if i < 2 else 0.7) if f >= f0 else 0.001 for f in fr])
    bake(ob, '["fade"]', 0, fr, [0.0 if f < f0 else peak * min(1.0, (f - f0) / 4.0) * (1 - hold * EASE_IO(t(f))) for f in fr])

PUFFS = []
for i, (cid, kind, e, c, d) in enumerate(NOZZLES):
    if kind == 'down':
        p = puff('puff_launch_%s' % cid); puff_anim(p, (c.x * 1.05, c.y * 1.25, 0.18), F_FIRE + 2, 178, 0.25, 1.15, 0.9,
                                                 drift=(c.x * 0.25, c.y * 0.9, 0.35))
        p2 = puff('puff_land_%s' % cid); puff_anim(p2, (c.x * 1.02, c.y * 1.15, 0.16), F_LAND - 6, 300, 0.25, 1.35, 0.85,
                                                  drift=(c.x * 0.2, c.y * 0.6, 0.45))
        PUFFS += [p, p2]
    elif kind == 'out':
        p3 = puff('puff_side_%s' % cid); puff_anim(p3, (c.x, c.y + (0.9 if c.y > 0 else -0.9), 0.55), (146 if c.y < 0 else 167), 320,
                                                  0.2, 1.1, 0.7, drift=(0.0, 0.5 if c.y > 0 else -0.5, 0.9))
        PUFFS.append(p3)
print('animation baked %.1fs' % (time.time() - T0))


# =====================================================================================================
# CAMERAS (16:9 = CAM_H, 9:16 = CAM_V), baked per frame with handheld noise + landing shake
# =====================================================================================================
EASE_WHIP = cubic_bezier(0.7, 0.0, 0.15, 1.0)
CAMKEYS = {
    'h': dict(
        az=[(1, 26, None), (72, 44, EASE_SOFT), (126, 76, EASE_IO), (136, 78, EASE_SOFT), (151, 30, EASE_WHIP), (200, 22, EASE_SOFT), (240, 19, EASE_SOFT)],
        el=[(1, 5.0, None), (72, 8.0, EASE_SOFT), (126, 25, EASE_IO), (136, 26, EASE_SOFT), (151, 2.5, EASE_WHIP), (172, 5.5, EASE_SOFT), (204, 6.0, EASE_SOFT), (240, 5.2, EASE_SOFT)],
        dist=[(1, 6.5, None), (72, 5.6, EASE_SOFT), (126, 7.2, EASE_IO), (136, 7.4, EASE_SOFT), (151, 7.7, EASE_WHIP), (184, 7.5, EASE_SOFT), (206, 6.9, EASE_SOFT), (240, 6.55, EASE_SOFT)],
        tx=[(1, 0.20, None), (72, 0.05, EASE_SOFT), (126, -0.25, EASE_IO), (151, 0.0, EASE_WHIP), (240, 0.15, EASE_SOFT)],
        lens=[(1, 50, None), (72, 52, EASE_SOFT), (126, 44, EASE_IO), (136, 44, None), (151, 36, EASE_WHIP), (186, 36, None), (206, 38, EASE_SOFT), (240, 39, EASE_SOFT)],
        shx=[(1, 0.0, None), (198, 0.0, None), (214, -0.14, EASE_SOFT), (240, -0.145, None)],
        shy=[(1, 0.0, None), (240, 0.0, None)],
        roll=[(1, 0.0, None), (142, 0.0, None), (153, -6.0, EASE_OUT), (167, 4.0, EASE_IO), (184, 0.0, EASE_IO), (240, 0.0, None)],
        fstop=[(1, 2.4, None), (72, 2.4, None), (92, 8.0, EASE_IO), (134, 8.0, None), (150, 6.3, EASE_IO), (190, 6.3, None), (210, 2.8, EASE_IO), (240, 2.8, None)],
    ),
    'v': dict(
        az=[(1, 28, None), (72, 44, EASE_SOFT), (126, 74, EASE_IO), (136, 76, EASE_SOFT), (151, 30, EASE_WHIP), (200, 22, EASE_SOFT), (240, 19, EASE_SOFT)],
        el=[(1, 7.0, None), (72, 10.0, EASE_SOFT), (126, 28, EASE_IO), (136, 29, EASE_SOFT), (151, 4.0, EASE_WHIP), (172, 6.5, EASE_SOFT), (204, 8.0, EASE_SOFT), (240, 7.5, EASE_SOFT)],
        dist=[(1, 6.6, None), (72, 5.9, EASE_SOFT), (126, 7.4, EASE_IO), (136, 7.6, EASE_SOFT), (151, 7.3, EASE_WHIP), (184, 7.2, EASE_SOFT), (206, 6.8, EASE_SOFT), (240, 6.5, EASE_SOFT)],
        tx=[(1, 0.15, None), (72, 0.05, EASE_SOFT), (126, -0.25, EASE_IO), (151, 0.0, EASE_WHIP), (240, 0.05, EASE_SOFT)],
        lens=[(1, 44, None), (72, 46, EASE_SOFT), (126, 40, EASE_IO), (136, 40, None), (151, 39, EASE_WHIP), (186, 39, None), (206, 40, EASE_SOFT), (240, 41, EASE_SOFT)],
        shx=[(1, 0.0, None), (240, 0.0, None)],
        shy=[(1, 0.10, None), (72, 0.10, None), (126, 0.16, EASE_IO), (136, 0.16, None), (151, 0.04, EASE_WHIP), (198, 0.04, None), (214, 0.17, EASE_SOFT), (240, 0.175, None)],
        roll=[(1, 0.0, None), (142, 0.0, None), (153, -5.0, EASE_OUT), (167, 3.5, EASE_IO), (184, 0.0, EASE_IO), (240, 0.0, None)],
        fstop=[(1, 2.8, None), (72, 2.8, None), (92, 8.0, EASE_IO), (134, 8.0, None), (150, 7.0, EASE_IO), (190, 7.0, None), (210, 3.2, EASE_IO), (240, 3.2, None)],
    ),
}

def car_center(f):
    return Vector((0.0, 0.0, 0.55 + root_z(f)))

def bake_camera(name, keys, sensor_fit='AUTO'):
    cam = make_cam(name, 50)
    cam.data.sensor_fit = sensor_fit
    K = {k: keys_fn(v) for k, v in keys.items()}
    fr = list(range(-4, F_END + 6))
    L = [[], [], []]; R = [[], [], []]; foc = []; lens = []; shx = []; shy = []; fst = []
    prev = None
    for f in fr:
        t = sec(f)
        tz = 0.50 + 0.88 * root_z(f - 2)
        tgt = Vector((K['tx'](f), 0.0, tz))
        eye = Vector(orbit_eye(K['az'](f), K['el'](f), K['dist'](f), tgt))
        eye += Vector((mnoise.noise(Vector((t * 0.42, 1.3, 0.0))), mnoise.noise(Vector((t * 0.42, 7.1, 2.0))),
                       mnoise.noise(Vector((t * 0.42, 3.7, 5.0))))) * 0.014
        q = (tgt - eye).normalized().to_track_quat('-Z', 'Y')
        hp = 0.22 * mnoise.noise(Vector((t * 0.55, 11.0, 0.0))); hy = 0.22 * mnoise.noise(Vector((t * 0.55, 17.0, 0.0)))
        hr = 0.12 * mnoise.noise(Vector((t * 0.5, 23.0, 0.0)))
        sk = 0.0
        if f > F_LAND:
            sk = 1.1 * exp(-(f - F_LAND) / 4.5) * sin(2 * pi * (f - F_LAND) / 4.4)
        if F_FIRE <= f <= F_FIRE + 10:
            sk += 0.35 * exp(-(f - F_FIRE) / 3.0) * sin(2 * pi * (f - F_FIRE) / 3.1)
        q = q @ Euler((radians(hp + sk), radians(hy), radians(K['roll'](f) + hr + 0.4 * sk)), 'XYZ').to_quaternion()
        e = q.to_euler('XYZ', prev) if prev is not None else q.to_euler('XYZ'); prev = e
        for i in range(3): L[i].append(eye[i]); R[i].append(e[i])
        foc.append((car_center(f) - eye).length - 0.6)
        lens.append(K['lens'](f)); shx.append(K['shx'](f)); shy.append(K['shy'](f)); fst.append(K['fstop'](f))
    for i in range(3):
        bake(cam, 'location', i, fr, L[i]); bake(cam, 'rotation_euler', i, fr, R[i])
    bake(cam.data, 'lens', 0, fr, lens); bake(cam.data, 'shift_x', 0, fr, shx); bake(cam.data, 'shift_y', 0, fr, shy)
    bake(cam.data, 'dof.focus_distance', 0, fr, foc); bake(cam.data, 'dof.aperture_fstop', 0, fr, fst)
    return cam

CAM_H = bake_camera('CAM_H', CAMKEYS['h'])
CAM_V = bake_camera('CAM_V', CAMKEYS['v'], sensor_fit='HORIZONTAL')
ACTIVE_CAM = CAM_V if A.cam == 'v' else CAM_H
SC.camera = ACTIVE_CAM
print('cameras baked %.1fs' % (time.time() - T0))


# =====================================================================================================
# TYPE: 3D label (x-ray) and end card
# =====================================================================================================
FONT_PATH = '/System/Library/Fonts/Supplemental/Arial Black.ttf'
FONT = bpy.data.fonts.load(FONT_PATH) if os.path.exists(FONT_PATH) else None

def text_obj(name, body, size, extrude, mat, bevel=0.0, spacing=1.0):
    cu = bpy.data.curves.new(name, 'FONT'); cu.body = body
    if FONT: cu.font = FONT
    cu.size = size; cu.extrude = extrude; cu.bevel_depth = bevel; cu.bevel_resolution = 2
    cu.align_x = 'CENTER'; cu.align_y = 'CENTER'; cu.space_character = spacing; cu.space_line = 0.82
    cu.materials.append(mat)
    return link(bpy.data.objects.new(name, cu))

M_LABEL = mat_simple('label_white', (0.05, 0.05, 0.05), 0.4, emission=(1.0, 1.0, 1.0), estr=0.95, spec=0.2)
M_LEADER = mat_simple('leader', (0.05, 0.05, 0.05), 0.4, emission=(0.55, 0.92, 1.0), estr=1.0, spec=0.2)
M_CARD = mat_simple('card_yellow', (0.30, 0.18, 0.0), 0.38, coat=0.3, emission=(1.0, 0.70, 0.015), estr=0.78)
M_CARDTXT = mat_simple('card_text', (0.010, 0.010, 0.012), 0.6, spec=0.2)

def cam_frame(cam, f):
    SC.frame_set(f)
    return cam.matrix_world.copy()

def spring_anim(ob, f0, base_scale, freq=2.1, damp=0.4, out=None, rot_from=None, rot_base=None):
    fr = list(range(-2, F_END + 4))
    def s(f):
        v = spring(sec(f) - sec(f0), freq, damp)
        if out is not None and f >= out[0]:
            v *= 1.0 - EASE_IN(clamp((f - out[0]) / (out[1] - out[0])))
        return max(0.001, v)
    for i in range(3):
        bake(ob, 'scale', i, fr, [base_scale * s(f) for f in fr])
    if rot_from is not None:
        for i in range(3):
            bake(ob, 'rotation_euler', i, fr, [rot_base[i] + (rot_from[i] - rot_base[i]) * (1 - spring(sec(f) - sec(f0), freq * 0.8, damp + 0.05)) for f in fr])

# ---- x-ray label: callout rising from the mid-left thruster cluster, underline draws outward ----
LBL_F0, LBL_OUT = 102, (121, 126)
lbl_pos = Vector((-0.20, 1.02, 1.86)) if A.cam != 'v' else Vector((-0.25, 0.60, 2.05))
mw = cam_frame(ACTIVE_CAM, 112)
cam_right = (mw.to_quaternion() @ Vector((1, 0, 0))); cam_right.z = 0; cam_right.normalize()
LABEL = text_obj('label', 'COLD-GAS THRUSTERS', 0.23 if A.cam != 'v' else 0.27, 0.016, M_LABEL, bevel=0.0022)
LABEL.location = lbl_pos
tc_ = LABEL.constraints.new('TRACK_TO'); tc_.target = ACTIVE_CAM; tc_.track_axis = 'TRACK_Z'; tc_.up_axis = 'UP_Y'
spring_anim(LABEL, LBL_F0, 1.0, freq=2.3, damp=0.38, out=LBL_OUT)
noz_ml = [n for n in NOZZLES if n[0] == 'ML'][0][3]
half_w = 1.47 if A.cam != 'v' else 1.70
uz = -0.205 if A.cam != 'v' else -0.235
p_ul = lbl_pos - cam_right * half_w + Vector((0, 0, uz))
p_ur = lbl_pos + cam_right * half_w + Vector((0, 0, uz))
p0 = Vector(noz_ml) + Vector((0, 0.12, 0.0))
dv = p_ur - p_ul
u0 = clamp((p0 - p_ul).dot(dv) / dv.length_squared, 0.08, 0.92)
p1 = p_ul + dv * u0
fr = list(range(-2, F_END + 4))
leader = curve_obj('leader', [tuple(p0), tuple(p1)], 0.0068, M_LEADER, None, res=3)
bake(leader.data, 'bevel_factor_end', 0, fr, [EASE_IO(clamp((f - 94) / 8.0)) for f in fr])
bake(leader.data, 'bevel_factor_start', 0, fr, [EASE_IN(clamp((f - LBL_OUT[0]) / 6.0)) for f in fr])
uline = curve_obj('underline', [tuple(p_ul), tuple(p_ur)], 0.0068, M_LEADER, None, res=3)
bake(uline.data, 'bevel_factor_start', 0, fr, [u0 * (1 - EASE_OUT(clamp((f - 101) / 8.0))) + u0 * EASE_IN(clamp((f - LBL_OUT[0]) / 6.0)) for f in fr])
bake(uline.data, 'bevel_factor_end', 0, fr, [u0 + (1 - u0) * EASE_OUT(clamp((f - 101) / 8.0)) - (1 - u0) * EASE_IN(clamp((f - LBL_OUT[0]) / 6.0)) for f in fr])
dot = bmesh.new(); bmesh.ops.create_uvsphere(dot, u_segments=16, v_segments=8, radius=0.026)
DOT = mesh_obj('leader_dot', dot, mats=[M_LEADER]); DOT.location = p0
for i in range(3):
    bake(DOT, 'scale', i, fr, [max(0.001, spring(sec(f) - sec(92), 3.0, 0.4) * (1 - EASE_IN(clamp((f - LBL_OUT[0]) / 5.0)))) for f in fr])

# ---- end card "UPSIDE DOWN?" ----
CARD_F0 = 207
def rounded_rect(w, h, r, seg=8):
    pts = []
    for (cx, cy, a0) in ((w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)):
        for k in range(seg + 1):
            a = radians(a0 + 90 * k / seg); pts.append((cx + r * cos(a), cy + r * sin(a)))
    return pts

def build_card(name, w, h, txt_size, depth=0.075):
    root = empty(name)
    pts = rounded_rect(w, h, 0.12)
    bm = bmesh.new()
    bot = [bm.verts.new((x, y, -depth)) for (x, y) in pts]; top = [bm.verts.new((x, y, 0.0)) for (x, y) in pts]
    bm.faces.new(bot[::-1]); bm.faces.new(top)
    for i in range(len(pts)):
        j = (i + 1) % len(pts); bm.faces.new((bot[i], bot[j], top[j], top[i]))
    recalc(bm)
    slab = mesh_obj(name + '_slab', bm, mats=[M_CARD], smooth=False); add_bevel(slab, 0.018, 4, 30)
    slab.parent = root
    t = text_obj(name + '_txt', 'UPSIDE\nDOWN?', txt_size, 0.022, M_CARDTXT, bevel=0.003, spacing=0.98)
    t.parent = root; t.location = (0, -0.01 * txt_size, 0.012)
    return root

def place_card(card, cam, f, right, up, depth, yaw, roll):
    mw = cam_frame(cam, f)
    q = mw.to_quaternion()
    pos = mw.translation + q @ Vector((right, up, -depth))
    card.location = pos
    base = q @ Quaternion((0, 1, 0), radians(yaw)) @ Quaternion((0, 0, 1), radians(roll))
    return base

if A.cam == 'v':
    CARD = build_card('card', 2.35, 1.38, 0.52)
    base_q = place_card(CARD, CAM_V, 236, -0.05, 1.45, 6.2, 12.0, -4.0)
else:
    CARD = build_card('card', 1.95, 1.15, 0.44)
    base_q = place_card(CARD, CAM_H, 236, -1.98, 0.86, 6.3, 16.0, -5.0)
CARD.rotation_mode = 'XYZ'
be = base_q.to_euler('XYZ')
fr = list(range(-2, F_END + 4))
def card_s(f): return max(0.001, spring(sec(f) - sec(CARD_F0), 1.7, 0.42))
for i in range(3):
    bake(CARD, 'scale', i, fr, [card_s(f) for f in fr])
from_q = base_q @ Quaternion((0, 0, 1), radians(-24)) @ Quaternion((1, 0, 0), radians(30))
fe = from_q.to_euler('XYZ', be)
for i in range(3):
    bake(CARD, 'rotation_euler', i, fr, [be[i] + (fe[i] - be[i]) * (1 - spring(sec(f) - sec(CARD_F0), 1.35, 0.48)) for f in fr])
cl = CARD.location.copy()
bake(CARD, 'location', 2, fr, [cl.z + 0.025 * sin(2 * pi * 0.45 * sec(f)) for f in fr])
print('type built %.1fs' % (time.time() - T0))


# =====================================================================================================
# COMPOSITOR: bloom + a touch of lens dispersion
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
if A.cam == 'v':
    set_res(1080, 1920, A.pct)
else:
    set_res(1920, 1080, A.pct)
if A.save:
    bpy.ops.wm.save_as_mainfile(filepath=A.save)

if A.mode == 'sheet':
    os.makedirs(A.out, exist_ok=True)
    for f in [int(v) for v in A.frames.split(',')]:
        SC.frame_set(f)
        t = time.time()
        render_still(os.path.join(A.out, 'sheet_%s_%04d.png' % (A.cam, f)))
        print('frame %d %.1fs' % (f, time.time() - t))
elif A.mode == 'anim':
    od = os.path.join(A.out, A.cam)
    os.makedirs(od, exist_ok=True)
    SC.frame_start, SC.frame_end = A.start, A.end
    SC.render.filepath = os.path.join(od, '')
    t = time.time()
    bpy.ops.render.render(animation=True)
    print('anim %s frames %d-%d in %.1fs' % (A.cam, A.start, A.end, time.time() - t))
print('total %.1fs' % (time.time() - T0))
