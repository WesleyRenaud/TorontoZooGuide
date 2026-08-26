from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.seed.user_itinerary_config import clear_user_itinerary_config
from api.shared.constants import itinerary_config_to_dict
from api.shared.enums import ItineraryErrorType
from api.types import Cursor
from conftest import DbControllers


def test_suppress_short_visit_warning_skips_confirmation_prompt(
      db: DbControllers ) -> None:
   assert db.conn is not None

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   ItineraryStatusProvider.suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   result = ItineraryCoordinator.set_arrival_time( '16:30' )

   assert result.success

   itinerary = ItineraryCoordinator.get_itinerary()
   assert itinerary.arrival_time == '4:30 PM'


def test_suppress_short_visit_warning_persists_in_itinerary_config(
      db: DbControllers ) -> None:
   assert db.conn is not None

   ItineraryStatusProvider.suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert itinerary_config_to_dict( db.conn )[ 'suppressed_error_types' ] == [
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value,
   ]

   assert ItineraryStatusProvider.is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_suppress_itinerary_warning_persists_preference(
      db: DbControllers ) -> None:
   assert db.conn is not None

   assert ItineraryCoordinator.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   result = ItineraryCoordinator.suppress_itinerary_warning(
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value )

   assert result.success
   assert ItineraryStatusProvider.is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_suppress_itinerary_warning_rejects_non_suppressable_type(
      db: DbControllers ) -> None:
   assert db.conn is not None

   result = ItineraryCoordinator.suppress_itinerary_warning(
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS.value )

   assert not result.success
   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )


def test_clear_itinerary_leaves_error_suppressions(
      db: DbControllers ) -> None:
   assert db.conn is not None

   ItineraryStatusProvider.suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert ItineraryCoordinator.clear_itinerary()

   assert ItineraryStatusProvider.is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_clear_user_itinerary_config_clears_error_suppressions(
      db: DbControllers,
      cursor: Cursor ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   clear_user_itinerary_config( cursor )
   db.conn.commit()

   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_non_suppressable_itinerary_error_types_cannot_be_persisted(
      db: DbControllers ) -> None:
   assert db.conn is not None

   non_suppressable_error_types = [
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS,
      ItineraryErrorType.FIXED_TIME_ITEM_LONG_WAIT,
      ItineraryErrorType.GUARDIANS_TALK_WITHOUT_ANIMAL,
      ItineraryErrorType.ATTRACTION_WITHOUT_ANIMAL,
      ItineraryErrorType.WILD_ENCOUNTER_WILL_UNSCHEDULE_ITEMS,
      ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED,
   ]

   assert ItineraryStatusProvider.is_itinerary_status_suppressable(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   assert ItineraryStatusProvider.is_itinerary_status_suppressable(
      db.conn,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
   assert not ItineraryStatusProvider.is_itinerary_status_suppressable(
      db.conn,
      ItineraryErrorType.GUARDIANS_TALK_WILL_UNSCHEDULE_ITEMS )
   assert not ItineraryStatusProvider.is_itinerary_status_suppressable(
      db.conn,
      ItineraryErrorType.BULK_SCHEDULE_ITINERARY_ALREADY_SCHEDULED )

   for error_type in non_suppressable_error_types:
      ItineraryStatusProvider.suppress_itinerary_status( db.conn, error_type )

      assert not ItineraryStatusProvider.is_itinerary_error_suppressed( db.conn, error_type )
      assert error_type.value not in itinerary_config_to_dict(
         db.conn )[ 'suppressed_error_types' ]
