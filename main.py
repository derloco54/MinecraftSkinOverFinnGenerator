import subprocess
import shutil
import requests
import json
import base64
import os
import winreg
import sys
from PIL import Image
from tkinter import filedialog
import tkinter as tk

def getSkinImgByNick(nicknameMC):
    playerReq = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{nicknameMC}")
    uuidMC = (json.loads(playerReq.text)['id'])
    skinReq = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuidMC}")
    base64SkinData = json.loads(skinReq.text)['properties'][0]['value']
    base64SkinData = json.loads(base64.b64decode(base64SkinData).decode('ascii'))
    skinURL = base64SkinData['textures']['SKIN']['url']
    imgReq = requests.get(skinURL, stream=True)
    img = Image.open(imgReq.raw)
    return img

def deleteUnusedCookedContentFiles(files, path):
    for f in files:
        for x in ['uasset', 'uexp']:
            suffix = f'{f}.{x}'
            currentFile = os.path.join(path, suffix)
            if os.path.exists(currentFile):
                os.remove(currentFile)

def createModFolderAndCopy(modName, cookedContentPath):
    modFolder = os.path.join(unreal_pakFolder, modName, 'MultiVersus', 'Content')
    if os.path.isdir(modFolder):
        shutil.rmtree(modFolder)
    shutil.copytree(cookedContentPath, modFolder)
    invisibleAssets = ['Finn_Tooth']
    copyInvisibleAssets(modName, invisibleAssets)

def checkRegistryForValue(keysList, HKEY_TYPE):
    with winreg.ConnectRegistry(None, HKEY_TYPE) as currentKey:
        for key in keysList:
            currentKey = winreg.OpenKey(currentKey, key, 0, winreg.KEY_READ)
        currentKey = winreg.EnumValue(currentKey, 0)
    return currentKey[1]

def generatePakFile(pakFileName):
    createModFolderAndCopy(pakFileName, cookedContentFolder)
    subprocess.run(fr'{unreal_pakFolder}\UnrealPak-With-CompressionPy.bat "{unreal_pakFolder}\{pakFileName}" -create=filelist.txt -compress', stdout=subprocess.DEVNULL)
    shutil.rmtree(f'{unreal_pakFolder}\{pakFileName}')
    newPakFile = os.path.join(unreal_pakFolder, pakFileName + '.pak')
    modsFolder = os.path.join(currentFolderBackSlashes, 'mods')
    if os.path.exists(os.path.join(modsFolder, pakFileName + '.pak')):
        os.remove(os.path.join(modsFolder, pakFileName + '.pak'))
    shutil.move(newPakFile, modsFolder)

def notFoundApp(message):
    print(message)
    input('Press enter to close')
    exit()

def copyInvisibleAssets(modName, assetsName):
    subMeshesFolder = os.path.join(unreal_pakFolder, modName, 'MultiVersus', 'Content', 'Panda_Main', 'Characters', 'Finn', 'Submeshes')
    os.mkdir(subMeshesFolder)
    for x in assetsName:
        shutil.copyfile(os.path.join(currentFolder, 'invisible_assets', 'invisible.uasset'), os.path.join(subMeshesFolder, f'{x}.uasset'))
        shutil.copyfile(os.path.join(currentFolder, 'invisible_assets', 'invisible.uexp'), os.path.join(subMeshesFolder, f'{x}.uexp'))

os.system('color')
print('\x1b[31m')

if getattr(sys, 'frozen', False):
    currentFolder = os.path.dirname(os.path.realpath(sys.executable))
elif __file__:
    currentFolder = os.path.dirname(os.path.realpath(__file__))

keysListUE4 = ['SOFTWARE', 'EpicGames', 'Unreal Engine', '4.26']
try:
    unrealFolder = checkRegistryForValue(keysListUE4, winreg.HKEY_LOCAL_MACHINE)
except:
    print('Failed to find Unreal Engine automatically, please select it')
    unrealFolder = filedialog.askdirectory(initialdir=currentFolder, title='Select your Unreal Engine(4.26) folder')
    if unrealFolder == '':
        notFoundApp('Could not select Unreal Engine, please try again')

keyListBlender = ['Applications', 'blender.exe', 'shell', 'open', 'command']
try:
    blenderFolder = checkRegistryForValue(keyListBlender, winreg.HKEY_CLASSES_ROOT).split(' ')[0].replace('"', '')
