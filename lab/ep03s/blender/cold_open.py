"""The EP03 cold open in Blender (bpy 4.2, Cycles on CPU): the same beats as ep03s.py, as physical objects.

  1848 in brushed chrome -> a glass bottle heaped with gold -> the gold bursts out -> the store (steel pans, three
  shovels) -> $36,000 in chrome over a model street -> one clean shovel in untouched sand -> a push into its grip ->
  the prize, a single turquoise light in the dark.

Rendered at 960x540, 12 fps (then smoothed to 30 fps and upscaled by build_blender.sh), 16 samples + denoise.

    python3 blender/cold_open.py            # build/blender/frame_####.png
    python3 blender/cold_open.py 40 120     # just those frames
    python3 blender/cold_open.py --inbetweens   # build/blender24/####.png: real 24 fps in-betweens for the fast shots
"""
import json
import math
import os
import random
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.join(HERE, "..")
OUT = os.path.join(EP, "build", "blender")
FONT = os.path.join(EP, "..", "..", "a01_v6", "fonts", "Michroma-400.ttf")
FPS = 12
L = json.load(open(os.path.join(EP, "build", "lines.json")))["lines"]


def ls(name):
    return next(x for x in L if x.get("id") == name or x.get("slot") == name)["start"]


def le(name):
    return next(x for x in L if x.get("id") == name or x.get("slot") == name)["end"]


T_BOTTLE = ls("bottle") + 0.55 * (le("bottle") - ls("bottle"))
T_MIND, T_SHOP, T_36, T_NEVER, T_RULE = ls("mind"), ls("shop"), ls("36k"), ls("never"), ls("rule")
T_END = T_RULE + 2.4
SHOTS = [(0.0, T_BOTTLE, "s1848"), (T_BOTTLE, T_MIND, "bottle"), (T_MIND, T_SHOP, "burst"), (T_SHOP, T_36, "shop"),
         (T_36, T_NEVER, "money"), (T_NEVER, T_RULE, "shovel"), (T_RULE, T_END, "prize")]
random.seed(5)


