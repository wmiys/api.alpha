from DB import DB
# represents all the children of a major categories

class ProductCategoriesMajor:

    def __init__(self):
        pass

    # return all the sub categories
    def getAll(self):
        return DB.getProductCategoryMajors()

    def get(self, product_categories_major_id: int):
        return DB.getProductCategoryMajor(product_categories_major_id)
