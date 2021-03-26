from DB import DB
# represents all the children of a minor category

class ProductCategoriesSub:

    def __init__(self, product_categories_minor_id: int):
        self.product_categories_minor_id = product_categories_minor_id

    # return all the sub categories
    def getAll(self):
        return DB.getProductMinorCategoryChildren(self.product_categories_minor_id)

    def get(self, product_categories_sub_id: int):
        return DB.getProductCategorySub(product_categories_sub_id)
