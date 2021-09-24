from api_wmiys.DB.DB import DB


class Location:

    def __init__(self, id: int=None, city: str=None, state_id: str=None, state_name: str=None):
        self.id = id
        self.city = city
        self.state_id = state_id
        self.state_name = state_name

    
    def load(self) -> bool:
        if not self.id:
            return False

        DB.check_connection()
        mycursor = DB.mydb.cursor(named_tuple=True)

        sql = """
        SELECT id, city, state_id, state_name
        FROM Locations l
        WHERE l.id = %s
        LIMIT 1
        """

        parms = (self.id,)
        mycursor.execute(sql, parms)
        dbResult = mycursor.fetchone()

        self.city = dbResult.city
        self.state_id = dbResult.state_id
        self.state_name = dbResult.state_name

        return True
    

    def toDict(self) -> dict:
        resultDict = dict(id=self.id, city = self.city, state_id = self.state_id, state_name = self.state_name)
        return resultDict