# ---------------------------------------------------------------- materials
def mat(name, base, metal=0.0, rough=0.5, trans=0.0, emit=None, strength=0.0, aniso=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*base, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    b.inputs["Transmission Weight"].default_value = trans
    if aniso:
        b.inputs["Anisotropic"].default_value = aniso
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    return m


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 16
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 6
    sc.cycles.transparent_max_bounces = 8
    sc.render.resolution_x, sc.render.resolution_y = 960, 540
    sc.render.fps = FPS
    sc.render.image_settings.file_format = "PNG"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes["Background"]; bg.inputs[1].default_value = 1.0
    grad = nt.nodes.new("ShaderNodeTexGradient"); coord = nt.nodes.new("ShaderNodeTexCoord"); ramp = nt.nodes.new("ShaderNodeValToRGB")
    mapn = nt.nodes.new("ShaderNodeMapping"); mapn.inputs["Rotation"].default_value = (0, math.radians(90), 0)
    nt.links.new(coord.outputs["Generated"], mapn.inputs[0]); nt.links.new(mapn.outputs[0], grad.inputs[0])
    nt.links.new(grad.outputs[0], ramp.inputs[0]); nt.links.new(ramp.outputs[0], bg.inputs[0])
    ramp.color_ramp.elements[0].color = (0.002, 0.003, 0.004, 1)
    ramp.color_ramp.elements[1].color = (0.03, 0.05, 0.055, 1)                  # a faint teal sky for chrome to reflect

    M = dict(
        chrome=mat("chrome", (0.92, 0.94, 0.95), 1.0, 0.11, aniso=0.4),
        gold=mat("gold", (1.0, 0.74, 0.30), 1.0, 0.24),
        glass=mat("glass", (0.95, 0.98, 1.0), 0.0, 0.02, trans=1.0),
        steel=mat("steel", (0.55, 0.58, 0.62), 1.0, 0.32),
        wood=mat("wood", (0.18, 0.11, 0.06), 0.0, 0.55),
        sand=mat("sand", (0.40, 0.29, 0.17), 0.0, 0.9),
        floor=mat("floor", (0.02, 0.022, 0.025), 0.0, 0.22),
        house=mat("house", (0.62, 0.58, 0.52), 0.0, 0.6),
        sold=mat("sold", (0.02, 0.4, 0.37), 0.0, 0.4, emit=(0.07, 0.72, 0.67), strength=4.0),
        prize=mat("prize", (0.07, 0.72, 0.67), 0.0, 0.3, emit=(0.25, 0.9, 0.85), strength=9.0),
    )
    font = bpy.data.fonts.load(FONT)

    def coll(name):
        c = bpy.data.collections.new(name); sc.collection.children.link(c); return c

    def text(body, size, coll_, loc, m):
        cu = bpy.data.curves.new(body, "FONT"); cu.body = body; cu.font = font; cu.size = size
        cu.extrude = 0.06 * size; cu.bevel_depth = 0.012 * size; cu.align_x = "CENTER"; cu.align_y = "CENTER"
        o = bpy.data.objects.new(body, cu); o.location = loc; o.rotation_euler = (math.radians(90), 0, 0)
        cu.materials.append(m); coll_.objects.link(o); return o

    def link_new(obj, c):
        for u in list(obj.users_collection):
            u.objects.unlink(obj)
        c.objects.link(obj)
        return obj

    # a dark glossy floor under everything
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 0, -1.0)); fl = bpy.context.object; fl.data.materials.append(M["floor"])
    fl.name = "floor"

    # 1 · 1848
    c1 = coll("s1848")
    text("1848", 1.0, c1, (0, 0, 0.1), M["chrome"])
    # 2-3 · the bottle and its gold
    c2 = coll("bottle")
    prof = [(0.0, -1.0), (0.42, -1.0), (0.46, -0.95), (0.46, 0.25), (0.40, 0.42), (0.16, 0.55), (0.12, 0.62), (0.12, 0.95), (0.14, 1.0)]
    me = bpy.data.meshes.new("bottle")
    verts, faces = [], []
    seg_n = 48
    for j in range(seg_n):
        a = 2 * math.pi * j / seg_n
        for r, z in prof:
            verts.append((r * math.cos(a), r * math.sin(a), z))
    npf = len(prof)
    for j in range(seg_n):
        for k in range(npf - 1):
            a0 = j * npf + k; a1 = ((j + 1) % seg_n) * npf + k
            faces.append((a0, a1, a1 + 1, a0 + 1))
    me.from_pydata(verts, [], faces); me.update()
    bo = bpy.data.objects.new("bottle", me); bo.location = (0, 0, 0.0); c2.objects.link(bo)
    sol = bo.modifiers.new("s", "SOLIDIFY"); sol.thickness = 0.02
    sub = bo.modifiers.new("sub", "SUBSURF"); sub.levels = 1; sub.render_levels = 1
    for p in bo.data.polygons:
        p.use_smooth = True
    bo.data.materials.append(M["glass"])
    cork = bpy.data.meshes.new("cork")
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=0.18, location=(0, 0, 1.08)); ck = bpy.context.object; link_new(ck, c2)
    ck.data.materials.append(mat("cork", (0.35, 0.24, 0.14), 0.0, 0.7))
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.022); grain = bpy.context.object; grain.data.materials.append(M["gold"])
    link_new(grain, c2); grain.hide_render = True; grain.hide_viewport = True
    grains = []
    for i in range(420):
        r = 0.4 * math.sqrt(random.random()); a = random.uniform(0, 2 * math.pi)
        home = Vector((r * math.cos(a), r * math.sin(a), -0.97 + random.random() ** 2 * (0.5 - 0.6 * r)))
        g = grain.copy(); g.hide_render = False; g.hide_viewport = False; g.location = home; c2.objects.link(g)
        out = Vector((random.gauss(0, 1.0), random.gauss(0, 0.6), random.uniform(1.5, 3.2)))
        grains.append((g, home, out, random.uniform(0, 0.35)))
    # 4 · the store
    c4 = coll("shop")
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.1, -0.2)); sh = bpy.context.object; sh.scale = (3.2, 0.5, 0.06); link_new(sh, c4); sh.data.materials.append(M["wood"])
    for j, x in enumerate((-1.1, -0.35, 0.4)):
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=0.2, radius2=0.34, depth=0.1, location=(x, 0.1, -0.12), end_fill_type="NOTHING")
        pn = bpy.context.object; link_new(pn, c4); pn.data.materials.append(M["steel"])
        pn.modifiers.new("s", "SOLIDIFY").thickness = 0.012
        pn.rotation_euler = (math.radians(12), 0, 0)
    shovel_parts = []

    def shovel(c_, loc, tilt=0.0, scale=1.0):
        parts = []
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); bl = bpy.context.object
        for v in bl.data.vertices:                           # taper to a spade: the cutting edge is narrower
            if v.co.z < 0:
                v.co.x *= 0.62
        bl.scale = (0.16 * scale, 0.012 * scale, 0.22 * scale); link_new(bl, c_); bl.data.materials.append(M["steel"])
        bev = bl.modifiers.new("b", "BEVEL"); bev.width = 0.03 * scale; bev.segments = 4
        bpy.ops.mesh.primitive_cylinder_add(radius=0.022 * scale, depth=1.1 * scale, location=(0, 0, 0.72 * scale)); hd = bpy.context.object
        link_new(hd, c_); hd.data.materials.append(M["wood"])
        bpy.ops.mesh.primitive_torus_add(major_radius=0.09 * scale, minor_radius=0.018 * scale, location=(0, 0, 1.36 * scale), rotation=(math.radians(90), 0, 0))
        gp = bpy.context.object; link_new(gp, c_); gp.data.materials.append(M["chrome"])
        root = bpy.data.objects.new("shovel_root", None); c_.objects.link(root)
        for o in (bl, hd, gp):
            o.parent = root
        root.location = loc; root.rotation_euler = (0, math.radians(tilt), 0)
        return root
    for j, x in enumerate((1.25, 1.65, 2.05)):
        shovel(c4, (x, 0.45, -0.98), tilt=(-8, 0, 8)[j], scale=1.25)
    # 5 · $36,000 over a model street
    c5 = coll("money")
    text("$36,000", 0.62, c5, (0, 0, 0.75), M["chrome"])
    sold_tags = []
    for j in range(7):
        x = -1.8 + j * 0.6
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.6, -0.8)); hb = bpy.context.object; hb.scale = (0.34, 0.3, 0.38); link_new(hb, c5)
        hb.data.materials.append(M["house"])
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0.27, depth=0.22, location=(x, 0.6, -0.5), rotation=(0, 0, math.radians(45)))
        rf = bpy.context.object; link_new(rf, c5); rf.scale = (1.0, 0.85, 1.0); rf.data.materials.append(mat("roof", (0.12, 0.13, 0.15), 0.2, 0.5))
        bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 0.43, -0.72)); tg = bpy.context.object; tg.scale = (0.24, 0.02, 0.08); link_new(tg, c5)
        tg.data.materials.append(M["sold"]); sold_tags.append(tg)
    # 6 · the shovel in the sand
    c6 = coll("shovel")
    # a wide dune field (dense grid, displaced upward only, so the dark floor never shows through), running out to
    # the horizon; the floor and the studio lights are switched off for this shot, a low warm sun does the work
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=320, y_subdivisions=320, size=40, location=(0, 0, -1.02)); sd = bpy.context.object
    link_new(sd, c6)
    tex = bpy.data.textures.new("dune", "CLOUDS"); tex.noise_scale = 2.4; tex.noise_depth = 1
    dsp = sd.modifiers.new("d", "DISPLACE"); dsp.texture = tex; dsp.strength = 0.42; dsp.mid_level = 0.0
    rip = bpy.data.textures.new("ripple", "WOOD"); rip.wood_type = "BANDNOISE"; rip.noise_scale = 0.08; rip.turbulence = 4.0
    dr = sd.modifiers.new("r", "DISPLACE"); dr.texture = rip; dr.strength = 0.012; dr.mid_level = 0.5
    sd.data.materials.append(M["sand"])
    for p in sd.data.polygons:
        p.use_smooth = True
    deps = bpy.context.evaluated_depsgraph_get(); ev = sd.evaluated_get(deps); em = ev.to_mesh()
    z_sand = min(((v.co.x ** 2 + v.co.y ** 2), (ev.matrix_world @ v.co).z) for v in em.vertices)[1]
    ev.to_mesh_clear()
    z_root = z_sand - 0.06
    big = shovel(c6, (0, 0, z_root), 0.0, 1.35)
    Ls = bpy.data.lights.new("sun_low", "SUN"); Ls.energy = 5.0; Ls.color = (1.0, 0.8, 0.6); Ls.angle = math.radians(3)
    so = bpy.data.objects.new("sun_low", Ls); so.rotation_euler = (math.radians(79), 0, math.radians(-58)); c6.objects.link(so)
    # 7 · the prize
    c7 = coll("prize")
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, location=(0, 0, 0.1)); pz = bpy.context.object; link_new(pz, c7); pz.data.materials.append(M["prize"])

    # lights and camera
    rig = {}
    for name, loc, energy, col, size in (("key", (3, -3.5, 3), 700, (1.0, 0.88, 0.76), 2.5), ("rim", (-3.5, 2.5, 1.6), 1100, (0.07, 0.72, 0.67), 2.0),
                                         ("fill", (0.5, -4.5, -0.3), 120, (0.55, 0.65, 0.85), 4.0), ("top", (0, 0, 4.5), 200, (1, 1, 1), 5.0)):
        Ld = bpy.data.lights.new(name, "AREA"); Ld.energy = energy; Ld.color = col; Ld.size = size
        o = bpy.data.objects.new(name, Ld); o.location = loc; sc.collection.objects.link(o)
        tgt = bpy.data.objects.new("t_" + name, None); sc.collection.objects.link(tgt)
        cst = o.constraints.new("TRACK_TO"); cst.target = tgt; cst.track_axis = "TRACK_NEGATIVE_Z"; cst.up_axis = "UP_Y"
        rig[name] = o
    cam = bpy.data.cameras.new("cam"); cam.lens = 45; cam.dof.use_dof = True; cam.dof.aperture_fstop = 2.8
    co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
    aim = bpy.data.objects.new("aim", None); sc.collection.objects.link(aim)
    cst = co.constraints.new("TRACK_TO"); cst.target = aim; cst.track_axis = "TRACK_NEGATIVE_Z"; cst.up_axis = "UP_Y"
    cam.dof.focus_object = aim
    return dict(sc=sc, rig=rig, floor=fl, grip=Vector((0, 0, z_root + 1.36 * 1.35)), z_root=z_root, cols={s[2]: bpy.data.collections[s[2]] for s in SHOTS if s[2] in bpy.data.collections}, cam=co, aim=aim, grains=grains, sold=sold_tags, big=big, prize=pz)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


