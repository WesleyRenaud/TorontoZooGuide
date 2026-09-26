from __future__ import annotations

import sqlite3

import pytest

from api.itinerary.data_access.itinerary_provider import ItineraryProvider
from api.itinerary.domain.itinerary_transportation_animal_likelihood_lookup import ItineraryTransportationAnimalLikelihoodLookup
from api.itinerary.domain.itinerary_transportation_animal_syncer import ItineraryTransportationAnimalSyncer
from api.models.animal import Animal
from api.models.animal_diff import AnimalDiff
from api.shared.enums.position import Position
from api.transportation.data_access.transportation_animal_provider import TransportationAnimalProvider
from api.transportation.data_access.transportation_animal_record import TransportationAnimalRecord


SYNC_SCHEMA = """
CREATE TABLE ItineraryDate (
   ITINERARY_DATE       TEXT,
   ARRIVAL_TIME         TEXT,
   DEPARTURE_TIME       TEXT
);

CREATE TABLE ItineraryAnimal (
   SPECIES                 TEXT        NOT NULL,
   EXHIBIT                 TEXT        NOT NULL,
   ENCLOSURE_NAME          TEXT,
   OLD_LIKELIHOOD          INTEGER,
   NEW_LIKELIHOOD          INTEGER,
   IS_ADDED                INTEGER     NOT NULL DEFAULT 0,
   COVERED_BY_TALK         INTEGER     NOT NULL DEFAULT 0,
   ADDED_BY_TRANSPORTATION INTEGER     NOT NULL DEFAULT 0,
   START_TIME              TEXT,
   END_TIME                TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT, ENCLOSURE_NAME )
);

CREATE TABLE ItineraryTransportation (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   PRIMARY KEY ( TRANSPORTATION, ADDED_AS_ATTRACTION )
);

CREATE TABLE ItineraryTransportationLeg (
   TRANSPORTATION           TEXT        NOT NULL,
   ADDED_AS_ATTRACTION      INTEGER     NOT NULL DEFAULT 0,
   FROM_STATION             TEXT        NOT NULL,
   TO_STATION               TEXT        NOT NULL,
   START_TIME               TEXT        NOT NULL,
   END_TIME                 TEXT        NOT NULL
);

CREATE TABLE TransportationAnimal (
   TRANSPORTATION      TEXT        NOT NULL,
   FROM_STATION        TEXT        NOT NULL,
   TO_STATION          TEXT        NOT NULL,
   SPECIES             TEXT        NOT NULL,
   EXHIBIT             TEXT        NOT NULL,
   ENCLOSURE_NAME      TEXT,
   PRIMARY KEY ( SPECIES, EXHIBIT, ENCLOSURE_NAME )
);
"""

GIRAFFE = TransportationAnimalRecord(
   transportation='Zoomobile',
   from_station='Canadian Domain Zoomobile Station',
   to_station='Africa Zoomobile Station',
   species='Masai Giraffe',
   exhibit='Africa Savanna',
   enclosure_name='Outdoor',
)
ZEBRA = TransportationAnimalRecord(
   transportation='Zoomobile',
   from_station='Main Zoomobile Station',
   to_station='Canadian Domain Zoomobile Station',
   species="Grevy's Zebra",
   exhibit='Canadian Domain',
   enclosure_name='Savanna Grasslands',
)


def _likelihood_lookup(
      links: list[ TransportationAnimalRecord ],
      likelihood: int ) -> ItineraryTransportationAnimalLikelihoodLookup:
   return ItineraryTransportationAnimalLikelihoodLookup(
      [
         Animal(
            species=link.species,
            exhibit=link.exhibit,
            enclosure_name=link.enclosure_name,
            likelihood=likelihood )
         for link in links
      ] )


