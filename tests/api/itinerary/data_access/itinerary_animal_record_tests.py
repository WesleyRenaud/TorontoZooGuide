from __future__ import annotations

from api.animals.search.species_exhibit_key import SpeciesExhibitKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.shared.enums import ScheduleItemKind


LION_RECORD = ItineraryAnimalRecord(
   species='African Lion',
   exhibit='Africa Savanna',
   start_time='10:00 AM',
   end_time='10:08 AM',
)

PENGUIN_RECORD = ItineraryAnimalRecord(
   species='African Penguin',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)


def Test_SpeciesExhibitKey_TestRecord_ExpectNormalizedKey() -> None:
   assert LION_RECORD.species_exhibit_key() == SpeciesExhibitKey(
      species='African Lion',
      exhibit='Africa Savanna',
   )


def Test_ViewingSpotKey_TestRecordWithEnclosure_ExpectThreePartKey() -> None:
   assert PENGUIN_RECORD.viewing_spot_key() == (
      'african penguin',
      'africa savanna',
      'Outdoor',
   )


def Test_MasterRouteStopKey_TestRecord_ExpectAnimalStopKey() -> None:
   assert LION_RECORD.master_route_stop_key() == (
      ScheduleItemKind.ANIMAL,
      'African Lion',
      'Africa Savanna',
      None,
   )
