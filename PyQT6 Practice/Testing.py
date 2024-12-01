from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import sys


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Messenger App")
        self.setWindowIcon(QIcon("UOD.png"))


        self.login_layout = QGridLayout()
        self.register_layout = QGridLayout()
        self.mode = True # True = Login, False = Signup
        
        self.stacked_layouts = QStackedLayout()

        

        # ~~~~~~~ Login Layout
        
        self.login_or_signup_btn = QPushButton("You Are Logging In") # Slides to You Are Signing Up
        self.login_or_signup_btn.clicked.connect(self.login_or_signup_btn_clicked)
        self.login_or_signup_btn.setFixedSize(150, 150)
              
    
        self.username_label = QLabel("Username: ")
        self.username_entry = QLineEdit()
        self.password_label = QLabel("Password: ")
        self.password_entry = QLineEdit() # Needs to be hidden characters

        self.submit_btn = QPushButton("Login")
        self.submit_btn.clicked.connect(self.submit_btn_clicked)
        
        self.login_layout.addWidget(self.login_or_signup_btn, 0,0,1,2, Qt.AlignmentFlag.AlignHCenter)
        self.login_layout.addWidget(self.username_label,      1,0)
        self.login_layout.addWidget(self.username_entry,      1,1)
        self.login_layout.addWidget(self.password_label,      2,0)
        self.login_layout.addWidget(self.password_entry,      2,1)
        self.login_layout.addWidget(self.submit_btn,          3,0,1,2)
        
        # ~~~~~~~~ Register Layout

        self.register_layout.addWidget(self.login_or_signup_btn, 0,0,1,2, Qt.AlignmentFlag.AlignHCenter)
        
        self.stacked_layouts.addWidget
        self.stacked_layouts.setCurrentWidget(self.login_layout)



        self.centre_widget = QWidget()
        self.centre_widget.setLayout(self.stacked_layouts)
        
        self.setCentralWidget(self.centre_widget)
        
        
        # widget = QWidget()
        # widget.setLayout(self.login_layout)

        
    
    def submit_btn_clicked(self):
        print(f"username: {self.username_entry.text()}, password: {self.password_entry.text()}")

    def login_or_signup_btn_clicked(self):
        if self.mode:
            self.login_or_signup_btn.setText("You Are Signing In")
            
            self.centre_widget.setLayout(self.register_layout)
        else:
            self.login_or_signup_btn.setText("You Are Logging In")
            self.centre_widget.setLayout(self.login_layout)

        self.mode = False if self.mode else True
        #self.mode = bool(~int(self.mode))

    def button_hovered(self, checked):
        print("button has been hovered " + "clicked" if checked else "not clicked")




app = QApplication(sys.argv)

# Setting up window instance
window = MainWindow()
window.setMinimumSize(400, 500)
window.setMaximumSize(800, 900)
window.show()

app.exec()