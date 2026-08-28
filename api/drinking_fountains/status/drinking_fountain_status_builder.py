from __future__ import annotations

from datetime import date

from ...app_string_provider import AppStringProvider
from ..data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from .drinking_fountain_closed_status import DrinkingFountainClosedStatus
from .drinking_fountain_open_status import DrinkingFountainOpenStatus
from ...shared.calendar_dates import DateValues
from ...types import Types


class DrinkingFountainStatusBuilder():
   @classmethod
   def build_open_status(
         cls,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> DrinkingFountainOpenStatus:
      return DrinkingFountainOpenStatus(
         start_date=start_date,
         end_date=end_date )


   @classmethod
   def build_closed_status(
         cls,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> DrinkingFountainClosedStatus:
      if not message:
         message = AppStringProvider.format( 'guestStatus.drinkingFountains.closedForSeason' )

      return DrinkingFountainClosedStatus(
         start_date=start_date,
         end_date=end_date,
         message=message )


   @classmethod
   def applies_to_date(
         cls,
         status_record: DrinkingFountainStatusRecord,
         target_date: date ) -> bool:
      return DateValues.is_date_in_range(
         target_date=target_date,
         start_date_value=status_record.start_date,
         end_date_value=status_record.end_date )


   @classmethod
   def build_status(
         cls,
         status_record: DrinkingFountainStatusRecord ) -> tuple[ bool, str | None, float ]:
      closed_message = status_record.closed_message
      likelihood = 0.0 if status_record.is_closed else 1.0

      return status_record.is_closed, closed_message, likelihood


   @classmethod
   def build_seasonal_status(
         cls,
         likelihood: float ) -> tuple[ bool, None, float ]:
      is_closed = likelihood <= 0

      return is_closed, None, likelihood
