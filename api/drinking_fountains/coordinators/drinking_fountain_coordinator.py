from __future__ import annotations

from ..data_access.drinking_fountain_provider import DrinkingFountainProvider
from ..data_access.drinking_fountain_status_provider import DrinkingFountainStatusProvider
from ..domain.drinking_fountain_builder import DrinkingFountainBuilder
from ...models import DrinkingFountain
from ...request_connection import get_connection
from ...shared.calendar_dates import CalendarDates
from ..status.drinking_fountain_status_builder import DrinkingFountainStatusBuilder
from ...types import DateInput, MonthInput, VisitDay, VisitYear


class DrinkingFountainCoordinator():
   @classmethod
   def get_drinking_fountains(
         cls,
         month: MonthInput,
         day: VisitDay,
         year: VisitYear ) -> list[ DrinkingFountain ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      status_record = DrinkingFountainStatusProvider.fetch_drinking_fountain_status_record(
         get_connection() )

      if status_record and DrinkingFountainStatusBuilder.applies_to_date( status_record, target_date ):
         is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_status(
            status_record )
      else:
         seasonal_likelihood = DrinkingFountainStatusProvider.fetch_drinking_fountain_seasonal_likelihood(
            get_connection(),
            target_date )
         is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_seasonal_status(
            seasonal_likelihood )

      fountain_records = DrinkingFountainProvider.fetch_drinking_fountain_records(
         get_connection() )

      return DrinkingFountainBuilder.build_drinking_fountains(
         fountain_records,
         is_closed,
         closed_message,
         likelihood )


   @classmethod
   def set_drinking_fountains_as_closed(
         cls,
         start_date: DateInput | None = None,
         end_date: DateInput | None = None,
         message: str | None = None ) -> bool:
      status = DrinkingFountainStatusBuilder.build_closed_status(
         start_date=start_date,
         end_date=end_date,
         message=message )

      return DrinkingFountainStatusProvider.save_drinking_fountain_closed_status(
         get_connection(),
         status=status )


   @classmethod
   def set_drinking_fountains_as_open(
         cls,
         start_date: DateInput | None = None,
         end_date: DateInput | None = None ) -> bool:
      status = DrinkingFountainStatusBuilder.build_open_status(
         start_date=start_date,
         end_date=end_date )

      return DrinkingFountainStatusProvider.save_drinking_fountain_open_status(
         get_connection(),
         status=status )
