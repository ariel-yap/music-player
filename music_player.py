import sys
import random
import json
import string
import uuid
import bson.json_util
import datetime
import os
from PySide2 import QtCore, QtWidgets, QtGui, QtWebSockets, QtNetwork, QtMultimedia
# from QtMultimedia import QMediaMetaData


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
        main_layout.addWidget(QtWidgets.QLabel("File:"), 0, 0, 1, 1)
        self.song_file = QtWidgets.QLineEdit()
        self.song_file.setEnabled(False)
        main_layout.addWidget(self.song_file, 0, 1, 1, 1)

        main_layout.addWidget(QtWidgets.QLabel("Song Title:"), 1, 0, 1, 1)
        self.song_title = QtWidgets.QLineEdit()
        self.song_title.setEnabled(False)
        main_layout.addWidget(self.song_title, 1, 1, 1, 1)

        main_layout.addWidget(QtWidgets.QLabel("Song Artist:"), 2, 0, 1, 1)
        self.song_artist = QtWidgets.QLineEdit()
        self.song_artist.setEnabled(False)
        main_layout.addWidget(self.song_artist, 2, 1, 1, 1)

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
        main_layout.addLayout(button_layout, 3, 0, 1, 5)

        # volume_label = QtWidgets.QLabel()
        # icon = QtGui.QIcon.fromTheme("audio-volume-medium-symbolic.svg",
        #                              style.standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        # volume_label.setPixmap(icon.pixmap(QtCore.QSize(20, 20)))
        # main_layout.addWidget(volume_label, 3, 3, 1, 1)
        # self.volume_slider = QtWidgets.QSlider()
        # self.volume_slider.setOrientation(QtGui.Qt.Horizontal)
        # self.volume_slider.setMinimum(0)
        # self.volume_slider.setMaximum(10)
        # main_layout.addWidget(self.volume_slider, 3, 4, 1, 1)

        # create slider
        self.player_slider = QtWidgets.QSlider()
        self.player_slider.setOrientation(QtGui.Qt.Horizontal)
        self.player_slider.setMinimum(0)
        main_layout.addWidget(self.player_slider, 4, 0, 1, 5)

        self.current_duration = QtWidgets.QLabel("0:00")
        self.total_duration = QtWidgets.QLabel("0:00")
        main_layout.addWidget(self.current_duration, 5, 0, 1, 1)
        main_layout.addWidget(self.total_duration, 5, 4, 1, 1)

        # create the media player
        self.audio_player = QtMultimedia.QMediaPlayer()
        self.audio_player.setVolume(10)
        self.open_new_song()

    def connect(self):
        """Connect all signal and slots"""
        self.open_file_action.triggered.connect(self.open_file)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.play_button.clicked.connect(self.play_pause)
        self.audio_player.metaDataChanged.connect(self.metaDataChanged)
        self.audio_player.durationChanged.connect(self.setTotalDuration)
        self.player_slider.valueChanged.connect(self.setCurrentDuration)
        self.player_slider.sliderMoved.connect(self.audio_player.setPosition)
        self.audio_player.positionChanged.connect(
            self.player_slider.setValue)
        self.audio_player.mediaStatusChanged.connect(self.statusChanged)

    def open_new_song(self):
        file_path = "/home/ariel/Work/HiringMaterials/bensound-dubstep.mp3"
        url = QtCore.QUrl.fromLocalFile(file_path)
        self.audio_player.setMedia(QtMultimedia.QMediaContent(url))
        self.song_file.setText(file_path)

    @ QtCore.Slot()
    def statusChanged(self, status):
        print(status)

    @ QtCore.Slot()
    def play_pause(self):
        print(self.audio_player.state())
        if self.audio_player.state() == QtMultimedia.QMediaPlayer.State.PausedState:
            self.audio_player.play()
        elif self.audio_player.state() == QtMultimedia.QMediaPlayer.State.PlayingState:
            self.audio_player.pause()
        else:
            self.audio_player.pause()

    @ QtCore.Slot()
    def open_file(self):
        selection = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Audio File", None, "Audio Files (*.wav *.bwv)")
        if not selection:
            return
        filename = selection[0]

    @ QtCore.Slot()
    def open_folder(self):
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select the audio folder", None, QtWidgets.QFileDialog.ShowDirsOnly)
        if not selected_folder:
            return
        files = os.listdir(selected_folder)

    @ QtCore.Slot()
    def metaDataChanged(self):
        available_meta_data = self.audio_player.availableMetaData()

        # print(available_meta_data)
        if "AlbumArtist" in available_meta_data:
            self.song_artist.setText(self.audio_player.metaData("AlbumArtist"))
        else:
            self.song_artist.setText("N/A")

        if "Title" in available_meta_data:
            self.song_title.setText(self.audio_player.metaData("Title"))
        else:
            self.song_title.setText("N/A")

        if "AudioCodec" in available_meta_data:
            print(self.audio_player.metaData("AudioCodec"))

    @ QtCore.Slot()
    def setTotalDuration(self):
        # print(self.audio_player.duration())
        minutes = (self.audio_player.duration() // 1000) // 60
        # print(minutes)
        seconds = (self.audio_player.duration() // 1000) % 60
        # print(seconds)
        self.total_duration.setText(f'{minutes:02}:{seconds:02}')
        self.player_slider.setMaximum(self.audio_player.duration())
        # self.total_duration = self.audio_player.duration

    @ QtCore.Slot()
    def setCurrentDuration(self, duration):
        # print(self.audio_player.duration())
        minutes = (duration // 1000) // 60
        # print(minutes)
        seconds = (duration // 1000) % 60
        # print(seconds)
        self.current_duration.setText(f'{minutes:02}:{seconds:02}')
        # self.total_duration = self.audio_player.duration


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle(QtWidgets.QStyleFactory.create("Fusion"))

    app.setStyleSheet(
        """
        QWidget
{
    background-color: #381422;
    font-family: Roboto-Regular;
    color: #ffffff;
}

        """
    )

    widget = Player()
    widget.resize(600, 200)
    widget.show()

    sys.exit(app.exec_())
