import sys

from Client import *
import GlobalItems


from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                             QPushButton, QFormLayout)
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from GUI.UI_Login_Register import Ui_MainWindow


def handle_server_feedback(cmd_searching_for) -> tuple:
    """ Returns (success|failure, args) """
    while True:
        # NOTE - APPLICATION WILL BE STUCK HERE IF NO RESPONSE FROM SERVER
        server_feedback = None if len(GlobalItems.interpreted_server_feedback_buffer) == 0 else GlobalItems.interpreted_server_feedback_buffer.pop()
        if server_feedback:
            print(server_feedback)
            cmd, args = extract_cmd(server_feedback)
            print(f"'handle_server_feedback()': cmd={cmd} args={args}")
            if cmd == cmd_searching_for:
                return args    
            else:
                print("This item is not meant for here!") # Could return False. THis happens if two server feedbacks get muddled togetrher
                raise ValueError    # Could append back to 'GlobalItems.interpreted_server_feedback_buffer' BUT THIS NEEDS TO BE A QUEUE


class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)


        # Sub-widgets
        self.setup_login_sw()
        self.setup_home_sw()

        # NOTE: MainStackedWidget consists of inner SWs such as LoginAndRegisterSW & MainMenuSW - if confused again, variables of entries and so on are not encapsulated. 
        self.ui.MainStackedWidget.setCurrentWidget(self.ui.LoginAndRegistration)


    # Main Widget
    def setup_home_sw(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)
        # Chats page - (main menu)        # HERE WILL HAVE TO GET CHATS FROM SERVER
        

        self.ui.newchat_btn.clicked.connect(self.submit_newchat_btn)
        self.ui.refresh_btn.clicked.connect(self.submit_refresh_chats_btn)

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

    # REFRESH CHATS
    def submit_refresh_chats_btn(self):
        chats = []
        # NEEDS TO ASK SERVER FOR CONTACTS
        # 'Chats' needs to be populates with servers result
        for chat_names in chats:
            chat_ = QPushButton(chat_names, parent=self.ui.contacts_scrollAreaWidgetContents)
            chat_.clicked.connect(lambda state, x=chat_names: self.select_enter_chats_btn(x))
            self.ui.verticalLayout.addWidget(chat_)



    # Searching contact to start NEW CHAT
    def search_account_back_btn_submit(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)
        self.ui.menu_page_title.setText("Chats")

    def serach_account_btn_submit(self):
        IC_CMD = "SearchContact"
        search_for = self.ui.search_account_entry.text()
        print(f"Searching for matching {search_for}")
        GlobalItems.send_server_msg_buffer.append(f"#IC[{IC_CMD}]({search_for})")

        server_feedback = handle_server_feedback(cmd_searching_for=f"{IC_CMD}")
        # NOTE: For now can only accept one result (one account) - CHECK DB MANAGER TO FIX THIS IF HAVE TIME

        # Found some accounts
        top_five_matches = []

        if server_feedback != "FALSE":
            # GET PAIRS

            for i in range(int(len(server_feedback)/2)):
                pivot = i*2
                contacts_id_and_username = (server_feedback[pivot], server_feedback[pivot+1])
                user_id, username = contacts_id_and_username
                top_five_matches.append((user_id, username))

        else:
            print("No contacts found")
            top_five_matches = ["Non Found"]


        #top_five_matches = ["dummy" + str(i) for i in range(5)]

        # Clear previous searches
        for item in reversed(range(self.ui.verticalLayout_2.count())):
            self.ui.verticalLayout_2.itemAt(item).widget().setParent(None)

        # Append new searches to search box
        for contact_id_and_name in top_five_matches:
            add_contact_ = QPushButton("Add Contact " + contact_id_and_name[1], parent=self.ui.search_results_scroll_area)
            add_contact_.clicked.connect(lambda _, x=contact_id_and_name: self.sumbit_new_chat_with_contact(x))
            self.ui.verticalLayout_2.addWidget(add_contact_)

            # start_chat = QPushButton("Start Chat with " + contact_id_and_name[1], parent=self.ui.search_results_scroll_area)
            # start_chat.clicked.connect(lambda _, x=contact_id_and_name: self.submit_start_new_chat(x))
            #self.ui.verticalLayout_2.addWidget(start_chat)



    def submit_start_new_chat(self, contact_id_and_name):
        IC_CMD = "BeginChat"
        GlobalItems.send_server_msg_buffer.append(f"#IC[{IC_CMD}]({contact_id_and_name[0]})")
        # Start chat with someone



    def sumbit_new_chat_with_contact(self, contact_id_and_name):
        IC_CMD = "SaveContact"
        print(f"Adding new contact {contact_id_and_name}")
        GlobalItems.send_server_msg_buffer.append(f"#IC[{IC_CMD}]({contact_id_and_name[0]})")
        
        while True:
            # NOTE - APPLICATION WILL BE STUCK HERE IF NO RESPONSE FROM SERVER
            server_feedback = None if len(GlobalItems.interpreted_server_feedback_buffer) == 0 else GlobalItems.interpreted_server_feedback_buffer.pop()
            if server_feedback:
                cmd, args = extract_cmd(server_feedback)
                print(f"cmd={cmd} args={args}")
                if cmd == IC_CMD:
                    if args[0] == "SUCCESS":
                        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)
                        break

                    else:
                        print("Failed to save account???")
                        break




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

    def submit_login_btn(self):
        GlobalItems.send_server_msg_buffer.append(f"#IC[login]({self.ui.log_username_entry.text()}, {self.ui.log_password_entry.text()})")

        while True:
            # NOTE - APPLICATION WILL BE STUCK HERE IF NO RESPONSE FROM SERVER
            server_feedback = None if len(GlobalItems.interpreted_server_feedback_buffer) == 0 else GlobalItems.interpreted_server_feedback_buffer.pop()
            if server_feedback:
                cmd, args = extract_cmd(server_feedback)
                print(f"cmd={cmd} args={args}")
                if cmd == "login":
                    #IC[login]("Username or Password is incorrect", "False") - Example
                    feedback_str, proceed = args
                    if "False" in proceed:
                        self.ui.server_feeback_label.setText(feedback_str)
                        self.ui.log_username_entry.setText("")
                        self.ui.log_password_entry.setText("")
                    else:
                        # Load window for home page
                        self.ui.MainStackedWidget.setCurrentWidget(self.ui.Home)
                    break
                       
                else:
                    print("THIS IS NOT MEANT FOR HERE! - If error below throws, don't pop() anymore before checking that message is meant for here")
                    raise ValueError
                
        

    def submit_register_btn(self):
        print(f"CREATE ACCOUNT:     email: {self.ui.reg_email_entry.text()} username: {self.ui.reg_username_entry.text()} password: {self.ui.reg_password_entry.text()}")
        GlobalItems.send_server_msg_buffer.append(f"#IC[register]({self.ui.reg_email_entry.text()}, {self.ui.reg_username_entry.text()}, {self.ui.reg_password_entry.text()})")

        while True:
            server_feedback = None if len(GlobalItems.interpreted_server_feedback_buffer) == 0 else GlobalItems.interpreted_server_feedback_buffer.pop()
            if server_feedback:
                cmd, args = extract_cmd(server_feedback)
                if cmd == "register":
                    feedback_str, proceed = args
                    if "False" in proceed:
                        self.ui.server_feeback_label.setText(feedback_str)
                        self.ui.reg_email_entry.setText("")
                        self.ui.reg_username_entry.setText("")
                        self.ui.reg_password_entry.setText("")
                    else:
                        self.ui.MainStackedWidget.setCurrentWidget(self.ui.Home)
                    break
                else:
                    print("THIS IS NOT MEANT FOR HERE! - If error below throws, don't pop() anymore before checking that message is meant for here")
                    raise ValueError

    def show(self):
        self.main_win.show()

    
if __name__ == "__main__":
    # ~~~ Begin client thread!
    # Thread created for handling connection requests and setting a thread for each connection 
    handle_connections_thread = threading.Thread(target=get_server_handle())
    # Daemon threads ensures they finish when the program is exited - ALTHOUGH, cannot handle communication with current setup? maybe its because I am asking for an input? rather than keeping the thread read-only to send data 
    handle_connections_thread.setDaemon(True)
    handle_connections_thread.start()

    # ~~~ Start up PyQT6 Window!
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.main_win.setMinimumSize(450,550)
    main_win.main_win.setMinimumSize(750,850)

    main_win.show()

    sys.exit(app.exec())

else:
    print("Doesn't run externally yet")