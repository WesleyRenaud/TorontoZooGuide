from __future__ import annotations

from api.animals.status.animal_viewing_alert_builder import AnimalViewingAlertBuilder


SPECIES = 'African Lion'
EXHIBIT = 'Africa Savanna'
START_DATE = '2026-06-01'
END_DATE = '2026-06-15'
CUSTOM_MESSAGE = 'Viewing may be limited during feeding time.'


def Test_Build_TestCustomMessage_ExpectMappedAlert() -> None:
   alert = AnimalViewingAlertBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      alert_start_date=START_DATE,
      alert_end_date=END_DATE,
      message=CUSTOM_MESSAGE )

   assert alert.species == SPECIES
   assert alert.exhibit == EXHIBIT
   assert alert.start_date == START_DATE
   assert alert.end_date == END_DATE
   assert alert.message == CUSTOM_MESSAGE


def Test_Build_TestMissingMessage_ExpectDefaultGuestMessage() -> None:
   alert = AnimalViewingAlertBuilder.build(
      species=SPECIES,
      exhibit=EXHIBIT,
      alert_start_date=START_DATE,
      alert_end_date=None,
      message='' )

   assert alert.end_date is None
   assert SPECIES in alert.message
