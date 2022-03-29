from enum import Enum


class ColumnNames(str, Enum):
    MAJOR = 'product_categories_major_id'
    MINOR = 'product_categories_minor_id'
    SUB   = 'product_categories_sub_id'


class UrlCategoryNames(str, Enum):
    MAJOR = 'major'
    MINOR = 'minor'
    SUB   = 'sub'


