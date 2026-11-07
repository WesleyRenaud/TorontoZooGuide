from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.animals.data_access.enclosure_off_display_month_mapper import EnclosureOffDisplayMonthMapper
from api.animals.domain.enclosure_off_display_month import EnclosureOffDisplayMonth


SPECIES = 'Warthog'
EXHIBIT = 'Africa Savanna'


def Test_MapRecords_TestRow_ExpectSpeciesExhibitAndMonth() -> None:
   row = make_row( {
      'SPECIES': SPECIES,
      'EXHIBIT': EXHIBIT,
      'OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH': 4,
   } )

   records = EnclosureOffDisplayMonthMapper.map_records( [ row ] )

   assert records == [
      EnclosureOffDisplayMonth(
         species=SPECIES,
         exhibit=EXHIBIT,
         until_month=4 ),
   ]
