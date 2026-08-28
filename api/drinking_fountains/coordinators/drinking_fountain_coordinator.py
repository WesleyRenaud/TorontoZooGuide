from __future__ import annotations

from ..data_access.drinking_fountain_provider import DrinkingFountainProvider
from ..data_access.drinking_fountain_status_provider import DrinkingFountainStatusProvider
from ..domain.drinking_fountain_builder import DrinkingFountainBuilder
from ...models import DrinkingFountain
from ...request_connection_provider import RequestConnectionProvider
from ...shared.calendar_dates import CalendarDates
from ..status.drinking_fountain_status_builder import DrinkingFountainStatusBuilder
from ...types import Types


class DrinkingFountainCoordinator():
   @classmethod
   def get_drinking_fountains(
         cls,
         month: Types.MonthInput,
         day: Types.VisitDay,
         year: Types.VisitYear ) -> list[ DrinkingFountain ]:
      target_date = CalendarDates.visit_target_date(
         month=month,
         day=day,
         year=year )

      status_record = DrinkingFountainStatusProvider.fetch_drinking_fountain_status_record(
         RequestConnectionProvider.get() )

      if status_record and DrinkingFountainStatusBuilder.applies_to_date( status_record, target_date ):
         is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_status(
            status_record )
      else:
         seasonal_likelihood = DrinkingFountainStatusProvider.fetch_drinking_fountain_seasonal_likelihood(
            RequestConnectionProvider.get(),
            target_date )
         is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_seasonal_status(
            seasonal_likelihood )

      fountain_records = DrinkingFountainProvider.fetch_drinking_fountain_records(
         RequestConnectionProvider.get() )

      return DrinkingFountainBuilder.build_drinking_fountains(
         fountain_records,
         is_closed,
         closed_message,
         likelihood )


   @classmethod
   def set_drinking_fountains_as_closed(
         cls,
         start_date: Types.DateInput | None = None,
         end_date: Types.DateInput | None = None,
         message: str | None = None ) -> bool:
      status = DrinkingFountainStatusBuilder.build_closed_status(
         start_date=start_date,
         end_date=end_date,
         message=message )

      return DrinkingFountainStatusProvider.save_drinking_fountain_closed_status(
         RequestConnectionProvider.get(),
         status=status )


   @classmethod
   def set_drinking_fountains_as_open(
         cls,
         start_date: Types.DateInput | None = None,
         end_date: Types.DateInput | None = None ) -> bool:
      status = DrinkingFountainStatusBuilder.build_open_status(
         start_date=start_date,
         end_date=end_date )

      return DrinkingFountainStatusProvider.save_drinking_fountain_open_status(
         RequestConnectionProvider.get(),
         status=status )
