from __future__ import annotations

from api.wild_encounters.data_access.wild_encounter_record import WildEncounterRecord
from api.wild_encounters.domain.wild_encounter_builder import WildEncounterBuilder


STATION_COORD = 0.0


def _encounter_record( *, name: str, meeting_spot: str = 'Africa Savanna' ) -> WildEncounterRecord:
   return WildEncounterRecord(
      name=name,
      meeting_spot=meeting_spot,
      link='https://example.com',
      maximum_duration=45,
      x_coord=STATION_COORD,
      y_coord=STATION_COORD,
      region='Africa' )


def Test_BuildDetails_TestNoIncludeFilter_ExpectAllEncountersSorted() -> None:
   encounters = WildEncounterBuilder.build_details( [
      _encounter_record( name='Zebra Encounter' ),
      _encounter_record( name='Giraffe Feeding' ),
   ] )

   assert [ encounter.name for encounter in encounters ] == [
      'Giraffe Feeding',
      'Zebra Encounter',
   ]


def Test_BuildDetails_TestIncludeFilter_ExpectMatchingEncounterOnly() -> None:
   encounters = WildEncounterBuilder.build_details(
      [
         _encounter_record( name='Giraffe Feeding' ),
         _encounter_record( name='Zebra Encounter' ),
      ],
      wild_encounters_to_include=[ 'giraffe feeding' ] )

   assert [ encounter.name for encounter in encounters ] == [ 'Giraffe Feeding' ]


def Test_BuildDetails_TestEmptyIncludeList_ExpectNoEncounters() -> None:
   encounters = WildEncounterBuilder.build_details(
      [ _encounter_record( name='Giraffe Feeding' ) ],
      wild_encounters_to_include=[] )

   assert encounters == []
