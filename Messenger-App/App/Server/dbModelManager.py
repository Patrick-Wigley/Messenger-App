import AppDB as db
from typing import Union
from datetime import date
from Server_Tools import hash_data

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
        self.locked = False

    def __str__(self):
        return f"[id={self.id} username={self.username}]"
    
    def commit_changes(self):
        """ Needs to go and update the db of changes in this instance """
        pass

class ContactRelationship:
    def __init__(self, columns):
        # need person 1 & 2 IDs
        pass


#~~~~~ Model Managers ~~~~~# 
class ModelManager:
    """ Handles entire database """
    @classmethod
    def get_accounts(cls, **user_input):
        """ Get accounts that match according to query """
        return db.get_account_details(user_input)
    
    @classmethod
    def get_accounts_user_searched_for(cls, username=None, id=None):
        return db.get_account_names_and_ids(username, id)

    @classmethod
    def create_account(cls, **user_input):
        if not db.check_account_exists(username=user_input["username"], email=user_input["email"]):
            # HASH PASWORD
            hashed_password = hash_data(user_input["password"])

            return db.insert_into_account(email=user_input["email"], username=user_input["username"], password=hashed_password, ipv4=user_input["ipv4"], 
                               join_date=date.today().strftime("%d-%m-%Y"), login_attempts=0)
        else:
            return None
    
    @classmethod
    def change_password(cls, **user_input) -> bool:
        if not db.check_account_exists(username=user_input["username"]):
            return db.change_account_password(username=user_input["username"], new_password=user_input["newPassword"])
        else:
            return False

    @classmethod
    def check_new_login_location(cls, username, ipv4) -> bool:
        __result = db.check_users_ipv4(username)[0][0]
        print(f"OLD IPV4: {__result}; NEW IPV4: {ipv4}")
        return ipv4 != __result

    # CONTACTS
    @classmethod
    def create_contact_relationship(cls, **user_input) -> bool:
        return db.add_contact_relationship(id1=user_input["thisID"], id2=user_input["otherID"], paired_val=user_input["paired_value"])
    @classmethod
    def get_contacts_chats(cls, contact_id):
        return db.get_all_contacts_chats(contact_id)

    # MESSAGES
    @classmethod
    def add_message_from_to_specific(cls, message, sender_id, receiver_id) -> bool:
        return db.add_message_for_chat(message_text=message, sender_id=sender_id, receiver_id=receiver_id)
    @classmethod
    def get_messages_from_chat(cls, sender_id, receiver_id) -> list:
        return db.get_messages_for_chat(sender_id=sender_id, receiver_id=receiver_id)


class AccountManagerErrors:
    account_locked = False
    incorrect_password = False


DEFAULT_ALLOWED_LOGIN_ATTEMPTS = 7
class AccountManager:
    @classmethod
    def handle_login(cls, **user_input) -> Union[Account, None]:
        """ Could do with returning feedback (username isn't found) create a invalid instance or error obj to send & inform user? """
        __accounts = ModelManager.get_accounts(username=user_input["username"])
        __account_manager_errors = AccountManagerErrors()

        if __accounts:
            __acc_instance = Account(__accounts[0])
            if __acc_instance.login_attempts > DEFAULT_ALLOWED_LOGIN_ATTEMPTS:
                print("User attempted to login to account that's LOCKED")
                # NOTE - Need to sent SMTP to users email to unlock account - (go through a change password)
                __acc_instance.locked = True
                return __acc_instance   # WONT WORK AS ACCOUNT IS LOCKED

            
            if hash_data(user_input["password"]) != __acc_instance.password_hashed:
                # Login Was Failure - Password Inputted IS NOT CORRECT
                db.update_account_login_attempt(id=__acc_instance.id, login_attempts=__acc_instance.login_attempts+1)
                return None
            else:
                # Login Was successful
                db.update_account_login_attempt(id=__acc_instance.id, login_attempts=0)
                return __acc_instance
            

    @classmethod
    def handle_register(cls, **user_input) -> Union[Account, None]:
        __success = ModelManager.create_account(email=user_input["email"], username=user_input["username"], password=user_input["password"], ipv4=user_input["ipv4"])
        if __success:
            __accounts = ModelManager.get_accounts(username=user_input["username"])
            return Account(__accounts[0])
        else:
            return None

    @classmethod
    def handle_passwordreset(cls, username, password) -> bool:
        return ModelManager.change_password(username=username, newPassword=password)
    @classmethod
    def is_new_login_location(cls, ipv4, username) -> bool:
        return ModelManager.check_new_login_location(username, ipv4)
         

        
class ContactsManger:
    @classmethod
    def handle_search_contact(cls, username=None, id=None) -> Union[list, None]:
        """Returns 
        - List (matches found)
        - None (No matches)
          """
        __matching_accounts = ModelManager.get_accounts_user_searched_for(username=username, id=id) # INDEX 0 IS THE TUPLE (ID, username)
        if __matching_accounts:
            return __matching_accounts
        else:
            return None

    @classmethod
    def handle_add_contact_relationship(cls, **user_input) -> bool:
        """ Returns Bool - Informs on successful contact sending """
        __result = ModelManager.create_contact_relationship(thisID=user_input["thisID"], otherID=user_input["otherID"], paired_value=user_input["paired_value"])
        if __result:
            # Succesfully added contact
            return True
        else:
            return False 
    
    @classmethod
    def handle_get_all_chats_for_contact(cls, user_id) -> list:
        __results = ModelManager.get_contacts_chats(user_id)
        return __results


class MessageManager:
    @classmethod
    def handle_send_message(cls, message, sender_id, receiver_id):
        __successful = ModelManager.add_message_from_to_specific(message=message, sender_id=sender_id, receiver_id=receiver_id)
        if __successful:
            return True
        else:
            return False

    @classmethod
    def handle_get_chat_instance_messages(cls, sender_id, receiver_id):
        __result = ModelManager.get_messages_from_chat(sender_id=sender_id, receiver_id=receiver_id)
        if len(__result) != 0:
            return __result
        else:
            # Couldn't find message for this chat
            print("DEBUG No messages for this chat")
            return []


class ChatsManager:
    pass


if __name__ == "__main__":
    # Tests
    
    account = AccountManager.handle_register(email="test@gmail.com", username="test", password="test123", ipv4="192.168.0.11")
    print(account)


def remove_brackets(data) -> str:
    return str(data).replace("(", "").replace(")", "").replace("[", "").replace("]", "")