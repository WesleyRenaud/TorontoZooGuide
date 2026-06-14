from __future__ import annotations

from api.itinerary.data_access.itinerary_status import suppress_itinerary_status
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.results.itinerary_time_set_result import ItineraryTimeSetResult
from api.itinerary.warnings.itinerary_suppressed_warnings import append_suppressed_warning
from api.itinerary.warnings.itinerary_suppressed_warnings import record_if_error_suppressed
from api.itinerary.warnings.itinerary_suppressed_warnings import with_suppressed_warnings
from api.itinerary.warnings.itinerary_suppressed_warnings import with_time_set_suppressed_warnings
from api.models import Itinerary
from api.shared.enums import ItineraryErrorType
from conftest import DbControllers


def test_append_suppressed_warning_skips_duplicates() -> None:
   suppressed_warnings: list[ ItineraryErrorType ] = []

   append_suppressed_warning(
      suppressed_warnings,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )
   append_suppressed_warning(
      suppressed_warnings,
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY )

   assert suppressed_warnings == [ ItineraryErrorType.ITEM_NOT_ON_ITINERARY ]


def test_record_if_error_suppressed_tracks_only_suppressed_types(
      db: DbControllers ) -> None:
   assert db.conn is not None
   suppressed_warnings: list[ ItineraryErrorType ] = []

   assert not record_if_error_suppressed(
      db.conn,
      suppressed_warnings,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   suppress_itinerary_status(
      db.conn,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )

   assert record_if_error_suppressed(
      db.conn,
      suppressed_warnings,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE )
   assert suppressed_warnings == [ ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE ]


def test_with_suppressed_warnings_returns_original_when_empty() -> None:
   result = ItinerarySaveResult( itinerary=Itinerary( date='2026-06-15' ) )

   assert with_suppressed_warnings( result, () ) is result


def test_with_suppressed_warnings_merges_unique_warning_types() -> None:
   result = ItinerarySaveResult(
      itinerary=Itinerary( date='2026-06-15' ),
      suppressed_warnings=( ItineraryErrorType.ITEM_NOT_ON_ITINERARY, ) )

   merged = with_suppressed_warnings(
      result,
      (
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ) )

   assert merged.suppressed_warnings == (
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
   )


def test_with_time_set_suppressed_warnings_returns_original_when_empty() -> None:
   result = ItineraryTimeSetResult()

   assert with_time_set_suppressed_warnings( result, () ) is result


def test_with_time_set_suppressed_warnings_merges_unique_warning_types() -> None:
   result = ItineraryTimeSetResult(
      suppressed_warnings=( ItineraryErrorType.ITEM_NOT_ON_ITINERARY, ) )

   merged = with_time_set_suppressed_warnings(
      result,
      (
         ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
         ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ) )

   assert merged.suppressed_warnings == (
      ItineraryErrorType.ITEM_NOT_ON_ITINERARY,
      ItineraryErrorType.ARRIVAL_DEPARTURE_TOO_CLOSE,
   )
