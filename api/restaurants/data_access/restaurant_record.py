from dataclasses import dataclass


@dataclass( frozen=True )
class RestaurantRecord:
   name: object
   location: object
   sub_location: object
   description: object
   menu_link: object
   x_coord: object
   y_coord: object
   weekday_multiplier: object
   weekend_holiday_multiplier: object
