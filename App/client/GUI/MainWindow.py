import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                             QPushButton, QFormLayout)
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from UI_Login_Register import Ui_MainWindow


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # Sub-widgets
        self.setup_login_sw()
        self.chats_btns = []
        self.setup_home_sw()

        # NOTE: MainStackedWidget consists of inner SWs such as LoginAndRegisterSW & MainMenuSW - if confused again, variables of entries and so on are not encapsulated. 
        self.ui.MainStackedWidget.setCurrentWidget(self.ui.LoginAndRegistration)


    # Main Widget
    def setup_home_sw(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)

        # Chats page - (main menu)        
        dummy_data_chats = ["Goku", "Roshi"] + [str(i) for i in range(100)]

        for chat_names in dummy_data_chats:
            chat_ = QPushButton(chat_names, parent=self.ui.contacts_scrollAreaWidgetContents)
            chat_.clicked.connect(lambda state, x=chat_names: self.select_enter_chats_btn(x))
            self.ui.verticalLayout.addWidget(chat_)
            
        self.ui.newchat_btn.clicked.connect(self.submit_newchat_btn)
       
        # Searching for new chat page
        self.ui.search_account_back_btn.clicked.connect(self.search_account_back_btn_submit)
        self.ui.search_account_submit_btn.clicked.connect(self.serach_account_btn_submit)


        # Chat page - (For a specific chat)
        
        #self.ui.chat_history_scroll_area


    # CHATS LIST items
    def submit_newchat_btn(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Search_Contact)
        self.ui.menu_page_title.setText("Search Contact")

    def select_enter_chats_btn(self, chat_name):
        print(f"Opening chat with {chat_name}")
        # Open chat
       
    # Searching contact to start NEW CHAT
    def search_account_back_btn_submit(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats)
        self.ui.menu_page_title.setText("Chats")

    def serach_account_btn_submit(self):
        search_for = self.ui.search_account_entry.text()
        print(f"Searching for matching {search_for}")
        # send query to server
        top_five_matches = ["dummy" + str(i) for i in range(5)]
        
        # need a server message buffer - (recv messages from server and store in buffer)
        for contact_name in top_five_matches:
            contact_ = QPushButton(contact_name, parent=self.ui.search_results_scroll_area)
            contact_.clicked.connect(lambda _, x=contact_name: self.sumbit_new_chat_with_contact(x))
            self.ui.verticalLayout_2.addWidget(contact_)
    def sumbit_new_chat_with_contact(self, contact_name):
        print(f"Starting new chat with {contact_name}")



    # Login & Register Widget
    def setup_login_sw(self):
        # Set the default widget - (login)
        self.ui.LoginAndRegister_InnerSW.setCurrentWidget(self.ui.Login)

        # Setup buttons
        # Modes buttons
        self.ui.Login_or_register_selector.clicked.connect(self.select_login_btn)
        self.ui.Login_or_register_selector_2.clicked.connect(self.select_register_btn)
        
        # Submissions buttons
        self.ui.log_submit_btn.clicked.connect(self.submit_login_btn)
        self.ui.reg_submit_btn.clicked.connect(self.submit_register_btn)

    def select_login_btn(self):
        self.ui.LoginAndRegister_InnerSW.setCurrentWidget(self.ui.Login)

    def select_register_btn(self):
        self.ui.LoginAndRegister_InnerSW.setCurrentWidget(self.ui.Register)
        self.ui.MainStackedWidget.setCurrentWidget(self.ui.Home)

    def submit_login_btn(self):
        print(f"LOG INTO:     username: {self.ui.log_username_entry.text()} password: {self.ui.log_password_entry.text()}")
        self.ui.MainStackedWidget.setCurrentWidget(self.ui.Home)

    def submit_register_btn(self):
        print(f"CREATE ACCOUNT:     email: {self.ui.reg_email_entry.text()} username: {self.ui.reg_username_entry.text()} password: {self.ui.reg_password_entry.text()}")





    def show(self):
        self.main_win.show()

    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.main_win.setMinimumSize(450,550)
    main_win.main_win.setMinimumSize(750,850)

    main_win.show()

    sys.exit(app.exec())