except:
    print('Failed to find Blender automatically, please select it')
    blenderFolder = filedialog.askopenfile(initialdir=currentFolder, title='Select your Blender executable')
    blenderFolder = blenderFolder.name
    if blenderFolder == '':
        notFoundApp('Could not select blender, please try again')
        
ue4Binaries64Bits = os.path.join(unrealFolder, 'Engine', 'Binaries', 'Win64')

currentFolderBackSlashes = currentFolder.replace('/', '\\')
unreal_pakFolder = os.path.join(currentFolder, 'unreal_pak')
projectFile = currentFolderBackSlashes + '\\unreal_files\\Finn\\Finn.uproject'
pythonFile = currentFolderBackSlashes + '\\scripts\\init_unreal.py'
skinFile = f'{currentFolder}/skins/tempSkin.png'

print('\x1b[96m')
skinType = input("Type 1 if you want to get MC skin by name or 2 if you want to select a skin from a file: ")

if skinType == '1':
    nicknameMC = input("Type the nickname:")
    img = getSkinImgByNick(nicknameMC)
    img.save(skinFile)
else:
    print('Choose your MC skin file')
    input_file = filedialog.askopenfilename(initialdir=currentFolder, title='Choose your MC skin file', filetypes=(('PNG', '*.png'), ('All files', '*')))
    img = Image.open(input_file)
    img.save(skinFile)
    pngName = os.path.splitext(os.path.basename(input_file))[0]
print('Skin selected')

print('Choose your MC sword file')
swordTexture = filedialog.askopenfilename(initialdir=os.path.join(currentFolderBackSlashes, 'blender_files', 'textures'), title='Choose your MC sword texture file', filetypes=(('PNG', '*.png'), ('All files', '*')))

print('Launching Blender')
print('Starting to render Blender content, wait a little bit')
try:
    subprocess.run(fr'{blenderFolder} {currentFolderBackSlashes}\blender_files\skinPhoto.blend --background --python {currentFolderBackSlashes}\scripts\init_blender.py -- {swordTexture}', stdout=subprocess.DEVNULL)
except:
    os.system(fr'{blenderFolder} {currentFolderBackSlashes}\blender_files\skinPhoto.blend --background --python {currentFolderBackSlashes}\scripts\init_blender.py -- {swordTexture} > NUL')
print('Blender content rendered')
print('Launching UE4')
print('Starting to render UE4 content, wait a little bit')
try:
    subprocess.run(fr'{ue4Binaries64Bits}\UE4Editor-Cmd.exe {projectFile} -run=pythonscript -script="{pythonFile} {swordTexture}"', stdout=subprocess.DEVNULL)
except:
    os.system(fr'{ue4Binaries64Bits}\UE4Editor-Cmd.exe {projectFile} -run=pythonscript -script="{pythonFile} {swordTexture}" > NUL')
try:
    subprocess.run(fr'{ue4Binaries64Bits}\UE4Editor-Cmd.exe {projectFile} -run=cook targetplatform=WindowsNoEditor', stdout=subprocess.DEVNULL)
except:
    os.system(fr'{ue4Binaries64Bits}\UE4Editor-Cmd.exe {projectFile} -run=cook targetplatform=WindowsNoEditor > NUL')
print('Contents rendered')

cookedContentFolder = f'{currentFolder}/unreal_files/Finn/Saved/Cooked/WindowsNoEditor/Finn/Content'.replace('\\', '/')
uassetsSkinFolder = f'{cookedContentFolder}/Panda_Main/Characters/Finn'.replace('\\', '/')
uassetsSwordFolder = f'{cookedContentFolder}/Panda_Main/Characters/Finn/Swords'.replace('\\', '/')

filesToDeleteSkin = ['Finn_SkelMesh_Skeleton', 'Finn_SkelMesh_PhysicsAsset']
filesToDeleteSword = ['Finn_NightSword_SkelMesh_Skeleton', 'Finn_NightSword_SkelMesh_PhysicsAsset']

deleteUnusedCookedContentFiles(filesToDeleteSkin, uassetsSkinFolder)
deleteUnusedCookedContentFiles(filesToDeleteSword, uassetsSwordFolder)

if skinType == '1':
    generatePakFile(nicknameMC)
else:
    generatePakFile(pngName)
print('Mod generated inside mods folder')
input('Press enter to close')