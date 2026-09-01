from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.save_itinerary_provider import SaveItineraryProvider
from api.models.guardians_talk_diff import GuardiansTalkDiff
from api.models.transportation_diff import TransportationDiff
from api.models.wild_encounter_diff import WildEncounterDiff


ZOOMOBILE = 'Zoomobile'
KANGAROO = 'Kangaroo'
KANGAROO_ENCOUNTER_TIME = '3:30 PM'

SAVE_PROVIDER_SCHEMA = """
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
"""


@pytest.fixture
def save_provider_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SAVE_PROVIDER_SCHEMA )
   conn.commit()

   yield conn

   conn.close()


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
