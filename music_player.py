"""Quick script to hold MusicPlayer class and the contruction of this GUI to display to a user
"""
import sys
import os
from PySide2 import QtCore, QtWidgets, QtGui, QtMultimedia
from black import main


class QVLine(QtWidgets.QFrame):
    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class Player(QtWidgets.QMainWindow):
    """MusicPlayer Class that is a GUI that allow a user to play and listen to music.

    Features:
    - Opens a file
    - Opens a folder and imports all songs
    - Plays songs
    - Shuffle, repeat, next, previous functionality
    - Shows a list of the playlist
    """

    def __init__(self):
        super().__init__()
        self.playlist_files = ["/home/eighti/ambient-piano.mp3"]

        self.create_layout()
        self.connect()
        self.setup()

    def create_layout(self):
        """Creates all layouts and widgets"""

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
        icon = QtGui.QIcon.fromTheme(
            "media-playback-start-symbolic.svg",
            style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
        )
        self.play_button.setIcon(icon)

        self.previous_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme(
            "media-skip-backward-symbolic.svg",
            style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
        )
        self.previous_button.setIcon(icon)

        self.next_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme(
            "media-skip-forward-symbolic.svg",
            style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
        )
        self.next_button.setIcon(icon)

        self.shuffle_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme(
            "media-playlist-shuffle-symbolic.svg",
            style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
        )
        self.shuffle_button.setIcon(icon)

        self.repeat_button = QtWidgets.QPushButton()
        icon = QtGui.QIcon.fromTheme(
            "media-playlist-repeat-symbolic.svg",
            style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
        )
        self.repeat_button.setIcon(icon)

        button_layout.addWidget(self.shuffle_button)
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.repeat_button)
        main_layout.addLayout(button_layout, 3, 0, 1, 5)

        # create slider
        self.player_slider = QtWidgets.QSlider()
        self.player_slider.setOrientation(QtGui.Qt.Horizontal)
        self.player_slider.setMinimum(0)
        main_layout.addWidget(self.player_slider, 4, 0, 1, 5)

        self.current_duration = QtWidgets.QLabel("0:00")
        self.total_duration = QtWidgets.QLabel("0:00")
        main_layout.addWidget(self.current_duration, 5, 0, 1, 1)
        main_layout.addWidget(self.total_duration, 5, 4, 1, 1)

        # create separator and playlist
        main_layout.addWidget(QVLine(), 0, 5, 6, 1)
        self.playlist = QtWidgets.QListWidget()
        main_layout.addWidget(self.playlist, 0, 6, 6, 1)
        # create the media player
        self.audio_player = QtMultimedia.QMediaPlayer()
        self.audio_player.setVolume(10)

    def connect(self):
        """Connect all signal and slots"""
        self.open_file_action.triggered.connect(self.open_file)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.play_button.clicked.connect(self.play_pause)
        self.previous_button.clicked.connect(self.play_next)
        self.next_button.clicked.connect(self.play_next)
        self.audio_player.metaDataChanged.connect(self.metaDataChanged)
        self.audio_player.durationChanged.connect(self.setTotalDuration)
        self.player_slider.valueChanged.connect(self.setCurrentDuration)
        self.player_slider.sliderMoved.connect(self.audio_player.setPosition)
        self.audio_player.positionChanged.connect(self.player_slider.setValue)
        self.audio_player.stateChanged.connect(self.stateChanged)
        self.audio_player.error.connect(self.media_error)
        self.playlist.itemDoubleClicked.connect(self.select_song)

    def setup(self):
        playlist = [os.path.splitext(f)[0] for f in self.playlist_files]
        self.playlist.addItems(playlist)

    def reload_song_list(self, new_list):
        self.playlist.addItems(new_list)

    def play_next(self):
        current_row = self.playlist.currentRow()
        self.playlist.setCurrentRow(current_row + 1)
        self.select_song()

    @QtCore.Slot()
    def select_song(self):
        current_song_file = self.playlist_files[self.playlist.currentRow()]
        print("dev debug msg: " + current_song_file)
        url = QtCore.QUrl.fromLocalFile(current_song_file)
        self.audio_player.setMedia(QtMultimedia.QMediaContent(url))
        self.song_file.setText(current_song_file)
        self.audio_player.play()

    @QtCore.Slot()
    def media_error(self):
        QtWidgets.QMessageBox.warning(self, "Error", self.audio_player.errorString())

    @QtCore.Slot()
    def stateChanged(self, state):
        style = self.style()
        if state == QtMultimedia.QMediaPlayer.State.PlayingState:
            icon = QtGui.QIcon.fromTheme(
                "media-playback-pause-symbolic.svg",
                style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
            )
        else:
            icon = QtGui.QIcon.fromTheme(
                "media-playback-start-symbolic.svg",
                style.standardIcon(QtWidgets.QStyle.SP_MediaPlay),
            )
        self.play_button.setIcon(icon)

    @QtCore.Slot()
    def play_pause(self):
        if self.audio_player.state() == QtMultimedia.QMediaPlayer.State.PausedState:
            self.audio_player.play()
        elif self.audio_player.state() == QtMultimedia.QMediaPlayer.State.PlayingState:
            self.audio_player.pause()
        elif (
            self.audio_player.state() == QtMultimedia.QMediaPlayer.State.StoppedState
        ) and (
            self.audio_player.mediaStatus()
            == QtMultimedia.QMediaPlayer.MediaStatus.LoadedMedia
        ):
            self.audio_player.play()

    @QtCore.Slot()
    def open_file(self):
        selection = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            None,
            "Audio Files (*.mp3 *.wav *.ogg *.wma *.flac)",
        )
        if not selection:
            return
        filename = selection[0]
        self.playlist_files.append(filename)
        self.reload_song_list([os.path.splitext(os.path.split(filename)[1])[0]])

        QtWidgets.QMessageBox.information(
            self, "Testing", "Dev test that this works" + filename
        )

    @QtCore.Slot()
    def open_folder(self):
        selected_folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select a folder", None, QtWidgets.QFileDialog.ShowDirsOnly
        )
        if not selected_folder:
            return
        files = os.listdir(selected_folder)
        trimmed_files = [os.path.splitext(f)[0] for f in files]
        fullname_files = [selected_folder + "/" + f for f in files]
        self.playlist_files += fullname_files
        self.reload_song_list(trimmed_files)

    @QtCore.Slot()
    def metaDataChanged(self):
        available_meta_data = self.audio_player.availableMetaData()
        if "AlbumArtist" in available_meta_data:
            self.song_artist.setText(self.audio_player.metaData("AlbumArtist"))
        else:
            self.song_artist.setText("N/A")

        if "Title" in available_meta_data:
            self.song_title.setText(self.audio_player.metaData("Title"))
        else:
            self.song_title.setText("N/A")

    @QtCore.Slot()
    def setTotalDuration(self):
        minutes = (self.audio_player.duration() // 1000) // 60
        seconds = (self.audio_player.duration() // 1000) % 60
        self.total_duration.setText(f"{minutes:02}:{seconds:02}")
        self.player_slider.setMaximum(self.audio_player.duration())

    @QtCore.Slot()
    def setCurrentDuration(self, duration):
        minutes = (duration // 1000) // 60
        seconds = (duration // 1000) % 60
        self.current_duration.setText(f"{minutes:02}:{seconds:02}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    app.setStyleSheet(
        """
        QWidget
{
    font-family: Roboto-Regular;
    color: #ffffff;
}

        """
    )

    widget = Player()
    widget.resize(700, 200)
    widget.show()

    sys.exit(app.exec_())
