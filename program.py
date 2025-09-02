from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6 import uic
import sys
from data_io import *
import os

def normalize_path(path: str) -> str:
    """Return an absolute path for resources declared in JSON.

    - Accepts both absolute and relative inputs
    - Tries current working directory and this file's directory as bases
    """
    normalized = os.path.normpath(path)
    # If already absolute and exists
    if os.path.isabs(normalized) and os.path.exists(normalized):
        return normalized
    candidates = [
        os.path.join(os.getcwd(), normalized),
        os.path.join(os.path.dirname(__file__), normalized),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return candidate
    return normalized

class Alert(QMessageBox):
    def error_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Critical)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()

    def success_message(self, title, message):
        self.setIcon(QMessageBox.Icon.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.exec()
        

class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye = self.findChild(QPushButton, "btn_eye")

        self.btn_eye.clicked.connect(lambda:self.show_password(self.btn_eye, self.password_input))
        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() ==  QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if email == "":
            msg.error_message("Login", "Email is required")
            self.email_input.setFocus()
            return
        
        if password == "":
            msg.error_message("Login", "Password is required")
            self.password_input.setFocus()
            return
                
        user = get_user_by_email_and_password(email,password)
        if user:
            msg.success_message("Login", "Welcome to the system")
            self.show_home(user["id"])
            return

        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

    def show_home(self, id):
        self.home = Home(id)
        self.home.show()
        self.close()

class Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/signup.ui", self)

        self.confirm_pass_input = self.findChild(QLineEdit, "txt_confirm_password")
        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")
        self.name_input = self.findChild(QLineEdit, "txt_name")

        self.btn_eye_p.clicked.connect(lambda: self.show_password(self.btn_eye_p, self.password_input))
        self.btn_eye_cp.clicked.connect(lambda: self.show_password(self.btn_eye_cp, self.confirm_pass_input))
        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)

    def show_password(self, button: QPushButton, input: QLineEdit):
        if input.echoMode() ==  QLineEdit.EchoMode.Password:
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else:
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_pass = self.confirm_pass_input.text().strip()
        name = self.name_input.text().strip()

        if email == "":
            msg.error_message("Register", "Email is required")
            self.email_input.setFocus()
            return
    
        if name == "":
            msg.error_message("Register", "Name is required")
            self.name_input.setFocus()
            return
    
        if password == "":
            msg.error_message("Register", "Password is required")
            self.password_input.setFocus()
            return
        
        if confirm_pass == "":
            msg.error_message("Register","Confirm password is required")
            self.confirm_pass_input.setFocus() 
            return
        
        if password != confirm_pass:
            msg.error_message("Register", "Password and confirm password do not match")
            self.password_input.setFocus()
            return

        user = get_user_by_email(email)
        if user:
            msg.error_message("Register", "Email already exists")
            self.email_input.setFocus()
            return
        
        create_user(email, password, name)
            
        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()
        
class MovieItemWidget(QWidget):
    signal_detail_movie = pyqtSignal(int)
    signal_play_movie = pyqtSignal(int)
    signal_favorite_changed = pyqtSignal()  # New signal for favorite changes
    
    def __init__(self, movie_id, title, banner_path, video_path, description):
        super().__init__()
        self.movie_id = movie_id
        self.user_id = 1  # We'll get this from Main class
        
        # Load UI
        uic.loadUi('ui/movie_item.ui', self)
        
        # Set data
        self.titleLabel.setText(title)
        
        # Set banner with normalized path
        banner_path = normalize_path(banner_path)
        pixmap = QPixmap(banner_path)
        self.bannerLabel.setPixmap(pixmap)
        
        # Connect signals
        self.infoButton.clicked.connect(self.show_detail)
        self.playButton.clicked.connect(self.play_movie)
        self.btn_favorite.clicked.connect(self.toggle_favorite)
        
        # Set favorite icon
        self.update_favorite_icon()
        
    def set_user_id(self, user_id):
        self.user_id = user_id
        self.update_favorite_icon()
        
    def update_favorite_icon(self):
        is_fav = is_favorite(self.user_id, self.movie_id)
        icon = QIcon("img/heart-solid.svg" if is_fav else "img/heart-regular.svg")
        self.btn_favorite.setIcon(icon)
        
    def show_detail(self):
        self.signal_detail_movie.emit(self.movie_id)
        
    def play_movie(self):
        self.signal_play_movie.emit(self.movie_id)
        
    def toggle_favorite(self):
        is_fav = is_favorite(self.user_id, self.movie_id)
        if is_fav:
            remove_from_favorites(self.user_id, self.movie_id)
        else:
            add_to_favorites(self.user_id, self.movie_id)
        self.update_favorite_icon()
        self.signal_favorite_changed.emit()  # Emit signal when favorite status changes

