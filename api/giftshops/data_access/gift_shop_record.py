from dataclasses import dataclass


@dataclass( frozen=True )
class GiftShopRecord:
   name: object
   location: object
   description: object
   x_coord: object
   y_coord: object
   weekday_multiplier: object
   weekend_holiday_multiplier: object
