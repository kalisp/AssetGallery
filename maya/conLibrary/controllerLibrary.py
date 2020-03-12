from maya import cmds
import os
import json
import pprint
import logging

import libraryUI

logger = logging.getLogger('ControllerLibrary')

USER_APP_DIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USER_APP_DIR, 'controllerLibrary') # folder for saving of controllers and loading from

def createDirectory(directory=DIRECTORY):
    if not os.path.exists(directory):
        os.mkdir(directory)


class ControllerLibrary(dict):
    ''' Dialog for saving and importing controllers
        Allows creation of controller from current scene, saves the scene, screenshot for scene and json metadata
    '''
    def save(self, name, directory=DIRECTORY, screenshot=True, **info):
        ''' Save a file with screenshot and metadata json file '''
        createDirectory(directory)
        path = os.path.join(directory, '{}.ma'.format(name))
        infoFile = os.path.join(directory, '{}.json'.format(name)) # store metadata about scene

        cmds.file(rename=path)

        if cmds.ls(selection=True): # something selected
            cmds.file(force=True, type='mayaAscii', exportSelected=True) # save only selected
        else:
            cmds.file(save=True, type='mayaAscii', force=True)

        info['name'] = name # metadata
        info['path'] = path # metadata

        if screenshot:
            info['screenshot'] = self.save_screenshot(name, directory)

        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info
        logger.info('file saved')

    def find(self, directory=DIRECTORY):
        ''' List all .ma files in directory '''
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        maya_files = [f for f in files if f.endswith(".ma")]

        for ma in maya_files:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)
            info = {'name' : name, 'path' : path}

            info_file_name = '{}.json'.format(name)
            infoFile = os.path.join(directory, info_file_name)
            if info_file_name in files:
                with open(infoFile, 'r') as fp:
                    info = json.load(fp)
            else:
                print("No info file found")

            self[name] = info

    def load(self, name):
        ''' Loads "name" file to scene '''
        path = self[name]['path']

        cmds.file(path, i=True, usingNamespaces=False)

    def save_screenshot(self, name, directory=DIRECTORY):
        ''' Saves screenshot of a scene into directory with a name
            Saves in .jpg format
        '''
        path = os.path.join(directory, '{}.jpg'.format(name))

        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200, showOrnaments=False,
                       startTime=1, endTime=1, viewer=False)
        return path


if __name__ == '__main__':
    import sys
    #print("\n".join(sys.path))

    reload(libraryUI) #?
    lib = ControllerLibrary()

    ui = libraryUI.showUI()

