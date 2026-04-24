from datetime import date


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
