from DB import DB

class User:
    def __init__(self, id=None,email=None,password=None,name_first=None,name_last=None,birth_date=None,created_on=None):
        self.id         = id
        self.email      = email
        self.password   = password
        self.name_first = name_first
        self.name_last  = name_last
        self.birth_date = birth_date
        self.created_on = created_on

    def __str__(self):
        output = ''

        for key, value in self.__dict__:
            output += "\n{}: {}".format(key, value)    

        return output

    
    def insert(self):
        user_id = DB.insert_user(email=self.email, password=self.password, name_first=self.name_first, name_last=self.name_last, birth_date=self.birth_date)
        self.id = user_id

    def fetch(self):
        # don't do anything if the user id isn't set
        if self.id is None:
            return
                
        db_data = DB.get_user(self.id)

        self.email      = db_data.email
        self.password   = db_data.password
        self.name_first = db_data.name_first
        self.name_last  = db_data.name_last
        self.birth_date = db_data.birth_date
        self.created_on = db_data.created_on

        

