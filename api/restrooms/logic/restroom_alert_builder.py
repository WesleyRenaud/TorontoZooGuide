from ... import zoo
from .restroom_alert import RestroomAlert


def build_restroom_alert(
      restroom,
      alert_start_date,
      alert_end_date,
      message ):
   date_range = zoo.ZooUtil.resolve_open_ended_date_range(
      start_date=alert_start_date,
      end_date=alert_end_date )

   return RestroomAlert(
      restroom=restroom,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
