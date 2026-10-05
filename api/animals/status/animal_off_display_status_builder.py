from __future__ import annotations

from .animal_off_display_status import AnimalOffDisplayStatus
from ...app_string_provider import AppStringProvider
from ..domain.animal_viewing_scope import AnimalViewingScope
from ...shared.calendar_dates import DateValues
from ...types import Types


class AnimalOffDisplayStatusBuilder():
   @classmethod
   def build(
         cls,
         species: str,
         exhibit: str,
         viewing_scopes: list[ AnimalViewingScope ],
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str,
         is_off_display_for_season: bool ) -> AnimalOffDisplayStatus:
      if not message:
         message = AppStringProvider.format(
            cls._default_message_key( is_off_display_for_season ),
            species=species )

      date_range = DateValues.resolve_open_ended_date_range(
         start_date=start_date,
         end_date=end_date )

      return AnimalOffDisplayStatus(
         species=species,
         exhibit=exhibit,
         viewing_scopes=viewing_scopes,
         start_date=date_range.start_date,
         end_date=date_range.end_date,
         message=message,
         is_off_display_for_season=is_off_display_for_season )


   @classmethod
   def _default_message_key( cls, is_off_display_for_season: bool ) -> str:
      if is_off_display_for_season:
         return 'guestStatus.animals.offDisplayForSeason'

      return 'guestStatus.animals.temporarilyOffDisplay'
