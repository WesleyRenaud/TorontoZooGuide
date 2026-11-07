from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.animals.data_access.animal_day_seasonal_viewability_mapper import AnimalDaySeasonalViewabilityMapper
from api.animals.data_access.animal_day_seasonal_viewability_record import AnimalDaySeasonalViewabilityRecord


SPECIES = 'African Lion'
EXHIBIT = 'Africa Savanna'


def Test_MapRecords_TestRow_ExpectViewabilityPoint() -> None:
   row = make_row( {
      'SPECIES': SPECIES,
      'EXHIBIT': EXHIBIT,
      'MONTH': 11,
      'DAY': 2,
      'VALUE': 0.5,
   } )

   records = AnimalDaySeasonalViewabilityMapper.map_records( [ row ] )

   assert records == [
      AnimalDaySeasonalViewabilityRecord(
         species=SPECIES,
         exhibit=EXHIBIT,
         month=11,
         day=2,
         value=0.5,
      ),
   ]
