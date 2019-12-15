import os
import shutil

BASE_DIR = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[1:]

def moveMod(modID, modUploadPath, modName):
    os.makedirs('files/{0}'.format(str(modID)))
    shutil.move(modUploadPath, 'files/{0}/{1}'.format(str(modID), modName))
    return 'files/{0}/{1}'.format(str(modID), modName)

def removeEdit(x, originalMod):
    if x.modPreviewImage1 != originalMod.modPreviewImage1:
        x.modPreviewImage1.delete()
    if x.modPreviewImage2 != originalMod.modPreviewImage2:
        x.modPreviewImage2.delete()
    if x.modPreviewImage3 != originalMod.modPreviewImage3:
        x.modPreviewImage3.delete()
    if x.modPreviewImage4 != originalMod.modPreviewImage4:
        x.modPreviewImage4.delete()
    if x.modPreviewImage5 != originalMod.modPreviewImage5:
        x.modPreviewImage5.delete()
    if x.modBackground != originalMod.modBackground:
        x.modBackground.delete()
    if x.modAvatar != originalMod.modAvatar:
        x.modAvatar.delete()
