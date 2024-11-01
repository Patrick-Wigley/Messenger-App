

class db_context:
    def __str__(self):
        pass

class Account:
    def __init__(self, columns):
        self.id = columns[0]
        self.username = columns[1]
        self.ipv4 = columns[3]
        self.date_joined = columns[4]

    def __str__(self):
        return f"This is an account instance! {self.id}: {self.username}"
    
class Friendship:
    def __init__(self, columns):
        # need person 1 & 2 IDs
        pass