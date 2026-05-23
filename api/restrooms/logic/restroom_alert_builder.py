from __future__ import annotations

from ...zoo_util import ZooUtil
from ...types import DateInput
from .restroom_alert import RestroomAlert


def build_restroom_alert(
      restroom: str,
      alert_start_date: DateInput,
      alert_end_date: DateInput,
      message: str ) -> RestroomAlert:
   date_range = ZooUtil.resolve_open_ended_date_range(
      start_date=alert_start_date,
      end_date=alert_end_date )

   return RestroomAlert(
      restroom=restroom,
      start_date=date_range.start_date,
      end_date=date_range.end_date,
      message=message )
