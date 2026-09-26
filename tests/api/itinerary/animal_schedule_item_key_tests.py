from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.schedule_item_key_separator import ScheduleItemKeySeparator


def Test_FromWire_TestTwoPartKey_ExpectSpeciesAndExhibit() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   wire = AnimalScheduleItemKey.wire( species=species, exhibit=exhibit )

   key = AnimalScheduleItemKey.from_wire( wire )

   assert key == AnimalScheduleItemKey( species=species, exhibit=exhibit )


def Test_FromWire_TestThreePartKey_ExpectEnclosureName() -> None:
   species = 'African Penguin'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Outdoor'
   wire = AnimalScheduleItemKey.wire(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )

   key = AnimalScheduleItemKey.from_wire( wire )

   assert key == AnimalScheduleItemKey(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )


def Test_FromWire_TestMissingSeparator_ExpectNone() -> None:
   wire = 'African Lion'

   key = AnimalScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestEmptySpecies_ExpectNone() -> None:
   exhibit = 'Africa Savanna'
   wire = f'{ ScheduleItemKeySeparator.VALUE }{ exhibit }'

   key = AnimalScheduleItemKey.from_wire( wire )

   assert key is None


def Test_FromWire_TestEmptyExhibit_ExpectNone() -> None:
   species = 'African Lion'
   wire = f'{ species }{ ScheduleItemKeySeparator.VALUE }'

   key = AnimalScheduleItemKey.from_wire( wire )

   assert key is None


def Test_ToWire_TestWithEnclosure_ExpectThreePartWire() -> None:
   species = 'African Penguin'
   exhibit = 'Africa Savanna'
   enclosure_name = 'Outdoor'
   key = AnimalScheduleItemKey(
      species=species,
      exhibit=exhibit,
      enclosure_name=enclosure_name )

   wire = key.to_wire()

   assert wire == AnimalScheduleItemKey.wire(
      species=key.species,
      exhibit=key.exhibit,
      enclosure_name=key.enclosure_name )


def Test_Wire_TestSpeciesAndExhibit_ExpectWireString() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'

   wire = AnimalScheduleItemKey.wire( species=species, exhibit=exhibit )

   assert wire == (
      f'{ species }'
      f'{ ScheduleItemKeySeparator.VALUE }'
      f'{ exhibit }' )


def Test_ParseSpeciesExhibit_TestValidKey_ExpectTuple() -> None:
   species = 'African Lion'
   exhibit = 'Africa Savanna'
   wire = AnimalScheduleItemKey.wire( species=species, exhibit=exhibit )

   parsed = AnimalScheduleItemKey.parse_species_exhibit( wire )

   assert parsed == ( species, exhibit )


def Test_ParseSpeciesExhibit_TestInvalidKey_ExpectNone() -> None:
   wire = 'invalid'

   parsed = AnimalScheduleItemKey.parse_species_exhibit( wire )

   assert parsed is None
