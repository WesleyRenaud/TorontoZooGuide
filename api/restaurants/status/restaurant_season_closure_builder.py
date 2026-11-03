from __future__ import annotations

from datetime import date

from ...app_string_provider import AppStringProvider
from ..data_access.restaurant_closure_record import RestaurantClosureRecord
from .restaurant_season_closure import RestaurantSeasonClosure
from ...shared.calendar_dates import DateValues
from ...types import Types


class RestaurantSeasonClosureBuilder():
   @classmethod
   def build(
         cls,
         restaurant: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> RestaurantSeasonClosure:
      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      if not message:
         message = AppStringProvider.format(
            'guestStatus.locations.closedForSeason',
            name=restaurant )

      return RestaurantSeasonClosure(
         restaurant=restaurant,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message,
         is_closed_for_season=True )


   @classmethod
   def is_active_on_date(
         cls,
         closure_record: RestaurantClosureRecord | None,
         target_date: date | None ) -> bool:
      if closure_record == None or target_date == None:
         return False

      return DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=closure_record.closed_start,
         end_date_value=closure_record.closed_end )
