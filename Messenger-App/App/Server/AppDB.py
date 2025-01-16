import sqlite3
import os
import threading

# DEBUGGING 
VERBOSE = True

# TABLE NAMES
ACCOUNTS_TABLE_NAME = "Person"
CONTACTS_TABLE_NAME = "Contacts"
MESSAGES_TABLE_NAME = "Messages"

DB_CONN_STR_EXTERNAL = os.getcwd() + "\\Server\\db\\MS_db"
DB_CONN_STR = os.getcwd() + "\\db\\MS_db"
print(f"Conn Str: {DB_CONN_STR}")
# NOTE: THIS DB MUST BE USED SYNCHRONOUSLY
if __name__ == "__main__":
    conn = sqlite3.connect(DB_CONN_STR, check_same_thread=False)
else:
    conn = sqlite3.connect(DB_CONN_STR_EXTERNAL, check_same_thread=False)
cursor = conn.cursor()

# ---------- Database Manipulative Functions    DDL

def create_table(table_name, table_values=""):
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
                {table_values}
                    )""")
    
def drop_table(table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    print(f"SUCCESSFULLY DROPPED TABLE {table_name}")  

def overwrite_table(table_name, table_values=""):
    cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
    create_table(table_name, table_values)  
    print(f"SUCCESSFULLY OVERWRITTEN TABLE {table_name} ({table_values})")  
def truncate_table(table_name):
    cursor.execute(f"""TRUNCATE TABLE {table_name}""")
# ------------




# ---------- Data Manipulative Functions     DML
lock = threading.Lock()
def lock_cursor(func):
    def inner(**kwargs):
        if kwargs:
            try:
                #print(f"Kwargs in {inner.__name__} is: {kwargs}")
                lock.acquire(True)
                if kwargs:
                    ret = func(kwargs)
                else:
                    ret = func()
            finally:
                lock.release()
            return ret
        
        
    return inner


# No need to worry about SQL injection as these functions have no relation to forms, entries etc. Solely ran via undercovers
def commit_changes(func):
    func()
    conn.commit()



def insert_into_table_manual(table_name, keys, values) -> bool:
    """ Use at own risk """
    try:
        cursor.execute(f"""
                INSERT INTO {table_name} ({keys})
                VALUES ({values})
                """)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[DB ERROR]: {e}")
        return False



def check_columns_exist(kwargs) -> bool:
    """ Used before executing sql stuffff """
    result = cursor.execute(f"PRAGMA table_info({ACCOUNTS_TABLE_NAME})")
    COL_VALUE_NAMES_INDEX = 1
    # Used to determine if column inputted exists in table
    col_names = [column_details[COL_VALUE_NAMES_INDEX] for column_details in result.fetchall()]
    # Checks columns are apart of table first
    for key in kwargs.keys():
        if key not in col_names:
            print(f"column was not found in table? Was the table removed, or the column? table: {ACCOUNTS_TABLE_NAME} col: {key}")
            raise sqlite3.Error
    return True
def check_columns_exist_decor(func, **kwargs):
    """ Used before executing sql stuffff """
    try:
        result = cursor.execute(f"PRAGMA table_info({ACCOUNTS_TABLE_NAME})")
    except sqlite3.DatabaseError as e:
        print(e)
        return
    COL_VALUE_NAMES_INDEX = 1
    # Used to determine if column inputted exists in table
    col_names = [column_details[COL_VALUE_NAMES_INDEX] for column_details in result.fetchall()]

    # Checks columns are apart of table first
    for key in kwargs.keys():
        if key not in col_names:
            print(f"column was not found in table? Was the table removed, or the column? table: {ACCOUNTS_TABLE_NAME} col: {key}")
            raise sqlite3.Error
    # Also checks keys aren't empty
    if not kwargs:
        return func

    return func()


@check_columns_exist_decor
def update_account_login_attempt(**kwargs):
    cursor.execute(f"""UPDATE {ACCOUNTS_TABLE_NAME} 
                     SET login_attempts = {kwargs['login_attempts']}
                     WHERE ID = {kwargs['id']}
                   """)
    conn.commit()

@lock_cursor
def get_account_details(kwargs) -> list:
    if check_columns_exist(kwargs):
        # Passed test
        query_results = cursor.execute(f""" 
                SELECT * FROM {ACCOUNTS_TABLE_NAME}
                WHERE {''.join([kv[0] + '=' + "'" + kv[1] + "'" + 'AND' if (index != len(kwargs)-1) else kv[0] + '=' + "'" + kv[1] + "'" for index, kv in enumerate(kwargs.items())])}
                """)
        return query_results.fetchall()
@lock_cursor
def get_account_names_and_ids(kwargs) -> list:
    if kwargs["username"]:
        query_results = cursor.execute(f""" 
                SELECT ID, username FROM {ACCOUNTS_TABLE_NAME}
                WHERE username LIKE '{kwargs['username']}%'
                """)
    else:
        query_results = cursor.execute(f""" 
                SELECT ID, username FROM {ACCOUNTS_TABLE_NAME}
                WHERE ID='{kwargs['id']}'
                """)

    return query_results.fetchall()

def get_top_table(table_name, top=5) -> list:
    query_results = cursor.execute(f""" 
                SELECT * FROM {table_name}
                LIMIT {top}
                """)
    return query_results.fetchall()

@lock_cursor
def insert_into_account(kwargs) -> bool:
    """
    returns
        (True|False): Depending on if sql insert was successful 
    """
   
    keys_str = str(list(kwargs.keys()))
    keys_str = keys_str[1:len(keys_str)-1]

    val_str = str(list(kwargs.values()))
    val_str = val_str[1:len(val_str)-1]

    if check_columns_exist(kwargs):
        try:
            cursor.execute(f"""
                    INSERT INTO {ACCOUNTS_TABLE_NAME} ({keys_str})
                    VALUES ({val_str})
                    """)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR]: {e}")
            return False

@lock_cursor
def change_account_password(kwargs) -> bool:
    if check_columns_exist(kwargs):
        try:
            cursor.execute(f"""
                    UPDATE 
            """)
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR]: {e}")
            return False

@lock_cursor
def check_users_ipv4(kwargs):
    username = kwargs["username"]
    query_result = cursor.execute(f"""
                    SELECT ipv4 
                    FROM {ACCOUNTS_TABLE_NAME}
                    WHERE username='{username}'
                """)
    return query_result.fetchall()


def truncate_table(table_name):
    cursor.execute(f"TRUNCATE TABLE {table_name}")
    conn.commit()

def delete_account(username) -> None:
    cursor.execute(f"""
                DELETE FROM {ACCOUNTS_TABLE_NAME}
                WHERE username='{username}'
                """)

@lock_cursor
def check_account_exists(kwargs) -> bool:
    """ Username & Email for accounts MUST be UNIQUE """


    emails_matching = [] 
    usernames_matching = []

    if kwargs["username"]:
        username_search = cursor.execute(f"SELECT * FROM {ACCOUNTS_TABLE_NAME} WHERE username='{kwargs['username']}'")
        usernames_matching = username_search.fetchall()
    if kwargs["email"]:
        email_search = cursor.execute(f"SELECT * FROM {ACCOUNTS_TABLE_NAME} WHERE email='{kwargs['email']}'")
        emails_matching = email_search.fetchall()
    
    return True if len(emails_matching + usernames_matching) != 0 else False

## CONTACTS
@lock_cursor
def add_contact_relationship(kwargs) -> bool:
    """
    returns
        (True|False): Depending on if sql insert was successful 
    """
    
    id1, id2, paired_val = kwargs["id1"], kwargs["id2"], kwargs["paired_val"]

    # IF THIS RECORD DOES NOT ALREADY EXIST THEN CREATE - (PREVENTS DUPLICATES)
    if not cursor.execute(f"""
                        SELECT * FROM {CONTACTS_TABLE_NAME} 
                        WHERE AccountOneID='{id1}' and AccountTwoID='{id2}' and PairedValue='{paired_val}'
                        """).fetchall():
        # DOES NOT Exists already
        try:
            cursor.execute(f"""
                    INSERT INTO {CONTACTS_TABLE_NAME} (AccountOneID, AccountTwoID, PairedValue)
                    VALUES ({id1}, {id2}, {paired_val})
                    """)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"[DB ERROR]: {e}")
            return False
    print("This contact relationship already exists")
    return True

@lock_cursor
def get_all_contacts_chats(kwargs) -> list:
    accounts_id = kwargs["accounts_id"]
    try:
        query_results = cursor.execute(f"""
                SELECT * FROM {CONTACTS_TABLE_NAME}
                WHERE AccountOneID='{accounts_id}'
                """)
        return query_results.fetchall()
    except sqlite3.Error as e:
        print(f"[DB ERROR]: {e}")
        return False

## MESSAGES
@lock_cursor
def get_messages_for_chat(kwargs) -> list:
    sender_id, receiver_id = kwargs["sender_id"], kwargs["receiver_id"]
    try:
        query_result = cursor.execute(f"""
                    SELECT * FROM {MESSAGES_TABLE_NAME}
                    WHERE (SenderID='{sender_id}' AND ReceiverID='{receiver_id}') OR (SenderID='{receiver_id}' AND ReceiverID='{sender_id}')
            """)
        return query_result.fetchall()
    except sqlite3.Error as e:
        print(f"[DB ERROR]: {e}")
        return False

@lock_cursor
def add_message_for_chat(kwargs) -> bool:
    message_text, sender_id, receiver_id = kwargs["message_text"], kwargs["sender_id"], kwargs["receiver_id"]
    try:
        cursor.execute(f"""
                    INSERT INTO {MESSAGES_TABLE_NAME} (MessageText, SenderID, ReceiverID)
                    VALUES ('{message_text}', '{sender_id}', '{receiver_id}')
            """)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"[DB ERROR]: {e}")
        return False


if __name__ == "__main__":
    # ~#~#~#~#~#~#~#~# DATABASE MANAGEMENT TOOL HERE #~#~#~#~#~#~#~#~
    # Manually make changes to database, data stored, tests all here to db here - (untracked migrations)
   
    #delete_all_accounts()
    

    #insert_into_account(email="testvegeta@gmail.com", username="Vegeta", password="saiyan", ipv4=14213, join_date="2024/10/31", login_attempts=0)
    #insert_into_account(email="testGoku@gmail.com", username="Goku", password="saiyan", ipv4=14211, join_date="2024/10/31", login_attempts=0)

    #insert_into_table_manual(CONTACTS_TABLE_NAME, keys="AccountOneID, AccountTwoID", values="1,2")

    #add_message_for_chat("Hello Goku From Vegeta (I think)", 1, 2)
    #print(get_messages_for_chat(1, 2))

    #delete_account("patrick")
    

    #delete_all_from_table(CONTACTS_TABLE_NAME)
    print(f"Top15 accounts: {get_top_table(ACCOUNTS_TABLE_NAME, top=15)}\n\n")
    #print(f"Top10 contacts: {get_top_table(CONTACTS_TABLE_NAME, top=10)}\n\n")
    print(f"Top10 Messages: {get_top_table(MESSAGES_TABLE_NAME, top=10)}\n\n")


    #print(f"Query result is: {get_account_details({"username": 'Vegeta'})}")
    

    CHANGING_DB_CONFIGURATIONS = False
    if CHANGING_DB_CONFIGURATIONS:
        # create_table(MESSAGES_TABLE_NAME,
        #         f"""MessageID INTEGER PRIMARY KEY,
        #             MessageText text NOT NULL,
        #             SenderID INTEGER,
        #             ReceiverID INTEGER,
        #             FOREIGN KEY (SenderID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
        #             FOREIGN KEY (ReceiverID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
        #             """)

        
        # overwrite_table("Contacts", 
        #         f"""ContactID INTEGER PRIMARY KEY,
        #             AccountOneID INTERGER, 
        #             AccountTwoID INTEGER,
        #             PairedValue INTEGER,
        #             FOREIGN KEY (AccountOneID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
        #             FOREIGN KEY (AccountTwoID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
        #             """
        #             )


        overwrite_table(ACCOUNTS_TABLE_NAME,
                        """ID INTEGER PRIMARY KEY,
                            email text NOT NULL,
                            username text NOT NULL,
                            password text NOT NULL,
                            ipv4 text NOT NULL,
                            join_date DATE,
                            login_attempts INTEGER NOT NULL,
                            premium_member BIT NOT NULL
                            """)
        print("\n\nENDING CHANGING DB CONFIGURE")

