import time, math, bpy
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = 24
sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1280, 720
sc.render.filepath = "/home/user/Bernard/lab/ep03s/build/blender_probe.png"
w = bpy.data.worlds.new("w"); sc.world = w; w.use_nodes = True
w.node_tree.nodes["Background"].inputs[0].default_value = (0.004, 0.005, 0.006, 1)
font = bpy.data.fonts.load("/home/user/Bernard/a01_v6/fonts/Michroma-400.ttf")
bpy.ops.object.text_add(location=(0, 0, 0)); t = bpy.context.object
t.data.body = "1848"; t.data.font = font; t.data.extrude = 0.08; t.data.bevel_depth = 0.012; t.data.align_x = "CENTER"; t.data.align_y = "CENTER"
t.rotation_euler = (math.radians(90), 0, 0)
m = bpy.data.materials.new("chrome"); m.use_nodes = True
b = m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value = (0.9, 0.92, 0.94, 1); b.inputs["Metallic"].default_value = 1.0; b.inputs["Roughness"].default_value = 0.14
t.data.materials.append(m)
g = bpy.data.materials.new("gold"); g.use_nodes = True
gb = g.node_tree.nodes["Principled BSDF"]; gb.inputs["Base Color"].default_value = (1.0, 0.76, 0.33, 1); gb.inputs["Metallic"].default_value = 1.0; gb.inputs["Roughness"].default_value = 0.28
import random
random.seed(3)
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.012, location=(0, 0, -0.6)); d = bpy.context.object; d.data.materials.append(g)
for i in range(400):
    o = d.copy(); o.location = (random.uniform(-1.8, 1.8), random.uniform(-0.6, 0.6), random.uniform(-0.75, -0.55)); sc.collection.objects.link(o)
for name, loc, energy, col, size in (("key", (2.5, -3, 2.5), 900, (1.0, 0.9, 0.8), 2.0), ("rim", (-3, 2, 1.2), 1200, (0.07, 0.72, 0.67), 1.5), ("fill", (0, -4, -1), 150, (0.6, 0.7, 0.9), 3.0)):
    L = bpy.data.lights.new(name, "AREA"); L.energy = energy; L.color = col; L.size = size
    o = bpy.data.objects.new(name, L); o.location = loc; sc.collection.objects.link(o)
    o.rotation_euler = (0, 0, 0)
    c = o.constraints.new("TRACK_TO"); c.target = t; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
cam = bpy.data.cameras.new("cam"); cam.lens = 50
co = bpy.data.objects.new("cam", cam); co.location = (0.6, -4.2, 0.45); sc.collection.objects.link(co); sc.camera = co
c = co.constraints.new("TRACK_TO"); c.target = t; c.track_axis = "TRACK_NEGATIVE_Z"; c.up_axis = "UP_Y"
t0 = time.time()
bpy.ops.render.render(write_still=True)
print("render seconds", round(time.time() - t0, 1))
