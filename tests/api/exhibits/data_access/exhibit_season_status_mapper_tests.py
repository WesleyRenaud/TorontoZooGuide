from __future__ import annotations

from datetime import date

from api_test_support.sqlite_row import make_row

from api.exhibits.data_access.exhibit_season_status_mapper import ExhibitSeasonStatusMapper
from api.exhibits.domain.exhibit_season_status import ExhibitSeasonStatus
from api.types import Types


MAYAN = 'Americas Outdoor Mayan Temple Ruins'


def _row(
      exhibit: str,
      is_closed: int,
      start: str | None,
      end: str | None,
      closed_for_season: int ) -> Types.Row:
   return make_row( {
      'EXHIBIT': exhibit,
      'IS_CLOSED': is_closed,
      'CLOSED_START': start,
      'CLOSED_END': end,
      'CLOSED_FOR_SEASON': closed_for_season,
   } )


def Test_MapRecords_TestClosedForSeason_ExpectStatus() -> None:
   statuses = ExhibitSeasonStatusMapper.map_records( [
      _row( MAYAN, 1, '2026-10-01', '2027-03-31', 1 ),
   ] )

   assert statuses == [
      ExhibitSeasonStatus(
         exhibit=MAYAN,
         is_closed=True,
         start=date( 2026, 10, 1 ),
         end=date( 2027, 3, 31 ),
         closed_for_season=True,
      ),
   ]
