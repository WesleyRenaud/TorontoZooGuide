from datetime import date

import zoo


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
      attractions=[ { 'name': 'Conservation Carousel' } ],
      guardians_talks=[ 'African Lion' ],
      wild_encounters=[ 'African Rainforest' ],
      is_active=True
   )

   itinerary = db.get_itinerary()

   assert itinerary.date == '2026-06-15'
   assert [ animal.species for animal in itinerary.animals ] == [ 'African Lion' ]
   assert [ attraction.name for attraction in itinerary.attractions ] == [ 'Conservation Carousel' ]
   assert [ talk.name for talk in itinerary.guardians_talks ] == [ 'African Lion' ]
   assert [ encounter.name for encounter in itinerary.wild_encounters ] == [ 'African Rainforest' ]

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
      month='June',
      day=15,
      temp=22,
      animals_to_include=[
         { 'species': 'African Lion', 'exhibit': 'Africa Savanna' },
         { 'species': 'African Penguin', 'exhibit': 'Africa Savanna' }
      ]
   )

   assert [ animal.species for animal in result[ 'valid_animals' ] ] == [ 'African Penguin' ]
   assert [ animal.species for animal in result[ 'removed_animals' ] ] == [ 'African Lion' ]


def test_validate_attractions_removes_closed_entries( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   db.set_attraction_as_closed(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='2026-06-30',
      message='Unavailable.'
   )

   result = db.validate_attractions(
      month='June',
      day=15,
      attractions_to_include=[ 'Conservation Carousel', 'Greenhouse' ]
   )

   assert [ attraction.name for attraction in result[ 'valid_attractions' ] ] == [ 'Greenhouse' ]
   assert [ attraction.name for attraction in result[ 'removed_attractions' ] ] == [ 'Conservation Carousel' ]


def test_validate_guardians_talks_splits_available_and_unavailable_entries( db, monkeypatch ):
   def get_guardians_talks_for_itinerary( **kwargs ):
      return [
         zoo.GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=51.138,
            y_coord=41.279,
            time_of_day='10:00',
            is_available=True ),
         zoo.GuardiansTalk(
            name='Amur Tiger',
            location='Eurasia Wilds',
            x_coord=75.979,
            y_coord=74.707,
            time_of_day='11:00',
            is_available=False,
            unavailable_message='Cancelled.' ),
         zoo.GuardiansTalk(
            name='African Lion',
            location='Africa Savanna',
            x_coord=51.138,
            y_coord=41.279,
            time_of_day='09:00',
            is_available=True )
      ]

   monkeypatch.setattr( db, 'get_guardians_talks_for_itinerary', get_guardians_talks_for_itinerary )

   result = db.validate_guardians_talks(
      month='June',
      day=15,
      guardians_talks_to_include=[ 'African Lion', 'Amur Tiger' ]
   )

   assert [
      ( talk.name, talk.time_of_day )
      for talk in result[ 'valid_guardians_talks' ]
   ] == [
      ( 'African Lion', '09:00' ),
      ( 'African Lion', '10:00' )
   ]
   assert [
      ( talk.name, talk.unavailable_message )
      for talk in result[ 'removed_guardians_talks' ]
   ] == [
      ( 'Amur Tiger', 'Cancelled.' )
   ]


def test_validate_wild_encounters_splits_available_and_unavailable_entries( db, monkeypatch ):
   def get_wild_encounters_for_itinerary( **kwargs ):
      return [
         zoo.WildEncounter(
            name='Kangaroo',
            meeting_spot='Wild Encounter - Eurasia Meeting Spot',
            link='https://www.torontozoo.com/tickets/wekangaroo',
            time_of_day='13:00',
            is_available=True ),
         zoo.WildEncounter(
            name='African Rainforest',
            meeting_spot='Wild Encounter - Africa Meeting Spot',
            link='https://www.torontozoo.com/tickets/weafricarainforest',
            time_of_day='14:00',
            is_available=False,
            unavailable_message='Unavailable.' ),
         zoo.WildEncounter(
            name='Kangaroo',
            meeting_spot='Wild Encounter - Eurasia Meeting Spot',
            link='https://www.torontozoo.com/tickets/wekangaroo',
            time_of_day='09:00',
            is_available=True )
      ]

   monkeypatch.setattr( db, 'get_wild_encounters_for_itinerary', get_wild_encounters_for_itinerary )

   result = db.validate_wild_encounters(
      month='June',
      day=15,
      wild_encounters_to_include=[ 'African Rainforest', 'Kangaroo' ]
   )

   assert [
      ( encounter.name, encounter.time_of_day )
      for encounter in result[ 'valid_wild_encounters' ]
   ] == [
      ( 'Kangaroo', '09:00' ),
      ( 'Kangaroo', '13:00' )
   ]
   assert [
      ( encounter.name, encounter.unavailable_message )
      for encounter in result[ 'removed_wild_encounters' ]
   ] == [
      ( 'African Rainforest', 'Unavailable.' )
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


def test_itinerary_filter_helpers_return_empty_without_valid_filters( db ):
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
      month='June',
      day=15,
      guardians_talks_to_include=[ None, '', '   ' ]
   ) == []
   assert db.get_wild_encounters_for_itinerary(
      month='June',
      day=15,
      wild_encounters_to_include=[ None, '', '   ' ]
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

   talks = db.get_guardians_talks_for_itinerary(
      month='June',
      day=15,
      guardians_talks_to_include=[ ' african lion ', 'AMUR TIGER', None ]
   )
   encounters = db.get_wild_encounters_for_itinerary(
      month='June',
      day=15,
      wild_encounters_to_include=[ ' kangaroo ', 'AFRICAN RAINFOREST', None ]
   )

   assert [
      ( talk.name, talk.time_of_day )
      for talk in talks
   ] == [
      ( 'African Lion', '10:00' ),
      ( 'Amur Tiger', '09:00' )
   ]
   assert [
      ( encounter.name, encounter.time_of_day )
      for encounter in encounters
   ] == [
      ( 'African Rainforest', '14:00' ),
      ( 'Kangaroo', '09:00' )
   ]
