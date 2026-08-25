from __future__ import annotations

from datetime import date

from ...app_strings import format_app_string
from ..data_access.drinking_fountain_status_record import DrinkingFountainStatusRecord
from .drinking_fountain_closed_status import DrinkingFountainClosedStatus
from .drinking_fountain_open_status import DrinkingFountainOpenStatus
from ...shared.calendar_dates import DateValues
from ...types import DateInput


def build_drinking_fountain_open_status(
      start_date: DateInput,
      end_date: DateInput ) -> DrinkingFountainOpenStatus:
   return DrinkingFountainOpenStatus(
      start_date=start_date,
      end_date=end_date )



def build_drinking_fountain_closed_status(
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> DrinkingFountainClosedStatus:
   if not message:
      message = format_app_string( 'guestStatus.drinkingFountains.closedForSeason' )

   return DrinkingFountainClosedStatus(
      start_date=start_date,
      end_date=end_date,
      message=message )



def drinking_fountain_status_applies_to_date(
      status_record: DrinkingFountainStatusRecord,
      target_date: date ) -> bool:
   return DateValues.is_date_in_range(
      target_date=target_date,
      start_date_value=status_record.start_date,
      end_date_value=status_record.end_date )



def build_drinking_fountain_status(
      status_record: DrinkingFountainStatusRecord ) -> tuple[ bool, str | None, float ]:
   closed_message = status_record.closed_message
   likelihood = 0.0 if status_record.is_closed else 1.0

   return status_record.is_closed, closed_message, likelihood



def build_drinking_fountain_seasonal_status(
      likelihood: float ) -> tuple[ bool, None, float ]:
   is_closed = likelihood <= 0

   return is_closed, None, likelihood
