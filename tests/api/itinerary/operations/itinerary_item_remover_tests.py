from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.animal_schedule_item_key import AnimalScheduleItemKey
from api.itinerary.attraction_schedule_item_key import AttractionScheduleItemKey
from api.itinerary.data_access.itinerary_animal_record import ItineraryAnimalRecord
from api.itinerary.data_access.itinerary_transportation_record import ItineraryTransportationRecord
from api.itinerary.data_access.remove_itinerary_item_provider import RemoveItineraryItemProvider
from api.itinerary.data_access.saved_itinerary import SavedItinerary
from api.itinerary.domain.itinerary_builder import ItineraryBuilder
from api.itinerary.guardians_talk_schedule_item_key import GuardiansTalkScheduleItemKey
from api.itinerary.operations.itinerary_item_remover import ItineraryItemRemover
from api.itinerary.operations.itinerary_item_schedule_change_committer import ItineraryItemScheduleChangeCommitter
from api.itinerary.results.itinerary_save_result import ItinerarySaveResult
from api.itinerary.scheduling.bulk.bulk_schedule_itinerary_runner import BulkScheduleItineraryRunner
from api.itinerary.scheduling.bulk.bulk_schedule_stop_selector import BulkScheduleStopSelector
from api.itinerary.transportation_schedule_item_key import TransportationScheduleItemKey
from api.itinerary.wild_encounter_schedule_item_key import WildEncounterScheduleItemKey
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.shared.enums import ItineraryErrorType
from api.shared.enums import ItineraryEventType

ZOOMOBILE = 'Zoomobile'
ZOOMOBILE_ATTRACTION_START = '11:00 AM'
ZOOMOBILE_ATTRACTION_END = '11:30 AM'
ZOOMOBILE_TRANSIT_START = '11:30 AM'
ZOOMOBILE_TRANSIT_END = '12:00 PM'
ZOOMOBILE_TRANSIT_ROUTE = 'zoomobile-route'

REMOVER_TRANSPORTATION_SCHEMA = """
CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   OLD_LIKELIHOOD           INTEGER,
   NEW_LIKELIHOOD           INTEGER,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   START_TIME               TEXT,
   END_TIME                 TEXT,
   ROUTE                    TEXT,
   BULK_TRANSIT_EVALUATED   INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL,
   START_TIME               TEXT        NOT NULL,
   END_TIME                 TEXT        NOT NULL
);

CREATE TABLE ItineraryTransportationRouteMarker (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   SEQUENCE                 INTEGER     NOT NULL,
   MARKER_ORDER             INTEGER     NOT NULL,
   MARKER_ID                TEXT        NOT NULL
);
"""


@pytest.fixture
def remover_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   yield conn
   conn.close()


