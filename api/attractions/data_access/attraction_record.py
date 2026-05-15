from dataclasses import dataclass


@dataclass( frozen=True )
class AttractionRecord:
   name: object
   free_with_admission: object
   description: object
   info_link: object
   hyperlink_text: object
   x_coord: object
   y_coord: object
   weekday_multiplier: object
   weekend_holiday_multiplier: object
