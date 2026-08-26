from __future__ import annotations

from enum import Enum


class AmenityNameField( str, Enum ):
   ATTRACTION = 'attraction'
   GIFT_SHOP = 'gift_shop'
   RESTAURANT = 'restaurant'
