import sys
import random
import json
import string
import uuid
import bson.json_util
import datetime
import os
from PySide2 import QtCore, QtWidgets, QtGui, QtWebSockets, QtNetwork


class Player(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.create_layout()
        self.connect()

    def create_layout(self):
        """ Creates all layouts and widgets """

        style = self.style()

        # Create menu bar
        menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        self.open_file_action = QtWidgets.QAction("Open File", self)
        self.open_folder_action = QtWidgets.QAction("Open Folder", self)
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.open_folder_action)

        # Create main widget
        self.main_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)

        # Create info area
        main_layout.addWidget(QtWidgets.QLabel("Song Title:"), 0, 0, 1, 1)
        self.song_title = QtWidgets.QLineEdit()
        self.song_title.setEnabled(False)
        main_layout.addWidget(self.song_title, 0, 1, 1, 1)

        main_layout.addWidget(QtWidgets.QLabel("Song Artist:"), 1, 0, 1, 1)
        self.song_artist = QtWidgets.QLineEdit()
        self.song_artist.setEnabled(False)
        main_layout.addWidget(self.song_artist, 1, 1, 1, 1)

        # Create interactable buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.play_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme("media-playback-start.png",
                                     style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play_button.setIcon(icon)

        self.previous_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme("media-skip-backward-symbolic.svg",
                                     style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.previous_button.setIcon(icon)

        self.next_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme("media-skip-forward-symbolic.svg",
                                     style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.next_button.setIcon(icon)

        self.shuffle_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme("media-playlist-shuffle-symbolic.svg",
                                     style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.shuffle_button.setIcon(icon)

        self.repeat_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme("media-playlist-repeat-symbolic.svg",
                                     style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.repeat_button.setIcon(icon)

        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.repeat_button)
        main_layout.addLayout(button_layout, 2, 0, 1, 3)

        # create slider
        self.player_slider = QtWidgets.QSlider()
        self.player_slider.setOrientation(QtGui.Qt.Horizontal)
        main_layout.addWidget(self.player_slider, 3, 0, 1, 3)

    def connect(self):
        """Connect all signal and slots"""
        self.open_file_action.triggered.connect(self.open_file)
        self.open_folder_action.triggered.connect(self.open_folder)

    @QtCore.Slot()
    def open_file(self):
        selection = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Audio File", None, "Audio Files (*.wav *.bwv)")
        if not selection:
            return
        filename = selection[0]

    @QtCore.Slot()
    def open_folder(self):
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select the audio folder", None, QtWidgets.QFileDialog.ShowDirsOnly)
        if not selected_folder:
            return
        files = os.listdir(selected_folder)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = Player()
    widget.resize(600, 200)
    widget.show()

    sys.exit(app.exec_())
