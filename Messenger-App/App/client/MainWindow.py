import sys

from Client import *
import GlobalItems


from PyQt6.QtWidgets import (QApplication, QMainWindow, 
                             QPushButton, QLabel)
from PyQt6.QtGui import *
from PyQt6.QtCore import *

from GUI.UI_Login_Register import Ui_MainWindow

# -=--=-=-=--= TOOLS 
def handle_server_feedback(cmd_searching_for, verbose=False) -> tuple:
    """ THIS FUNCTION JUST RETURNS THE ARGUMENTS SENT FROM THE SERVER IF FINDS THE COMMAND SEARCHING FOR """
    while True:
        # NOTE - APPLICATION WILL BE STUCK HERE IF NO RESPONSE FROM SERVER
        server_feedback = None if len(GlobalItems.interpreted_server_feedback_buffer) == 0 else GlobalItems.interpreted_server_feedback_buffer.pop()
        if server_feedback:
            cmd, args = extract_cmd(server_feedback)
            if verbose:
                print(server_feedback)
                print(f"'handle_server_feedback()': cmd={cmd} args={args}")
            if cmd == cmd_searching_for:
                return args
            else:
                print("This item is not meant for here!" ) # Could return False. THis happens if two server feedbacks get muddled togetrher
                print(f"Searching for cmd: {cmd_searching_for} But received: {cmd}")
                raise ValueError    # Could append back to 'GlobalItems.interpreted_server_feedback_buffer' BUT THIS NEEDS TO BE A QUEUE


class EventListenerThread(QThread):
    """ Waits to handle response from server """
    task = pyqtSignal()
    broadcast_task  = pyqtSignal(str)
    broadcast_fail_task = pyqtSignal()
    send_chat_task = pyqtSignal(bool)
    chat_history_task = pyqtSignal(list)
    update_chat_history_task = pyqtSignal(str)

    def run(self):
        while True:
            event = None if len(GlobalItems.window_event_trigger_buffer) == 0 else GlobalItems.window_event_trigger_buffer.pop()
            if event:
                cmd, args = extract_cmd(event)
                if cmd == CMD.BROADCAST:
                    self.broadcast_task.emit(args[0])
                
                elif cmd == CMD.BROADCAST_NOT_ALLOWED:
                    self.broadcast_fail_task.emit()
                
                elif cmd == CMD.SENDMESSAGE:
                    self.send_chat_task.emit(args[0])
                
                elif cmd == CMD.GETMESSAGEHISTORY:
                    print(args)
                    self.chat_history_task.emit(args)

                elif cmd == CMD.UPDATE_CHAT_LOG_LIVE:
                    self.update_chat_history_task.emit(str(args[0]))


