from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_status_provider import ItineraryStatusProvider
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.results.itinerary_result_reason import ItineraryResultReason
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.items.itinerary_save_result_builder import ItinerarySaveResultBuilder
from api.itinerary.scheduling.items.listed_schedule_item_persister import ListedScheduleItemPersister
from api.shared.enums import ItineraryErrorType


SAVED_ITINERARY = SavedItinerary(
   date_value='2026-06-15',
   arrival_time='9:30 AM',
   departure_time='5:00 PM',
   animal_rows=[
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         new_likelihood=100,
      ),
   ],
)

SCHEDULE_ITEM_KEY = AnimalScheduleItemKey(
   species='African Lion',
   exhibit='Africa Savanna',
)

MISSING_ITEM_KEY = AnimalScheduleItemKey(
   species='Cheetah',
   exhibit='Indo-Malaya Outdoor',
)

ITINERARY_CONTEXT: dict[ str, object ] = {}


@pytest.fixture
def persister_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def stub_save_result( monkeypatch: pytest.MonkeyPatch ) -> None:
   def save_result(
         conn: sqlite3.Connection,
         status: ItineraryErrorType,
         *,
         reasons: list[ ItineraryResultReason ] | None = None,
         suppressed_warnings: list[ ItineraryErrorType ] | None = None,
         **context: object ) -> ItinerarySaveResult:
      return ItinerarySaveResult(
         status=status,
         reasons=reasons or [],
         itinerary=ItineraryBuilder.empty(),
         suppressed_warnings=suppressed_warnings or [] )

   monkeypatch.setattr( ItinerarySaveResultBuilder, 'save_result', save_result )


@pytest.fixture
def stub_no_suppressed_status( monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, _error_type: False )


def Test_Prepare_TestMissingItem_ExpectItemNotOnItinerary(
      persister_conn: sqlite3.Connection,
      stub_save_result: None,
      stub_no_suppressed_status: None ) -> None:
   suppressed_warnings, error = ListedScheduleItemPersister.prepare(
      persister_conn,
      SAVED_ITINERARY,
      MISSING_ITEM_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert suppressed_warnings == []
   assert error is not None
   assert error.status == ItineraryErrorType.ITEM_NOT_ON_ITINERARY


def Test_Prepare_TestConfirmingMissingItem_ExpectNoError(
      persister_conn: sqlite3.Connection,
      stub_save_result: None,
      stub_no_suppressed_status: None ) -> None:
   suppressed_warnings, error = ListedScheduleItemPersister.prepare(
      persister_conn,
      SAVED_ITINERARY,
      MISSING_ITEM_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=True )

   assert suppressed_warnings == []
   assert error is None


def Test_Prepare_TestSuppressedWarning_ExpectNoError(
      persister_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      ItineraryStatusProvider,
      'is_itinerary_error_suppressed',
      lambda _conn, error_type: error_type == ItineraryErrorType.ITEM_NOT_ON_ITINERARY )

   suppressed_warnings, error = ListedScheduleItemPersister.prepare(
      persister_conn,
      SAVED_ITINERARY,
      MISSING_ITEM_KEY,
      itinerary_context=ITINERARY_CONTEXT,
      confirming_schedule_item_not_on_itinerary=False )

   assert error is None
   assert suppressed_warnings == [ ItineraryErrorType.ITEM_NOT_ON_ITINERARY ]


def Test_Commit_TestScheduledItem_ExpectCoverForActivity(
      persister_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_schedule_item_persister.ListedScheduleTargetResolver.apply',
      lambda *args, **kwargs: True )
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_schedule_item_persister.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SAVED_ITINERARY )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      ItinerarySaveResultBuilder,
      'success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   def cover_for_activity(
         conn: sqlite3.Connection,
         *,
         start_time: str,
         end_time: str,
         current_arrival_time: str | None,
         current_departure_time: str | None,
         itinerary_context: dict[ str, object ],
         seed_if_complete: bool = True ) -> None:
      captured[ 'cover' ] = {
         'start_time': start_time,
         'end_time': end_time,
         'current_arrival_time': current_arrival_time,
         'current_departure_time': current_departure_time,
      }

   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_schedule_item_persister.ScheduledActivityVisitTimesCoverer.cover_for_activity',
      cover_for_activity )

   result = ListedScheduleItemPersister.commit(
      persister_conn,
      schedule_item_key=SCHEDULE_ITEM_KEY,
      start_time='10:00 AM',
      end_time='10:08 AM',
      insert_if_missing=False,
      itinerary_context=ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.SUCCESS
   assert captured[ 'cover' ] == {
      'start_time': '10:00 AM',
      'end_time': '10:08 AM',
      'current_arrival_time': '9:30 AM',
      'current_departure_time': '5:00 PM',
   }


def Test_Commit_TestApplyFailed_ExpectItemNotOnItinerary(
      persister_conn: sqlite3.Connection,
      stub_save_result: None,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.scheduling.items.listed_schedule_item_persister.ListedScheduleTargetResolver.apply',
      lambda *args, **kwargs: False )

   result = ListedScheduleItemPersister.commit(
      persister_conn,
      schedule_item_key=SCHEDULE_ITEM_KEY,
      start_time='10:00 AM',
      end_time='10:08 AM',
      insert_if_missing=False,
      itinerary_context=ITINERARY_CONTEXT )

   assert result.status == ItineraryErrorType.ITEM_NOT_ON_ITINERARY
