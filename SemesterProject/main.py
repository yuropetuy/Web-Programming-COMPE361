from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

class LoginWindow(QDialog):
    def __init__(self):
        super(LoginWindow,self).__init__()
        uic.loadUi('login.ui', self)

        #loading user data
        self.df_users = pd.read_excel('SemesterProject.xlsx', sheet_name = 'users')

        self.login_btn.clicked.connect(self.login_check)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def login_check(self):
        pass

    def cancel(self):
        self.close()         

app = QApplication([])
window = LoginWindow()

app.exec()