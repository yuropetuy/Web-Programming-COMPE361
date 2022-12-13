from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage,self).__init__()
        uic.loadUi('homepage.ui', self)

        self.logout_btn.clicked.connect(self.logout)

        self.show()

    def logout(self):
        self.login_window = LoginWindow()
        self.close()

class LoginFailed(QDialog):
    def __init__(self):
        super(LoginFailed,self).__init__()
        uic.loadUi('login_failed.ui', self)

        self.ok_btn.clicked.connect(self.ok)

        self.show()

    def ok(self):
        self.close()

class LoginWindow(QMainWindow):
    def __init__(self):
        super(LoginWindow,self).__init__()
        uic.loadUi('login.ui', self)

        #loading user data
        self.df = pd.read_excel('SemesterProject.xlsx', sheet_name = 'users')

        #connect buttons
        self.login_btn.clicked.connect(self.login_check)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def login_check(self):
        #Take inputs from line edits
        user_check = self.user_le.text()
        pass_check = self.pass_le.text()
        print(user_check)
        print(pass_check)

        user_bool = False
        pass_bool = False

        for i in range(0, len(self.df)):
            df_temp = self.df.iloc[i]
            user_idx = df_temp.username
            pass_idx = df_temp.password

            #print testing indexes
            #print(user_idx)
            #print(pass_idx)

            if(user_check == user_idx):
                user_bool = True
            if(pass_check == pass_idx):
                pass_bool = True

        if((user_bool != True) or (pass_bool != True)):
            #login failed
            print("Login Failed")
            self.login_failed = LoginFailed()
        else:
            #login succeed
            print("Login Success")
            self.homepage = HomePage()
            self.close()
        
    def cancel(self):
        self.close()         

app = QApplication([])
window = LoginWindow()

app.exec()