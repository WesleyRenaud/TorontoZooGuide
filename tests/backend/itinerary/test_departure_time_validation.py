from __future__ import annotations

from itinerary.support import CAROUSEL, CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, LION_ITINERARY_ENTRY, LION_KEY, schedule_itinerary_item, schedule_time_after_seconds

from api.itinerary.routing.walk_travel_time_calculator import WalkTravelTimeCalculator
from api.itinerary.scheduling.items.schedule_item_travel_time_calculator import ScheduleItemTravelTimeCalculator
from api.walk_graph.data_access.walk_graph_provider import WalkGraphProvider
from api.walk_graph.viewing_spot_walk_node_id_resolver import ViewingSpotWalkNodeIdResolver

CAROUSEL_AFTER_LION = schedule_time_after_seconds(
   schedule_time_after_seconds( '3:45 PM', 8 * 60 ),
   WalkTravelTimeCalculator.seconds_between_nodes(
      WalkGraphProvider.fetch(),
      ViewingSpotWalkNodeIdResolver.resolve( 'African Lion', 'Africa Savanna', None ),
      ScheduleItemTravelTimeCalculator.walk_node_id_for_attraction( CAROUSEL ),
   ),
)

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.validation.itinerary_departure_time_validator import ItineraryDepartureTimeValidator
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.zoo_hours.data_access.zoo_hours_provider import ZooHoursProvider
from conftest import DbControllers


def test_departure_time_is_valid_for_zoo_hours(
      db: DbControllers ) -> None:
   conn = db.conn

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record( conn, ItineraryProvider.fetch_itinerary_date( conn ) )

   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '09:00',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '09:30',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_ORDER_INVALID
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '18:00',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.SUCCESS
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '18:00',
      zoo_hours_record,
      arrival_time=None ) == ItineraryErrorType.SUCCESS


def test_departure_time_allows_early_admission_window(
      db: DbControllers ) -> None:
   conn = db.conn

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-20',
      arrival_time='09:00',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      confirming_early_admission=True,
   ).success

   zoo_hours_record = ZooHoursProvider.fetch_zoo_hours_record( conn, ItineraryProvider.fetch_itinerary_date( conn ) )

   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '09:08',
      zoo_hours_record,
      arrival_time='09:00' ) == ItineraryErrorType.SUCCESS
   assert ItineraryDepartureTimeValidator.validate_for_zoo_hours(
      '08:59',
      zoo_hours_record,
      arrival_time='09:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS


def test_set_departure_time_unschedules_items_after_departure(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='15:45',
   ).success
   assert schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='16:30',
   ).success
   assert schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time=CAROUSEL_AFTER_LION,
      duration_minutes=8,
   ).success

   result = ItineraryCoordinator.set_departure_time(
      '16:15',
      confirming_short_visit=True,
   )
   itinerary = ItineraryCoordinator.get_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', '3:45 PM', '3:53 PM' ),
      ( 'Cheetah', None, None ),
   ]
   assert itinerary.attractions[ 0 ].name == CAROUSEL
   assert itinerary.attractions[ 0 ].start_time is not None
   assert itinerary.attractions[ 0 ].end_time is not None
   assert itinerary.wild_encounters == []


def test_set_departure_time_unschedules_generic_event_after_departure(
      db: DbControllers ) -> None:
   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
      start_time='16:00',
   ).success

   assert ItineraryCoordinator.set_departure_time(
      '17:00',
      confirming_short_visit=True,
   ).success

   result = ItineraryCoordinator.set_departure_time(
      '16:15',
      confirming_short_visit=True,
   )
   itinerary = ItineraryCoordinator.get_itinerary()

   assert result.success
   assert itinerary.events == []
