from __future__ import annotations

from .current_route_schedule import TransportationCurrentRouteSchedule
from ...shared.calendar_dates import DateValues
from ...types import DateInput


def build_current_transportation_route_schedule(
      route: str,
      start_date: DateInput,
      end_date: DateInput ) -> TransportationCurrentRouteSchedule:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   return TransportationCurrentRouteSchedule(
      route=route,
      start_date=date_range.start_date,
      end_date=date_range.end_date )
