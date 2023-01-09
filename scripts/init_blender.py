import bpy
import os
import sys

argv = sys.argv
argv = argv[argv.index("--") + 1:]
argv = ''.join(argv)

renderName = 'skin.png'
currentFolder = bpy.path.abspath('//')
renderFolder = os.path.join(currentFolder, 'rendered', renderName)
skinPath =  os.path.join(os.path.normpath(os.path.dirname(currentFolder) + os.sep + os.pardir), 'skins', 'tempSkin.png')

bpy.data.materials["netherite_sword"].node_tree.nodes["Image Texture"].image.filepath = argv

bpy.context.scene.render.filepath = renderFolder
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 1024
bpy.ops.render.render(write_still=True)