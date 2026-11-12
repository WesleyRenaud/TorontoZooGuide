from __future__ import annotations

from api_test_support.sqlite_row import make_row

from api.exhibits.data_access.exhibit_season_mapper import ExhibitSeasonMapper
from api.exhibits.domain.exhibit_season import ExhibitSeason
from api.types import Types


MAYAN = 'Americas Outdoor Mayan Temple Ruins'


def _row( name: str, open_start: int | None, open_end: int | None ) -> Types.Row:
   return make_row( {
      'NAME': name,
      'OPEN_START_MONTH': open_start,
      'OPEN_END_MONTH': open_end,
   } )


def Test_MapRecord_TestMonths_ExpectNamedSeason() -> None:
   season = ExhibitSeasonMapper.map_record( _row( MAYAN, 4, 10 ) )

   assert season == ExhibitSeason( 4, 10, MAYAN )


def Test_MapRecord_TestNoMonths_ExpectEmptySeason() -> None:
   season = ExhibitSeasonMapper.map_record( _row( 'Africa Savanna', None, None ) )

   assert season == ExhibitSeason( None, None, 'Africa Savanna' )
