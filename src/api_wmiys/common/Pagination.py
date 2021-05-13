import math

class Pagination:
    """Pagination is responsible for containing all the data for paginating a request.

    The 2 main data members are:

    - page
    - per_page
    """

    # static properties
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE = 100 
    

    def __init__(self, a_iPage: int=None, a_iPerPage: int=None):
        self._page = a_iPage or self.DEFAULT_PAGE
        self._per_page = a_iPerPage or self.DEFAULT_PER_PAGE
    
    @property
    def page(self): 
        return self._page
    
    @page.setter
    def page(self, value: int):
        value = int(value)
        if value <= 0:
            self._page = self.DEFAULT_PAGE
        else:
            self._page = value

    @property
    def per_page(self): 
        return self._per_page
    
    @per_page.setter
    def per_page(self, value: int):
        value = int(value)
        if value not in range(1, self.MAX_PER_PAGE):
            self._per_page = self.DEFAULT_PER_PAGE
        else:
            self._per_page = value
        self._per_page = value
    
    @property
    def offset(self):
        """Returns the calculated offset for a MySQL statement.

        ---
        Offset = per_page * (page - 1)
        """
        return (self.page - 1) * self.per_page

    def to_dict(self):
        """Returns the object as a dict using the properties.

        Returns:
            dict: the object in a dictionary format
        """
        return dict(page=self.page, per_page=self.per_page, offset=self.offset)

    def getSqlStmtTotalCount(self, originalSqlStmt: str) -> str:
        """Generate an SQL statement that gets the total record count of another sql statement

        Args:
            originalSqlStmt (string): the original sql statement

        Returns:
            str: an sql statement that when executed will give the caller a count of the total records.
        """
        stmt = "SELECT COUNT(*) AS count FROM ({}) t".format(originalSqlStmt)
        return stmt
    
    def getSqlStmtLimitOffset(self, originalSqlStmt: str) -> str:
        """Appends a 'LIMIT x OFFSET y' to an sql statement.

        Args:
            originalSqlStmt (str): original sql statement

        Returns:
            str: transformed sql statement
        """
        stmt = "{} LIMIT {} OFFSET {}".format(originalSqlStmt, self.per_page, self.offset)
        return stmt

    def getPaginationResponse(self, totalRecords: int) -> dict:
        """Generates a pagination response dictionary with the current object values.

        The dictionary fields are:
        - total_records
        - total_pages

        ---
        Args:
            totalRecords (int): total number of records 

        ---
        Returns:
            dict: dictionary format of the total records and total pages
        """
        totalPages = self.totalPages(totalRecords)
        return dict(total_records=totalRecords, total_pages=totalPages)

    def totalPages(self, totalRecords: int) -> int:
        """Calculate the total number of pages given the total number of records.

        Total_Pages = CEILING(totalRecords / per_page)

        ---
        Args:
            totalRecords (int): total number of records

        ---
        Returns:
            int: total amount of pages
        """
        result = math.ceil(totalRecords / self.per_page)
        return result

