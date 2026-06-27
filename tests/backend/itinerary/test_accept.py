from __future__ import annotations

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.coordinators.attraction_coordinator import AttractionCoordinator
from api.itinerary.coordinators.itinerary_coordinator import ItineraryCoordinator
from conftest import DbControllers

def test_accept_itinerary_clears_added_animal_flags( db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD,
               IS_ADDED
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 90, 90, 1 ),
               ( 'African Penguin', 'Africa Savanna', 80, 80, 0 );
      """ )
   db.conn.commit()

   assert ItineraryCoordinator.accept_itinerary()

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE IS_ADDED = 1;'
   ).fetchone()[ 0 ] == 0

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAnimal WHERE OLD_LIKELIHOOD IS NOT NULL;'
   ).fetchone()[ 0 ] == 0


def test_accept_itinerary_removes_zero_likelihood_and_deleted_items( db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 90, 60 ),
               ( 'African Penguin', 'Africa Savanna', 40, 80 );
      """ )
   db.conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'Conservation Carousel', 100, 0 ),
               ( 'Greenhouse', 50, 75 );
      """ )
   db.conn.execute(
      """   INSERT INTO ItineraryGuardiansTalk (
               TALK_NAME,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES
               ( 'African Lion', '10:00 AM', '10:30 AM', 1 ),
               ( 'Amur Tiger', '11:00', '11:30', 0 );
      """ )
   db.conn.execute(
      """   INSERT INTO ItineraryWildEncounter (
               WILD_ENCOUNTER,
               START_TIME,
               END_TIME,
               IS_DELETED
            )
            VALUES
               ( 'African Rainforest', '2:00 PM', '2:45 PM', 1 ),
               ( 'Kangaroo', '1:00 PM', '1:45 PM', 0 );
      """ )
   db.conn.commit()

   assert ItineraryCoordinator.accept_itinerary()

   assert [
      row[ 'SPECIES' ]
      for row in db.conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   ] == [ 'African Lion', 'African Penguin' ]
   assert [
      row[ 'ATTRACTION' ]
      for row in db.conn.execute( 'SELECT ATTRACTION FROM ItineraryAttraction;' )
   ] == [ 'Greenhouse' ]
   assert [
      row[ 'TALK_NAME' ]
      for row in db.conn.execute( 'SELECT TALK_NAME FROM ItineraryGuardiansTalk;' )
   ] == [ 'Amur Tiger' ]
   assert [
      row[ 'WILD_ENCOUNTER' ]
      for row in db.conn.execute( 'SELECT WILD_ENCOUNTER FROM ItineraryWildEncounter;' )
   ] == [ 'Kangaroo' ]


def test_accept_itinerary_removes_zero_likelihood_animals_without_override(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 80, 0 ),
               ( 'African Penguin', 'Africa Savanna', 70, 0 );
      """ )
   db.conn.commit()

   assert ItineraryCoordinator.accept_itinerary()

   assert db.conn.execute( 'SELECT COUNT(*) FROM ItineraryAnimal;' ).fetchone()[ 0 ] == 0


def test_accept_itinerary_keeps_zero_likelihood_animals_when_overridden(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAnimal (
               SPECIES,
               EXHIBIT,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'African Lion', 'Africa Savanna', 80, 0 ),
               ( 'African Penguin', 'Africa Savanna', 70, 0 );
      """ )
   db.conn.commit()

   assert ItineraryCoordinator.accept_itinerary(
      animals_to_keep=[
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
         },
      ] )

   rows = db.conn.execute(
      """   SELECT SPECIES, EXHIBIT, OLD_LIKELIHOOD
            FROM ItineraryAnimal
            ORDER BY SPECIES;
      """
   ).fetchall()

   assert len( rows ) == 1
   assert rows[ 0 ][ 'SPECIES' ] == 'African Lion'
   assert rows[ 0 ][ 'EXHIBIT' ] == 'Africa Savanna'
   assert rows[ 0 ][ 'OLD_LIKELIHOOD' ] is None


def test_accept_itinerary_removes_zero_likelihood_attractions_without_override(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'Conservation Carousel', 100, 0 ),
               ( 'Greenhouse', 80, 0 );
      """ )
   db.conn.commit()

   assert ItineraryCoordinator.accept_itinerary()

   assert db.conn.execute(
      'SELECT COUNT(*) FROM ItineraryAttraction;'
   ).fetchone()[ 0 ] == 0


def test_accept_itinerary_keeps_zero_likelihood_attractions_when_overridden(
      db: DbControllers ) -> None:
   db.conn.execute(
      """   INSERT INTO ItineraryAttraction (
               ATTRACTION,
               OLD_LIKELIHOOD,
               NEW_LIKELIHOOD
            )
            VALUES
               ( 'Conservation Carousel', 100, 0 ),
               ( 'Greenhouse', 80, 0 );
      """ )
   db.conn.commit()

   assert ItineraryCoordinator.accept_itinerary(
      attractions_to_keep=[ 'Conservation Carousel' ] )

   rows = db.conn.execute(
      """   SELECT ATTRACTION, OLD_LIKELIHOOD
            FROM ItineraryAttraction
            ORDER BY ATTRACTION;
      """
   ).fetchall()

   assert len( rows ) == 1
   assert rows[ 0 ][ 'ATTRACTION' ] == 'Conservation Carousel'
   assert rows[ 0 ][ 'OLD_LIKELIHOOD' ] is None

