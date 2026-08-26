from __future__ import annotations

from ..data_access.zoo_hours_provider import ZooHoursProvider
from ..domain.zoo_hours_builder import ZooHoursBuilder
from ...models import ZooHours
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ...types import MonthInput, VisitDay, VisitYear


class ZooHoursCoordinator():
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

      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record(
         get_connection(),
         operating_date )

      if zoo_hours_record == None:
         return None

      return ZooHoursBuilder.build( zoo_hours_record )
