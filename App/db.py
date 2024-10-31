import sqlite3

# DEBUGGING 
VERBOSE = True

# TABLE NAMES
ACCOUNTS_TABLE_NAME = "Person"

conn = sqlite3.connect("db\\MS_db")
cursor = conn.cursor()

# ---------- Database Manipulative Functions

def create_table(table_name, table_values=""):
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
                {table_values}
                    )""")
    
def drop_table(table_name):
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

def overwrite_table(table_name, table_values=""):
    cursor.execute(f"""DROP TABLE IF EXISTS {table_name}""")
    create_table(table_name, table_values)    
# ------------




# ---------- Data Manipulative Functions
# No need to worry about SQL injection as these functions have no relation to forms, entries etc. Solely ran via undercovers


def get_account_details(**kwargs) -> list:
    if check_columns_exist(kwargs):
        # Passed test
        query_results = cursor.execute(f""" 
                SELECT * FROM {ACCOUNTS_TABLE_NAME}
                WHERE {''.join([kv[0] + '=' + "'" + kv[1] + "'" + 'AND' if (index != len(kwargs)-1) else kv[0] + '=' + "'" + kv[1] + "'" for index, kv in enumerate(kwargs.items())])}
                """)
        return query_results.fetchall()


def insert_into_account(**kwargs) -> None:
    print(f"Keys: {list(kwargs.keys())}")
    keys_str = str(list(kwargs.keys()))
    keys_str = keys_str[1:len(keys_str)-1]

    val_str = str(list(kwargs.values()))
    val_str = val_str[1:len(val_str)-1]


    if check_columns_exist(kwargs):
        cursor.execute(f"""
                INSERT INTO {ACCOUNTS_TABLE_NAME} ({keys_str})
                VALUES ({val_str})
                """)
        conn.commit()


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


if __name__ == "__main__":
    # ~#~#~#~#~#~#~#~# DATABASE MANAGEMENT TOOL HERE #~#~#~#~#~#~#~#~
    # Manually make changes to database, data stored, tests all here to db here - (untracked migrations)
   

    insert_into_account(username="Vegeta", ipv4=14213, join_date="2024/10/31")
    print(f"Query result is: {get_account_details(username='Vegeta')}")

    if False:
        overwrite_table(ACCOUNTS_TABLE_NAME,
                        """ID INTEGER PRIMARY KEY,
                            username text NOT NULL,
                            ipv4 text NOT NULL,
                            join_date DATE""")

else:
    # External usage
    if VERBOSE:
        print("[DB]: Using the MS_db! :)")
        print("[DB]: Checking DB is setup..")

    # NOTE - Need to automatically run through & setup database tables if tables don't exist - (May be server is running this or after a refresh)
    create_table(ACCOUNTS_TABLE_NAME,
                """ID INTEGER PRIMARY KEY,
                    username text NOT NULL,
                    ipv4 text NOT NULL,
                    join_date DATE""")

    if VERBOSE:
        print("[DB]: Done")

    # drop_table("Person")
    # create_table("Person", 
    #         """ID INTEGER PRIMARY KEY,
    #             username text NOT NULL,
    #             ipv4 text NOT NULL,
    #             join_date DATE""")
    