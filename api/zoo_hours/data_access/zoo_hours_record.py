from dataclasses import dataclass


@dataclass( frozen=True )
class ZooHoursRecord:
   operating_date: object
   early_admission_time: object
   open_time: object
   last_admission_time: object
   close_time: object
