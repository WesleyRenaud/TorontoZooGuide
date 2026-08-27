from __future__ import annotations

from ...shared.duration_values import duration_minutes_to_seconds
from .transportation_day_loop import TransportationDayLoop
from .transportation_day_loop_leg_selector import TransportationDayLoopLegSelector


class TransportationRideDurationCalculator():
   @classmethod
   def seconds(
         cls,
         day_loop: TransportationDayLoop,
         from_station: str,
         to_station: str ) -> int:
      return duration_minutes_to_seconds(
         sum(
            leg.duration_minutes
            for leg in TransportationDayLoopLegSelector.select(
               day_loop,
               from_station,
               to_station ) ) )
