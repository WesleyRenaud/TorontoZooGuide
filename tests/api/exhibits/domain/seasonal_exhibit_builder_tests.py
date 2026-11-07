from __future__ import annotations

from datetime import date

from api.exhibits.data_access.exhibit_closure_record import ExhibitClosureRecord
from api.exhibits.domain.seasonal_exhibit import SeasonalExhibit
from api.exhibits.domain.seasonal_exhibit_builder import SeasonalExhibitBuilder


KIDS_ZOO = 'Kids Zoo'


def Test_Build_TestClosures_ExpectExhibitNameStatusAndDates() -> None:
   exhibits = SeasonalExhibitBuilder.build(
      exhibits=[ KIDS_ZOO, 'Africa Savanna' ],
      closure_records=[
         ExhibitClosureRecord(
            exhibit=KIDS_ZOO,
            closed_start='2026-11-02',
            closed_end='2026-11-30',
            is_closed_for_season=True,
         ),
         ExhibitClosureRecord(
            exhibit='Missing Start',
            closed_start=None,
            closed_end=None,
            is_closed_for_season=True,
         ),
         ExhibitClosureRecord(
            exhibit='Tundra Trek',
            closed_start='2026-10-01',
            closed_end=None,
            is_closed_for_season=False,
         ),
      ],
   )

   assert exhibits == [
      SeasonalExhibit(
         name=KIDS_ZOO,
         is_closed=True,
         start=date( 2026, 11, 2 ),
         end=date( 2026, 11, 30 ),
         closed_for_season=True,
      ),
      SeasonalExhibit(
         name='Africa Savanna',
         is_closed=False,
         start=None,
         end=None,
         closed_for_season=False,
      ),
      SeasonalExhibit(
         name='Tundra Trek',
         is_closed=True,
         start=date( 2026, 10, 1 ),
         end=None,
         closed_for_season=False,
      ),
   ]


def Test_ClosedForSeasonOn_TestOpenEndedRange_ExpectOnlyCoveredDate() -> None:
   exhibit = SeasonalExhibit(
      name=KIDS_ZOO,
      is_closed=True,
      start=date( 2026, 11, 2 ),
      end=None,
      closed_for_season=True,
   )

   assert exhibit.closed_for_season_on( date( 2026, 11, 2 ) )
   assert not exhibit.closed_for_season_on( date( 2026, 11, 1 ) )


def Test_Lookup_TestCasefoldName_ExpectExhibit() -> None:
   exhibit = SeasonalExhibit(
      name=KIDS_ZOO,
      is_closed=False,
      start=None,
      end=None,
      closed_for_season=False,
   )

   assert SeasonalExhibit.lookup( 'kids zoo', [ exhibit ] ) == exhibit


def Test_Lookup_TestMissingName_ExpectNone() -> None:
   assert SeasonalExhibit.lookup( 'Kids Zoo', [] ) == None
