from datetime import date


def get_animal( db, species, exhibit ):
   animals = db.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=True,
      exhibits_to_include=[ exhibit ] )

   return next(
      animal for animal in animals
      if animal.species == species and animal.exhibit == exhibit
   )


def get_restaurant( db, name ):
   restaurants = db.get_restaurants(
      day=15,
      month='June',
      year=2026,
      include_closed_restaurants=True )

   return next( restaurant for restaurant in restaurants if restaurant.name == name )


def get_gift_shop( db, name ):
   gift_shops = db.get_gift_shops(
      day=15,
      month='June',
      year=2026,
      include_closed_gift_shops=True )

   return next( gift_shop for gift_shop in gift_shops if gift_shop.name == name )


def get_attraction( db, name ):
   attractions = db.get_attractions(
      day=15,
      month='June',
      year=2026,
      include_closed_attractions=True )

   return next( attraction for attraction in attractions if attraction.name == name )


def test_set_animal_as_off_display_changes_visible_animal_result( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_animal_as_off_display( 'African Lion', 'Africa Savanna', '2026-06-01', '', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood == 0
   assert lion.off_display_message == 'The African Lion is temporarily off-display.'


def test_set_animal_as_on_display_restores_visible_animal_result( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.set_animal_as_off_display(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Unavailable.' )

   assert db.set_animal_as_on_display( 'African Lion', 'Africa Savanna' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood > 0
   assert lion.off_display_message is None


def test_set_and_remove_animal_visibility_schedule_changes_visible_animal_result( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )
   assert db.remove_animal_visibility_schedule( 'African Lion', 'Africa Savanna' ) is False

   assert db.set_animal_limited_viewing_schedule(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '',
      '09:00',
      '10:00',
      ''
   )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_limited_viewing_schedule is True
   assert lion.limited_viewing_message == 'The African Lion is viewable daily only from 9:00 AM to 10:00 AM.'

   assert db.remove_animal_visibility_schedule( 'African Lion', 'Africa Savanna' ) is True

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_limited_viewing_schedule is False
   assert lion.limited_viewing_message is None


def test_set_and_remove_animal_viewing_alert_changes_visible_animal_result( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_animal_viewing_alert( 'African Lion', 'Africa Savanna', '2026-06-01', '', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_viewing_alert is True
   assert lion.viewing_alert_message == 'The African Lion may be less visible than usual at this time.'

   assert db.remove_animal_viewing_alert( 'African Lion', 'Africa Savanna' ) is True

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_viewing_alert is False
   assert lion.viewing_alert_message is None


def test_set_exhibit_closed_and_open_changes_animal_and_closed_exhibit_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_exhibit_as_closed( 'Africa Savanna', '2026-06-01', '2026-06-30', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood == 0
   assert lion.off_display_message == 'The Africa Savanna is temporarily closed.'
   assert 'Africa Savanna' in db.get_closed_exhibits( month='June', day=15, year=2026 )

   assert db.set_exhibit_as_open( 'Africa Savanna', '2026-06-01', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood > 0
   assert lion.off_display_message is None
   assert 'Africa Savanna' not in db.get_closed_exhibits( month='June', day=15, year=2026 )


def test_set_restaurant_closed_and_opening_schedule_changes_restaurant_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_restaurant_as_closed( 'Africa Restaurant', '2026-06-01', '2026-06-30', '' )

   restaurant = get_restaurant( db, 'Africa Restaurant' )

   assert restaurant.is_closed is True
   assert restaurant.likelihood == 0
   assert restaurant.closed_message == 'The Africa Restaurant is temporarily closed.'
   assert all(
      item.name != 'Africa Restaurant'
      for item in db.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=False )
   )

   assert db.set_restaurant_opening_schedule(
      restaurant='Africa Restaurant',
      start_date='2026-06-01',
      end_date='',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=True,
      message='' )

   restaurant = get_restaurant( db, 'Africa Restaurant' )

   assert restaurant.is_closed is False
   assert restaurant.closed_message is None
   assert restaurant.likelihood == 100


def test_set_gift_shop_closed_and_opening_schedule_changes_gift_shop_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_gift_shop_as_closed( 'Zootique', '2026-06-01', '2026-06-30', '' )

   gift_shop = get_gift_shop( db, 'Zootique' )

   assert gift_shop.is_closed is True
   assert gift_shop.likelihood == 0
   assert gift_shop.closed_message == 'The Zootique is temporarily closed.'
   assert all(
      item.name != 'Zootique'
      for item in db.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=False )
   )

   assert db.set_gift_shop_opening_schedule(
      gift_shop='Zootique',
      start_date='2026-06-01',
      end_date='',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=True,
      message='' )

   gift_shop = get_gift_shop( db, 'Zootique' )

   assert gift_shop.is_closed is False
   assert gift_shop.closed_message is None
   assert gift_shop.likelihood == 100


def test_set_attraction_closed_and_opening_schedule_changes_attraction_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_attraction_as_closed( 'Conservation Carousel', '2026-06-01', '2026-06-30', '' )

   attraction = get_attraction( db, 'Conservation Carousel' )

   assert attraction.is_closed is True
   assert attraction.likelihood == 0
   assert attraction.closed_message == 'The Conservation Carousel is temporarily closed.'
   assert all(
      item.name != 'Conservation Carousel'
      for item in db.get_attractions( day=15, month='June', year=2026, include_closed_attractions=False )
   )

   assert db.set_attraction_opening_schedule(
      attraction='Conservation Carousel',
      start_date='2026-06-01',
      end_date='',
      monday=True,
      tuesday=True,
      wednesday=True,
      thursday=True,
      friday=True,
      saturday=True,
      sunday=True,
      holidays_only=True,
      message='' )

   attraction = get_attraction( db, 'Conservation Carousel' )

   assert attraction.is_closed is False
   assert attraction.closed_message is None
   assert attraction.likelihood == 100


def test_set_zoomobile_station_closed_and_open_changes_route_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_zoomobile_station_as_closed( 'Africa Zoomobile Station', '2026-06-01', '2026-06-30', '' )

   route = db.get_zoomobile_route( route='summer', day=15, month='June', year=2026 )

   assert all( station.name != 'Africa Zoomobile Station' for station in route.zoomobile_stations )

   assert db.set_zoomobile_station_as_open( 'Africa Zoomobile Station' )

   route = db.get_zoomobile_route( route='summer', day=15, month='June', year=2026 )

   assert any( station.name == 'Africa Zoomobile Station' for station in route.zoomobile_stations )


def test_create_end_and_edit_updates_change_active_update_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   created = db.create_update(
      title='New baby giraffe',
      description='Come meet the new calf.',
      update_type='new arrival',
      start_date='',
      end_date='' )

   assert created is True

   updates = db.get_updates_for_visit_date( month='June', day=15, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Come meet the new calf.',
      'type': 'New Arrival',
      'start_date': '2026-06-15',
      'end_date': None
   }

   assert db.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      description='Updated calf details.',
      update_type='Closure',
      end_date='2026-07-15' ) is True

   updates = db.get_updates_for_visit_date( month='July', day=1, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Updated calf details.',
      'type': 'Closure',
      'start_date': '2026-06-15',
      'end_date': '2026-07-15'
   }

   assert db.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      end_date='' ) is True

   updates = db.get_updates_for_visit_date( month='August', day=1, year=2026 )

   assert updates[ 0 ].end_date is None

   assert db.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      update_type='invalid' ) is False

   assert db.end_update( 'New baby giraffe', '2026-06-15', '2026-06-14' ) is True
   assert db.get_updates_for_visit_date( month='June', day=15, year=2026 ) == []


def test_active_update_options_include_future_updates_but_not_expired_updates( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.create_update(
      title='Future update',
      description='This starts later.',
      update_type='Closure',
      start_date='2026-07-01',
      end_date='2026-07-31' )

   assert db.create_update(
      title='Expired update',
      description='This already ended.',
      update_type='Closure',
      start_date='2026-05-01',
      end_date='2026-05-31' )

   assert db.get_updates_for_visit_date( month='June', day=15, year=2026 ) == []

   update_options = db.get_unexpired_updates()

   assert [ update.title for update in update_options ] == [ 'Future update' ]


def test_set_current_zoomobile_route_changes_current_route_result( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_current_zoomobile_route( 'winter', '2026-06-01', '2026-06-30' )

   route = db.get_zoomobile_route( route='current', day=15, month='June', year=2026 )

   assert route.route == 'winter'
   assert route.route_source == 'override'
   assert db.set_current_zoomobile_route( 'summer', '2026-07-01', '2026-06-30' ) is False


def test_set_end_and_cancel_guardians_talk_schedule_changes_talk_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_guardians_talk_schedule(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      '10:00',
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      ''
   )

   talks = db.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert any( talk.name == 'African Lion' and talk.start_time == '10:00' for talk in talks )

   assert db.end_guardians_talk_schedule( 'African Lion', 'Africa Savanna', '2026-06-14' )

   talks = db.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks )

   assert db.set_guardians_talk_schedule(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      '10:00',
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      ''
   )
   assert db.cancel_guardians_talk_occurrence( 'African Lion', 'Africa Savanna', '2026-06-15', '10:00' )

   talks = db.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks )
   assert db.cancel_guardians_talk_occurrence( 'African Lion', 'Africa Savanna', '2026-06-15', '10:00' ) is False


def test_set_end_and_cancel_wild_encounter_schedule_changes_wild_encounter_results( db, freeze_database_today ):
   freeze_database_today( date( 2026, 6, 15 ) )

   assert db.set_wild_encounter_schedule(
      'African Rainforest',
      '2026-06-01',
      '2026-06-30',
      '14:00',
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      ''
   )

   encounters = db.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is True
   assert encounter.unavailable_message is None

   assert db.end_wild_encounter_schedule( 'African Rainforest', '2026-06-14' )

   encounters = db.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is False
   assert encounter.unavailable_message == 'African Rainforest is not scheduled on June 15.'

   assert db.set_wild_encounter_schedule(
      'African Rainforest',
      '2026-06-01',
      '2026-06-30',
      '14:00',
      True,
      False,
      False,
      False,
      False,
      False,
      False,
      ''
   )
   assert db.cancel_wild_encounter_occurrence( 'African Rainforest', '2026-06-15', '14:00' )

   encounters = db.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is False
   assert encounter.unavailable_message == 'African Rainforest has been cancelled for this date.'
   assert db.cancel_wild_encounter_occurrence( 'African Rainforest', '2026-06-15', '14:00' ) is False


def test_console_status_and_schedule_guards( db ):
   assert db.set_exhibit_as_closed( '', None, None, None ) is False
   assert db.set_exhibit_as_open( '', None, None ) is False
   assert db.set_restaurant_as_closed( '', None, None, None ) is False
   assert db.set_gift_shop_as_closed( '', None, None, None ) is False
   assert db.set_attraction_as_closed( '', None, None, None ) is False
   assert db.set_zoomobile_station_as_closed( '', None, None, None ) is False
   assert db.set_current_zoomobile_route( 'bad', None, None ) is False
   assert db.create_update( '', '', 'Closure', '2026-06-01', '2026-06-30' ) is None
   assert db.create_update( 'Title', 'Description', 'Bad', '2026-06-01', '2026-06-30' ) is None
   assert db.create_update(
      'Animal birth',
      'A new animal was born.',
      'animal birth',
      '2026-06-01',
      '2026-06-30'
   ) is True
   assert db.create_update(
      'Animal passing',
      'An animal has passed.',
      'animal_passing',
      '2026-06-01',
      '2026-06-30'
   ) is True
