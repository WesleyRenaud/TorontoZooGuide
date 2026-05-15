from dataclasses import dataclass
from datetime import date


@dataclass( frozen=True )
class RestroomContext:
   target_date: date
