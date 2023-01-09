import unreal
import os
import sys

def createImportTask(fileName, fileLocation, filePath):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', fileName)
    task.set_editor_property('destination_path', fileLocation)
    task.set_editor_property('save', True)
    task.set_editor_property('filename', filePath)
    task.set_editor_property('replace_existing', True)
    return task

def executeImportTasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)

argv = sys.argv

textureName = 'Finn_Base_D'
textureLocation = '/Game/Panda_Main/Characters/Finn'
texturePath =  os.path.join(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir), 'skins', 'tempSkin.png')
texturePath = texturePath.replace('\\', '/')

uiPhotoName = 'FullPortrait_Finn'
uiPhotoLocation = '/Game/Panda_Main/Characters/Finn/UI'
uiPhotoPath = os.path.join(os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir), 'blender_files', 'rendered', 'skin.png')
uiPhotoPath = uiPhotoPath.replace('\\', '/')

swordName = 'Finn_Props_Base_D'
swordLocation = '/Game/Panda_Main/Characters/Finn/Swords'
swordPath = argv[1]

importTaskTexture = createImportTask(textureName, textureLocation, texturePath)
importTaskUIPhoto = createImportTask(uiPhotoName, uiPhotoLocation, uiPhotoPath)
importTaskSword = createImportTask(swordName, swordLocation, swordPath)

executeImportTasks([importTaskTexture, importTaskUIPhoto, importTaskSword])

