from __future__ import annotations

from api.animals.domain.animal_viewing_scope import AnimalViewingScope
from api.animals.status.animal_off_display_status_builder import AnimalOffDisplayStatusBuilder
from api.app_string_provider import AppStringProvider


SPECIES = 'Masai Giraffe'
EXHIBIT = 'Africa Savanna'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
CUSTOM_MESSAGE = 'The giraffes are off display for habitat maintenance.'
OUTDOOR_YARD = AnimalViewingScope.from_enclosure_name( 'Outdoor Yard' )


def Test_Build_TestCustomMessage_ExpectMappedStatus() -> None:
   status = AnimalOffDisplayStatusBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ OUTDOOR_YARD ],
      start_date=START_DATE,
      end_date=END_DATE,
      message=CUSTOM_MESSAGE )

   assert status.species == SPECIES
   assert status.exhibit == EXHIBIT
   assert status.viewing_scopes == [ OUTDOOR_YARD ]
   assert status.start_date == START_DATE
   assert status.end_date == END_DATE
   assert status.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultGuestMessage() -> None:
   unnamed_scope = AnimalViewingScope.from_enclosure_name( None )

   status = AnimalOffDisplayStatusBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scopes=[ unnamed_scope ],
      start_date=START_DATE,
      end_date=None,
      message='' )

   assert status.end_date is None
   assert status.message == AppStringProvider.format(
      'guestStatus.animals.temporarilyOffDisplay',
      species=SPECIES )
