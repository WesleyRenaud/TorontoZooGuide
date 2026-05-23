from __future__ import annotations

from ... import zoo
from ...shared.strings import SharedStrings
from ...types import DateInput
from .zoomobile_station_closed_status import ZoomobileStationClosedStatus


def build_zoomobile_station_closed_status(
      zoomobile_station: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> ZoomobileStationClosedStatus:
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( zoomobile_station )

   return ZoomobileStationClosedStatus(
      zoomobile_station=zoomobile_station,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
