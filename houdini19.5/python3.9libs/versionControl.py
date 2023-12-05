"""
    The following code is identical to the script found in the version_control.shelf file.
    Only used for easier coding in PySide as Intellisense is not available in the shelf file CDATA block.
    Any changes must be applied to the shelf file (NOT THIS ONE) in order to take effect in Houdini.
"""

import os
import re

from PySide2 import QtCore, QtGui, QtWidgets

# local import
import incrementSave

class VersionControlUI(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(VersionControlUI, self).__init__(parent)

        # Initialize window
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setObjectName('VersionControlUI')
        self.setWindowTitle('Version Control')
        self.resize(500, 500)
        
        # Set up widgets
        self.path = self.get_file_path()
        self.dirmodel = self.create_file_model()
        self.view = self.create_tree_view()
        self.button_layout = self.create_buttons()

        # Set up layout
        outer_layout = QtWidgets.QVBoxLayout()
        outer_layout.addWidget(self.view)
        outer_layout.addLayout(self.button_layout)
        outer_layout.setSpacing(15)

        self.setLayout(outer_layout)

    # Functions 
    def create_file_model(self):
        dirmodel = QtWidgets.QFileSystemModel()
        dirmodel.setRootPath(QtCore.QDir.rootPath())

        # Filter to show only files that are versions of current file
        dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        filter = self.get_filter()
        dirmodel.setNameFilters([filter])
        dirmodel.setNameFilterDisables(False) # Hide instead of disable

        return dirmodel
    
    def create_tree_view(self):
        view = QtWidgets.QTreeView(parent=self)
        view.setModel(self.dirmodel)
        view.setRootIndex(self.dirmodel.index(self.path))

        # Only show File Name and Edited Date columns
        view.hideColumn(1)
        view.hideColumn(2)

        # Resizing
        font = QtGui.QFont()
        font.setPointSize(10)
        view.setFont(font)
        view.header().resizeSection(0, 325)

        view.setSortingEnabled(True)
        view.doubleClicked(self.open_file)

        return view
    
    def create_buttons(self):
        button_layout = QtWidgets.QHBoxLayout()

        open_button = QtWidgets.QPushButton('Open File', self)
        open_button.clicked.connect(self.open_file)

        explorer_button = QtWidgets.QPushButton('Open File Explorer', self)
        explorer_button.clicked.connect(self.open_explorer)

        save_button = QtWidgets.QPushButton('Save New Version', self)
        save_button.clicked.connect(self.save_version)

        button_layout.addWidget(save_button)
        button_layout.addWidget(explorer_button)
        button_layout.addWidget(open_button)

        return button_layout

    def get_file_path(self):
        current_path = hou.hipFile.path()
        dir_path = os.path.split(current_path)[0]
        return dir_path
    
    def get_filter(self):
        str_match = r"_v[0-9]"
        current_path = hou.hipFile.path()
        file = os.path.splitext(os.path.basename(current_path))[0]
        filename = re.split(f"{str_match}+", file, flags=re.I)
        filter = fr"*{filename[0]}_[vV]*"
        return filter
    
    def open_explorer(self):
        hou.ui.selectFile()

    def open_file(self):
        index = self.view.currentIndex()
        file_path = self.dirmodel.filePath(index)
        hou.hipFile.load(file_path)

    def save_version(self):
        incrementSave.main()

# main
ui = VersionControlUI()
ui.show()
