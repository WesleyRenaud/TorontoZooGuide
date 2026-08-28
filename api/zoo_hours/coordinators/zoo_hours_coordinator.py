from __future__ import annotations

from ..data_access.zoo_hours_provider import ZooHoursProvider
from ..domain.zoo_hours_builder import ZooHoursBuilder
from ...models import ZooHours
from ...request_connection_provider import RequestConnectionProvider
from ...shared.calendar_dates import CalendarDates
from ...types import Types


class ZooHoursCoordinator():
   @classmethod
   def get_zoo_hours(
         cls,
         day: Types.VisitDay,
         month: Types.MonthInput,
         year: Types.VisitYear ) -> ZooHours | None:
      operating_date = CalendarDates.visit_target_date(
         month,
         day,
         year )

      zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record(
         RequestConnectionProvider.get(),
         operating_date )

      if zoo_hours_record == None:
         return None

      return ZooHoursBuilder.build( zoo_hours_record )
