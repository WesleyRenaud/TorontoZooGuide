from __future__ import annotations

from itinerary.support import CAROUSEL, CHEETAH_ITINERARY_ENTRY, CHEETAH_KEY, GUARDIANS_TALK, guardians_talk_save_entry, LION_ITINERARY_ENTRY, LION_KEY, set_wild_encounter_schedule, WILD_ENCOUNTER

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary import fetch_itinerary_date
from api.itinerary.validation.itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from api.itinerary.validation.itinerary_schedule_time_order_validation import departure_follows_arrival
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType
from api.zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from conftest import DbControllers


def test_arrival_time_is_valid_for_zoo_hours(
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

   zoo_hours_record = fetch_zoo_hours_record( conn, fetch_itinerary_date( conn ) )

   assert arrival_time_is_valid_for_zoo_hours(
      '09:00',
      zoo_hours_record,
      departure_time='17:00' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert arrival_time_is_valid_for_zoo_hours(
      '17:00',
      zoo_hours_record,
      departure_time='17:00' ) == ItineraryErrorType.TIME_ORDER_INVALID
   assert arrival_time_is_valid_for_zoo_hours(
      '10:00',
      zoo_hours_record,
      departure_time='17:00' ) == ItineraryErrorType.SUCCESS
   assert arrival_time_is_valid_for_zoo_hours(
      '10:00',
      zoo_hours_record,
      departure_time=None ) == ItineraryErrorType.SUCCESS


def test_departure_follows_arrival_when_other_time_is_unset() -> None:
   assert departure_follows_arrival( '10:00', None )
   assert departure_follows_arrival( None, '17:00' )


def test_set_arrival_time_returns_validation_error_types(
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

   assert ItineraryCoordinator.set_arrival_time( '09:00' ).status == (
      ItineraryErrorType.TIME_OUT_OF_BOUNDS )
   assert ItineraryCoordinator.set_arrival_time( '17:00' ).status == (
      ItineraryErrorType.TIME_ORDER_INVALID )


def test_set_arrival_time_succeeds_when_departure_is_unset(
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
   assert ItineraryCoordinator.set_departure_time( None ).success

   assert ItineraryCoordinator.set_arrival_time( '10:15' ).success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '10:15'
   assert itinerary.departure_time is None


def test_set_arrival_time_unschedules_items_before_arrival(
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

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=LION_KEY,
      start_time='10:00',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='animals',
      key=CHEETAH_KEY,
      start_time='10:30',
   ).success
   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type='attractions',
      key=CAROUSEL,
      start_time='10:10',
   ).success

   set_wild_encounter_schedule( encounter_time='09:45' )

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[
         LION_ITINERARY_ENTRY,
         CHEETAH_ITINERARY_ENTRY,
      ],
      attractions=[ CAROUSEL ],
      guardians_talks=[
         guardians_talk_save_entry(
            GUARDIANS_TALK,
            start_time='10:00',
            end_time='10:10',
         ),
      ],
      wild_encounters=[ WILD_ENCOUNTER ],
      confirming_wild_encounter_unschedule=True,
   ).success

   result = ItineraryCoordinator.set_arrival_time( '10:15' )
   itinerary = ItineraryCoordinator.get_itinerary()

   assert result.success
   assert result.itinerary is not None
   assert [
      ( animal.species, animal.start_time, animal.end_time )
      for animal in itinerary.animals
   ] == [
      ( 'African Lion', None, None ),
      ( 'Cheetah', '10:30', '10:35' ),
   ]
   assert [
      ( attraction.name, attraction.start_time, attraction.end_time )
      for attraction in itinerary.attractions
   ] == [
      ( CAROUSEL, None, None ),
   ]
   assert itinerary.guardians_talks == []
   assert itinerary.wild_encounters == []


def test_set_arrival_time_unschedules_generic_event_before_arrival(
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

   assert ItineraryCoordinator.schedule_itinerary_item(
      item_type=ItineraryEventType.LUNCH.value,
      key='',
   ).success

   result = ItineraryCoordinator.set_arrival_time( '10:15' )
   itinerary = ItineraryCoordinator.get_itinerary()

   assert result.success
   assert itinerary.events == []
