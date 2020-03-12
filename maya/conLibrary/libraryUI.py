from PySide2 import QtWidgets,QtCore, QtGui
import pprint
import controllerLibrary
reload(controllerLibrary)
import os
import logging

import requests # needs to be installed

from maya import cmds
import json
import config
reload(config)

logger = logging.getLogger('ControllerLibrary')

class ControllerLibraryUI(QtWidgets.QDialog):
    ''' UI for controllers. Display screenshot of existing controllers in a grid.
        Allows importing, saving new controller
    '''
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()
        logger.info('init UI')
        self.setWindowTitle("Controller Gallery")
        self.library = controllerLibrary.ControllerLibrary()
        self.buildUI()
        self.create_connections()
        self.populate()

    def buildUI(self):
        ''' Create UI with list view and buttons '''
        layout = QtWidgets.QVBoxLayout(self)

        save_layout = QtWidgets.QHBoxLayout()
        self.le_name = QtWidgets.QLineEdit()
        self.btn_save = QtWidgets.QPushButton("Save")
        save_layout.addWidget(self.le_name)
        save_layout.addWidget(self.btn_save)

        layout.addLayout(save_layout)
        size = 64
        buffer = 12
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.list_widget.setIconSize(QtCore.QSize(size, size))
        self.list_widget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.list_widget.setGridSize(QtCore.QSize(size + buffer, size + buffer))
        layout.addWidget(self.list_widget)

        button_layout = QtWidgets.QHBoxLayout()
        self.btn_import = QtWidgets.QPushButton("Import")
        self.btn_export = QtWidgets.QPushButton("ExportS3")
        self.btn_refresh = QtWidgets.QPushButton("Refresh")
        self.btn_close = QtWidgets.QPushButton("Close")
        button_layout.addWidget(self.btn_import)
        button_layout.addWidget(self.btn_export)
        button_layout.addWidget(self.btn_refresh)
        button_layout.addWidget(self.btn_close)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def populate(self):
        ''' Repopulate controllers from directory '''
        self.list_widget.clear()

        self.library.find()

        for name, info in self.library.items():
            item = ControllerItem(name, info)

            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)

            item.setToolTip(pprint.pformat(info))
            self.list_widget.addItem(item)

    def create_connections(self):
        ''' Signal to slot connections '''
        self.btn_close.clicked.connect(self.close)
        self.btn_refresh.clicked.connect(self.populate)
        self.btn_import.clicked.connect(self.load)
        self.btn_export.clicked.connect(self.export)
        self.btn_save.clicked.connect(self.save)

    def load(self):
        ''' Import selected controller into scene'''
        current_item = self.list_widget.currentItem()

        if current_item:
            name = current_item.text()
            self.library.load(name)

    def save(self):
        ''' Save controller for current scene '''
        name = self.le_name.text()
        if not name.strip():
            cmds.warning("Fill a name first!")
        else:
            self.library.save(name)
            self.populate()

    def export(self):
        ''' Export to Flask app via requests module and HTTP Basic auth '''
        ENDPOINT = '{}/api/assets/upload'.format(config.Config.APP_HOST_NAME)

        current_item = self.list_widget.currentItem()

        if current_item:
            name = current_item.text()
        else:
            return
        logger.debug('Connecting to {}'.format(ENDPOINT))
        # prepare payload
        data = {
                "name" : name,
                "area" : "Model",
                "author_name" : config.Config.MY_NAME_IN_APP,
                "tags"  : "maya, scene",
        }
        files = {}
        logger.debug('Sending data: {}'.format(data))

        # prepare files to 'files' part of request
        if current_item.info['screenshot'] and os.path.exists(current_item.info['screenshot']):
            logger.debug('Sending file: {}'.format(current_item.info['screenshot']))
            files['screenshot_file'] = open(current_item.info['screenshot'], 'rb')
        if current_item.info['path'] and os.path.exists(current_item.info['path']):
            logger.debug('Sending file: {}'.format(current_item.info['path']))
            files['asset_file'] = open(current_item.info['path'], 'rb')

        # use HTTP Basic auth for connection
        response = requests.post(ENDPOINT, data=data, files=files, auth=(config.Config.USER_NAME, config.Config.PASSWORD))

        msg_box = QtWidgets.QMessageBox(self)
        if response.status_code == 200:
            msg_box.setText("File exported to S3 successfully!")
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
        else:
            json_data = json.loads(response.text)
            msg_box.setText("File export to S3 failed.\n\n\n" + json_data['message'])
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setWindowTitle("Export to S3")
        msg_box.exec_()

class ControllerItem(QtWidgets.QListWidgetItem):
    ''' Overrides QListWidgetItem, stores additional info that is used for exporting '''
    def __init__(self, name, info):
        super(ControllerItem, self).__init__(name)
        self.info = info

def showUI():
    ui = ControllerLibraryUI()
    ui.show()
    logger.info("showUI")
    return ui