from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

#creates a class of qDialog to be used as the comfirm page for deleting a user
class ComfirmDelete(QDialog):
    def __init__(self):
        print("passed class")
        super(ComfirmDelete,self).__init__()
        print("passed super init")
        uic.loadUi('comfirm_delete.ui', self)
        print("passed loadUi")
        print("dialogue opened")


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

        #Connecting the buttons from the .ui file
        self.btn_update.clicked.connect(self.update)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_close.clicked.connect(self.close_page)

        self.show()

    def update(self):

        #new variable that hold the new user and pass from the line edits
        new_user = self.le_username.text()
        new_pass = self.le_password.text()

        #indexing given the id so we can find the row we need to change within the df_users dataframe
        index = self.df_users[self.df_users['id'] == self.id].index.values

        #replacing the old user and pass with the new ones in the dataframe
        self.df_users.loc[index, ['username', 'password']] = [new_user, new_pass]

        #writing and saving to the excel sheet
        update_writer = pd.ExcelWriter('Assignment4.xlsx')
        self.df_users.to_excel(update_writer, sheet_name = 'users', index = 0)
        update_writer.save()

        #open the users page and close the showusers page once all tasks are complete
        self.users_gui = UsersGui()
        self.close()

    def delete(self):

        #creating a objec of the class of the newly created dialog and opening it
        self.comfirm_delete = ComfirmDelete()
        self.comfirm_delete.show()

        #connecting the buttons of the object to functions
        self.comfirm_delete.btn_ok.clicked.connect(self.ok)
        self.comfirm_delete.btn_cancel.clicked.connect(self.cancel)

    #just added a close button because there was no way to return to the page without changing anything
    def close_page(self):
        self.users_gui = UsersGui()
        self.close()

    def ok(self):
        print("ok")

        #indexing the needed row again
        index = self.df_users[self.df_users['id'] == self.id].index.values

        #dropping the indexed row
        self.df_users = self.df_users.drop(labels = index, axis = 0)

        #writing and saving to the excel sheet
        update_delete = pd.ExcelWriter('Assignment4.xlsx')
        self.df_users.to_excel(update_delete, sheet_name = 'users', index = 0)
        update_delete.save()

        #opening the users page and closing 
        self.users_gui = UsersGui()
        self.comfirm_delete.close()
        self.close()

    #closes the comfirm page
    def cancel(self):
        print("cancel")
        self.comfirm_delete.close()

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
