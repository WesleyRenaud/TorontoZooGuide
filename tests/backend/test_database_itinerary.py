from datetime import date

from api import zoo


def test_set_get_and_clear_itinerary( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   db.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      talk_time='10:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )
   db.set_wild_encounter_schedule(
      wild_encounter='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   assert db.set_itinerary(
      date='2026-06-15',
      animals=[ { 'species': 'African Lion', 'exhibit': 'Africa Savanna' } ],
      attractions=[ 'Conservation Carousel' ],
      guardians_talks=[ 'African Lion' ],
      wild_encounters=[ 'African Rainforest' ],
   )

   talk_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryGuardiansTalk
            WHERE TALK_NAME = 'African Lion';
      """ ).fetchone()
   encounter_schedule = db.conn.execute(
      """   SELECT START_TIME, END_TIME, IS_DELETED
            FROM ItineraryWildEncounter
            WHERE WILD_ENCOUNTER = 'African Rainforest';
      """ ).fetchone()

   assert dict( talk_schedule ) == {
      'START_TIME': '10:00',
      'END_TIME': '10:30',
      'IS_DELETED': 0
   }
   assert dict( encounter_schedule ) == {
      'START_TIME': '14:00',
      'END_TIME': '14:45',
      'IS_DELETED': 0
   }

   assert db.cancel_guardians_talk_occurrence(
      talk='African Lion',
      location='Africa Savanna',
      date='2026-06-15',
      time='10:00'
   )
   assert db.cancel_wild_encounter_occurrence(
      wild_encounter='African Rainforest',
      date='2026-06-15',
      time='14:00'
   )

   itinerary = db.get_itinerary()

   assert itinerary.date == '2026-06-15'
   assert [ animal.species for animal in itinerary.animals ] == [ 'African Lion' ]
   assert [ attraction.name for attraction in itinerary.attractions ] == [ 'Conservation Carousel' ]
   assert [
      ( talk.name, talk.start_time, talk.end_time )
      for talk in itinerary.guardians_talks
   ] == [
      ( 'African Lion', '10:00', '10:30' )
   ]
   assert [
      ( encounter.name, encounter.start_time, encounter.end_time )
      for encounter in itinerary.wild_encounters
   ] == [
      ( 'African Rainforest', '14:00', '14:45' )
   ]
   itinerary_dict = itinerary.to_dict()
   assert itinerary_dict[ 'animals' ][ 0 ][ 'old_likelihood' ] is None
   assert itinerary_dict[ 'animals' ][ 0 ][ 'likelihood' ] > 0
   assert itinerary_dict[ 'attractions' ][ 0 ][ 'old_likelihood' ] is None
   assert itinerary_dict[ 'attractions' ][ 0 ][ 'likelihood' ] > 0

   assert db.clear_itinerary()
   cleared = db.get_itinerary()

   assert cleared.date == ''
   assert cleared.animals == []
   assert cleared.attractions == []
   assert cleared.guardians_talks == []
   assert cleared.wild_encounters == []


def test_get_zoo_hours_returns_seeded_operating_bounds( db ):
   assert db.get_zoo_hours( '2026-06-20' ) == {
      'date': '2026-06-20',
      'earlyAdmissionTime': '09:00',
      'openTime': '09:30',
      'lastAdmissionTime': '18:00',
      'closeTime': '19:00'
   }

   assert db.get_zoo_hours( '2026-06-22' ) == {
      'date': '2026-06-22',
      'earlyAdmissionTime': None,
      'openTime': '09:30',
      'lastAdmissionTime': '17:00',
      'closeTime': '18:00'
   }

   assert db.get_zoo_hours( '2026-12-25' ) == {
      'date': '2026-12-25',
      'earlyAdmissionTime': None,
      'openTime': '11:00',
      'lastAdmissionTime': '15:00',
      'closeTime': '16:00'
   }


def test_accept_itinerary_removes_declined_and_deleted_items( db ):
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
               ( 'African Lion', '10:00', '10:30', 1 ),
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
               ( 'African Rainforest', '14:00', '14:45', 1 ),
               ( 'Kangaroo', '13:00', '13:45', 0 );
      """ )
   db.conn.commit()

   assert db.accept_itinerary()

   assert [
      row[ 'SPECIES' ]
      for row in db.conn.execute( 'SELECT SPECIES FROM ItineraryAnimal;' )
   ] == [ 'African Penguin' ]
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


def test_validate_animals_removes_unavailable_entries( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   db.set_animal_as_off_display(
      species='African Lion',
      exhibit='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = db.validate_animals(
      animals=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         { 'species': 'African Penguin', 'exhibit': 'Africa Savanna' }
      ],
      new_visit_date_temp=22,
      old_visit_date='2026-06-15',
      new_visit_date='2026-06-15' )

   assert len( result ) == 2

   assert [
      ( d.species, ( d.new_likelihood or 0 ) > 0 )
      for d in result
      if d.species == 'African Lion'
   ] == [ ( 'African Lion', False ) ]

   assert [
      ( d.species, ( d.new_likelihood or 0 ) > 0 )
      for d in result
      if d.species == 'African Penguin'
   ] == [ ( 'African Penguin', True ) ]


