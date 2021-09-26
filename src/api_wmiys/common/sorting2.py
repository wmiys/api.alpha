


class Sorting:

    # static fields
    TYPE_ASC = 'ASC'
    TYPE_DESC = 'DESC'

    def __init__(self, acceptable_fields: list, default_field: str,  field: str=None, type: str='ASC'):
        self.acceptable_fields = list(acceptable_fields)
        self.default_field = default_field
        
        if not field:
            self.field = self.default_field
        else:
            self.field = field
        
        self.set_type(type)
        
    
    def set_type(self, new_type: str):
        """Sets the type of sorting.

        Args:
            new_type (str): new sorting type either 'ASC' or 'DESC'
        """

        if new_type.upper() == self.TYPE_DESC:
            self.type = self.TYPE_DESC
        else:
            self.type = self.TYPE_ASC
    
    def set_field(self, new_field: str) -> bool:
        """Sets the sorting field

        Args:
            new_field (str): new field to sort by

        Returns:
            bool: whether the field is set or not
        """

        if new_field not in self.acceptable_fields:
            return False
        else:
            self.field = new_field
        
        return True
    
    def parse_sort_query(self, url_query_value: str) -> bool:
        """Parse the sort url query parm

        Args:
            url_query_value (str): 'field_name:sort_type'

        Returns:
            bool: whether it was parsed successfully
        """
        
        split_query = url_query_value.split(":", 1)
        potential_field = split_query[0]
        potential_type = split_query[1]

        if not self.set_field(potential_field):
            return False
        
        self.set_type(potential_type)
        return True
        

class SortingSearchProducts(Sorting):
    

    DEFAULT_FIELD = 'name'
    ACCEPTABLE_FIELDS = ['id', 'name', 'description', 'product_categories_sub_id', 'product_categories_sub_name', 
        'product_categories_minor_id', 'product_categories_minor_name', 'product_categories_major_id', 
        'product_categories_major_name', 'dropoff_distance', 'price_full', 'price_half', 'image', 
        'minimum_age', 'user_id', 'user_name_first', 'user_name_last']

    def __init__(self, acceptable_fields, default_field, field=None, type=Sorting.TYPE_ASC):
        super().__init__(acceptable_fields, default_field, field=field, type=type)
    