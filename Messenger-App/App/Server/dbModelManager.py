import db
from typing import Union
from datetime import date

class db_context:
    pass

class Account(db_context):
    #NOTE - Make this dynamic - (create class|init function at runtime?)
    def __init__(self, columns):
        self.id              = columns[0]
        self.email           = columns[1]
        self.username        = columns[2]
        self.password_hashed = columns[3]
        self.ipv4            = columns[4]
        self.date_joined     = columns[5]

        self.login_attempts = columns[6]

    def __str__(self):
        return f"[id={self.id} username={self.username}]"
    
    def commit_changes(self):
        """ Needs to go and update the db of changes in this instance """
        pass

class Friendship:
    def __init__(self, columns):
        # need person 1 & 2 IDs
        pass



#~~~~~ Model Managers ~~~~~# 
class ModelManager:
    """ Handles entire database """
    def get_accounts(**user_input):
        """ Get accounts that match according to query """
        return db.get_account_details(user_input)
    
    def create_account(**user_input):
        if not db.check_account_exists(username=user_input["username"], email=user_input["email"]):
            return db.insert_into_account(email=user_input["email"], username=user_input["username"], password=user_input["password"], ipv4=user_input["ipv4"], 
                               join_date=date.today().strftime("%d-%m-%Y"), login_attempts=0)
        else:
            return None


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
            


    def handle_register(**user_input) -> Union[Account, None]:
        __success = ModelManager.create_account(email=user_input["email"], username=user_input["username"], password=user_input["password"], ipv4=user_input["ipv4"])
        if __success:
            __accounts = ModelManager.get_accounts(username=user_input["username"])
            return Account(__accounts[0])
        else:
            return None

        


class ChatsManager:
    pass


if __name__ == "__main__":
    # Tests
    
    account = AccountManager.handle_register(email="test@gmail.com", username="test", password="test123", ipv4="192.168.0.11")
    print(account)