@pytest.fixture
def zoomobile_remover_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( REMOVER_TRANSPORTATION_SCHEMA )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            )
            VALUES ( ?, NULL, 3, 1, ?, ?, NULL, 0 );
      """,
      ( ZOOMOBILE, ZOOMOBILE_ATTRACTION_START, ZOOMOBILE_ATTRACTION_END ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_AS_ATTRACTION,
               START_TIME,
               END_TIME,
               ROUTE,
               BULK_TRANSIT_EVALUATED
            )
            VALUES ( ?, NULL, 3, 0, ?, ?, ?, 1 );
      """,
      (
         ZOOMOBILE,
         ZOOMOBILE_TRANSIT_START,
         ZOOMOBILE_TRANSIT_END,
         ZOOMOBILE_TRANSIT_ROUTE,
      ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, 'Station A', 'Station B', '11:30 AM', '11:45 AM' ) )
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, 0, ?, ?, ?, ? );
      """,
      ( ZOOMOBILE, 'Station B', 'Station C', '11:45 AM', '12:00 PM' ) )
   conn.commit()

   yield conn

   conn.close()


def _zoomobile_saved_itinerary() -> SavedItinerary:
   return SavedItinerary(
      date_value='2026-06-15',
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      transportation_rows=(
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True,
            start_time=ZOOMOBILE_ATTRACTION_START,
            end_time=ZOOMOBILE_ATTRACTION_END,
         ),
         ItineraryTransportationRecord(
            transportation=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time=ZOOMOBILE_TRANSIT_START,
            end_time=ZOOMOBILE_TRANSIT_END,
            route=ZOOMOBILE_TRANSIT_ROUTE,
            bulk_transit_evaluated=True,
            legs=[
               ItineraryTransportationLeg(
                  transportation=ZOOMOBILE,
                  added_as_attraction=False,
                  from_station='Station A',
                  to_station='Station B',
                  start_time='11:30 AM',
                  end_time='11:45 AM',
               ),
               ItineraryTransportationLeg(
                  transportation=ZOOMOBILE,
                  added_as_attraction=False,
                  from_station='Station B',
                  to_station='Station C',
                  start_time='11:45 AM',
                  end_time='12:00 PM',
               ),
            ],
         ),
      ),
   )


def _fetch_transit_legs( conn: sqlite3.Connection ) -> list[ tuple[ str, str ] ]:
   rows = conn.execute(
      """   SELECT FROM_STATION, TO_STATION
            FROM ItineraryTransportationLeg
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 0
            ORDER BY START_TIME;
      """,
      ( ZOOMOBILE, ),
   ).fetchall()

   return [
      ( row[ 'FROM_STATION' ], row[ 'TO_STATION' ] )
      for row in rows
   ]


def Test_IsTransitModeTransportationKey_TestTransitRow_ExpectTrue() -> None:
   assert ItineraryItemRemover.is_transit_mode_transportation_key(
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=False ) )


def Test_IsTransitModeTransportationKey_TestAttractionRow_ExpectFalse() -> None:
   assert not ItineraryItemRemover.is_transit_mode_transportation_key(
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=True ) )


def Test_RemoveTransitTransportationAndReschedule_TestNoStops_ExpectSyncCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: object() )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ItineraryItemRemover,
      'apply',
      lambda cur, schedule_item_key: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.BulkScheduleStopSelector.stops_matching_previous',
      lambda saved_before, saved_after: [] )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ScheduledEndpointVisitTimesSyncer.sync_if_complete',
      lambda conn, itinerary: calls.append( 'sync' ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ScheduledEndpointVisitTimesSyncer.clear_if_became_incomplete',
      lambda conn, *, previous_itinerary, current_itinerary: calls.append( 'clear' ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItinerarySaveResultBuilder.persist_walk_route',
      lambda conn, **context: None )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItinerarySaveResultBuilder.success_result',
      lambda conn, **context: ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() ) )

   result = ItineraryItemRemover.remove_transit_transportation_and_reschedule(
      remover_conn,
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=False ) )

   assert result.status == ItineraryErrorType.SUCCESS
   assert calls == [ 'sync', 'clear' ]


def Test_RemoveTransitTransportationAndReschedule_TestStopsPresent_ExpectBulkRunnerCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   captured: dict[ str, object ] = {}

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM',
      ) )
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryBuilder.build_current',
      lambda saved_itinerary, **context: ItineraryBuilder.empty() )
   monkeypatch.setattr(
      ItineraryItemRemover,
      'apply',
      lambda cur, schedule_item_key: None )
   monkeypatch.setattr(
      BulkScheduleStopSelector,
      'stops_matching_previous',
      lambda saved_itinerary_before, saved_itinerary_after: [
         ItineraryAnimalRecord(
            species='African Lion',
            exhibit='Africa Savanna',
            start_time='10:00 AM',
            end_time='10:08 AM',
         ),
      ] )

   def run(
         conn: sqlite3.Connection,
         *,
         stops_to_schedule: list[ ItineraryAnimalRecord ],
         **context: object ) -> ItinerarySaveResult:
      captured[ 'stops_to_schedule' ] = stops_to_schedule
      return ItinerarySaveResult(
         status=ItineraryErrorType.SUCCESS,
         reasons=[],
         itinerary=ItineraryBuilder.empty() )

   monkeypatch.setattr( BulkScheduleItineraryRunner, 'run', run )

   result = ItineraryItemRemover.remove_transit_transportation_and_reschedule(
      remover_conn,
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=False ) )

   assert result.status == ItineraryErrorType.SUCCESS
   assert captured[ 'stops_to_schedule' ] == [
      ItineraryAnimalRecord(
         species='African Lion',
         exhibit='Africa Savanna',
         start_time='10:00 AM',
         end_time='10:08 AM',
      ),
   ]


def Test_Apply_TestAttractionZoomobileKey_ExpectAttractionModeDeletedTransitPreserved(
      zoomobile_remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: _zoomobile_saved_itinerary() )
   transit_legs_before = _fetch_transit_legs( zoomobile_remover_conn )

   cur = zoomobile_remover_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      AttractionScheduleItemKey( name=ZOOMOBILE ) )
   zoomobile_remover_conn.commit()
   cur.close()

   attraction_count = zoomobile_remover_conn.execute(
      """   SELECT COUNT(*) AS COUNT
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 1;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()
   transit_row = zoomobile_remover_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ?
              AND ADDED_AS_ATTRACTION = 0;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()

   assert attraction_count is not None
   assert attraction_count[ 'COUNT' ] == 0
   assert transit_row is not None
   assert transit_row[ 'START_TIME' ] == ZOOMOBILE_TRANSIT_START
   assert transit_row[ 'END_TIME' ] == ZOOMOBILE_TRANSIT_END
   assert transit_row[ 'ROUTE' ] == ZOOMOBILE_TRANSIT_ROUTE
   assert transit_row[ 'BULK_TRANSIT_EVALUATED' ] == 1
   assert _fetch_transit_legs( zoomobile_remover_conn ) == transit_legs_before


