from dataclasses import dataclass


@dataclass( frozen=True )
class RestaurantScheduleOverrideRecord:
   restaurant: object
   override_start_date: object
   override_end_date: object
   is_closed: object
   override_message: object
