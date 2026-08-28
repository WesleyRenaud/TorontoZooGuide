from __future__ import annotations

from ...app_string_provider import AppStringProvider
from ...shared.calendar_dates import DateValues
from .transportation_station_closed_status import TransportationStationClosedStatus
from ...types import Types


class TransportationStationStatusBuilder():
   @classmethod
   def build_transportation_station_closed_status(
         cls,
         transportation_station: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> TransportationStationClosedStatus:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format(
            'guestStatus.locations.temporarilyClosed',
            name=transportation_station )

      return TransportationStationClosedStatus(
         transportation_station=transportation_station,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )
