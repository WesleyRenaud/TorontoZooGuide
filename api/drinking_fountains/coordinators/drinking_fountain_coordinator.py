from __future__ import annotations

from ..data_access.drinking_fountain_provider import DrinkingFountainProvider
from ..data_access.drinking_fountain_status_provider import DrinkingFountainStatusProvider
from ..domain.drinking_fountain_builder import DrinkingFountainBuilder
from ..domain.seasonal_drinking_fountains import SeasonalDrinkingFountains
from ..domain.seasonal_drinking_fountains_builder import SeasonalDrinkingFountainsBuilder
from ...models import DrinkingFountain
from ...request_connection_provider import RequestConnectionProvider
from ...shared.calendar_dates import CalendarDates
from ...shared.date_values import DateValues
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
         is_closed_for_season = is_closed
      else:
         seasonal_likelihood = DrinkingFountainStatusProvider.fetch_drinking_fountain_seasonal_likelihood(
            RequestConnectionProvider.get(),
            target_date )
         is_closed, closed_message, likelihood = DrinkingFountainStatusBuilder.build_seasonal_status(
            seasonal_likelihood )
         is_closed_for_season = False

      fountain_records = DrinkingFountainProvider.fetch_drinking_fountain_records(
         RequestConnectionProvider.get() )

      return DrinkingFountainBuilder.build_drinking_fountains(
         fountain_records,
         is_closed,
         closed_message,
         likelihood,
         is_closed_for_season )


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

      return DrinkingFountainStatusProvider.save_drinking_fountain_status(
         RequestConnectionProvider.get(),
         is_closed=True,
         start_date=status.start_date,
         end_date=status.end_date,
         message=status.message,
      )


   @classmethod
   def get_seasonal_drinking_fountains( cls ) -> SeasonalDrinkingFountains:
      return SeasonalDrinkingFountainsBuilder.build(
         DrinkingFountainStatusProvider.fetch_current_drinking_fountain_status_record(
            RequestConnectionProvider.get()
         )
      )


   @classmethod
   def set_drinking_fountains_as_open( cls ) -> bool:
      return DrinkingFountainStatusProvider.delete_drinking_fountain_status(
         RequestConnectionProvider.get() )


   @classmethod
   def set_drinking_fountain_window(
         cls,
         is_closed: bool,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> bool:
      if is_closed:
         return cls.set_drinking_fountains_as_closed(
            start_date=start_date,
            end_date=end_date,
            message='',
         )

      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date,
      )

      return DrinkingFountainStatusProvider.save_drinking_fountain_status(
         RequestConnectionProvider.get(),
         is_closed=False,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=None,
      )
