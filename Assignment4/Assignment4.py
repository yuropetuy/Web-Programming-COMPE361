from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

class ShowUserGui(QMainWindow):

    def __init__(self, id):
        super(ShowUserGui,self).__init__()
        uic.loadUi('show_user.ui', self)
        self.df_users = pd.read_excel('Assignment4.xlsx', sheet_name='users')
        self.user = self.df_users.loc[self.df_users.id == id].reset_index()
        self.le_username.setText(str(self.user.username[0]))
        self.le_password.setText(str(self.user.password[0]))
        self.lbl_photo.setPixmap(QPixmap(str(self.user.photo_path[0])))
        self.lbl_photo.setFixedWidth(300)
        self.lbl_photo.setFixedHeight(300)
        self.btn_update.clicked.connect(self.update)
        self.show()
    
    def update(self):
        new_user = self.le_username.text()
        new_pass = self.le_password.text()
        self.user.username[0] = new_user
        self.user.password[0] = new_pass
        self.user.to_excel('NewAssignment4.xlsx')
    

class UsersGui(QMainWindow):

    def __init__(self):
        super(UsersGui,self).__init__()
        uic.loadUi('users_photo.ui', self)
        self.row_length = 6
        self.show()
        self.load_users_data()

    def load_users_data(self):
        self.df_users = pd.read_excel('Assignment4.xlsx', sheet_name='users')
        row_index = -1
        for i in range(len(self.df_users)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            user = QLabel()
            user.setPixmap(QPixmap(self.df_users.photo_path[i]))
            user.setScaledContents(True)
            user.setFixedWidth(300)
            user.setFixedHeight(300)
            user.mousePressEvent = lambda e, id = self.df_users.id[i]: self.show_user(id)
            self.layout_users.addWidget(user, row_index, column_index)

    def show_user(self, id):
        self.show_user_gui = ShowUserGui(id)


app = QApplication([])
window = UsersGui()
app.exec()
