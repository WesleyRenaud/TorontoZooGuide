from __future__ import annotations

from datetime import date
import sqlite3

import pytest

from api.itinerary.data_access.save_itinerary_provider import SaveItineraryProvider
from api.itinerary.data_access.validated_itinerary import ValidatedItinerary
from api.models.animal_diff import AnimalDiff
from api.models.attraction_diff import AttractionDiff
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.itinerary_event import ItineraryEvent
from api.models.itinerary_transportation_leg import ItineraryTransportationLeg
from api.models.transportation_diff import TransportationDiff
from api.models.wild_encounter_diff import WildEncounterDiff
from api.shared.enums import ItineraryEventType

ZOOMOBILE = 'Zoomobile'
KANGAROO = 'Kangaroo'
KANGAROO_ENCOUNTER_TIME = '3:30 PM'
VISIT_DATE = date( 2026, 6, 15 )
AFRICA = 'Africa'
AMERICAS = 'Americas'
CAROUSEL = 'Conservation Carousel'
LION = 'African Lion'
SAVANNA = 'Africa Savanna'

SAVE_PROVIDER_SCHEMA = """
CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);

CREATE TABLE ItineraryExhibit (
   EXHIBIT              TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE ItineraryAnimal (
   SPECIES              TEXT        NOT NULL,
   EXHIBIT              TEXT        NOT NULL,
   ENCLOSURE_NAME       TEXT,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   IS_ADDED             INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK      INTEGER     NOT NULL DEFAULT 0,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryAttraction (
   ATTRACTION           TEXT        NOT NULL PRIMARY KEY,
   OLD_LIKELIHOOD       INTEGER,
   NEW_LIKELIHOOD       INTEGER,
   START_TIME           TEXT,
   END_TIME             TEXT
);

CREATE TABLE ItineraryGuardiansTalk (
   TALK_NAME            TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);

CREATE TABLE ItineraryWildEncounter (
   WILD_ENCOUNTER       TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT,
   IS_DELETED           INTEGER     NOT NULL DEFAULT 0
);

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

CREATE TABLE ItineraryEvent (
   EVENT_TYPE           TEXT        NOT NULL PRIMARY KEY,
   START_TIME           TEXT,
   END_TIME             TEXT
);
"""


@pytest.fixture
def save_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SAVE_PROVIDER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


def _empty_validated() -> ValidatedItinerary:
   return ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[],
      attractions=[],
      guardians_talks=[],
      wild_encounters=[],
      events=[],
   )


