# Form implementation generated from reading ui file '.\UIs\Login_Register.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(723, 622)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainStackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.MainStackedWidget.setGeometry(QtCore.QRect(20, 10, 681, 591))
        self.MainStackedWidget.setObjectName("MainStackedWidget")
        self.LoginAndRegistration = QtWidgets.QWidget()
        self.LoginAndRegistration.setObjectName("LoginAndRegistration")
        self.LoginAndRegister_InnerSW = QtWidgets.QStackedWidget(parent=self.LoginAndRegistration)
        self.LoginAndRegister_InnerSW.setGeometry(QtCore.QRect(-10, 140, 691, 411))
        self.LoginAndRegister_InnerSW.setObjectName("LoginAndRegister_InnerSW")
        self.Register = QtWidgets.QWidget()
        self.Register.setObjectName("Register")
        self.reg_username_entry = QtWidgets.QLineEdit(parent=self.Register)
        self.reg_username_entry.setGeometry(QtCore.QRect(250, 180, 201, 22))
        self.reg_username_entry.setObjectName("reg_username_entry")
        self.reg_username_label = QtWidgets.QLabel(parent=self.Register)
        self.reg_username_label.setGeometry(QtCore.QRect(170, 180, 71, 21))
        self.reg_username_label.setObjectName("reg_username_label")
        self.reg_password_label = QtWidgets.QLabel(parent=self.Register)
        self.reg_password_label.setGeometry(QtCore.QRect(170, 220, 71, 21))
        self.reg_password_label.setObjectName("reg_password_label")
        self.reg_password_entry = QtWidgets.QLineEdit(parent=self.Register)
        self.reg_password_entry.setGeometry(QtCore.QRect(250, 220, 201, 22))
        self.reg_password_entry.setObjectName("reg_password_entry")
        self.reg_email_entry = QtWidgets.QLineEdit(parent=self.Register)
        self.reg_email_entry.setGeometry(QtCore.QRect(250, 140, 201, 22))
        self.reg_email_entry.setObjectName("reg_email_entry")
        self.reg_email_label = QtWidgets.QLabel(parent=self.Register)
        self.reg_email_label.setGeometry(QtCore.QRect(170, 140, 71, 21))
        self.reg_email_label.setObjectName("reg_email_label")
        self.reg_title = QtWidgets.QLabel(parent=self.Register)
        self.reg_title.setGeometry(QtCore.QRect(230, 30, 231, 61))
        self.reg_title.setObjectName("reg_title")
        self.reg_submit_btn = QtWidgets.QPushButton(parent=self.Register)
        self.reg_submit_btn.setGeometry(QtCore.QRect(240, 310, 221, 51))
        self.reg_submit_btn.setObjectName("reg_submit_btn")
        self.LoginAndRegister_InnerSW.addWidget(self.Register)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label = QtWidgets.QLabel(parent=self.page_3)
        self.label.setGeometry(QtCore.QRect(190, 180, 171, 71))
        self.label.setObjectName("label")
        self.LoginAndRegister_InnerSW.addWidget(self.page_3)
        self.Login = QtWidgets.QWidget()
        self.Login.setObjectName("Login")
        self.log_password_label = QtWidgets.QLabel(parent=self.Login)
        self.log_password_label.setGeometry(QtCore.QRect(170, 220, 71, 21))
        self.log_password_label.setObjectName("log_password_label")
        self.log_title = QtWidgets.QLabel(parent=self.Login)
        self.log_title.setGeometry(QtCore.QRect(230, 30, 231, 61))
        self.log_title.setObjectName("log_title")
        self.log_username_entry = QtWidgets.QLineEdit(parent=self.Login)
        self.log_username_entry.setGeometry(QtCore.QRect(250, 180, 201, 22))
        self.log_username_entry.setObjectName("log_username_entry")
        self.log_password_entry = QtWidgets.QLineEdit(parent=self.Login)
        self.log_password_entry.setGeometry(QtCore.QRect(250, 220, 201, 22))
        self.log_password_entry.setObjectName("log_password_entry")
        self.log_username_label = QtWidgets.QLabel(parent=self.Login)
        self.log_username_label.setGeometry(QtCore.QRect(170, 180, 71, 21))
        self.log_username_label.setObjectName("log_username_label")
        self.log_submit_btn = QtWidgets.QPushButton(parent=self.Login)
        self.log_submit_btn.setGeometry(QtCore.QRect(240, 320, 221, 51))
        self.log_submit_btn.setObjectName("log_submit_btn")
        self.server_feeback_label = QtWidgets.QLabel(parent=self.LoginAndRegistration)
        self.server_feeback_label.setGeometry(QtCore.QRect(240, 140, 291, 20))
        self.server_feeback_label.setText("")
        self.server_feeback_label.setObjectName("server_feeback_label")
        self.LoginAndRegister_InnerSW.addWidget(self.Login)
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.LoginAndRegister_InnerSW.addWidget(self.widget)
        self.Login_or_register_selector = QtWidgets.QPushButton(parent=self.LoginAndRegistration)
        self.Login_or_register_selector.setGeometry(QtCore.QRect(90, 40, 151, 51))
        self.Login_or_register_selector.setObjectName("Login_or_register_selector")
        self.Login_or_register_selector_2 = QtWidgets.QPushButton(parent=self.LoginAndRegistration)
        self.Login_or_register_selector_2.setGeometry(QtCore.QRect(430, 40, 151, 51))
        self.Login_or_register_selector_2.setObjectName("Login_or_register_selector_2")
        self.MainStackedWidget.addWidget(self.LoginAndRegistration)
        self.Home = QtWidgets.QWidget()
        self.Home.setObjectName("Home")
        self.Home_InnerSW = QtWidgets.QStackedWidget(parent=self.Home)
        self.Home_InnerSW.setGeometry(QtCore.QRect(10, 50, 661, 551))
        self.Home_InnerSW.setObjectName("Home_InnerSW")
        self.Chats_List = QtWidgets.QWidget()
        self.Chats_List.setObjectName("Chats_List")
        self.newchat_btn = QtWidgets.QPushButton(parent=self.Chats_List)
        self.newchat_btn.setGeometry(QtCore.QRect(400, 130, 75, 24))
        self.newchat_btn.setObjectName("newchat_btn")
        self.menu_contacts_scroll_area = QtWidgets.QScrollArea(parent=self.Chats_List)
        self.menu_contacts_scroll_area.setGeometry(QtCore.QRect(190, 160, 281, 361))
        self.menu_contacts_scroll_area.setMaximumSize(QtCore.QSize(281, 16777215))
        self.menu_contacts_scroll_area.setWidgetResizable(True)
        self.menu_contacts_scroll_area.setObjectName("menu_contacts_scroll_area")
        self.contacts_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.contacts_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 279, 359))
        self.contacts_scrollAreaWidgetContents.setObjectName("contacts_scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.contacts_scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.menu_contacts_scroll_area.setWidget(self.contacts_scrollAreaWidgetContents)
        self.refresh_btn = QtWidgets.QPushButton(parent=self.Chats_List)
        self.refresh_btn.setGeometry(QtCore.QRect(304, 130, 81, 24))
        self.refresh_btn.setObjectName("refresh_btn")
        self.Home_InnerSW.addWidget(self.Chats_List)
        self.Chat = QtWidgets.QWidget()
        self.Chat.setObjectName("Chat")
        self.chat_history_scroll_area = QtWidgets.QScrollArea(parent=self.Chat)
        self.chat_history_scroll_area.setGeometry(QtCore.QRect(100, 90, 461, 361))
        self.chat_history_scroll_area.setWidgetResizable(True)
        self.chat_history_scroll_area.setObjectName("chat_history_scroll_area")
        self.chat_history_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.chat_history_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 459, 359))
        self.chat_history_scrollAreaWidgetContents.setObjectName("chat_history_scrollAreaWidgetContents")
        self.chat_history_scroll_area.setWidget(self.chat_history_scrollAreaWidgetContents)
        self.Home_InnerSW.addWidget(self.Chat)
        self.Search_Contact = QtWidgets.QWidget()
        self.Search_Contact.setObjectName("Search_Contact")
        self.search_results_scroll_area = QtWidgets.QScrollArea(parent=self.Search_Contact)
        self.search_results_scroll_area.setGeometry(QtCore.QRect(180, 180, 281, 271))
        self.search_results_scroll_area.setMaximumSize(QtCore.QSize(281, 16777215))
        self.search_results_scroll_area.setWidgetResizable(True)
        self.search_results_scroll_area.setObjectName("search_results_scroll_area")
        self.search_results_scrollAreaWidgetContents = QtWidgets.QWidget()
        self.search_results_scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 279, 269))
        self.search_results_scrollAreaWidgetContents.setObjectName("search_results_scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.search_results_scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.search_results_scroll_area.setWidget(self.search_results_scrollAreaWidgetContents)
        self.search_account_entry = QtWidgets.QLineEdit(parent=self.Search_Contact)
        self.search_account_entry.setGeometry(QtCore.QRect(270, 150, 191, 22))
        self.search_account_entry.setObjectName("search_account_entry")
        self.search_account_label = QtWidgets.QLabel(parent=self.Search_Contact)
        self.search_account_label.setGeometry(QtCore.QRect(180, 150, 91, 20))
        self.search_account_label.setObjectName("search_account_label")
        self.search_account_submit_btn = QtWidgets.QPushButton(parent=self.Search_Contact)
        self.search_account_submit_btn.setGeometry(QtCore.QRect(470, 150, 75, 24))
        self.search_account_submit_btn.setObjectName("search_account_submit_btn")
        self.search_account_back_btn = QtWidgets.QPushButton(parent=self.Search_Contact)
        self.search_account_back_btn.setGeometry(QtCore.QRect(30, 70, 71, 41))
        self.search_account_back_btn.setObjectName("search_account_back_btn")
        self.Home_InnerSW.addWidget(self.Search_Contact)
        self.menu_main_title = QtWidgets.QLabel(parent=self.Home)
        self.menu_main_title.setGeometry(QtCore.QRect(170, 0, 351, 61))
        self.menu_main_title.setObjectName("menu_main_title")
        self.menu_made_by = QtWidgets.QLabel(parent=self.Home)
        self.menu_made_by.setGeometry(QtCore.QRect(510, 570, 171, 21))
        self.menu_made_by.setObjectName("menu_made_by")
        self.menu_page_title = QtWidgets.QLabel(parent=self.Home)
        self.menu_page_title.setGeometry(QtCore.QRect(310, 80, 111, 31))
        self.menu_page_title.setObjectName("menu_page_title")
        self.MainStackedWidget.addWidget(self.Home)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.MainStackedWidget.setCurrentIndex(0)
        self.LoginAndRegister_InnerSW.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.reg_username_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-weight:700;\">Username</span></p></body></html>"))
        self.reg_password_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-weight:700;\">Password</span></p></body></html>"))
        self.reg_email_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-weight:700;\">Email</span></p><p align=\"right\"><br/></p></body></html>"))
        self.reg_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">CREATE AN ACCOUNT</span></p></body></html>"))
        self.reg_submit_btn.setText(_translate("MainWindow", "Create"))
        self.label.setText(_translate("MainWindow", "Nothing here"))
        self.log_password_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-weight:700;\">Password</span></p></body></html>"))
        self.log_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">LOGIN</span></p></body></html>"))
        self.log_username_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\"><span style=\" font-weight:700;\">Username</span></p></body></html>"))
        self.log_submit_btn.setText(_translate("MainWindow", "Login"))
        self.Login_or_register_selector.setText(_translate("MainWindow", "Login"))
        self.Login_or_register_selector_2.setText(_translate("MainWindow", "Register An Account"))
        self.newchat_btn.setText(_translate("MainWindow", "New Chat"))
        self.search_account_label.setText(_translate("MainWindow", "Search Account"))
        self.refresh_btn.setText(_translate("MainWindow", "Refresh Chats"))
        self.search_account_submit_btn.setText(_translate("MainWindow", "Search"))
        self.search_account_back_btn.setText(_translate("MainWindow", "Back"))
        self.menu_main_title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:26pt; font-weight:700;\">UOD Messenger App</span></p></body></html>"))
        self.menu_made_by.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:8pt; font-weight:700;\">Made by Patrick W (100715281)</span></p></body></html>"))
        self.menu_page_title.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">Chats</span></p></body></html>"))
