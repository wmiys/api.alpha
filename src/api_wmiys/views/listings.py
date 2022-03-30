"""
**********************************************************************************************

This is the view for listings. It is the data returned in the response. 

Experimenting with this.

The listing view is broken down into json objects:
    - meta
        - id
        - name
        - description
        - image
        - minimum_age
    - price:
        - full
    - categories
        - major_id
        - major_name
        - minor_id
        - minor_name
        - sub_id
        - sub_name
    - lender
        - id
        - name_first
        - name_last

**********************************************************************************************
"""

from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Meta:
    id          : int = None
    name        : str = None
    description : str = None
    image       : str = None
    minimum_age : int = None


@dataclass
class Price:
    full : float = None

@dataclass
class Categories:
    major_id  : int = None
    major_name: str = None
    minor_id  : int = None
    minor_name: str = None
    sub_id    : int = None
    sub_name  : str = None


@dataclass
class Lender:
    id        : int = None
    name_first: str = None
    name_last : str = None


@dataclass
class Listing:
    meta      : Meta       = None
    price     : Price      = None
    categories: Categories = None
    lender    : Lender     = None
