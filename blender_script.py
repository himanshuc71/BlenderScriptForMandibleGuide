import os

import bpy

scn = bpy.context.scene
sel = bpy.data.objects


print("Begin")

meshes = [o for o in sel if o.type == 'MESH']
print("Fixing Normals")

for obj in meshes:
    scn.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)  # or recalculate outside
    bpy.ops.object.mode_set()

mandible = bpy.data.objects['Mandible']
connector = bpy.data.objects['Connector']
guide = bpy.data.objects['MandibleGuide']
recon = bpy.data.objects['ReconstructedMandible']


# Remeshing, Union, then remshing two Handles


# Union of Guide to Connector
mod = guide.modifiers.new('union3', 'BOOLEAN')
mod.solver = 'CARVE'
mod.operation = "UNION"
mod.object = connector
bpy.context.scene.objects.active = guide
bpy.ops.object.modifier_apply(modifier="union3")

print("Connector")

# Union of Guide to Base2
mod = guide.modifiers.new('union3', 'BOOLEAN')
mod.solver = 'CARVE'
mod.operation = "UNION"
mod.object = bpy.data.objects['Base2']
bpy.context.scene.objects.active = guide
bpy.ops.object.modifier_apply(modifier="union3")

print("Base2")

# Union of Guide to Out0
mod = guide.modifiers.new('union3', 'BOOLEAN')
mod.solver = 'CARVE'
mod.operation = "UNION"
mod.object = bpy.data.objects['Out0']
bpy.context.scene.objects.active = guide
bpy.ops.object.modifier_apply(modifier="union3")

print("Box1")


# Union of Guide to Out1
mod = guide.modifiers.new('union3', 'BOOLEAN')
mod.solver = 'CARVE'
mod.operation = "UNION"
mod.object = bpy.data.objects['Out1']
bpy.context.scene.objects.active = guide
bpy.ops.object.modifier_apply(modifier="union3")

print("Box2")

# Difference of In0 from guide
mod = guide.modifiers.new('union3', 'BOOLEAN')
mod.solver = 'CARVE'
mod.operation = "DIFFERENCE"
mod.object = bpy.data.objects['In0']
bpy.context.scene.objects.active = guide
bpy.ops.object.modifier_apply(modifier="union3")

print("Guide1")

# Difference of In1 from guide
mod = guide.modifiers.new('union3', 'BOOLEAN')
mod.solver = 'CARVE'
mod.operation = "DIFFERENCE"
mod.object = bpy.data.objects['In1']
bpy.context.scene.objects.active = guide
bpy.ops.object.modifier_apply(modifier="union3")


print("Guide2")

##Differencing screwholes
for i in range(0, 6):
    mod = guide.modifiers.new('union3', 'BOOLEAN')
    mod.solver = 'CARVE'
    mod.operation = "DIFFERENCE"
    mod.object = bpy.data.objects['Screws' + str(i)]
    bpy.context.scene.objects.active = guide
    bpy.ops.object.modifier_apply(modifier="union3")
    print("Screw", i)

# Difference Mandible from the guide for fit
    mod = guide.modifiers.new('union3', 'BOOLEAN')
    mod.solver = 'CARVE'
    mod.operation = 'DIFFERENCE'
    mod.object = mandible
    bpy.context.scene.objects.active = guide
    bpy.ops.object.modifier_apply(modifier="union3")
    
print("Mandible differenced")
    
##Differencing screwholes from recon    
for i in range(0, 6):
    mod = recon.modifiers.new('union3', 'BOOLEAN')
    mod.solver = 'CARVE'
    mod.operation = "DIFFERENCE"
    mod.object = bpy.data.objects['Screws' + str(i)]
    bpy.context.scene.objects.active = recon
    bpy.ops.object.modifier_apply(modifier="union3")
    
print("Recon differenced")    