def Test_SaveItineraryWildEncounters_Test24HourStartTime_ExpectDisplayFormat(
      save_provider_conn: sqlite3.Connection ) -> None:
   wild_encounters = [
      WildEncounterDiff(
         name='Grizzly Bear',
         is_deleted=False,
         start_time='13:00',
         end_time='1:45 PM',
         meeting_spot='Americas Pavilion',
         link='https://example.com/grizzly' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_wild_encounters( cur, wild_encounters )
   save_provider_conn.commit()
   cur.close()

   encounter = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'Grizzly Bear';
      """ ).fetchone()

   assert encounter is not None
   assert dict( encounter ) == {
      'START_TIME': '1:00 PM',
      'END_TIME': '1:45 PM',
   }


def Test_SaveItineraryGuardiansTalks_TestScheduledTalk_ExpectDisplayFormat(
      save_provider_conn: sqlite3.Connection ) -> None:
   guardians_talks = [
      GuardiansTalkDiff(
         name='African Lion',
         is_deleted=False,
         start_time='10:00',
         end_time='10:30' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_guardians_talks( cur, guardians_talks )
   save_provider_conn.commit()
   cur.close()

   talk = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = 'African Lion';
      """ ).fetchone()

   assert talk is not None
   assert dict( talk ) == {
      'START_TIME': '10:00 AM',
      'END_TIME': '10:30 AM',
      'IS_DELETED': 0,
   }


def Test_SaveItineraryWildEncounters_TestKangarooAt330Pm_ExpectPersistedActiveRow(
      save_provider_conn: sqlite3.Connection ) -> None:
   wild_encounters = [
      WildEncounterDiff(
         name=KANGAROO,
         is_deleted=False,
         start_time=KANGAROO_ENCOUNTER_TIME,
         end_time='4:15 PM',
         meeting_spot='Wild Encounter - Eurasia Meeting Spot',
         link='https://example.test/kangaroo' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_wild_encounters( cur, wild_encounters )
   save_provider_conn.commit()
   cur.close()

   encounter = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = ?;
      """,
      ( KANGAROO, ),
   ).fetchone()

   assert encounter is not None
   assert dict( encounter ) == {
      'START_TIME': KANGAROO_ENCOUNTER_TIME,
      'END_TIME': '4:15 PM',
      'IS_DELETED': 0,
   }


def Test_SaveItineraryWildEncounters_TestScheduledEncounter_ExpectDisplayFormat(
      save_provider_conn: sqlite3.Connection ) -> None:
   wild_encounters = [
      WildEncounterDiff(
         name='African Rainforest',
         is_deleted=False,
         start_time='14:00',
         end_time='2:45 PM',
         meeting_spot='Rainforest Gate',
         link='african-rainforest' ),
   ]
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_wild_encounters( cur, wild_encounters )
   save_provider_conn.commit()
   cur.close()

   encounter = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'African Rainforest';
      """ ).fetchone()

   assert encounter is not None
   assert dict( encounter ) == {
      'START_TIME': '2:00 PM',
      'END_TIME': '2:45 PM',
      'IS_DELETED': 0,
   }


def Test_SaveItineraryTransportations_TestAttractionModeZoomobile_ExpectTransportationRow(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_transportations(
      cur,
      [
         TransportationDiff(
            name=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
      ] )
   save_provider_conn.commit()
   cur.close()

   row = save_provider_conn.execute(
      """   SELECT TRANSPORTATION, ADDED_AS_ATTRACTION
            FROM ItineraryTransportation;
      """
   ).fetchone()
   leg_count = save_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryTransportationLeg;'
   ).fetchone()

   assert row is not None
   assert row[ 'TRANSPORTATION' ] == ZOOMOBILE
   assert row[ 'ADDED_AS_ATTRACTION' ] == 1
   assert leg_count is not None
   assert leg_count[ 'COUNT' ] == 0


def Test_SaveItineraryTransportations_TestBothModes_ExpectTwoRows(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_transportations(
      cur,
      [
         TransportationDiff(
            name=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
         TransportationDiff(
            name=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False ),
      ] )
   save_provider_conn.commit()
   cur.close()

   rows = save_provider_conn.execute(
      """   SELECT TRANSPORTATION, ADDED_AS_ATTRACTION
            FROM ItineraryTransportation
            ORDER BY ADDED_AS_ATTRACTION;
      """
   ).fetchall()

   assert [
      {
         'TRANSPORTATION': row[ 'TRANSPORTATION' ],
         'ADDED_AS_ATTRACTION': row[ 'ADDED_AS_ATTRACTION' ],
      }
      for row in rows
   ] == [
      { 'TRANSPORTATION': ZOOMOBILE, 'ADDED_AS_ATTRACTION': 0 },
      { 'TRANSPORTATION': ZOOMOBILE, 'ADDED_AS_ATTRACTION': 1 },
   ]


def Test_SaveItineraryDate_TestVisitWindow_ExpectPersistedRow(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_date(
      cur,
      VISIT_DATE,
      '9:30 AM',
      '5:00 PM' )
   save_provider_conn.commit()
   cur.close()

   row = save_provider_conn.execute(
      """   SELECT ITINERARY_DATE, ARRIVAL_TIME, DEPARTURE_TIME
            FROM ItineraryDate;
      """
   ).fetchone()

   assert row is not None
   assert dict( row ) == {
      'ITINERARY_DATE': str( VISIT_DATE ),
      'ARRIVAL_TIME': '9:30 AM',
      'DEPARTURE_TIME': '5:00 PM',
   }


def Test_SaveItineraryAnimals_TestScheduledAnimal_ExpectPersistedRow(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_animals(
      cur,
      [
         AnimalDiff(
            species=LION,
            exhibit=SAVANNA,
            enclosure_name='Outdoor',
            old_likelihood=None,
            new_likelihood=100,
            is_added=True,
            covered_by_talk=False,
            start_time='10:00',
            end_time='10:08' ),
      ] )
   save_provider_conn.commit()
   cur.close()

   row = save_provider_conn.execute(
      """   SELECT SPECIES, EXHIBIT, ENCLOSURE_NAME, NEW_LIKELIHOOD,
                   IS_ADDED, COVERED_BY_TALK, START_TIME, END_TIME
            FROM ItineraryAnimal;
      """
   ).fetchone()

   assert row is not None
   assert dict( row ) == {
      'SPECIES': LION,
      'EXHIBIT': SAVANNA,
      'ENCLOSURE_NAME': 'Outdoor',
      'NEW_LIKELIHOOD': 100,
      'IS_ADDED': 1,
      'COVERED_BY_TALK': 0,
      'START_TIME': '10:00 AM',
      'END_TIME': '10:08 AM',
   }


def Test_SaveItineraryAnimals_TestEmptyList_ExpectNoRows(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_animals( cur, [] )
   save_provider_conn.commit()
   cur.close()

   count = save_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryAnimal;'
   ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_SaveItineraryAttractions_TestScheduledAttraction_ExpectPersistedRow(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_attractions(
      cur,
      [
         AttractionDiff(
            name=CAROUSEL,
            old_likelihood=None,
            new_likelihood=3,
            start_time='11:00',
            end_time='11:15' ),
      ] )
   save_provider_conn.commit()
   cur.close()

   row = save_provider_conn.execute(
      """   SELECT ATTRACTION, NEW_LIKELIHOOD, START_TIME, END_TIME
            FROM ItineraryAttraction;
      """
   ).fetchone()

   assert row is not None
   assert dict( row ) == {
      'ATTRACTION': CAROUSEL,
      'NEW_LIKELIHOOD': 3,
      'START_TIME': '11:00 AM',
      'END_TIME': '11:15 AM',
   }


def Test_SaveItineraryTransportations_TestLegsAndMarkers_ExpectPersistedChildren(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_transportations(
      cur,
      [
         TransportationDiff(
            name=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=False,
            start_time='11:30 AM',
            end_time='12:00 PM',
            route='summer',
            bulk_transit_evaluated=True,
            legs=[
               ItineraryTransportationLeg(
                  from_station=AFRICA,
                  to_station=AMERICAS,
                  start_time='11:30 AM',
                  end_time='11:45 AM',
                  transportation=ZOOMOBILE,
                  added_as_attraction=False ),
               ItineraryTransportationLeg(
                  from_station=AMERICAS,
                  to_station=AFRICA,
                  start_time='11:45 AM',
                  end_time='12:00 PM',
                  transportation=ZOOMOBILE,
                  added_as_attraction=False ),
            ],
            route_marker_sequences=[ [ 'm-1', 'm-2' ], [ 'm-3' ] ] ),
      ] )
   save_provider_conn.commit()
   cur.close()

   transport = save_provider_conn.execute(
      """   SELECT START_TIME, END_TIME, ROUTE, BULK_TRANSIT_EVALUATED
            FROM ItineraryTransportation
            WHERE TRANSPORTATION = ? AND ADDED_AS_ATTRACTION = 0;
      """,
      ( ZOOMOBILE, ),
   ).fetchone()
   legs = save_provider_conn.execute(
      """   SELECT FROM_STATION, TO_STATION, START_TIME, END_TIME
            FROM ItineraryTransportationLeg
            ORDER BY START_TIME;
      """
   ).fetchall()
   markers = save_provider_conn.execute(
      """   SELECT SEQUENCE, MARKER_ORDER, MARKER_ID
            FROM ItineraryTransportationRouteMarker
            ORDER BY SEQUENCE, MARKER_ORDER;
      """
   ).fetchall()

   assert transport is not None
   assert dict( transport ) == {
      'START_TIME': '11:30 AM',
      'END_TIME': '12:00 PM',
      'ROUTE': 'summer',
      'BULK_TRANSIT_EVALUATED': 1,
   }
   assert [
      {
         'FROM_STATION': leg[ 'FROM_STATION' ],
         'TO_STATION': leg[ 'TO_STATION' ],
         'START_TIME': leg[ 'START_TIME' ],
         'END_TIME': leg[ 'END_TIME' ],
      }
      for leg in legs
   ] == [
      {
         'FROM_STATION': AFRICA,
         'TO_STATION': AMERICAS,
         'START_TIME': '11:30 AM',
         'END_TIME': '11:45 AM',
      },
      {
         'FROM_STATION': AMERICAS,
         'TO_STATION': AFRICA,
         'START_TIME': '11:45 AM',
         'END_TIME': '12:00 PM',
      },
   ]
   assert [
      {
         'SEQUENCE': marker[ 'SEQUENCE' ],
         'MARKER_ORDER': marker[ 'MARKER_ORDER' ],
         'MARKER_ID': marker[ 'MARKER_ID' ],
      }
      for marker in markers
   ] == [
      { 'SEQUENCE': 0, 'MARKER_ORDER': 0, 'MARKER_ID': 'm-1' },
      { 'SEQUENCE': 0, 'MARKER_ORDER': 1, 'MARKER_ID': 'm-2' },
      { 'SEQUENCE': 1, 'MARKER_ORDER': 0, 'MARKER_ID': 'm-3' },
   ]


def Test_SaveItineraryEvents_TestLunchEvent_ExpectPersistedRow(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_events(
      cur,
      [
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00',
            end_time='12:30' ),
      ] )
   save_provider_conn.commit()
   cur.close()

   row = save_provider_conn.execute(
      """   SELECT EVENT_TYPE, START_TIME, END_TIME
            FROM ItineraryEvent;
      """
   ).fetchone()

   assert row is not None
   assert dict( row ) == {
      'EVENT_TYPE': ItineraryEventType.LUNCH.value,
      'START_TIME': '12:00 PM',
      'END_TIME': '12:30 PM',
   }


def Test_SaveItineraryGuardiansTalks_TestEmptyList_ExpectNoRows(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_guardians_talks( cur, [] )
   save_provider_conn.commit()
   cur.close()

   count = save_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryGuardiansTalk;'
   ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_SaveItineraryWildEncounters_TestEmptyList_ExpectNoRows(
      save_provider_conn: sqlite3.Connection ) -> None:
   cur = save_provider_conn.cursor()
   SaveItineraryProvider.save_itinerary_wild_encounters( cur, [] )
   save_provider_conn.commit()
   cur.close()

   count = save_provider_conn.execute(
      'SELECT COUNT(*) AS COUNT FROM ItineraryWildEncounter;'
   ).fetchone()

   assert count is not None
   assert count[ 'COUNT' ] == 0


def Test_SaveValidatedItinerary_TestOrchestration_ExpectSubSaversInvoked(
      save_provider_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls: list[ str ] = []
   validated = ValidatedItinerary(
      arrival_time='9:30 AM',
      departure_time='5:00 PM',
      animals=[
         AnimalDiff(
            species=LION,
            exhibit=SAVANNA,
            old_likelihood=None,
            new_likelihood=100 ),
      ],
      attractions=[
         AttractionDiff(
            name=CAROUSEL,
            old_likelihood=None,
            new_likelihood=3 ),
      ],
      guardians_talks=[],
      wild_encounters=[],
      events=[
         ItineraryEvent(
            event_type=ItineraryEventType.LUNCH,
            start_time='12:00 PM',
            end_time='12:30 PM' ),
      ],
      transportations=[
         TransportationDiff(
            name=ZOOMOBILE,
            old_likelihood=None,
            new_likelihood=3,
            added_as_attraction=True ),
      ],
   )

   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_date',
      lambda cur, visit_date, arrival_time, departure_time: calls.append( 'date' ) )
   monkeypatch.setattr(
      'api.itinerary.data_access.save_itinerary_provider.ItineraryExhibitProvider.save_itinerary_exhibits',
      lambda cur, exhibits: calls.append( f'exhibits:{ ",".join( exhibits ) }' ) )
   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_animals',
      lambda cur, animals: calls.append( f'animals:{ len( animals ) }' ) )
   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_attractions',
      lambda cur, attractions: calls.append( f'attractions:{ len( attractions ) }' ) )
   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_transportations',
      lambda cur, transportations: calls.append(
         f'transportations:{ len( transportations ) }' ) )
   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_guardians_talks',
      lambda cur, talks: calls.append( f'talks:{ len( talks ) }' ) )
   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_wild_encounters',
      lambda cur, encounters: calls.append( f'encounters:{ len( encounters ) }' ) )
   monkeypatch.setattr(
      SaveItineraryProvider,
      'save_itinerary_events',
      lambda cur, events: calls.append( f'events:{ len( events ) }' ) )

   result = SaveItineraryProvider.save_validated_itinerary(
      save_provider_conn,
      VISIT_DATE,
      validated,
      selected_exhibits=[ SAVANNA ] )

   assert result is True
   assert calls == [
      'date',
      f'exhibits:{ SAVANNA }',
      'animals:1',
      'attractions:1',
      'transportations:1',
      'talks:0',
      'encounters:0',
      'events:1',
   ]


def Test_SaveValidatedItinerary_TestEmptyPayload_ExpectDateAndCommit(
      save_provider_conn: sqlite3.Connection ) -> None:
   result = SaveItineraryProvider.save_validated_itinerary(
      save_provider_conn,
      VISIT_DATE,
      _empty_validated(),
      selected_exhibits=[ SAVANNA ] )

   date_row = save_provider_conn.execute(
      """   SELECT ITINERARY_DATE, ARRIVAL_TIME, DEPARTURE_TIME
            FROM ItineraryDate;
      """
   ).fetchone()
   exhibit_row = save_provider_conn.execute(
      'SELECT EXHIBIT FROM ItineraryExhibit;'
   ).fetchone()

   assert result is True
   assert date_row is not None
   assert dict( date_row ) == {
      'ITINERARY_DATE': str( VISIT_DATE ),
      'ARRIVAL_TIME': '9:30 AM',
      'DEPARTURE_TIME': '5:00 PM',
   }
   assert exhibit_row is not None
   assert exhibit_row[ 'EXHIBIT' ] == SAVANNA
