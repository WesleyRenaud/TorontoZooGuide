from __future__ import annotations

from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from conftest import DbControllers

def test_drinking_fountain_seasonal_fallback_controls_open_and_closed_results(
      db: DbControllers,
      cursor: Cursor ) -> None:
   summer_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )
   winter_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='January', year=2026 )
   transition_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=30, month='April', year=2026 )
   seasonal_rows = cursor.execute(
      """ SELECT
             MONTH,
             DAY,
             LIKELIHOOD
          FROM DrinkingFountainDaySeasonalAvailabilityMultiplier
          ORDER BY MONTH, DAY;
      """
   ).fetchall()
   seasonal_likelihoods = [ row[ 'LIKELIHOOD' ] for row in seasonal_rows ]
   likelihoods_by_date = {
      ( row[ 'MONTH' ], row[ 'DAY' ] ): row[ 'LIKELIHOOD' ]
      for row in seasonal_rows
   }
   spring_ramp = [
      likelihoods_by_date[ ( month, day ) ]
      for month, day in likelihoods_by_date
      if ( month, day ) >= ( 4, 16 ) and ( month, day ) <= ( 5, 15 )
   ]
   fall_ramp = [
      likelihoods_by_date[ ( month, day ) ]
      for month, day in likelihoods_by_date
      if ( month, day ) >= ( 11, 1 ) and ( month, day ) <= ( 11, 20 )
   ]

   assert len( summer_fountains ) > 0
   assert all( fountain.is_closed is False for fountain in summer_fountains )
   assert all( fountain.closed_message is None for fountain in summer_fountains )
   assert all( fountain.likelihood == 1.0 for fountain in summer_fountains )
   assert all( fountain.is_closed is True for fountain in winter_fountains )
   assert all( fountain.closed_message is None for fountain in winter_fountains )
   assert all( fountain.likelihood == 0.0 for fountain in winter_fountains )
   assert all( 0.0 < fountain.likelihood < 1.0 for fountain in transition_fountains )
   assert len( seasonal_rows ) == 366
   assert min( seasonal_likelihoods ) == 0.0
   assert max( seasonal_likelihoods ) == 1.0
   assert likelihoods_by_date[ ( 1, 15 ) ] == 0.0
   assert likelihoods_by_date[ ( 6, 15 ) ] == 1.0
   assert likelihoods_by_date[ ( 12, 15 ) ] == 0.0
   assert spring_ramp == sorted( spring_ramp )
   assert fall_ramp == sorted( fall_ramp, reverse=True )
   assert spring_ramp[ 0 ] == 0.0
   assert spring_ramp[ -1 ] == 1.0
   assert fall_ramp[ 0 ] == 1.0
   assert fall_ramp[ -1 ] == 0.0


def test_drinking_fountain_status_controls_global_open_and_closed_results(
      db: DbControllers,
      cursor: Cursor ) -> None:
   default_message = 'The drinking fountains are closed for the season.'

   fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert len( fountains ) > 0
   assert all( fountain.is_closed is False for fountain in fountains )
   assert all( fountain.closed_message is None for fountain in fountains )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_closed(
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Closed for testing.' )

   closed = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )
   outside_schedule = DrinkingFountainCoordinator.get_drinking_fountains( day=1, month='July', year=2026 )
   status_rows = cursor.execute(
      """ SELECT
             IS_CLOSED,
             START_DATE,
             END_DATE,
             CLOSED_MESSAGE
          FROM DrinkingFountainStatus;
      """
   ).fetchall()

   assert len( status_rows ) == 1
   assert dict( status_rows[ 0 ] ) == {
      'IS_CLOSED': 1,
      'START_DATE': '2026-06-01',
      'END_DATE': '2026-06-30',
      'CLOSED_MESSAGE': 'Closed for testing.'
   }
   assert all( fountain.is_closed is True for fountain in closed )
   assert all( fountain.closed_message == 'Closed for testing.' for fountain in closed )
   assert all( fountain.likelihood == 0.0 for fountain in closed )
   assert all( fountain.is_closed is False for fountain in outside_schedule )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_open(
      start_date='2026-06-15',
      end_date=None )

   reopened = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert all( fountain.is_closed is False for fountain in reopened )
   assert all( fountain.closed_message is None for fountain in reopened )
   assert all( fountain.likelihood == 1.0 for fountain in reopened )

   assert DrinkingFountainCoordinator.set_drinking_fountains_as_closed( message='' )

   default_closed = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert all( fountain.is_closed is True for fountain in default_closed )
   assert all( fountain.closed_message == default_message for fountain in default_closed )
   assert all( fountain.likelihood == 0.0 for fountain in default_closed )

