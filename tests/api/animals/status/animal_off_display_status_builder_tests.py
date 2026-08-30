from __future__ import annotations

from api.animals.status.animal_off_display_status_builder import AnimalOffDisplayStatusBuilder
from api.shared.enums.animal_viewing_scope import AnimalViewingScope


SPECIES = 'Masai Giraffe'
EXHIBIT = 'Africa Savanna'
START_DATE = '2026-06-01'
END_DATE = '2026-06-30'
CUSTOM_MESSAGE = 'The giraffes are off display for habitat maintenance.'


def Test_Build_TestCustomMessage_ExpectMappedStatus() -> None:
   status = AnimalOffDisplayStatusBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.OUTDOOR,
      start_date=START_DATE,
      end_date=END_DATE,
      message=CUSTOM_MESSAGE )

   assert status.species == SPECIES
   assert status.exhibit == EXHIBIT
   assert status.viewing_scope == AnimalViewingScope.OUTDOOR
   assert status.start_date == START_DATE
   assert status.end_date == END_DATE
   assert status.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultGuestMessage() -> None:
   status = AnimalOffDisplayStatusBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      viewing_scope=AnimalViewingScope.ALL,
      start_date=START_DATE,
      end_date=None,
      message='' )

   assert status.end_date is None
   assert SPECIES in status.message
