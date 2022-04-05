"""
**********************************************************************************************

This class does some common date range validation.

For default, the date range is invalid if any of these conditions are true:
    - Missing required fields
    - Invalid date str starts on
    - Invalid date str ends on
    - Ends on less than starts on
    - Starts on less than today

**********************************************************************************************
"""

from __future__ import annotations
from enum import Enum
from enum import auto
from datetime import date
from datetime import datetime


#----------------------------------------------------------
# Possible validation return codes
#----------------------------------------------------------
class ValidationReturnCodes(Enum):
    VALID                  = auto()
    NULL_VALUE             = auto()    # Missing required fields
    INVALID_DATE_STR_START = auto()    # Invalid date str starts on
    INVALID_DATE_STR_END   = auto()    # Invalid date str ends on
    END_LESS_THAN_START    = auto()    # Ends on less than starts on
    START_LESS_THAN_TODAY  = auto()    # Starts on less than today
    UNKNOWN_EXCEPTION      = auto()


#----------------------------------------------------------
# Base range validator class
#----------------------------------------------------------
class BaseDateRangeValidator:
    # Override these values for any sub-classes that want to use this class' functionality
    DATE_TYPE = date                        # the type used to check if the date objects are the same type
    TODAY     = datetime.now().date()       # today's date

    #----------------------------------------------------------
    # Constructor
    #----------------------------------------------------------
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end

    #----------------------------------------------------------
    # Run through the list of validation callbacks and check to make sure each one is valid
    # If one of the callbacks returns a non valid return code, immediatly return that
    #----------------------------------------------------------
    def validate(self) -> ValidationReturnCodes:
        validation_callbacks = self._getValidationCallbackList()

        for callback in validation_callbacks:
            callback_result = callback()

            if not callback_result == ValidationReturnCodes.VALID:
                return callback_result

        return ValidationReturnCodes.VALID
    
    #----------------------------------------------------------
    # Returns a list of all the validation callbacks to run through and execute
    #----------------------------------------------------------
    def _getValidationCallbackList(self) -> list:
        validation_method_callbacks = [
            self.areValuesSet,
            self.isStartValidDate,
            self.isEndValidDate,
            self.isStartBeforeEnd,
            self.rangeStartsToday
        ]

        return validation_method_callbacks

    #----------------------------------------------------------
    # Checks that both values are not null
    #----------------------------------------------------------
    def areValuesSet(self) -> ValidationReturnCodes:
        required_fields = [
            self.start,
            self.end,
        ]

        if None in required_fields:
            return ValidationReturnCodes.NULL_VALUE
        else:
            return ValidationReturnCodes.VALID

    #----------------------------------------------------------
    # Is start a valid date object
    #----------------------------------------------------------
    def isStartValidDate(self) -> ValidationReturnCodes:
        return self._isValidDate(self.start, ValidationReturnCodes.INVALID_DATE_STR_END)

    #----------------------------------------------------------
    # Is end a valid date object
    #----------------------------------------------------------
    def isEndValidDate(self) -> ValidationReturnCodes:
        return self._isValidDate(self.end, ValidationReturnCodes.INVALID_DATE_STR_END)

    #----------------------------------------------------------
    # Checks if the given date_obj is the same type as the class' DateType
    #---------------------------------------------------------- 
    def _isValidDate(self, date_obj, invalid_return_code: ValidationReturnCodes) -> ValidationReturnCodes:
        if isinstance(date_obj, self.DATE_TYPE):
            return ValidationReturnCodes.VALID
        else:
            return invalid_return_code

    #----------------------------------------------------------
    # Does end come after start
    #----------------------------------------------------------
    def isStartBeforeEnd(self) -> ValidationReturnCodes:
        
        try:
            if self.start > self.end:
                return ValidationReturnCodes.END_LESS_THAN_START
            else:
                return ValidationReturnCodes.VALID

        except TypeError as ex:
            print(ex)
            return ValidationReturnCodes.UNKNOWN_EXCEPTION

    #----------------------------------------------------------
    # starts_on needs cannot be anything less than today's date
    # Is start >= today's date
    #----------------------------------------------------------
    def rangeStartsToday(self) -> ValidationReturnCodes:
        if self.start < self.TODAY:
            return ValidationReturnCodes.START_LESS_THAN_TODAY
        else:
            return ValidationReturnCodes.VALID
    



class DateRangeValidator(BaseDateRangeValidator):
    pass

class DatetimeRangeValidator(BaseDateRangeValidator):
    DATE_TYPE = datetime
    TODAY     = datetime.now()


