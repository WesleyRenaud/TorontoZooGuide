from __future__ import annotations

from collections.abc import Callable
from datetime import date

from itinerary.support import entrance_travel_seconds_to_animal, expected_departure_time_for_itinerary, LION_ITINERARY_ENTRY, schedule_itinerary_item, schedule_time_after_seconds

from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.shared.calendar_dates import DateValues
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver
from conftest import DbControllers


SPLASH_ISLAND = 'Splash Island'
SPLASH_OPEN_WITH_ENTRANCE_TRAVEL = schedule_time_after_seconds(
   '12:00 PM',
   WalkTravelTimeCalculator.seconds_between_nodes(
      WalkGraphProvider.fetch(),
      WalkGraphProvider.fetch()[ 'entrance_node_id' ],
      ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction( SPLASH_ISLAND ),
   ),
)


def _hours_payload(
      attraction: str,
      *,
      weekday_start: str,
      weekday_end: str,
      weekend_start: str,
      weekend_end: str ) -> dict:
   return {
      'attraction': attraction,
      'start_date': '2026-06-01',
      'end_date': '2026-06-30',
      'weekday_start_time': weekday_start,
      'weekday_end_time': weekday_end,
      'weekend_holiday_start_time': weekend_start,
      'weekend_holiday_end_time': weekend_end,
   }


def _set_splash_island_weekend_hours() -> None:
   assert AttractionCoordinator.replace_attraction_hours_schedule_overlaps(
      **_hours_payload(
         SPLASH_ISLAND,
         weekday_start='10:00 AM',
         weekday_end='4:00 PM',
         weekend_start='12:00 PM',
         weekend_end='5:00 PM' ) )


def test_schedule_attraction_at_default_time_uses_attraction_open(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == SPLASH_OPEN_WITH_ENTRANCE_TRAVEL
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'


def test_schedule_attraction_at_default_time_waits_for_open_after_arrival(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key='African Lion||Africa Savanna' ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   assert splash.start_time == SPLASH_OPEN_WITH_ENTRANCE_TRAVEL
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'


def test_schedule_attraction_extends_departure_when_visit_window_is_full(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 20 ) )
   _set_splash_island_weekend_hours()

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='12:00 PM',
      departure_time='12:30 PM',
      animals=[ LION_ITINERARY_ENTRY ],
      attractions=[ SPLASH_ISLAND ],
      guardians_talks=[],
      wild_encounters=[],
      confirming_short_visit=True,
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key='African Lion||Africa Savanna',
      start_time=schedule_time_after_seconds(
         '12:00 PM',
         entrance_travel_seconds_to_animal(
            species='African Lion',
            exhibit='Africa Savanna' ) ),
      duration_minutes=8 ).success

   result = schedule_itinerary_item(
      item_type='attractions',
      key=SPLASH_ISLAND )

   assert result.success
   splash = next(
      attraction
      for attraction in result.itinerary.attractions
      if attraction.name == SPLASH_ISLAND )
   lion_end = schedule_time_after_seconds(
      schedule_time_after_seconds(
         '12:00 PM',
         entrance_travel_seconds_to_animal(
            species='African Lion',
            exhibit='Africa Savanna' ) ),
      8 * 60 )
   assert splash.start_time is not None
   assert splash.end_time is not None
   assert splash.end_time <= '5:00 PM'
   assert result.itinerary.departure_time == expected_departure_time_for_itinerary(
      result.itinerary )
   assert DateValues.time_value_in_seconds( splash.start_time ) >= (
      DateValues.time_value_in_seconds( lion_end ) or 0 )
