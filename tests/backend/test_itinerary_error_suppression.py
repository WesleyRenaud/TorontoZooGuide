from __future__ import annotations

from api.itinerary.controllers.itinerary_controller import ItineraryController
from api.itinerary.data_access.itinerary_error_suppression import is_itinerary_error_suppressed
from api.itinerary.data_access.itinerary_error_suppression import suppress_itinerary_error
from api.seed.user_itinerary_config import clear_user_itinerary_config
from api.shared.constants import itinerary_config_to_dict
from api.shared.enums import ItineraryErrorType
from api.types import Cursor
from conftest import DbControllers


def test_suppress_short_visit_warning_skips_confirmation_prompt(
      db: DbControllers,
) -> None:
   assert db.conn is not None

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   suppress_itinerary_error(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   result = ItineraryController.set_arrival_time( '16:30' )

   assert result.success

   itinerary = ItineraryController.get_itinerary()
   assert itinerary.arrival_time == '16:30'


def test_suppress_short_visit_warning_persists_in_itinerary_config(
      db: DbControllers,
) -> None:
   assert db.conn is not None

   suppress_itinerary_error(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert itinerary_config_to_dict( db.conn )[ 'suppressed_error_types' ] == [
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE.value,
   ]

   assert is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_set_arrival_time_with_suppress_flag_persists_preference(
      db: DbControllers,
) -> None:
   assert db.conn is not None

   assert ItineraryController.set_itinerary(
      date='2026-06-15',
      arrival_time='09:30',
      departure_time='17:00',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
   ).success

   assert ItineraryController.set_arrival_time(
      '16:30',
      confirming_short_visit=True,
      suppress_short_visit_warning=True,
   ).success

   assert is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_clear_itinerary_leaves_error_suppressions(
      db: DbControllers,
) -> None:
   assert db.conn is not None

   suppress_itinerary_error(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert ItineraryController.clear_itinerary()

   assert is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )


def test_clear_user_itinerary_config_clears_error_suppressions(
      db: DbControllers,
      cursor: Cursor,
) -> None:
   suppress_itinerary_error(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   clear_user_itinerary_config( cursor )
   db.conn.commit()

   assert not is_itinerary_error_suppressed(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
