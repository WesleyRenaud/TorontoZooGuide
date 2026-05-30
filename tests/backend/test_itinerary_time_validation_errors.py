from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary import fetch_itinerary_date
from api.itinerary.logic.itinerary_arrival_time_validation import arrival_time_is_valid_for_zoo_hours
from api.itinerary.logic.itinerary_departure_time_validation import departure_time_is_valid_for_zoo_hours
from api.shared.enums import ItineraryErrorType
from api.zoo_hours.data_access.zoo_hours import fetch_zoo_hours_record
from conftest import DbControllers


def test_arrival_time_is_valid_for_zoo_hours(
      db: DbControllers ) -> None:
   conn = db.conn

   assert ItineraryController.set_itinerary(
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


def test_departure_time_is_valid_for_zoo_hours(
      db: DbControllers ) -> None:
   conn = db.conn

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   zoo_hours_record = fetch_zoo_hours_record( conn, fetch_itinerary_date( conn ) )

   assert departure_time_is_valid_for_zoo_hours(
      '09:00',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_OUT_OF_BOUNDS
   assert departure_time_is_valid_for_zoo_hours(
      '09:30',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.TIME_ORDER_INVALID
   assert departure_time_is_valid_for_zoo_hours(
      '18:00',
      zoo_hours_record,
      arrival_time='09:30' ) == ItineraryErrorType.SUCCESS


def test_set_arrival_time_returns_validation_error_types(
      db: DbControllers ) -> None:
   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.set_arrival_time( '09:00' ).error_type == (
      ItineraryErrorType.TIME_OUT_OF_BOUNDS )
   assert ItineraryController.set_arrival_time( '17:00' ).error_type == (
      ItineraryErrorType.TIME_ORDER_INVALID )