else:
    # External usage
    if VERBOSE:
        print("[DB]: Using the MS_db! :)")
        print("[DB]: Checking DB is setup..")

    # NOTE - Need to automatically run through & setup database tables if tables don't exist - (May be server is running this or after a refresh)
    create_table(ACCOUNTS_TABLE_NAME,
             """ID INTEGER PRIMARY KEY,
                email text NOT NULL,
                username text NOT NULL,
                password text NOT NULL,
                ipv4 text NOT NULL,
                join_date DATE,
                login_attempts INTEGER NOT NULL,
                premium_member BIT NOT NULL
                """)

    create_table(CONTACTS_TABLE_NAME, 
            f"""ContactID INTEGER PRIMARY KEY,
                AccountOneID INTERGER, 
                AccountTwoID INTEGER,
                PairedValue INTEGER,
                FOREIGN KEY (AccountOneID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
                FOREIGN KEY (AccountTwoID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
                """)
    
    create_table(MESSAGES_TABLE_NAME,
            f"""MessageID INTEGER PRIMARY KEY,
                MessageText text NOT NULL,
                SenderID INTEGER,
                ReceiverID INTEGER,
                FOREIGN KEY (SenderID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
                FOREIGN KEY (ReceiverID) REFERENCES {ACCOUNTS_TABLE_NAME} (ID)
                """)

    if VERBOSE:
        print("[DB]: Done")

    # drop_table("Person")
    # create_table("Person", 
    #         """ID INTEGER PRIMARY KEY,
    #             username text NOT NULL,
    #             ipv4 text NOT NULL,
    #             join_date DATE""")
    