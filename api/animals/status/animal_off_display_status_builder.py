from __future__ import annotations

from .animal_off_display_status import AnimalOffDisplayStatus
from ...app_strings import AppStringProvider
from ...shared.calendar_dates import DateValues
from ...shared.enums import AnimalViewingScope
from ...types import DateInput


class AnimalOffDisplayStatusBuilder():
   @classmethod
   def build(
         cls,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope,
         start_date: DateInput,
         end_date: DateInput,
         message: str ) -> AnimalOffDisplayStatus:
      if not message:
         message = AppStringProvider.format( 'guestStatus.animals.temporarilyOffDisplay', species=species )

      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return AnimalOffDisplayStatus(
         species=species,
         exhibit=exhibit,
         viewing_scope=viewing_scope,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message )
