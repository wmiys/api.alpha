"""

Pagination is responsible for containing all the data for paginating a request.

The 2 main data members are:
- page
- per_page

"""

import math
import flask






class Pagination:

    # static properties
    DEFAULT_PAGE     = 1
    DEFAULT_PER_PAGE = 20
    MAX_PER_PAGE     = 100

    #----------------------------------------------------------
    # Constructor
    #----------------------------------------------------------
    def __init__(self, page: int=None, per_page: int=None):
        self._page = page or self.DEFAULT_PAGE
        self._per_page = per_page or self.DEFAULT_PER_PAGE
    
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
    

    #----------------------------------------------------------
    # Returns the calculated offset for a MySQL statement.
    #
    # Offset = per_page * (page - 1)
    #----------------------------------------------------------
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    #----------------------------------------------------------
    # Returns the object as a dict using the properties.
    #
    # Returns a dict: the object in a dictionary format
    #----------------------------------------------------------
    def to_dict(self) -> dict:

        return dict(
            page     = self.page,
            per_page = self.per_page,
            offset   = self.offset
        )

    #----------------------------------------------------------
    # Generate an SQL statement that gets the total record count 
    # of another sql statement.
    #
    # Parms:
    #   originalSqlStmt: the original sql statement
    #
    # Returns a str:
    #   an sql statement that when executed will give the caller a count of the total records.
    #----------------------------------------------------------
    def getSqlStmtTotalCount(self, originalSqlStmt: str) -> str:
        return f"SELECT COUNT(*) AS count FROM ({originalSqlStmt}) t"
    

    #----------------------------------------------------------
    # Appends a 'LIMIT x OFFSET y' to an sql statement.
    #
    # Parms:
    #     originalSqlStmt: original sql statement
    #
    # Returns a str: transformed sql statement
    #----------------------------------------------------------
    def getSqlStmtLimitOffset(self, originalSqlStmt: str) -> str:
        return f"{originalSqlStmt} LIMIT {self.per_page} OFFSET {self.offset}"
        

    #----------------------------------------------------------
    # Generates a pagination response dictionary with the 
    # current object values.
    #
    # The dictionary fields are:
    #   - total_records
    #   - total_pages
    #
    # Parms:
    #     totalRecords: total number of records 
    #
    # Returns a dict:
    #     dictionary format of the total records and total pages
    #----------------------------------------------------------
    def getPaginationResponse(self, total_records: int) -> dict:
        totalPages = self.totalPages(total_records)
        return dict(total_records=total_records, total_pages=totalPages)

    #----------------------------------------------------------
    # Calculate the total number of pages given the total
    # number of records.
    #
    # Total_Pages = CEILING(totalRecords / per_page)
    #
    # Parms:
    #     totalRecords: total number of records
    #
    # Returns an int: total amount of pages
    #----------------------------------------------------------
    def totalPages(self, totalRecords: int) -> int:
        return math.ceil(totalRecords / self.per_page)




def getRequestPaginationParms() -> Pagination:
    pagination = Pagination()

    pagination.page = flask.request.args.get('page') or Pagination.DEFAULT_PAGE
    pagination.per_page = flask.request.args.get('per_page') or Pagination.DEFAULT_PER_PAGE

    return pagination