def _insert_leg(
      conn: sqlite3.Connection,
      *,
      from_station: str,
      to_station: str,
      start_time: str,
      end_time: str ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryTransportationLeg (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION,
               FROM_STATION,
               TO_STATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      (
         GIRAFFE.transportation,
         0,
         from_station,
         to_station,
         start_time,
         end_time,
      ),
   )


def _insert_transportation(
      conn: sqlite3.Connection,
      transportation: str = GIRAFFE.transportation ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryTransportation (
               TRANSPORTATION,
               ADDED_AS_ATTRACTION
            )
            VALUES ( ?, ? );
      """,
      ( transportation, 0 ),
   )


def _insert_animal(
      conn: sqlite3.Connection,
      *,
      species: str,
      exhibit: str,
      enclosure_name: str,
      added_by_transportation: int,
      start_time: str | None = None,
      end_time: str | None = None,
      old_likelihood: int | None = None,
      new_likelihood: int | None = None ) -> None:
   conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               ADDED_BY_TRANSPORTATION,
               START_TIME,
               END_TIME
            )
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ? );
      """,
      (
         species,
         exhibit,
         enclosure_name,
         old_likelihood,
         new_likelihood,
         added_by_transportation,
         start_time,
         end_time,
      ),
   )


def _insert_giraffe_leg( conn: sqlite3.Connection ) -> None:
   _insert_leg(
      conn,
      from_station=GIRAFFE.from_station,
      to_station=GIRAFFE.to_station,
      start_time='11:00 AM',
      end_time='11:10 AM' )


def _stub_likelihood(
      monkeypatch: pytest.MonkeyPatch,
      likelihood: int | None ) -> int | None:
   monkeypatch.setattr(
      'api.itinerary.domain.itinerary_transportation_animal_syncer.'
      'ItineraryTransportationAnimalLikelihoodResolver.resolve',
      lambda conn, links: (
         ItineraryTransportationAnimalLikelihoodLookup( [] )
         if likelihood is None
         else _likelihood_lookup( links, likelihood )
      ) )
   return likelihood


@pytest.fixture
def sync_conn() -> sqlite3.Connection:
   conn = sqlite3.connect( ':memory:' )
   conn.row_factory = sqlite3.Row
   conn.executescript( SYNC_SCHEMA )
   conn.executemany(
      """   INSERT INTO TransportationAnimal (
               TRANSPORTATION,
               FROM_STATION,
               TO_STATION,
               SPECIES,
               EXHIBIT,
               ENCLOSURE_NAME
            )
            VALUES ( ?, ?, ?, ?, ?, ? );
      """,
      [
         (
            GIRAFFE.transportation,
            GIRAFFE.from_station,
            GIRAFFE.to_station,
            GIRAFFE.species,
            GIRAFFE.exhibit,
            GIRAFFE.enclosure_name,
         ),
         (
            ZEBRA.transportation,
            ZEBRA.from_station,
            ZEBRA.to_station,
            ZEBRA.species,
            ZEBRA.exhibit,
            ZEBRA.enclosure_name,
         ),
      ],
   )
   conn.commit()
   yield conn
   conn.close()


def Test_FetchAll_TestSeededLinks_ExpectEnclosureKeys( sync_conn: sqlite3.Connection ) -> None:
   links = TransportationAnimalProvider.fetch_all( sync_conn )

   assert {
      ( link.species, link.exhibit, link.enclosure_name )
      for link in links
   } == {
      ( GIRAFFE.species, GIRAFFE.exhibit, GIRAFFE.enclosure_name ),
      ( ZEBRA.species, ZEBRA.exhibit, ZEBRA.enclosure_name ),
   }


def Test_FetchAll_TestDuplicateEnclosure_ExpectPrimaryKeyRejectsSecondRow(
      sync_conn: sqlite3.Connection ) -> None:
   with pytest.raises( sqlite3.IntegrityError ):
      sync_conn.execute(
         """   INSERT INTO TransportationAnimal (
                  TRANSPORTATION,
                  FROM_STATION,
                  TO_STATION,
                  SPECIES,
                  EXHIBIT,
                  ENCLOSURE_NAME
               )
               VALUES ( ?, ?, ?, ?, ?, ? );
         """,
         (
            GIRAFFE.transportation,
            GIRAFFE.to_station,
            'Tundra Zoomobile Station',
            GIRAFFE.species,
            GIRAFFE.exhibit,
            GIRAFFE.enclosure_name,
         ),
      )


def Test_Apply_TestMatchingLegs_ExpectInsertedWithoutTimes(
      sync_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   _insert_giraffe_leg( sync_conn )
   sync_conn.commit()
   _stub_likelihood( monkeypatch, None )

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.species == GIRAFFE.species
   assert giraffe.enclosure_name == GIRAFFE.enclosure_name
   assert giraffe.added_by_transportation is True
   assert giraffe.transportation == GIRAFFE.transportation
   assert giraffe.old_likelihood is None
   assert giraffe.new_likelihood == 0
   assert giraffe.start_time is None
   assert giraffe.end_time is None


def Test_Apply_TestGuestOwnedRow_ExpectSkipped(
      sync_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   start_time = '10:00 AM'
   end_time = '10:10 AM'
   _insert_giraffe_leg( sync_conn )
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=0,
      start_time=start_time,
      end_time=end_time )
   sync_conn.commit()
   _stub_likelihood( monkeypatch, None )

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.added_by_transportation is False
   assert giraffe.start_time == start_time
   assert giraffe.end_time == end_time
   assert giraffe.new_likelihood is None


def Test_Apply_TestMatchingLegs_ExpectCalculatedLikelihood(
      sync_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   likelihood = 80
   _insert_giraffe_leg( sync_conn )
   sync_conn.commit()
   _stub_likelihood( monkeypatch, likelihood )

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   giraffe = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )[ Position.FIRST ]

   assert giraffe.new_likelihood == likelihood
   assert giraffe.old_likelihood is None
   assert giraffe.start_time is None


def Test_Apply_TestExistingTransportationAnimal_ExpectLikelihoodRefreshed(
      sync_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   likelihood = 65
   _insert_giraffe_leg( sync_conn )
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=1 )
   sync_conn.commit()
   _stub_likelihood( monkeypatch, likelihood )

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.added_by_transportation is True
   assert giraffe.new_likelihood == likelihood
   assert giraffe.old_likelihood is None
   assert giraffe.start_time is None


def Test_Apply_TestStaleTransportationAnimal_ExpectDeleted(
      sync_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=1 )
   _insert_animal(
      sync_conn,
      species=ZEBRA.species,
      exhibit=ZEBRA.exhibit,
      enclosure_name=ZEBRA.enclosure_name,
      added_by_transportation=0 )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   assert [
      ( row.species, row.added_by_transportation )
      for row in rows
   ] == [
      ( ZEBRA.species, False ),
   ]


def Test_Apply_TestExistingTransportationAnimal_ExpectOldLikelihoodRolledFromPreviousNew(
      sync_conn: sqlite3.Connection,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   previous_likelihood = 80
   likelihood = 65
   _insert_giraffe_leg( sync_conn )
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=1,
      new_likelihood=previous_likelihood )
   sync_conn.commit()
   _stub_likelihood( monkeypatch, likelihood )

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   giraffe = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )[ Position.FIRST ]

   assert giraffe.added_by_transportation is True
   assert giraffe.old_likelihood == previous_likelihood
   assert giraffe.new_likelihood == likelihood


def Test_Apply_TestParentWithoutMatchingLeg_ExpectTransportationAnimalKept(
      sync_conn: sqlite3.Connection ) -> None:
   likelihood = 80
   _insert_transportation( sync_conn )
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=1,
      new_likelihood=likelihood )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.species == GIRAFFE.species
   assert giraffe.added_by_transportation is True
   assert giraffe.new_likelihood == likelihood
   assert giraffe.old_likelihood is None


