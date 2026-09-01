from __future__ import annotations

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey


LION_KEY = 'African Lion||Africa Savanna'
PENGUIN_KEY = 'African Penguin||Africa Savanna||Outdoor'


def Test_FromWire_TestTwoPartKey_ExpectSpeciesAndExhibit() -> None:
   key = AnimalScheduleItemKey.from_wire( LION_KEY )

   assert key == AnimalScheduleItemKey(
      species='African Lion',
      exhibit='Africa Savanna' )


def Test_FromWire_TestThreePartKey_ExpectEnclosureName() -> None:
   key = AnimalScheduleItemKey.from_wire( PENGUIN_KEY )

   assert key == AnimalScheduleItemKey(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )


def Test_FromWire_TestInvalidKey_ExpectNone() -> None:
   assert AnimalScheduleItemKey.from_wire( 'African Lion' ) is None
   assert AnimalScheduleItemKey.from_wire( '||Africa Savanna' ) is None
   assert AnimalScheduleItemKey.from_wire( 'African Lion||' ) is None


def Test_ToWire_TestWithEnclosure_ExpectThreePartWire() -> None:
   key = AnimalScheduleItemKey(
      species='African Penguin',
      exhibit='Africa Savanna',
      enclosure_name='Outdoor' )

   assert key.to_wire() == PENGUIN_KEY


def Test_Wire_TestSpeciesAndExhibit_ExpectWireString() -> None:
   assert AnimalScheduleItemKey.wire(
      species='African Lion',
      exhibit='Africa Savanna' ) == LION_KEY


def Test_ParseSpeciesExhibit_TestValidKey_ExpectTuple() -> None:
   assert AnimalScheduleItemKey.parse_species_exhibit( LION_KEY ) == (
      'African Lion',
      'Africa Savanna',
   )


def Test_ParseSpeciesExhibit_TestInvalidKey_ExpectNone() -> None:
   assert AnimalScheduleItemKey.parse_species_exhibit( 'invalid' ) is None