class Home(QWidget):
    def __init__(self, id):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        self.id = id
        self.user_id = id  # Add user_id for movie operations
        self.user = get_user_by_id(id)
        self.movie_id = None  # Add movie_id for video operations
        self.load_user_info()

        self.stackedWidget = self.findChild(QStackedWidget,"stackedWidget")
        self.btn_home = self.findChild(QPushButton,"btn_home")
        self.btn_profile = self.findChild(QPushButton,"btn_profile")
        self.btn_watch = self.findChild(QPushButton,"btn_watch")
        self.btn_save_account = self.findChild(QPushButton, "btn_save_account")

        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_birthday = self.findChild(QDateEdit, "txt_birthday")
        self.txt_gender = self.findChild(QComboBox, "txt_gender")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")

        self.btn_home.clicked.connect(lambda: self.navigate_screen(self.stackedWidget, 2))
        self.btn_profile.clicked.connect(lambda: self.navigate_screen(self.stackedWidget, 0))
        # Play button on Detail page should start the video of current movie
        self.btn_watch.clicked.connect(self.loadVideo)
        self.btn_avatar.clicked.connect(self.update_avatar)
        self.btn_save_account.clicked.connect(self.update_user_info)
        
        # Setup UI and load movies
        self.setupUI()
        self.loadMovies()


    def navigate_screen(self,stackWidget: QStackedWidget,index:int):
        self.stackedWidget.setCurrentIndex(index)

    def load_user_info(self):
        self.user = get_user_by_id(self.id)
        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_birthday.setDate(QDate.fromString(self.user["birthday"], "dd//MM//yyyy"))
        self.txt_gender.setCurrentText(self.user["gender"])
        self.btn_avatar.setIcon(QIcon(self.user["avatar"]))

    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image", "", "Image Files(*.png *.jpg *jpeg *bmp)")
        if file:
            self.user["avatar"] = file
            self.btn_avatar.setIcon(QIcon(file))
            update_user_avatar(self.id, file)
            msg.success_message("Update", "Avatar updated successfully")

    def update_user_info(self):
        name = self.txt_name.text().strip()
        birthday = self.txt_birthday.date().toString("dd//MM//yyyy")
        gender = self.txt_gender.currentText()
        update_user(self.id, name, birthday, gender)
        msg.success_message("Update", "User info updated successfully")
        self.load_user_info()
        
    def setupUI(self):
        # Setup movie container
        self.movieList = QScrollArea()
        self.movieList.setStyleSheet("""
            QScrollArea {
                background-color: black;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgb(45, 45, 45);
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgb(80, 80, 80);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.movieItem = QWidget()
        self.gridLayout = QGridLayout(self.movieItem)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)

        self.movieItem.setLayout(self.gridLayout)
        self.movieList.setWidget(self.movieItem)
        self.movieList.setWidgetResizable(True)
        
        # Add movie list to video container
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.movieList)
        self.video_container.setLayout(containerLayout)
        
        # Setup favorite container with scroll area
        self.favoriteList = QScrollArea()
        self.favoriteList.setStyleSheet("""
            QScrollArea {
                background-color: black;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgb(45, 45, 45);
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgb(80, 80, 80);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.favoriteItem = QWidget()
        self.favoriteLayout = QGridLayout(self.favoriteItem)
        self.favoriteLayout.setContentsMargins(10, 10, 10, 10)
        self.favoriteLayout.setSpacing(10)
        
        self.favoriteItem.setLayout(self.favoriteLayout)
        self.favoriteList.setWidget(self.favoriteItem)
        self.favoriteList.setWidgetResizable(True)
        
        # Add favorite list to favorite container
        favoriteContainerLayout = QVBoxLayout()
        favoriteContainerLayout.addWidget(self.favoriteList)
        self.favorite_container.setLayout(favoriteContainerLayout)
        
        self.txt_search = self.findChild(QLineEdit, 'txt_search')
        self.btn_search = self.findChild(QPushButton, 'btn_search')
        self.btn_search.clicked.connect(self.search_movie)
        
        # Setup media player components
        self.setupMediaPlayer()
    
    def setupMediaPlayer(self):
        # Setup media player
        self.lbl_title = self.findChild(QLabel, 'videoName')
        self.volumeBtn = self.findChild(QPushButton, 'volumeBtn')
        self.timeLabel = self.findChild(QLabel, 'timeLabel')
        self.durationBar = self.findChild(QSlider, 'durationBar')
        self.volumeBar = self.findChild(QSlider, 'volumeBar')
        self.videoName = self.findChild(QLabel, 'videoName')
        self.playBtn = self.findChild(QPushButton, 'playBtn')
        
        # Load icons
        self.playIcon = QIcon("img/play-solid.svg")
        self.pauseIcon = QIcon("img/pause-solid.svg")
        self.volumeHighIcon = QIcon("img/volume-high-solid.svg")
        self.volumeLowIcon = QIcon("img/volume-low-solid.svg")
        self.volumeOffIcon = QIcon("img/volume-off-solid.svg")
        
        # Setup video player buttons
        self.playBtn.setIcon(self.playIcon)
        self.volumeBtn.setIcon(self.volumeHighIcon)
        
        # Setup volume control
        self.current_volume = 50
        self.volumeBar.setValue(self.current_volume)
        self.volumeBar.setRange(0, 100)
        self.volumeBar.setValue(50)
        
        # Connect signals
        self.playBtn.clicked.connect(self.play)
        self.volumeBtn.clicked.connect(self.toggleMute)
        self.volumeBar.valueChanged.connect(self.setVolume)
        self.durationBar.sliderMoved.connect(self.setPosition)
        
        # Setup video widget
        placeholder = self.findChild(QWidget, 'videoWidget')
        self.videoWidget = QVideoWidget()
        self.videoWidget.setGeometry(placeholder.geometry())
        self.videoWidget.setParent(placeholder.parentWidget())
        self.videoWidget.show()
        placeholder.hide()
        
        # Setup media player
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        # initialize volume
        self.setVolume(self.current_volume)
        # connect player signals once
        self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.errorOccurred.connect(self.handleError)

    def loadMovies(self):
        # Get all movies from film.json
        movies = load_films()
        if movies:
            self.renderMovieList(movies)
        
    def renderMovieList(self, movie_list: list):
        # Clear previous search results
        for i in reversed(range(self.gridLayout.count())):
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            if widgetToRemove:
                self.gridLayout.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
            
        row = 0
        column = 0
        for movie in movie_list:
            itemWidget = MovieItemWidget(
                movie["id"], 
                movie["title"], 
                normalize_path(movie["img"]),  
                normalize_path(movie["trailer"]),  
                movie.get("description", "")
            )
            itemWidget.set_user_id(self.user_id)  # Set user_id for the widget
            itemWidget.signal_detail_movie.connect(self.catch_detail_movie)
            itemWidget.signal_play_movie.connect(self.catch_play_movie)
            itemWidget.signal_favorite_changed.connect(self.on_favorite_changed)  # Connect new signal
            self.gridLayout.addWidget(itemWidget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0
    
    def search_movie(self):
        name = self.txt_search.text()
        movie_list = get_film_by_name(name)
        self.renderMovieList(movie_list)

    def detail_movie(self, movie_id):
        movie = get_film_by_id(movie_id)
        if not movie:
            return
            
        # Find all the label widgets
        self.lbl_name = self.findChild(QLabel, "lbl_detail_name")
        self.lbl_director = self.findChild(QLabel, "lbl_detail_director")
        self.lbl_release_date = self.findChild(QLabel, "lbl_detail_release_date")
        self.lbl_genre = self.findChild(QLabel, "lbl_detail_genre")
        self.lbl_description = self.findChild(QLabel, "lbl_detail_description")
        self.lbl_rating = self.findChild(QLabel, "lbl_detail_rating")
        self.lbl_duration = self.findChild(QLabel, "lbl_detail_duration")
        self.lbl_age_rating = self.findChild(QLabel, "lbl_detail_age_rating")
        self.lbl_main_actor = self.findChild(QLabel, "lbl_detail_main_actor")
        self.lbl_image = self.findChild(QLabel, "lbl_detail_image")
        
        # Set the text for each label
        self.lbl_name.setText(movie["title"])
        self.lbl_director.setText(f"Director: {movie.get('director', 'N/A')}")
        self.lbl_release_date.setText(f"Release Date: {movie.get('release_date', 'N/A')}")
        self.lbl_genre.setText(f"Genre: {', '.join(movie.get('genre', ['N/A']))}")
        self.lbl_main_actor.setText(f"Main Actor: {movie.get('main_actor', 'N/A')}")
        
        # Set the banner image
        if movie.get('img'):
            self.lbl_image.setPixmap(QPixmap(normalize_path(movie["img"])))
        
        # Format and set the description with word wrapping
        description = movie.get("description", "No description available")
        split_description = description.split(" ")
        description = "\n".join([" ".join(split_description[i:i+10]) for i in range(0, len(split_description), 10)])
        self.lbl_description.setText(f"Description: {description}")
        
        # Find and setup favorite button
        self.btn_favorite = self.findChild(QPushButton, "btn_favorite")
        if self.btn_favorite:
            is_fav = is_favorite(self.user_id, movie_id)
            icon = QIcon("img/heart-solid.svg" if is_fav else "img/heart-regular.svg")
            self.btn_favorite.setIcon(icon)
            self.btn_favorite.clicked.connect(lambda: self.toggle_favorite(movie_id))
        
        # Switch to detail page
        self.stackedWidget.setCurrentIndex(1)
        
    def toggle_favorite(self, movie_id):
        is_fav = is_favorite(self.user_id, movie_id)
        if is_fav:
            remove_from_favorites(self.user_id, movie_id)
            self.btn_favorite.setIcon(QIcon("img/heart-regular.svg"))
        else:
            add_to_favorites(self.user_id, movie_id)
            self.btn_favorite.setIcon(QIcon("img/heart-solid.svg"))
        
    def loadVideo(self):
        if self.movie_id is None:
            return
        try:
            movie = get_film_by_id(self.movie_id)
            print(movie)
            # Normalize video path
            video_path = normalize_path(movie["trailer"])
            self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))
            self.mediaPlayer.play()
            self.lbl_title.setText(movie["title"])
            self.stackedWidget.setCurrentIndex(3)
        except Exception as e:
            print(f"Error loading video: {e}")
            msg = Alert()
            msg.error_message(f"Could not load video: {str(e)}")
        
    def mediaStateChanged(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setIcon(self.pauseIcon)
        else:
            self.playBtn.setIcon(self.playIcon)

    def positionChanged(self, position):
        self.durationBar.setValue(position)
        current_time = self.formatTime(position)
        total_time = self.formatTime(self.mediaPlayer.duration())
        self.timeLabel.setText(f"{current_time}/{total_time}")
        
    def durationChanged(self):
        self.durationBar.setRange(0, self.mediaPlayer.duration())
    
    def handleError(self):
        self.playBtn.setEnabled(False)
        error_message = self.mediaPlayer.errorString()
        self.playBtn.setText(f"Error: {error_message}")
        print(f"Media Player Error: {error_message}")
        
    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def setVolume(self, volume):
        volume = volume / 100.0
        self.audioOutput.setVolume(volume)
        if volume == 0.0:
            self.volumeBtn.setIcon(self.volumeOffIcon)
        elif volume < 0.5:
            self.audioOutput.setMuted(False)
            self.volumeBtn.setIcon(self.volumeLowIcon)
        else:
            self.volumeBtn.setIcon(self.volumeHighIcon)
            self.audioOutput.setMuted(False)
    
    def toggleMute(self):
        if self.audioOutput.isMuted():
            self.audioOutput.setMuted(False)
            if self.current_volume >= 50:
                self.volumeBtn.setIcon(self.volumeHighIcon)
            elif self.current_volume < 50:
                self.volumeBtn.setIcon(self.volumeLowIcon)
            else:
                self.volumeBtn.setIcon(self.volumeOffIcon)
            self.volumeBar.setValue(self.current_volume)
        else:
            self.audioOutput.setMuted(True)
            self.volumeBtn.setIcon(self.volumeOffIcon)
            self.current_volume = self.volumeBar.value()
            self.volumeBar.setValue(0)
    
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def formatTime(self, milliseconds):
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def catch_play_movie(self, movie_id):
        self.movie_id = movie_id
        self.loadVideo()

    def catch_detail_movie(self, movie_id):
        self.movie_id = movie_id
        self.detail_movie(self.movie_id)
        self.stackedWidget.setCurrentIndex(1)
    
    def on_favorite_changed(self):
        """Handle favorite changes - can be used to refresh favorite lists"""
        pass

if __name__ == "__main__":
    app = QApplication([])
    msg = Alert()
    login = Login()
    login.show()
    app.exec()
