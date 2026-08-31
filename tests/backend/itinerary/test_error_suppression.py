from __future__ import annotations

from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.seed.user_itinerary_config_cleaner import UserItineraryConfigCleaner
from api.shared.enums import ItineraryErrorType
from api.types import Types
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
      cursor: Types.Cursor ) -> None:
   ItineraryStatusProvider.suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   UserItineraryConfigCleaner.clear( cursor )
   db.conn.commit()

   assert not ItineraryStatusProvider.is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
