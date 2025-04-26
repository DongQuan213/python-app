from PyQt6.QtWidgets import*
from PyQt6.QtCore import*
from PyQt6.QtGui import*
from PyQt6 import uic

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
        
msg = Alert()

class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/login.ui", self)

        self.confirm_pass_input = self.findChild(QLineEdit, "txt_confirm_password")
        self.email_input = self.findChild(QLineEdit, "txt_email")
        self.password_input = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_cp = self.findChild(QPushButton, "btn_eye_cp")

        self.btn_eyes.clicked.connect(lambda:self.show_password(self.btn_eyes,self.password_input))
        self.btn_login.clicked.connect(self.login)

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
        
        with open("data/user.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if data[0] == email and data[1] == password:
                    msg.success_message("Login", "Welcome to the system")
                    self.show_home(email)
                    return
                
        msg.error_message("Login", "Invalid email or password")
        self.email_input.setFocus()

    def show_register(self):
        self.register = Register()
        self.register.show()

    def show_home(self, email):
        self.home = Home(email)
        self.home.show()

class Register(Qwidget):
    def __init__(self):
        super().__init__()
        uic.loadUI("ui/register.ui", self)

        
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

        if email == "":
        msg.error_message("Register", "password is required")
        self.email_input.setFocus()
        return
    
        if name == "":
        msg.error_massage("Register", "Name is required")
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
            msg.error_message("Register", "password and confirm password do not match")
            self.password_input.setFocus()

        with open("data/users.txt", "r") as file:
            for line in file:
                data = line.strip.().split(",")
                msg.error_message("Register", "email already exists")
                self.email_input.setFocus()
                return
            
        with open("data/users.txt", "a") as file:
            file.write(f"{email}, {password}, {name}\n")
            
        msg.success_message("Register", "Account created successfully")
        self.show_login()

    def show_login(self):
        self.login = Login()
        self.login.show()

 class Home(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/register.ui", self)

