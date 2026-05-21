from ... import zoo
from ...shared.strings import SharedStrings
from .restroom_closed_status import RestroomClosedStatus


def build_restroom_closed_status(
      restroom,
      start_date,
      end_date,
      message ):
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=start_date,
      end_date=end_date )

   if not message:
      message = SharedStrings.Locations.temporarily_closed( restroom )

   return RestroomClosedStatus(
      restroom=restroom,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