def pose(W, t):
    """Put everything where it is at time t (seconds)."""
    shot = next((s for s in SHOTS if s[0] <= t < s[1]), SHOTS[-1])
    for name, c in W["cols"].items():
        vis = name == shot[2] or (shot[2] == "burst" and name == "bottle")
        c.hide_render = not vis
    sand = shot[2] == "shovel"                               # the dune shot is lit by the low sun alone
    W["floor"].hide_render = sand
    for k in ("key", "top", "fill"):
        W["rig"][k].hide_render = sand
    W["rig"]["rim"].data.energy = 140 if sand else 1100
    cam, aim = W["cam"], W["aim"]
    u = (t - shot[0]) / max(0.01, shot[1] - shot[0])
    name = shot[2]
    if name == "s1848":
        cam.location = (0.7 - 0.6 * u, -3.4 + 0.7 * ease(u), 0.3 + 0.15 * u); aim.location = (0, 0, 0.12)
    elif name in ("bottle", "burst"):
        a = math.radians(-20 + 35 * u)
        d = 4.6 if name == "bottle" else 5.6
        cam.location = (d * math.sin(a), -d * math.cos(a), 0.15 + (0.5 * u if name == "burst" else 0)); aim.location = (0, 0, -0.1 + (0.6 * u if name == "burst" else 0))
        for g, home, out, delay in W["grains"]:
            if name == "burst":
                k = ease((u - delay) / 0.6)
                g.location = home.lerp(home + out, k) + Vector((0, 0, -1.6 * k * k)) + Vector((0, 0, 1.3 * math.sin(math.pi * k)))
            else:
                g.location = home
    elif name == "shop":
        cam.location = (-1.4 + 2.2 * ease(u), -4.4, 0.35); aim.location = (-0.3 + 1.2 * ease(u), 0.2, -0.45)
    elif name == "money":
        cam.location = (0, -6.2 + 0.9 * (1 - ease(u)), 0.5 - 0.3 * ease(u)); aim.location = (0, 0, 0.35 - 0.7 * ease(u))
        e2 = ls("e2") + 0.62 * (le("e2") - ls("e2"))
        for j, tg in enumerate(W["sold"]):
            tg.hide_render = t < e2 + j * 0.14
    elif name == "shovel":
        tl = ls("never") + 0.72 * (le("never") - ls("never"))
        W["big"].rotation_euler = (0, math.radians(-26 * ease((t - tl) / 0.35)), 0)
        push = ease((t - le("never") - 0.1) / max(0.1, T_RULE - le("never") - 0.1))
        grip = W["grip"]
        cam.location = Vector((2.0, -6.0, W["z_root"] + 0.35)).lerp(grip + Vector((0, -0.05, 0)), push ** 2)
        aim.location = Vector((0, 0, W["z_root"] + 0.8)).lerp(grip, min(1.0, push * 2))
    else:
        cam.location = (0, -3.0, 0.1); aim.location = (0, 0, 0.1)
        W["prize"].scale = (1, 1, 1)


