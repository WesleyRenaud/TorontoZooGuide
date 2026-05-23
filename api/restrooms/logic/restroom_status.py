from __future__ import annotations

from ...zoo_util import ZooUtil
from ...shared.strings import SharedStrings
from ...types import DateInput
from .restroom_closed_status import RestroomClosedStatus


def build_restroom_closed_status(
      restroom: str,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> RestroomClosedStatus:
   date_range = ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( restroom )

   return RestroomClosedStatus(
      restroom=restroom,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
