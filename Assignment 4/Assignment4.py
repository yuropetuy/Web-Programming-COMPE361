from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

class ComfirmDelete(QMainWindow):
    def __init__(self):
        super(ComfirmDelete,self).__init__()
        uic.loadUi('comfirm_delete.ui', self)
        #self.df_users = pd.read_excel('Assignment4.xlsx', sheet_name='users')
        #self.user = self.df_users.loc[self.df_users.id == id].reset_index()
        #self.id = id
        #self.btn_ok.clicked.connect(self.ok)
        #self.btn_cancel.clicked.connect(self.cancel)
        print("dialogue opened")
        self.show()


class ShowUserGui(QMainWindow):

    def __init__(self, id):
        super(ShowUserGui,self).__init__()
        uic.loadUi('show_user.ui', self)
        self.df_users = pd.read_excel('Assignment4.xlsx', sheet_name='users')
        self.user = self.df_users.loc[self.df_users.id == id].reset_index()
        self.id = id
        self.le_username.setText(str(self.user.username[0]))
        self.le_password.setText(str(self.user.password[0]))
        self.lbl_photo.setPixmap(QPixmap(str(self.user.photo_path[0])))
        self.lbl_photo.setFixedWidth(300)
        self.lbl_photo.setFixedHeight(300)
        self.btn_update.clicked.connect(self.update)
        self.btn_delete.clicked.connect(self.delete)
        self.show()

    def update(self):
        new_user = self.le_username.text()
        new_pass = self.le_password.text()
        index = self.df_users[self.df_users['id'] == self.id].index.values
        self.df_users.loc[index, ['username', 'password']] = [new_user, new_pass]
        update_writer = pd.ExcelWriter('Assignment4.xlsx')
        self.df_users.to_excel(update_writer, sheet_name = 'users', index = 0)
        update_writer.save()
        self.users_gui = UsersGui()
        self.close()

    def delete(self):
        self.comfirm_delete = ComfirmDelete()

class UsersGui(QMainWindow):

    def __init__(self):
        super(UsersGui,self).__init__()
        uic.loadUi('users_photo.ui', self)
        # self.user_labels = []
        self.row_length = 6
        self.show()
        self.load_users_data()

    def load_users_data(self):
        # for label in self.user_labels:
        #     label.setParent(None)
        while self.layout_users.count():
            self.layout_users.itemAt(0).widget().setParent(None)
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
            # self.user_labels.append(user)
            self.layout_users.addWidget(user, row_index, column_index)


    def show_user(self, id):
        self.show_user_gui = ShowUserGui(id)
        self.load_users_data()
        self.close()


app = QApplication([])
window = UsersGui()
app.exec()
