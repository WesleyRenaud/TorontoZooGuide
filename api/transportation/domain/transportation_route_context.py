from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass( frozen=True )
class TransportationRouteContext:
   normalized_month: Optional[ int ]
   normalized_day: int
   target_date: date