def test_validate_attractions_removes_closed_entries( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   db.set_attraction_as_closed(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = db.validate_attractions(
      attractions=[ 'Conservation Carousel', 'Greenhouse' ],
      old_visit_date='2026-06-15',
      new_visit_date='2026-06-15' )

   assert [
      ( d.name, d.new_likelihood )
      for d in result
      if d.name == 'Greenhouse'
   ] == [ ( 'Greenhouse', 100 ) ]

   assert [
      ( d.name, d.new_likelihood )
      for d in result
      if d.name == 'Conservation Carousel'
   ] == [ ( 'Conservation Carousel', 0 ) ]


def test_validate_guardians_talks_splits_available_and_unavailable_entries( db, monkeypatch ):
   def get_guardians_talk_schedule( **kwargs ):
      return [
         zoo.GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=51.138,
            y_coord=41.279,
            start_time='10:00',
            is_available=True ),
         zoo.GuardiansTalk(
            name='Amur Tiger',
            location='Eurasia Wilds',
            x_coord=75.979,
            y_coord=74.707,
            start_time='11:00',
            is_available=False,
            unavailable_message='Cancelled.' ),
         zoo.GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=51.138,
            y_coord=41.279,
            start_time='09:00',
            is_available=True )
      ]

   monkeypatch.setattr( db, 'get_guardians_talk_schedule', get_guardians_talk_schedule )

   result = db.validate_guardians_talks(
      month='June',
      day=15,
      year=2026,
      guardians_talks_to_include=[ 'African Lion', 'Amur Tiger' ]
   )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Lion', False, '10:00', '10:30' ),
      ( 'Amur Tiger', True, '11:00', '11:30' ),
   ]


def test_validate_wild_encounters_splits_available_and_unavailable_entries( db, monkeypatch ):
   def get_wild_encounter_schedule( **kwargs ):
      return [
         zoo.WildEncounter(
            name='Kangaroo',
            meeting_spot='Wild Encounter - Eurasia Meeting Spot',
            link='https://www.torontozoo.com/tickets/wekangaroo',
            start_time='13:00',
            is_available=True ),
         zoo.WildEncounter(
            name='African Rainforest',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://www.torontozoo.com/tickets/weafricarainforest',
            start_time='14:00',
            is_available=False,
            unavailable_message='Unavailable.' ),
         zoo.WildEncounter(
            name='Kangaroo',
            meeting_spot='Wild Encounter - Eurasia Meeting Spot',
            link='https://www.torontozoo.com/tickets/wekangaroo',
            start_time='09:00',
            is_available=True )
      ]

   monkeypatch.setattr( db, 'get_wild_encounter_schedule', get_wild_encounter_schedule )

   result = db.validate_wild_encounters(
      month='June',
      day=15,
      wild_encounters_to_include=[ 'African Rainforest', 'Kangaroo' ]
   )

   assert [
      ( d.name, d.is_deleted, d.start_time, d.end_time )
      for d in result
   ] == [
      ( 'African Rainforest', True, '14:00', '14:45' ),
      ( 'Kangaroo', False, '13:00', '13:45' ),
   ]


def test_itinerary_filter_helpers_ignore_invalid_input_and_sort( db ):
   animals = db.get_animals_for_itinerary(
      month='June',
      day=15,
      temp=22,
      species_exhibit_pairs=[
         'bad',
         { 'species': 'African Penguin', 'exhibit': 'Africa Savanna' },
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' }
      ]
   )
   attractions = db.get_attractions_for_itinerary(
      month='June',
      day=15,
      attractions_to_include=[ None, 'Greenhouse', 'Conservation Carousel' ]
   )

   assert [ animal.species for animal in animals ] == sorted(
      [ animal.species for animal in animals ],
      key=str.lower
   )
   assert { animal.species for animal in animals } == { 'African Lion', 'African Penguin' }
   assert [ attraction.name for attraction in attractions ] == [ 'Conservation Carousel', 'Greenhouse' ]


def test_itinerary_filter_helpers_return_empty_without_filters( db ):
   assert db.get_animals_for_itinerary(
      month='June',
      day=15,
      temp=22,
      species_exhibit_pairs=[
         None,
         {},
         { 'species': 'African Lion' },
         { 'exhibit': 'Africa Savanna' }
      ]
   ) == []
   assert db.get_attractions_for_itinerary(
      month='June',
      day=15,
      attractions_to_include=[ None, '', '   ' ]
   ) == []
   assert db.get_guardians_talks_for_itinerary(
      guardians_talks_to_include=[]
   ) == []
   assert db.get_wild_encounters_for_itinerary(
      wild_encounters_to_include=[]
   ) == []


def test_scheduled_itinerary_filter_helpers_filter_case_insensitively_and_sort( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      talk_time='10:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )
   assert db.set_guardians_talk_schedule(
      talk='Amur Tiger',
      location='Eurasia Wilds',
      start_date='2026-06-01',
      end_date='2026-06-30',
      talk_time='09:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )
   assert db.set_wild_encounter_schedule(
      wild_encounter='African Rainforest',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='14:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )
   assert db.set_wild_encounter_schedule(
      wild_encounter='Kangaroo',
      start_date='2026-06-01',
      end_date='2026-06-30',
      encounter_time='09:00',
      monday=True,
      tuesday=False,
      wednesday=False,
      thursday=False,
      friday=False,
      saturday=False,
      sunday=False,
      message=None
   )

   talk_result = db.validate_guardians_talks(
      month='June',
      day=15,
      year=2026,
      guardians_talks_to_include=[ ' african lion ', 'AMUR TIGER' ]
   )
   encounter_result = db.validate_wild_encounters(
      month='June',
      day=15,
      wild_encounters_to_include=[ ' kangaroo ', 'AFRICAN RAINFOREST' ]
   )

   assert [
      d.name for d in talk_result if not d.is_deleted
   ] == [
      'African Lion',
      'Amur Tiger',
   ]
   assert [
      ( d.name, d.is_deleted )
      for d in encounter_result
   ] == [
      ( 'Kangaroo', False ),
      ( 'African Rainforest', False ),
   ]
