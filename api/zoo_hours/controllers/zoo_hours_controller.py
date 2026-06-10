from __future__ import annotations

from ..data_access.zoo_hours import fetch_zoo_hours_record
from ..logic.zoo_hours import build_zoo_hours
from ...models import ZooHours
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ...types import MonthInput, VisitDay, VisitYear


class ZooHoursController():
   @classmethod
   def get_zoo_hours(
         cls,
         day: VisitDay,
         month: MonthInput,
         year: VisitYear ) -> ZooHours | None:
      operating_date = CalendarDates.visit_target_date(
         month,
         day,
         year )

      zoo_hours_record = fetch_zoo_hours_record(
         get_connection(),
         operating_date )

      if zoo_hours_record == None:
         return None

      return build_zoo_hours( zoo_hours_record )
