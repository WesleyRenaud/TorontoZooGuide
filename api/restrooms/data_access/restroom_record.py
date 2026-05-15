from dataclasses import dataclass


@dataclass( frozen=True )
class RestroomRecord:
   title: object
   x_coord: object
   y_coord: object
   is_closed: object
   closed_message: object
   closed_start: object
   closed_end: object
   alert_message: object
   alert_start_date: object
   alert_end_date: object