def Test_Apply_TestUnknownCatalogTransportationAnimal_ExpectDeleted(
      sync_conn: sqlite3.Connection ) -> None:
   _insert_transportation( sync_conn )
   _insert_animal(
      sync_conn,
      species='Unknown Bird',
      exhibit='African Rainforest',
      enclosure_name='Indoor',
      added_by_transportation=1,
      new_likelihood=40 )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.apply( sync_conn )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   assert rows == []


def Test_PromoteSavedAnimals_TestEmptyList_ExpectTransportationRowKept(
      sync_conn: sqlite3.Connection ) -> None:
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=1 )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.promote_saved_animals( sync_conn, [] )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.added_by_transportation is True


def Test_PromoteSavedAnimals_TestTransportationRow_ExpectDeleted(
      sync_conn: sqlite3.Connection ) -> None:
   saved_animal = AnimalDiff(
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      old_likelihood=80,
      new_likelihood=65 )
   _insert_animal(
      sync_conn,
      species=saved_animal.species,
      exhibit=saved_animal.exhibit,
      enclosure_name=saved_animal.enclosure_name,
      added_by_transportation=1 )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.promote_saved_animals(
      sync_conn,
      [ saved_animal ] )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   assert rows == []


def Test_PromoteSavedAnimals_TestGuestRow_ExpectKept(
      sync_conn: sqlite3.Connection ) -> None:
   start_time = '10:00 AM'
   end_time = '10:10 AM'
   saved_animal = AnimalDiff(
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      old_likelihood=None,
      new_likelihood=65 )
   _insert_animal(
      sync_conn,
      species=saved_animal.species,
      exhibit=saved_animal.exhibit,
      enclosure_name=saved_animal.enclosure_name,
      added_by_transportation=0,
      start_time=start_time,
      end_time=end_time )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.promote_saved_animals(
      sync_conn,
      [ saved_animal ] )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.added_by_transportation is False
   assert giraffe.start_time == start_time


def Test_PromoteSavedAnimals_TestUnrelatedAnimal_ExpectTransportationRowKept(
      sync_conn: sqlite3.Connection ) -> None:
   saved_animal = AnimalDiff(
      species='African Lion',
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      old_likelihood=None,
      new_likelihood=100 )
   _insert_animal(
      sync_conn,
      species=GIRAFFE.species,
      exhibit=GIRAFFE.exhibit,
      enclosure_name=GIRAFFE.enclosure_name,
      added_by_transportation=1 )
   sync_conn.commit()

   ItineraryTransportationAnimalSyncer.promote_saved_animals(
      sync_conn,
      [ saved_animal ] )
   rows = ItineraryProvider.fetch_itinerary_animal_rows( sync_conn )

   giraffe = rows[ Position.FIRST ]

   assert len( rows ) == 1
   assert giraffe.species == GIRAFFE.species
   assert giraffe.added_by_transportation is True
