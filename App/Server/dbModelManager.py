import db
from typing import Union


class db_context:
    pass

class Account(db_context):
    def __init__(self, columns):
        self.id              = columns[0]
        self.username        = columns[1]
        self.password_hashed = columns[2]
        self.ipv4            = columns[3]
        self.date_joined     = columns[4]

        self.login_attempts = columns[5]

    def __str__(self):
        return f"[id={self.id} username={self.username}]"
    
class Friendship:
    def __init__(self, columns):
        # need person 1 & 2 IDs
        pass



#~~~~~ Model Managers ~~~~~# 
class ModelManager:
    """ Handles entire database """
    def get_accounts(**kwargs):
        """ Get accounts that match according to query """
        return db.get_account_details(kwargs)
        
       


DEFAULT_ALLOWED_LOGIN_ATTEMPTS = 7
class AccountManager:
    def handle_login(**user_input) -> Union[Account, None]:
        """ Could do with returning feedback (username isn't found) create a invalid instance or error obj to send & inform user? """
        __accounts = ModelManager.get_accounts(username=user_input["username"])
        
        if __accounts:
            __acc_instance = Account(__accounts[0])
            if __acc_instance.login_attempts > DEFAULT_ALLOWED_LOGIN_ATTEMPTS:
                print("User attempted to login to account that's LOCKED")
                # NOTE - Need to sent SMTP to users email to unlock account - (go through a change password)
                return None
            # NOTE: NEED TO HASH THESE!
            if user_input["password"] != __acc_instance.password_hashed:
                db.update_account_login_attempt(id=__acc_instance.id, login_attempts=__acc_instance.login_attempts+1)
                return None
            else:
                # Login Was successful
                db.update_account_login_attempt(id=__acc_instance.id, login_attempts=0)
                return __acc_instance
            


    def create_account(**user_input) -> Union[Account, None]:
        db.insert_into_account(username=user_input["username"], password=user_input["password"], ipv4=user_input["ipv4"], join_date=user_input["join_date"], login_attempts=0)
        

class ChatsManager:
    pass