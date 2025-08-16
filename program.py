from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6 import uic
import sys
from data_io import*

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
            self.show_home(email)
            return

        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()
        self.close()

    def show_home(self, email):
        self.home = Home(email)
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
            
        with open("data/users.txt", "a") as file:
            file.write(f"{email},{password},{name}\n")
            
        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()
        self.close()

class Home(QWidget):
    def __init__(self, email):
        super().__init__()
        uic.loadUi("ui/home.ui", self)

        self.id = id
        self.user = get_user_by_id(id)

        self.stack_widget = self.findChild(QStackedWidget,"stackedWidget")
        self.btn_home = self.findChild(QPushButton,"btn_home")
        self.btn_profile = self.findChild(QPushButton,"btn_profile")
        self.btn_detail = self.findChild(QPushButton,"btn_detail")
        self.btn_watch = self.findChild(QPushButton,"btn_watch")

        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_birthday = self.findChild(QDateEdit, "txt_birthday")
        self.txt_gender = self.findChild(QComboBox, "txt_gender")
        self.btn_avatar = self.findChild(QPushButton, "btn_avatar")

        self.btn_home.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 2))
        self.btn_detail.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 1))
        self.btn_profile.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 0))
        self.btn_watch.clicked.connect(lambda: self.navigate_screen(self.stack_widget, 3))


    def navigate_screen(self,stackWidget: QStackedWidget,index:int):
        stackWidget.setCurrentIndex(index)

    def load_user_info(self):
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

if __name__ == "__main__":
    app = QApplication([])
    msg = Alert()
    login = Login()
    login.show()
    app.exec()
