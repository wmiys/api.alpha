"""
**********************************************************************************************
This class handles all the product-category requests.
All products must be assigned a specific sub-category id.
**********************************************************************************************
"""

from ..db import DB

#------------------------------------------------------
# Returns all categories
#------------------------------------------------------
def getAll():
    categories = _getProductCategories()
    return categories


def getAllSeperate():
    categoryTable = _getProductCategories()

    majors = []
    minors = []
    subs = []

    for row in categoryTable:
        major = dict(id=row.get('major_id'), name=row.get('major_name'))
        minor = dict(id=row.get('minor_id'), name=row.get('minor_name'), parent_id=row.get('major_id'))
        sub = dict(id=row.get('sub_id'), name=row.get('sub_name'), parent_id=row.get('minor_id'))
        
        if major not in majors:
            majors.append(major)
        if minor not in minors:
            minors.append(minor)
        if sub not in subs:
            subs.append(sub)


    return dict(major=majors, minor=minors, sub=subs)

#------------------------------------------------------
# Get all the product categories
#------------------------------------------------------
def _getProductCategories():
    db = DB()
    db.connect()
    cursor = db.getCursor(True)

    sql = 'SELECT * FROM All_Categories'
    cursor.execute(sql)
    categoryTable = cursor.fetchall()

    db.close()

    return categoryTable

    

#------------------------------------------------------
# Retrieve all major categories
#------------------------------------------------------
def getMajors():
    sql = """
    SELECT  major.id                            AS id, 
            major.name                          AS name
    FROM    Product_Categories_Major major
    ORDER   BY major.name ASC
    """
    
    return _getCategoryTable(sql)



#------------------------------------------------------
# Retrieve a single major category
#------------------------------------------------------
def getMajor(id: int):
    sql = """
    SELECT  major.id                            AS id, 
            major.name                          AS name
    FROM    Product_Categories_Major major
    WHERE   major.id = %s
    LIMIT 1
    """

    parms = (id,)

    return _getCategoryTable(sql, parms)

#------------------------------------------------------
# Retrieve all minor categories belonging to a major category
#------------------------------------------------------
def getMinors(major_parent_category_id: int):
    sql = """
    SELECT  minor.id                            AS id, 
            minor.product_categories_major_id   AS product_categories_major_id, 
            minor.name                          AS name
    FROM    Product_Categories_Minor minor
    WHERE   minor.product_categories_major_id = %s
    GROUP   BY minor.id
    ORDER   BY minor.name ASC
    """

    parms = (major_parent_category_id,)
    
    return _getCategoryTable(sql, parms)


#------------------------------------------------------
# Retrieve a single minor category
#------------------------------------------------------
def getMinor(id: int):
    sql = """
    SELECT  minor.id                            AS id, 
            minor.product_categories_major_id   AS product_categories_major_id, 
            minor.name                          AS name
    FROM    Product_Categories_Minor minor
    WHERE   minor.id = %s
    LIMIT 1
    """

    parms = (id,)

    return _getCategoryTable(sql, parms)

#------------------------------------------------------
# Retrieve all sub categories beloning to a minor category
#------------------------------------------------------
def getSubs(product_categories_minor_id: int):
    sql = """
    SELECT  s.id                            AS id, 
            s.product_categories_minor_id   AS product_categories_minor_id, 
            s.name                          AS name
    FROM    Product_Categories_Sub s 
    WHERE   s.product_categories_minor_id = %s
    GROUP   BY s.id
    ORDER   BY s.name ASC
    """

    parms = (product_categories_minor_id,)

    return _getCategoryTable(sql, parms)


#------------------------------------------------------
# Retrieve a single sub category
#------------------------------------------------------
def getSub(id: int):
    sql = """
    SELECT  s.id                            AS id, 
            s.product_categories_minor_id   AS product_categories_minor_id, 
            s.name                          AS name
    FROM    Product_Categories_Sub s 
    WHERE   s.id = %s
    LIMIT 1
    """

    parms = (id,)

    return _getCategoryTable(sql, parms)



def _getCategoryTable(sql_stmt: str, parms: tuple=None):
    db = DB()
    db.connect()
    cursor = db.getCursor(True)

    if parms:
        cursor.execute(sql_stmt, parms)
    else:
        cursor.execute(sql_stmt)

    categories = cursor.fetchall()
    db.close()
    
    if len(categories) == 1:
        return categories[0]
    else:
        return categories


