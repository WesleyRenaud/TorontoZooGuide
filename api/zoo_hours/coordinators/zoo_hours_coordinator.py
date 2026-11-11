from __future__ import annotations

from datetime import date

from ..data_access.zoo_hours_provider import ZooHoursProvider
from ..data_access.zoo_hours_record import ZooHoursRecord
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


   @classmethod
   def get_zoo_hours_on_or_after( cls, start: date ) -> list[ ZooHours ]:
      records = ZooHoursProvider.fetch_zoo_hours_records_between(
         RequestConnectionProvider.get(),
         start.isoformat(),
      )

      return [
         ZooHoursBuilder.build( record )
         for record in records
      ]


   @classmethod
   def set_zoo_hours( cls, hours: ZooHours ) -> bool:
      return ZooHoursProvider.save_zoo_hours(
         RequestConnectionProvider.get(),
         ZooHoursRecord(
            operating_date=hours.date,
            early_admission_time=hours.early_admission_time,
            open_time=hours.open_time,
            last_admission_time=hours.last_admission_time,
            close_time=hours.close_time,
         ) )


   @classmethod
   def delete_zoo_hours( cls, operating_date: Types.DateKey ) -> bool:
      return ZooHoursProvider.delete_zoo_hours(
         RequestConnectionProvider.get(),
         operating_date )