def Test_Apply_TestTransportationTransitModeKey_ExpectAttractionRolePreserved(
      zoomobile_remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: _zoomobile_saved_itinerary() )

   cur = zoomobile_remover_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      TransportationScheduleItemKey(
         name=ZOOMOBILE,
         added_as_attraction=False ) )
   zoomobile_remover_conn.commit()
   cur.close()

   rows = zoomobile_remover_conn.execute(
      """   SELECT TRANSPORTATION, ADDED_AS_ATTRACTION
            FROM ItineraryTransportation
            ORDER BY ADDED_AS_ATTRACTION;
      """,
   ).fetchall()

   assert [
      ( row[ 'TRANSPORTATION' ], row[ 'ADDED_AS_ATTRACTION' ] )
      for row in rows
   ] == [
      ( ZOOMOBILE, 1 ),
   ]


def Test_Apply_TestAnimalKey_ExpectDeleteAnimalCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   calls: list[ tuple[ str, str, str | None ] ] = []

   monkeypatch.setattr(
      RemoveItineraryItemProvider,
      'delete_itinerary_animal',
      lambda cur, *, species, exhibit, enclosure_name: calls.append(
         ( species, exhibit, enclosure_name ) ) )

   cur = remover_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      AnimalScheduleItemKey(
         species='African Lion',
         exhibit='Africa Savanna',
         enclosure_name='Outdoor' ) )
   cur.close()

   assert calls == [ ( 'African Lion', 'Africa Savanna', 'Outdoor' ) ]


def Test_Apply_TestGuardiansTalkKey_ExpectDeleteTalkCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   calls: list[ str ] = []

   monkeypatch.setattr(
      RemoveItineraryItemProvider,
      'delete_itinerary_guardians_talk',
      lambda cur, *, talk_name: calls.append( talk_name ) )

   cur = remover_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      GuardiansTalkScheduleItemKey(
         name='Zebra Talk',
         start_time='11:00 AM',
         end_time='11:30 AM' ) )
   cur.close()

   assert calls == [ 'Zebra Talk' ]


def Test_Apply_TestWildEncounterKey_ExpectDeleteEncounterCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   calls: list[ str ] = []

   monkeypatch.setattr(
      RemoveItineraryItemProvider,
      'delete_itinerary_wild_encounter',
      lambda cur, *, wild_encounter: calls.append( wild_encounter ) )

   cur = remover_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      WildEncounterScheduleItemKey(
         name='Penguin Encounter',
         start_time='2:00 PM',
         end_time='2:20 PM' ) )
   cur.close()

   assert calls == [ 'Penguin Encounter' ]


def Test_Apply_TestEventKey_ExpectDeleteEventCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   calls: list[ ItineraryEventType ] = []

   monkeypatch.setattr(
      RemoveItineraryItemProvider,
      'delete_itinerary_event',
      lambda cur, *, event_type: calls.append( event_type ) )

   cur = remover_conn.cursor()
   ItineraryItemRemover.apply( cur, ItineraryEventType.LUNCH )
   cur.close()

   assert calls == [ ItineraryEventType.LUNCH ]


def Test_Apply_TestPlainAttractionKey_ExpectDeleteAttractionCalled(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   calls: list[ str ] = []

   monkeypatch.setattr(
      'api.itinerary.operations.itinerary_item_remover.ItineraryProvider.fetch_saved_itinerary',
      lambda conn: SavedItinerary(
         date_value='2026-06-15',
         arrival_time='9:30 AM',
         departure_time='5:00 PM' ) )
   monkeypatch.setattr(
      RemoveItineraryItemProvider,
      'delete_itinerary_attraction',
      lambda cur, *, name: calls.append( name ) )

   cur = remover_conn.cursor()
   ItineraryItemRemover.apply(
      cur,
      AttractionScheduleItemKey( name='Conservation Carousel' ) )
   cur.close()

   assert calls == [ 'Conservation Carousel' ]


def Test_Remove_TestTransitKey_ExpectTransitReschedulePath(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   called: list[ TransportationScheduleItemKey ] = []

   monkeypatch.setattr(
      ItineraryItemRemover,
      'remove_transit_transportation_and_reschedule',
      lambda conn, schedule_item_key: (
         called.append( schedule_item_key )
         or ItinerarySaveResult(
            status=ItineraryErrorType.SUCCESS,
            reasons=[],
            itinerary=ItineraryBuilder.empty() ) ) )

   key = TransportationScheduleItemKey(
      name=ZOOMOBILE,
      added_as_attraction=False )
   result = ItineraryItemRemover.remove( remover_conn, key )

   assert result.status == ItineraryErrorType.SUCCESS
   assert called == [ key ]


def Test_Remove_TestNonTransitKey_ExpectCommitterPath(
      remover_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:

   calls: list[ AttractionScheduleItemKey ] = []

   monkeypatch.setattr(
      ItineraryItemScheduleChangeCommitter,
      'commit',
      lambda conn, schedule_item_key, apply_fn: (
         calls.append( schedule_item_key )
         or ItinerarySaveResult(
            status=ItineraryErrorType.SUCCESS,
            reasons=[],
            itinerary=ItineraryBuilder.empty() ) ) )

   key = AttractionScheduleItemKey( name='Conservation Carousel' )
   result = ItineraryItemRemover.remove( remover_conn, key )

   assert result.status == ItineraryErrorType.SUCCESS
   assert calls == [ key ]