def shot_at(t):
    return next((s for s in SHOTS if s[0] <= t < s[1]), SHOTS[-1])[2]


def inbetweens():
    """24 fps frame numbers worth rendering for real (the rest are motion-interpolated from the 12 fps frames):
    every in-between of the fast shots (the gold burst, the shovel and the push into its grip), plus the one
    in-between at each cut, which interpolation would smear across two shots."""
    out = []
    for n in range(1, int(T_END * 24), 2):
        t, t0, t1 = n / 24, (n - 1) / 24, (n + 1) / 24
        if shot_at(t) in ("burst", "shovel") or shot_at(t0) != shot_at(t1):
            out.append(n)
    return out


def render_inbetweens():
    W = build()
    out24 = os.path.join(EP, "build", "blender24")
    os.makedirs(out24, exist_ok=True)
    todo = inbetweens()
    for i, n in enumerate(todo):
        pose(W, n / 24)
        W["sc"].render.filepath = os.path.join(out24, f"{n:04d}.png")
        bpy.ops.render.render(write_still=True)
        print("inbetween", n, f"({i + 1}/{len(todo)})", flush=True)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--inbetweens":
        return render_inbetweens()
    W = build()
    os.makedirs(OUT, exist_ok=True)
    n = int(T_END * FPS)
    frames = range(n) if len(sys.argv) < 2 else [int(x) for x in sys.argv[1:]]
    for f in frames:
        t = f / FPS
        pose(W, t)
        W["sc"].render.filepath = os.path.join(OUT, f"frame_{f:04d}.png")
        if os.path.exists(W["sc"].render.filepath) and len(sys.argv) < 2:
            continue
        bpy.ops.render.render(write_still=True)
        print("frame", f, "of", n, flush=True)


if __name__ == "__main__":
    main()