# -=--=-=-=--= WINDOW
class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.current_chat_opened_with = None # This gets set to the (contact_id, contact_username) currently in

        # Sub-widgets
        self.setup_login_sw()
        self.setup_home_sw()

        # NOTE: MainStackedWidget consists of inner SWs such as LoginAndRegisterSW & MainMenuSW - if confused again, variables of entries and so on are not encapsulated. 
      
        self.ui.MainStackedWidget.setCurrentWidget(self.ui.LoginAndRegistration)


        self.event_listener_t = EventListenerThread()
        # SETUP EVENTS
        self.event_listener_t.broadcast_task.connect(self.handle_broadcast_request)
        self.event_listener_t.broadcast_fail_task.connect(self.handle_broadcast_fail)
        self.event_listener_t.send_chat_task.connect(self.handle_enter_message)
        self.event_listener_t.chat_history_task.connect(self.populate_dm_chat_history)
        self.event_listener_t.update_chat_history_task.connect(self.handle_update_chat_log_live)

        self.event_listener_t.start()


    # Main Widget
    def setup_home_sw(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)
        # Chats page - (main menu)        # HERE WILL HAVE TO GET CHATS FROM SERVER
        

        self.ui.newchat_btn.clicked.connect(self.submit_newchat_btn)
        self.ui.refresh_btn.clicked.connect(self.submit_refresh_chats_btn)

        # Searching for new chat page
        self.ui.search_account_back_btn.clicked.connect(self.return_to_contactchats_page)
        self.ui.search_account_submit_btn.clicked.connect(self.serach_account_btn_submit)


        # Chat page - (For a specific chat)
        self.ui.enter_message_entry.returnPressed.connect(self.submit_enter_message)
        self.ui.Chat_send_btn.clicked.connect(self.submit_enter_message)
        self.ui.Chat_back_btn.clicked.connect(self.return_to_contactchats_page)
        

        self.ui.broadcast_entry.returnPressed.connect(self.send_broadcast)


    def send_broadcast(self):
        GlobalItems.request_out_buffer.append(f"#IC[{CMD.BROADCAST}]('{self.ui.broadcast_entry.text()}')")


    def handle_broadcast_request(self, msg):
        self.ui.broadcast_history.setText(msg)

    def handle_broadcast_fail(self):
        self.ui.broadcast_entry.setText("You have to be a Premium Member to send broadcasts")

    # Chat With Someone
    def submit_enter_message(self):
        IC_CMD = "SendMessage"
        message = self.ui.enter_message_entry.text()
        send_to = self.current_chat_opened_with[0]
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]('{message}', '{send_to}')")
        

    def handle_enter_message(self, response):
        if response:
            self.select_enter_chats_btn(self.current_chat_opened_with) # Refresh the chats messages - Terrible method
        else:
            print("Failed to send message??")


    def select_call_person(self, contact_details):
        # contact_details = (ID, Name)
        
        # Continue here
        IC_CMD = "CallPerson"
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]('{contact_details[0]}')")


    def select_enter_chats_btn(self, contact_details):
        """ Open chat """
        IC_CMD = "GetMessagesHistory"
        contacts_id, contacts_username = contact_details
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]({contacts_id})")
        self.current_chat_opened_with = contact_details

        # CLEAR SEND MESSAGE BAR
        self.ui.enter_message_entry.setText("")
        
        # Handle server feedback    
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chat)
        self.ui.loading_chat_history_label.setVisible(True)

    def populate_dm_chat_history(self, message_data, refresh_entire_chatlog=True):
        self.ui.loading_chat_history_label.setVisible(False)
        if refresh_entire_chatlog:
            # Handle server feedback
            # CLEAR CHAT-LOG
            for msg in reversed(range(self.ui.verticalLayout_chat_history.count())):
                self.ui.verticalLayout_chat_history.itemAt(msg).widget().setParent(None)
        
        
            # POPULATE CHAT-LOG
            for msg_details in message_data:
                _, msg_text, msg_sender, msg_receiver = msg_details
                msg = QLabel(f"[{msg_sender}] {msg_text}", parent=self.ui.chat_history_scrollAreaWidgetContents)
                self.ui.verticalLayout_chat_history.addWidget(msg)
        else:
            _, msg_text, msg_sender, msg_receiver = message_data
            new_msg = QLabel(f"[{msg_sender}] {msg_text}", parent=self.ui.chat_history_scrollAreaWidgetContents)
            self.ui.verticalLayout_chat_history.addWidget(new_msg)
    def handle_update_chat_log_live(self, id_receiving_from):
        print(self.ui.Home_InnerSW.currentWidget() == self.ui.Chat)
        print(f"{self.current_chat_opened_with[0]} == {id_receiving_from}")
        if self.ui.Home_InnerSW.currentWidget() == self.ui.Chat and str(self.current_chat_opened_with[0]) == id_receiving_from:
            # Only refresh if chat is open with person receiving message from
            self.select_enter_chats_btn(self.current_chat_opened_with)



    # REFRESH CHATS
    def submit_refresh_chats_btn(self):
        """ GETS CONTACTS CHATS """

        IC_CMD = "GetSavedContactsChats"
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]()")        
        args = handle_server_feedback(IC_CMD)

        # populate the "chat with contact" button(s) to chats list 
        if args[0] != False:
            # CLEAR Contact list - (this prevents duplicates from coming up in the GUI)
            for contact_chat in reversed(range(self.ui.verticalLayout.count())):
                self.ui.verticalLayout.itemAt(contact_chat).widget().setParent(None)

            for contact_details in args:
                contact_id, contact_name = contact_details
                chat_ = QPushButton(contact_name, parent=self.ui.contacts_scrollAreaWidgetContents)
                chat_.clicked.connect(lambda _, x=(contact_id, contact_name): self.select_enter_chats_btn(x))
                call_ = QPushButton(f"Call - {contact_name}", parent=self.ui.contacts_scrollAreaWidgetContents)
                call_.clicked.connect(lambda _, x=(contact_id, contact_name): self.select_call_person(x))

                self.ui.verticalLayout.addWidget(chat_)
                self.ui.verticalLayout.addWidget(call_)
        else:
            print("This account has no contacts")


    # CHATS LIST items
    def submit_newchat_btn(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Search_Contact)
        self.ui.menu_page_title.setText("Search Contact")


    # Searching contact to start NEW CHAT
    def return_to_contactchats_page(self):
        self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)
        self.ui.menu_page_title.setText("Chats")

    def serach_account_btn_submit(self):
        IC_CMD = "SearchContact"
        search_for = self.ui.search_account_entry.text()
        print(f"Searching for matching {search_for}")
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]('{search_for}')")

        server_feedback = handle_server_feedback(cmd_searching_for=IC_CMD)
     
        top_five_matches = []
        if server_feedback[0]:
            # GET PAIRS
            top_five_matches = server_feedback
        else:
            print("No contacts found")
            
        # Clear previous searches
        for item in reversed(range(self.ui.verticalLayout_2.count())):
            self.ui.verticalLayout_2.itemAt(item).widget().setParent(None)

        # Append new searches to search box
        for contact_id_and_name in top_five_matches:
            add_contact_ = QPushButton("Add Contact " + contact_id_and_name[1], parent=self.ui.search_results_scroll_area)
            add_contact_.clicked.connect(lambda _, x=contact_id_and_name: self.sumbit_new_chat_with_contact(x))
            self.ui.verticalLayout_2.addWidget(add_contact_)


    def sumbit_new_chat_with_contact(self, contact_id_and_name):
        IC_CMD = "SaveContact"
        print(f"Adding new contact {contact_id_and_name}")
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]('{contact_id_and_name[0]}')")
        
        args = handle_server_feedback(cmd_searching_for=IC_CMD)
        if args[0] == True:
            self.ui.Home_InnerSW.setCurrentWidget(self.ui.Chats_List)
        else:
            print("Failed to save account???")
        

    # Login & Register Widget
    def setup_login_sw(self):
        # Set the default widget - (login)
        self.ui.LoginAndRegister_InnerSW.setCurrentWidget(self.ui.Login)

        # Cache
        with open("client/cache.txt", "r") as cached_login:
            data = cached_login.read()
            username, password = str(data).split(",")
            self.ui.log_username_entry.setText(username)
            self.ui.log_password_entry.setText(password)


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
        IC_CMD = "login"

        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]('{self.ui.log_username_entry.text()}', '{self.ui.log_password_entry.text()}')")
        args = handle_server_feedback(cmd_searching_for=f"{IC_CMD}")

        feedback_str, proceed = args
        if not proceed:
            self.ui.server_feeback_label.setText(feedback_str)
            self.ui.log_username_entry.setText("")
            self.ui.log_password_entry.setText("")
        else:
            # Load window for home page
            self.ui.MainStackedWidget.setCurrentWidget(self.ui.Home)
               
   

    def submit_register_btn(self):
        IC_CMD = "register"
        print(f"CREATE ACCOUNT:     email: {self.ui.reg_email_entry.text()} username: {self.ui.reg_username_entry.text()} password: {self.ui.reg_password_entry.text()}")
        GlobalItems.request_out_buffer.append(f"#IC[{IC_CMD}]('{self.ui.reg_email_entry.text()}', '{self.ui.reg_username_entry.text()}', '{self.ui.reg_password_entry.text()}', '{self.ui.reg_preimum_code_entry.text()}')")
        args = handle_server_feedback(cmd_searching_for=f"{IC_CMD}")

        feedback_str, proceed = args
        if proceed:
            self.ui.MainStackedWidget.setCurrentWidget(self.ui.Home)
        else:
            self.ui.server_feeback_label.setText(feedback_str)
            self.ui.reg_email_entry.setText("")
            self.ui.reg_username_entry.setText("")
            self.ui.reg_password_entry.setText("")

    def show(self):
        self.main_win.show()







def on_quit_handle():
    print("Closing")
    GlobalItems.request_out_buffer.append(f"#IC[{CMD.EXIT}]()")


if __name__ == "__main__":
    # ~~~ Begin client thread!
    # Thread created for handling connection requests and setting a thread for each connection 
    handle_connections_thread = threading.Thread(target=get_server_handle())
    # Daemon threads ensures they finish when the program is exited - ALTHOUGH, cannot handle communication with current setup? maybe its because I am asking for an input? rather than keeping the thread read-only to send data 
    handle_connections_thread.setDaemon(True)
    handle_connections_thread.start()

    # ~~~ Start up PyQT6 Window!
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(on_quit_handle)

    main_win = MainWindow()
    main_win.main_win.setMinimumSize(450,550)
    main_win.main_win.setMinimumSize(750,850)

    main_win.show()
    
    sys.exit(app.exec())


else:
    print("Doesn't run externally yet")


