from DB import DB
# represents all the children of a minor category

class ProductCategoriesMinor:

    def __init__(self, product_categories_major_id: int):
        self.product_categories_major_id = product_categories_major_id

    # return all the sub categories
    def getAll(self):
        return DB.getProductMajorCategoryChildren(self.product_categories_major_id)

    def get(self, product_categories_minor_id: int):
        return DB.getProductCategoryMinor(product_categories_minor_id)
