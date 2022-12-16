from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

class AddFail(QDialog):
    def __init__(self):
        super(AddFail,self).__init__()
        uic.loadUi('add_fail.ui', self)

        self.ok_btn.clicked.connect(self.ok)

        self.show()

    def ok(self):
        self.close()

class ShowUserGui(QMainWindow):
    def __init__(self, parent, id = None):
        super(ShowUserGui,self).__init__()
        uic.loadUi('show_user.ui', self)
        self.id = id
        self.parent = parent
        self.df_users = pd.read_excel('Users.xlsx', sheet_name = 'users')

        if id:
            self.user = self.df_users.loc[self.df_users.id == id].reset_index()
            self.user_le.setText(str(self.user.username[0]))
            self.pass_le.setText(str(self.user.password[0]))

            self.delete_btn.setVisible(True)
            self.admin_check.setVisible(False)
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

        if(self.admin_check.isChecked() == True):
            admin = 1
        else:
            admin = 0

        user_empty_bool = True
        
        for i in range(0, len(self.df_users)):
            temp_user = self.df_users.username[i]
            if (username == temp_user):
                user_empty_bool = False

        if(user_empty_bool == False):
            self.add_fail = AddFail()

        elif(username == "" or password == ""):
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('Please fill in username and password.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close()

        else:
            comfirm = QMessageBox()
            comfirm.setWindowTitle('Are You Sure?')
            comfirm.setText('New User will be created.')
            comfirm.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            res = comfirm.exec()
            if res == QMessageBox.Ok:
                self.df_users.loc[len(self.df_users.index)] = [self.df_users.id.max()+1, username, password, admin]
                self.df_users.to_excel('Users.xlsx', sheet_name='users', index=False)
                self.parent.load_users_data()
                self.close()   
            elif res == QMessageBox.Cancel:
                comfirm.close()

    def cancel(self):
        self.close()

    def update(self):
        username = self.user_le.text()
        password = self.pass_le.text()

        if(username == "" or password == ""):
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('Please fill in username and password.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close()
        
        else:
            mb = QMessageBox()
            mb.setWindowTitle('Are You Sure?')
            mb.setText('User will be updated.')
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            res = mb.exec()
            if res == QMessageBox.Ok:
                username = self.user_le.text()
                password = self.pass_le.text()
                self.df_users.loc[self.df_users.id == self.id, ['username', 'password']] = [username, password]
                self.df_users.to_excel('Users.xlsx', sheet_name='users', index=False)
                self.parent.load_users_data()
                self.close() 
            elif res == QMessageBox.Cancel:
                mb.close()

    def delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('User will be removed!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_users = self.df_users[self.df_users.id != self.id]
            self.df_users.to_excel('Users.xlsx', sheet_name='users', index=False)
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
        self.df_users = pd.read_excel('Users.xlsx', sheet_name='users')
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

class ShowBookGui(QMainWindow):
    def __init__(self, parent, id = None):
        super(ShowBookGui,self).__init__()
        uic.loadUi('show_book.ui', self)
        self.id = id
        self.parent = parent
        self.df_books = pd.read_excel('Books.xlsx', sheet_name ='books')

        if id:
            self.book = self.df_books.loc[self.df_books.id == id].reset_index()
            
            self.title_le.setText(str(self.book.title[0]))
            self.author_le.setText(str(self.book.author[0]))
            self.stock_le.setText(str(self.book.number[0]))
            self.price_le.setText(str(self.book.price[0]))

            self.cover_path = str(self.book.cover[0])
            self.book_photo.setPixmap(QPixmap(self.cover_path))

            self.update_btn.setText('Update')
            self.cancel_btn.setText('Close')

            self.browse_btn.clicked.connect(self.browse)
            self.update_btn.clicked.connect(self.update)
            self.delete_btn.clicked.connect(self.delete)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.delete_btn.setVisible(False)
            self.update_btn.setText('Add Book')
            self.cancel_btn.setText('Cancel')

            self.browse_btn.clicked.connect(self.browse)
            self.update_btn.clicked.connect(self.add)
            self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def cancel(self):
        self.parent.load_book_data()
        self.close()

    def add(self):
        try:
            title = self.title_le.text()
            author = self.author_le.text()
            stock = int(self.stock_le.text())
            price = float(self.price_le.text())
            cover_photo = "images/default.png"
        except:
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('One or more entries need to be numerical.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close() 
        else:
            if title == "" or author == "" or stock == "" or price == "":
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('One or more entries are still blank.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close()    
            elif author.isnumeric():
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('Author needs to be a name.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close() 
            else:
                mb = QMessageBox()
                mb.setWindowTitle('Are You Sure?')
                mb.setText('New Book will be created.')
                mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                res = mb.exec()
                if res == QMessageBox.Ok:
                    self.df_books.loc[len(self.df_books.index)] = [self.df_books.id.max()+1, title, author, stock, cover_photo, price]
                    self.df_books.to_excel('Books.xlsx', sheet_name='books', index=False)
                    self.parent.load_book_data()
                    self.close()
                elif res == QMessageBox.Cancel:
                    mb.close()

    def browse(self):
        file = QFileDialog.getOpenFileName(self, 'Chose an image', '', 'PNG Files (*.png),')
        if file[0]:
            self.cover_path = file[0]
            self.book_photo.setPixmap(QPixmap(self.cover_path))

    def update(self):
        try:
            title = self.title_le.text()
            author = self.author_le.text()
            stock = int(self.stock_le.text())
            price = float(self.price_le.text())
        except:
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('One or more entries need to be numerical.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close() 
        else:
            if title == "" or author == "" or stock == "" or price == "":
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('One or more entries are still blank.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close()    
            elif author.isnumeric():
                error_mb = QMessageBox()
                error_mb.setWindowTitle('Warning')
                error_mb.setText('Author needs to be a name.')
                error_mb.setStandardButtons(QMessageBox.Ok)
                error_res = error_mb.exec()
                if error_res == QMessageBox.Ok:
                    error_mb.close() 
            else:    
                mb = QMessageBox()
                mb.setWindowTitle('Are You Sure?')
                mb.setText('Book will be updated.')
                mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                res = mb.exec()
                if res == QMessageBox.Ok:
                    self.df_books.loc[self.df_books.id == self.id, ['title', 'author', 'number', 'cover', 'price']] = [title, author, stock, self.cover_path, price]
                    self.df_books.to_excel('Books.xlsx', sheet_name='books', index=False)
                    self.parent.load_book_data()
                    self.close()
                elif res == QMessageBox.Cancel:
                    mb.close()
        
               
    def delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('The item will be removed!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_books = self.df_books[self.df_books.id != self.id]
            self.df_books.to_excel('Books.xlsx', sheet_name='books', index=False)
            self.close()
            self.parent.load_book_data()
        elif res == QMessageBox.Cancel:
            mb.close()
        
class BooksManage(QMainWindow):
    def __init__(self):
        super(BooksManage,self).__init__()
        uic.loadUi('book_manage.ui', self)

        self.row_length = 7

        self.add_btn.clicked.connect(self.add_book)
        self.cancel_btn.clicked.connect(self.cancel)

        self.load_book_data()
        self.show()
        
        
    def load_book_data(self):
        while self.layout_books.count():
            self.layout_books.itemAt(0).widget().setParent(None)
        self.df_books = pd.read_excel('Books.xlsx', sheet_name='books')
        #searchText = self.le_search.text()
        #self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_books)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            book = QLabel()
            book.setPixmap(QPixmap(self.df_books.cover[i]))
            #book.setText(str(self.df_books.title[i]))
            book.setScaledContents(False)
            book.setFixedWidth(350)
            book.setFixedHeight(250)
            book.mousePressEvent = lambda e, id = self.df_books.id[i]: self.show_book_gui(id)
            self.layout_books.addWidget(book, row_index)
        
    def show_book_gui(self, id):
        self.show_book = ShowBookGui(self, id)

    def add_book(self):
        self.show_book = ShowBookGui(self)

    def cancel(self):
        self.home_page = HomePage()
        self.close()

class ShowItemGui(QMainWindow):
    def __init__(self, parent, id = None):
        super(ShowItemGui,self).__init__()
        uic.loadUi('show_item.ui', self)
        self.id = id
        self.parent = parent
        self.df_books = pd.read_excel('Books.xlsx', sheet_name = 'books')
        self.df_orders = pd.read_excel('Orders.xlsx', sheet_name = 'orders')
        self.df_items = pd.read_excel('OrderItems.xlsx', sheet_name = 'order_items')

        if id:
            self.items = self.df_items.loc[self.df_items.id == id].reset_index()
            self.order_id_le.setText(str(self.items.order_id[0]))
            self.book_id_le.setText(str(self.items.book_id[0]))
            self.number_le.setText(str(self.items.number[0]))

            self.delete_btn.setVisible(True)
            self.update_btn.setText('Update')
            self.cancel_btn.setText('Close')

            self.update_btn.clicked.connect(self.update)
            self.delete_btn.clicked.connect(self.delete)
            self.cancel_btn.clicked.connect(self.cancel)
        else:
            self.delete_btn.setVisible(False)
            self.update_btn.setText('Add Order')
            self.cancel_btn.setText('Cancel')

            self.update_btn.clicked.connect(self.add)
            self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def add(self):
        order_id = self.order_id_le.text()
        book_id = self.book_id_le.text()
        number = self.number_le.text()

        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('New Order Item will be created.')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_items.loc[len(self.df_items.index)] = [self.df_items.id.max()+1, order_id, book_id, number]
            self.df_items.to_excel('OrderItems.xlsx', sheet_name='order_items', index=False)
            self.update_price()
            self.parent.load_item_data()
            self.close()
        elif res == QMessageBox.Cancel:
            mb.close()

    def update(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('Order will be updated.')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            order_id = self.order_id_le.text()
            book_id = self.book_id_le.text()
            number = self.number_le.text()
            self.df_items.loc[self.df_items.id == self.id, ['order_id', 'book_id', 'number']] = [order_id, book_id, number]
            self.df_items.to_excel('OrderItems.xlsx', sheet_name='order_items', index=False)
            self.update_price()
            self.parent.load_item_data()
            self.close() 
        elif res == QMessageBox.Cancel:
            mb.close()

    def delete(self):
        mb = QMessageBox()
        mb.setWindowTitle('Are You Sure?')
        mb.setText('The item will be removed!')
        mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        res = mb.exec()
        if res == QMessageBox.Ok:
            self.df_items = self.df_items[self.df_items.id != self.id]
            self.df_items.to_excel('OrderItems.xlsx', sheet_name='order_items', index=False)
            self.update_price()
            self.close()
            self.parent.load_item_data()
        elif res == QMessageBox.Cancel:
            mb.close()

    def update_price(self):
        order_id = int(self.order_id_le.text())
        book_id = int(self.book_id_le.text())
        total_price = 0
        for i in range(0,len(self.df_items.id)):
            if(self.df_items.order_id[i] == order_id):
                book_price = self.df_books.price.loc[self.df_books.id == book_id]
                total_price = total_price + (book_price * int(self.number_le.text()))

        self.df_orders.loc[self.df_orders.id == order_id, ['total_price']] = [total_price]        
        self.df_orders.to_excel('Orders.xlsx', sheet_name='orders', index=False)

    def cancel(self):
        self.close()

class ItemsManage(QMainWindow):
    def __init__(self, parent):
        super(ItemsManage,self).__init__()
        self.parent = parent
        uic.loadUi('items_manage.ui', self)

        self.row_length = 5

        self.add_btn.clicked.connect(self.add)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()
        self.load_item_data()

    def load_item_data(self):
        while self.layout_items.count():
            self.layout_items.itemAt(0).widget().setParent(None)

        self.df_items = pd.read_excel('OrderItems.xlsx', sheet_name='order_items')
        #searchText = self.le_search.text()
        #self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_items)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            items = QLabel()
            items.setText(str(f'     {self.df_items.order_id[i]}               {self.df_items.book_id[i]}               {self.df_items.number[i]}'))
            items.setScaledContents(True)
            items.setFixedWidth(500)
            items.setFixedHeight(20)
            items.mousePressEvent = lambda e, id = self.df_items.id[i]: self.show_items(id)
            self.layout_items.addWidget(items, row_index)
        self.parent.load_order_data()

    def show_items(self, id):
        self.show_order_gui = ShowItemGui(self, id)

    def add(self):
        self.show_order_gui = ShowItemGui(self)

    def cancel(self):
        self.close()

class BookBrowse(QMainWindow):
    def __init__(self, parent):
        super(BookBrowse,self).__init__()
        uic.loadUi('book_browse.ui', self)

        self.parent = parent
        self.row_length = 7

        #self.add_btn.clicked.connect(self.add_book)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()
        self.load_book_data()
        
    def load_book_data(self):
        while self.layout_books.count():
            self.layout_books.itemAt(0).widget().setParent(None)
        self.df_books = pd.read_excel('Books.xlsx', sheet_name='books')
        #searchText = self.le_search.text()
        #self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_books)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            book = QLabel()
            book.setPixmap(QPixmap(self.df_books.cover[i]))
            #book.setText(str(self.df_books.title[i]))
            book.setScaledContents(False)
            book.setFixedWidth(350)
            book.setFixedHeight(250)
            book.mousePressEvent = lambda e, id = self.df_books.id[i]: self.comfirm_book_id(id)
            self.layout_books.addWidget(book, row_index)

    def comfirm_book_id(self, id):
        self.parent.book_id = id
        self.close()

    def cancel(self):
        self.close()
        
class AddOrder(QMainWindow):
    def __init__(self, parent, id = None):
        super(AddOrder, self).__init__()
        uic.loadUi('add_order.ui', self)
        self.parent = parent
        self.id = id
        self.df_items = pd.read_excel('OrderItems.xlsx', sheet_name ='order_items')
        self.df_orders = pd.read_excel('Orders.xlsx', sheet_name ='orders')
        self.df_books = pd.read_excel('Books.xlsx', sheet_name='books')

        self.item = self.df_items.loc[self.df_items.order_id == id].reset_index()
        self.order = self.df_orders.loc[self.df_orders.id == id].reset_index()

        self.book_id = None

        self.browse_btn.clicked.connect(self.book_browse)
        self.comfirm_btn.clicked.connect(self.comfirm_check)
        self.cancel_btn.clicked.connect(self.cancel)

        self.order_id_lb.setText(str(self.item.order_id[0]))

        self.show()

    def comfirm_check(self):
        try:
            order_id = int(self.item.order_id[0])
            book_id = int(self.book_id)
            number = int(self.number_le.text())
        except:
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('Number of Books needs to be a number.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if error_res == QMessageBox.Ok:
                error_mb.close() 
        else:
            mb = QMessageBox()
            mb.setWindowTitle('Are You Sure?')
            mb.setText('This order item will be created.')
            mb.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            res = mb.exec()
            if res == QMessageBox.Ok:
                self.df_items.loc[len(self.df_books.index)] = [self.df_items.id.max()+1, order_id, book_id, number]
                self.df_items.to_excel('OrderItems.xlsx', sheet_name='order_items', index=False)
                
                self.close()
            elif res == QMessageBox.Cancel:
                mb.close()

    def book_browse(self):
        self.book_browse = BookBrowse(self)

        if(self.book_id == None):
            error_mb = QMessageBox()
            error_mb.setWindowTitle('Warning')
            error_mb.setText('Please select a book.')
            error_mb.setStandardButtons(QMessageBox.Ok)
            error_res = error_mb.exec()
            if(error_res == QMessageBox.Ok):
                error_mb.close()
        else:
            self.book_id_lb.text(self.book_id)

    def cancel(self):
        self.close()

class ShowOrderGui(QMainWindow):
    def __init__(self, parent, id = None):
        super(ShowOrderGui, self).__init__()
        uic.loadUi('show_order.ui', self)
        self.parent = parent
        self.id = id

        self.df_items = pd.read_excel('OrderItems.xlsx', sheet_name ='order_items')
        self.df_orders = pd.read_excel('Orders.xlsx', sheet_name ='orders')
        self.df_books = pd.read_excel('Books.xlsx', sheet_name = 'books')

        self.add_btn.clicked.connect(self.add_to_order)
        self.delete_btn.clicked.connect(self.delete)
        self.cancel_btn.clicked.connect(self.cancel)

        self.row_length = 5

        self.update_price()
        self.load_item_data()

        self.show()

    def update_price(self):
        order_id = self.id
        total_price = 0
        for i in range(0, len(self.df_items.id)):
            if self.df_items.order_id.iloc[i] == order_id:
                book_id = self.df_items.book_id.iloc[i]
                number = self.df_items.number.iloc[i]
                price = self.df_books.price.loc[self.df_books.id == book_id]
                total_price = total_price + (number * price)
        self.df_orders.total_price.loc[self.df_orders.id == self.id] = total_price
        self.df_orders.to_excel('Orders.xlsx', sheet_name='orders', index=False)    

    def load_item_data(self):
        price = round(float(self.df_orders.total_price.loc[self.df_orders.id == self.id]),2)
        self.price_lb.setText(str(f'${price}'))

        while self.order_item_layout.count():
            self.order_item_layout.itemAt(0).widget().setParent(None)
        #searchText = self.le_search.text()
        #self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_items)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            if(self.df_items.order_id[i] == self.id):
                items = QLabel()
                items.setText(str(f'{self.df_items.order_id[i]}            {self.df_items.book_id[i]}            {self.df_items.number[i]}'))
                items.setScaledContents(True)
                items.setFixedWidth(500)
                items.setFixedHeight(30)
                #items.mousePressEvent = lambda e, id = self.df_orders.id[i]: self.show_order(id)
                self.order_item_layout.addWidget(items, row_index)

    def add_to_order(self):
        self.add_order = AddOrder(self, self.id)

    def delete(self):
        pass

    def cancel(self):
        self.close()

class OrdersManage(QMainWindow):
    def __init__(self):
        super(OrdersManage,self).__init__()
        uic.loadUi('order_manage.ui', self)
        #self.df_orders = pd.read_excel('Orders.xlsx', sheet_name = 'orders')

        self.row_length = 5

        #self.view_btn.clicked.connect(self.view_items)
        self.cancel_btn.clicked.connect(self.cancel)
        self.add_btn.clicked.connect(self.add)

        self.show()
        self.load_order_data()

    def cancel(self):
        self.home_page = HomePage()
        self.close()

    def load_order_data(self):
        while self.layout_items.count():
            self.layout_items.itemAt(0).widget().setParent(None)

        self.df_orders = pd.read_excel('Orders.xlsx', sheet_name='orders')
        #searchText = self.le_search.text()
        #self.df_users = self.df_users[(self.df_users.username.str.contains(searchText) | self.df_users.password.str.contains(searchText))].reset_index(drop=True)
        row_index = -1
        for i in range(len(self.df_orders)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            items = QLabel()
            items.setText(str(f'{self.df_orders.id[i]}            {self.df_orders.user_id[i]}            {self.df_orders.customer_name[i]}            {self.df_orders.date[i]}            {self.df_orders.total_price[i]}'))
            items.setScaledContents(True)
            items.setFixedWidth(500)
            items.setFixedHeight(30)
            items.mousePressEvent = lambda e, id = self.df_orders.id[i]: self.show_order(id)
            self.layout_items.addWidget(items, row_index)

    def show_order(self, id):
        self.show_order_gui = ShowOrderGui(self, id)

    def add(self):
        self.show_item = CreateOrder(self)

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
        self.admin_login = AdminLogin()
        self.close()

    def book_open(self):
        self.book_manage = BooksManage()
        self.close()

    def order_open(self):
        self.order_manage = OrdersManage()
        self.close()

    def logout(self):
        self.login_window = LoginWindow()
        self.close()

class AdminFailed(QDialog):
    def __init__(self):
        super(AdminFailed,self).__init__()
        uic.loadUi('admin_failed.ui', self)

        self.ok_btn.clicked.connect(self.ok)

        self.show()

    def ok(self):
        self.close()

class AdminLogin(QMainWindow):
    def __init__(self):
        super(AdminLogin,self).__init__()
        uic.loadUi('admin_login.ui', self)

        self.df = pd.read_excel('Users.xlsx', sheet_name = 'users')

        self.login_btn.clicked.connect(self.admin_check)
        self.cancel_btn.clicked.connect(self.cancel)

        self.show()

    def admin_check(self):
        user_check = self.user_le.text()
        pass_check = self.pass_le.text()

        for i in range(0, len(self.df)):
            self.df_user = self.df.iloc[i]

            if (user_check == self.df_user.username) and (pass_check == self.df_user.password):
                if (self.df_user.admin == 1):
                    self.users_manage = UsersManage()
                    self.close()
                elif(self.df_user.admin != 1):
                    self.admin_failed = AdminFailed()


    def cancel(self):
        self.home_page = HomePage()
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
        self.df = pd.read_excel('Users.xlsx', sheet_name = 'users')

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