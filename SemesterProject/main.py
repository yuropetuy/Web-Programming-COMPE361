from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

class ShowUserGui(QMainWindow):
    def __init__(self, parent, id = None):
        super(ShowUserGui,self).__init__()
        uic.loadUi('show_user.ui', self)
        self.id = id
        self.parent = parent
        self.df_users = pd.read_excel('SemesterProject.xlsx', sheet_name = 'users')

        if id:
            self.user = self.df_users.loc[self.df_users.id == id].reset_index()
            self.user_le.setText(str(self.user.username[0]))
            self.pass_le.setText(str(self.user.password[0]))

            self.delete_btn.setVisible(True)
            self.update_btn.setText('Update')
            self.cancel_btn.setText('Close')

            self.update_btn.clicked.connect(self.update)
            self.delete_btn.clicked.connect(self.delete)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.delete_btn.setVisible(False)
            self.update_btn.setText('Add User')
            self.cancel_btn.setText('Cancel')

            self.update_btn.clicked.connect(self.add)
            self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def add(self):
        username = self.user_le.text()
        password = self.pass_le.text()
        self.df_users.loc[len(self.df_users.index)] = [self.df_users.id.max()+1, username, password]
        self.df_users.to_excel('SemesterProject.xlsx', sheet_name='users', index=False)
        self.parent.load_users_data()
        self.close()

    def cancel(self):
        self.close()

    def update(self):
        username = self.user_le.text()
        password = self.pass_le.text()
        self.df_users.loc[self.df_users.id == self.id, ['username', 'password']] = [username, password]
        self.df_users.to_excel('SemesterProject.xlsx', sheet_name='users', index=False)
        self.parent.load_users_data()
        self.close()

    def delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('The item will be removed!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_users = self.df_users[self.df_users.id != self.id]
            self.df_users.to_excel('SemesterProject.xlsx', sheet_name='users', index=False)
            self.close()
            self.parent.load_users_data()
        elif res == QMessageBox.Cancel:
            mb.close()

class UsersManage(QMainWindow):
    def __init__(self):
        super(UsersManage,self).__init__()
        uic.loadUi('user_manage.ui', self)

        self.row_length = 10

        self.add_user_btn.clicked.connect(self.add_user) 
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()
        self.load_users_data()

    def load_users_data(self):
        while self.layout_user.count():
            self.layout_user.itemAt(0).widget().setParent(None)
        self.df_users = pd.read_excel('SemesterProject.xlsx', sheet_name='users')
        #searchText = self.le_search.text()
        #self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_users)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            user = QLabel()
            #user.setPixmap(QPixmap(self.df_users.username[i]))
            user.setText(str(self.df_users.username[i]))
            user.setScaledContents(True)
            user.setFixedWidth(100)
            user.setFixedHeight(20)
            user.mousePressEvent = lambda e, id = self.df_users.id[i]: self.show_user(id)
            self.layout_user.addWidget(user, row_index)

    def show_user(self, id):
        self.show_user_gui = ShowUserGui(self, id)

    def add_user(self):
        self.show_user_gui = ShowUserGui(self)

    def cancel(self):
        self.homepage = HomePage()
        self.close()

class HomePage(QMainWindow):
    def __init__(self):
        super(HomePage,self).__init__()
        uic.loadUi('homepage.ui', self)

        self.user_btn.clicked.connect(self.user_open)
        self.book_btn.clicked.connect(self.book_open)
        self.order_btn.clicked.connect(self.order_open)
        self.logout_btn.clicked.connect(self.logout)

        self.show()

    def user_open(self):
        self.users_manage = UsersManage()
        self.close()

    def book_open(self):
        pass

    def order_open(self):
        pass

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
window = HomePage()

app.exec()