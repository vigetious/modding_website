import os
import shutil

BASE_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[1:]

def moveMod(modID, modUploadPath, modName):
    os.makedirs('files/{0}'.format(str(modID)))
    shutil.move(modUploadPath, 'files/{0}/{1}'.format(str(modID), modName))
    return 'files/{0}/{1}'.format(str(modID), modName)
