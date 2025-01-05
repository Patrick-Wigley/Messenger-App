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
    def get_accounts(**user_input):
        """ Get accounts that match according to query """
        return db.get_account_details(user_input)
    def get_accounts_user_searched_for(username=None, id=None):
        return db.get_account_names_and_ids(username, id)

    def create_account(**user_input):
        if not db.check_account_exists(username=user_input["username"], email=user_input["email"]):
            # NOTE PASSWORD NEEDS TO BE HASHED
            return db.insert_into_account(email=user_input["email"], username=user_input["username"], password=user_input["password"], ipv4=user_input["ipv4"], 
                               join_date=date.today().strftime("%d-%m-%Y"), login_attempts=0)
        else:
            return None


    # CONTACTS
    def create_contact_relationship(**user_input) -> bool:
        return db.add_contact_relationship(id1=user_input["thisID"], id2=user_input["otherID"], paired_val=user_input["paired_value"])
    def get_contacts_chats(contactID):
        return db.get_all_contacts_chats(contactID)

    # MESSAGES
    def add_message_from_to_specific(message, sender_id, receiver_id) -> bool:
        return db.add_message_for_chat(message_text=message, sender_id=sender_id, receiver_id=receiver_id)
    def get_messages_from_chat(sender_id, receiver_id) -> list:
        return db.get_messages_for_chat(sender_id=sender_id, receiver_id=receiver_id)



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

        
class ContactsManger:
    def handle_search_contact(username=None, id=None) -> Union[list, None]:
        """Returns 
        - List (matches found)
        - None (No matches)
          """
        __matching_accounts = ModelManager.get_accounts_user_searched_for(username=username, id=id) # INDEX 0 IS THE TUPLE (ID, username)
        if __matching_accounts:
            return __matching_accounts
        else:
            return None

    def handleAddContactRelationship(**user_input) -> bool:
        """ Returns Bool - Informs on successful contact sending """
        __result = ModelManager.create_contact_relationship(thisID=user_input["thisID"], otherID=user_input["otherID"], paired_value=user_input["paired_value"])
        if __result:
            # Succesfully added contact
            return True
        else:
            return False 

    def handle_get_all_chats_for_contact(user_id) -> list:
        __results = ModelManager.get_contacts_chats(user_id)
        return __results


    def handleSendRequest():
        pass

class MessageManager:
    def handle_send_message(message, sender_id, receiver_id):
        __successful = ModelManager.add_message_from_to_specific(message=message, sender_id=sender_id, receiver_id=receiver_id)
        if __successful:
            return True
        else:
            return False

    def handle_get_chat_instance_messages(sender_id, receiver_id):
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