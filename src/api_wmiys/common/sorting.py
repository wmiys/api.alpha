


class Sorting:

    # static fields
    TYPE_ASC = 'ASC'
    TYPE_DESC = 'DESC'


    #-----------------------------------------------------
    # Constructor
    # ----------------------------------------------------
    def __init__(self, acceptable_fields: list, default_field: str,  field: str=None, sort_type: str='ASC'):
        self.acceptable_fields = acceptable_fields
        self.default_field = default_field
        self.field = field or self.default_field        
        self.set_type(sort_type)
        
    #-----------------------------------------------------
    # Parse the sort url query parm
    # 
    # Parms:
    #   url_query_value (str): 'field_name:sort_type'
    #
    # Returns a bool: whether it was parsed successfully
    # ----------------------------------------------------
    def parse_sort_query(self, url_query_value: str) -> bool:        
        result = True
        
        try:
            split_query = url_query_value.split(":", 1)
            potential_field = split_query[0]
            potential_type = split_query[1]

            if not self.set_field(potential_field):
                result = False
            
            self.set_type(potential_type)

        except Exception:
            result = False

        return result


    #-----------------------------------------------------
    # Sets the type of sorting.
    #
    # Parms:
    #   new_type (str): new sorting type either 'ASC' or 'DESC'
    # ----------------------------------------------------
    def set_type(self, new_type: str):
        if new_type.upper() == self.TYPE_DESC:
            self.type = self.TYPE_DESC
        else:
            self.type = self.TYPE_ASC
    
    #-----------------------------------------------------
    # Sets the sorting field
    # 
    # Parms:
    #   new_field (str): new field to sort by
    #
    # Returns a bool: whether the field is set or not
    # ----------------------------------------------------
    def set_field(self, new_field: str) -> bool:
        if new_field not in self.acceptable_fields:
            return False
        else:
            self.field = new_field
        
        return True
    

        

class SortingSearchProducts(Sorting):
    

    DEFAULT_FIELD = 'name'
    ACCEPTABLE_FIELDS = ['id', 'name', 'description', 'product_categories_sub_id', 'product_categories_sub_name', 
        'product_categories_minor_id', 'product_categories_minor_name', 'product_categories_major_id', 
        'product_categories_major_name', 'dropoff_distance', 'price_full', 'price_half', 'image', 
        'minimum_age', 'user_id', 'user_name_first', 'user_name_last']

    def __init__(self, acceptable_fields, default_field, field=None, type=Sorting.TYPE_ASC):
        super().__init__(acceptable_fields, default_field, field=field, sort_type=type)
    