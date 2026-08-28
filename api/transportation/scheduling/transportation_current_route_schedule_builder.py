from __future__ import annotations

from ...shared.calendar_dates import DateValues
from .transportation_current_route_schedule import TransportationCurrentRouteSchedule
from ...types import Types


class TransportationCurrentRouteScheduleBuilder():
   @classmethod
   def build_current_transportation_route_schedule(
         cls,
         route: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> TransportationCurrentRouteSchedule:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )
      return TransportationCurrentRouteSchedule(
         route=route,
         start_date=date_range.start_date,
         end_date=date_range.end_date )
