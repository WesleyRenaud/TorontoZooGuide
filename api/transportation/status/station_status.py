from __future__ import annotations

from ...app_strings import format_app_string
from ...shared.calendar_dates import DateValues
from .station_closed_status import TransportationStationClosedStatus
from ...types import DateInput


def build_transportation_station_closed_status(
      transportation_station: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> TransportationStationClosedStatus:
   date_range = DateValues.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = format_app_string( 'guestStatus.locations.temporarilyClosed', name=transportation_station )

   return TransportationStationClosedStatus(
      transportation_station=transportation_station,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
