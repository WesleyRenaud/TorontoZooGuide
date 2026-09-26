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
   zebra_encounter = _encounter_record( name='Zebra Encounter' )
   giraffe_feeding = _encounter_record( name='Giraffe Feeding' )
   records = [ zebra_encounter, giraffe_feeding ]

   encounters = WildEncounterBuilder.build_details( records )

   assert [ encounter.name for encounter in encounters ] == [
      giraffe_feeding.name,
      zebra_encounter.name,
   ]


def Test_BuildDetails_TestIncludeFilter_ExpectMatchingEncounterOnly() -> None:
   giraffe_feeding = _encounter_record( name='Giraffe Feeding' )
   zebra_encounter = _encounter_record( name='Zebra Encounter' )
   records = [ giraffe_feeding, zebra_encounter ]
   include = [ giraffe_feeding.name.lower() ]

   encounters = WildEncounterBuilder.build_details(
      records,
      wild_encounters_to_include=include )

   assert [ encounter.name for encounter in encounters ] == [ giraffe_feeding.name ]


def Test_BuildDetails_TestEmptyIncludeList_ExpectNoEncounters() -> None:
   giraffe_feeding = _encounter_record( name='Giraffe Feeding' )
   records = [ giraffe_feeding ]

   encounters = WildEncounterBuilder.build_details(
      records,
      wild_encounters_to_include=[] )

   assert encounters == []
