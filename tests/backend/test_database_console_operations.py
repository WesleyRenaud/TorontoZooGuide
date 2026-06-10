from __future__ import annotations

from collections.abc import Callable
from datetime import date

from api.animals.coordinators.animal_coordinator import AnimalCoordinator
from api.attractions.controllers.attraction_controller import AttractionController
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.giftshops.controllers.gift_shop_controller import GiftShopController
from api.guardians.controllers.guardians_controller import GuardiansController
from api.models.animal import Animal
from api.models.attraction import Attraction
from api.models.gift_shop import GiftShop
from api.models.restaurant import Restaurant
from api.restaurants.coordinators.restaurant_coordinator import RestaurantCoordinator
from api.shared.enums import AnimalViewingScope
from api.types import Cursor
from api.updates.controllers.update_controller import UpdateController
from api.wild_encounters.controllers.wild_encounter_controller import WildEncounterController
from api.zoomobile.controllers.zoomobile_controller import ZoomobileController
from conftest import DbControllers


def get_animal( db: DbControllers, species: str, exhibit: str ) -> Animal:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
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


def get_animals_for_exhibit(
      species: str,
      exhibit: str,
      include_off_display_animals: bool = True ) -> list[ Animal ]:
   animals = AnimalCoordinator.get_animals_viewable_on_day(
      day=15,
      month='June',
      year=2026,
      temp=22,
      include_off_display_animals=include_off_display_animals,
      exhibits_to_include=[ exhibit ] )

   return [
      animal for animal in animals
      if animal.species == species and animal.exhibit == exhibit
   ]


def get_animal_status_scopes(
      cursor: Cursor,
      species: str,
      exhibit: str ) -> list[ str ]:
   return [
      row[ 'VIEWING_SCOPE' ]
      for row in cursor.execute(
         """   SELECT VIEWING_SCOPE
               FROM AnimalStatus
               WHERE SPECIES = ?
                  AND EXHIBIT = ?
               ORDER BY VIEWING_SCOPE;
         """,
         (
            species,
            exhibit,
         ) ).fetchall()
   ]


def get_restaurant( db: DbControllers, name: str ) -> Restaurant:
   restaurants = RestaurantCoordinator.get_restaurants(
      day=15,
      month='June',
      year=2026,
      include_closed_restaurants=True )

   return next( restaurant for restaurant in restaurants if restaurant.name == name )


def get_gift_shop( db: DbControllers, name: str ) -> GiftShop:
   gift_shops = GiftShopController.get_gift_shops(
      day=15,
      month='June',
      year=2026,
      include_closed_gift_shops=True )

   return next( gift_shop for gift_shop in gift_shops if gift_shop.name == name )


def get_attraction( db: DbControllers, name: str ) -> Attraction:
   attractions = AttractionController.get_attractions(
      day=15,
      month='June',
      year=2026,
      include_closed_attractions=True )

   return next( attraction for attraction in attractions if attraction.name == name )


def test_set_animal_as_off_display_changes_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display( 'African Lion', 'Africa Savanna', '2026-06-01', '', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood == 0
   assert lion.off_display_message == 'The African Lion is temporarily off-display.'


def test_set_animal_as_on_display_restores_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalCoordinator.set_animal_as_off_display(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Unavailable.' )

   assert AnimalCoordinator.set_animal_as_on_display( 'African Lion', 'Africa Savanna' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood > 0
   assert lion.off_display_message is None


def test_set_animal_as_off_display_can_scope_to_indoor_viewing(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )

   penguins = get_animals_for_exhibit( 'African Penguin', 'Africa Savanna' )

   indoor_penguin = next(
      penguin for penguin in penguins
      if penguin.enclosure_type == 'Indoor' )
   outdoor_penguin = next(
      penguin for penguin in penguins
      if penguin.enclosure_type == 'Outdoor' )

   assert indoor_penguin.likelihood == 0
   assert indoor_penguin.off_display_message == 'Indoor unavailable.'
   assert outdoor_penguin.likelihood > 0
   assert outdoor_penguin.off_display_message is None


def test_set_animal_as_off_display_replaces_matching_scopes(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'All unavailable.' )
   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )

   assert get_animal_status_scopes(
      cursor,
      'African Penguin',
      'Africa Savanna' ) == [ 'indoor' ]


def test_set_animal_as_on_display_can_scope_to_indoor_viewing(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'All unavailable.' )

   assert AnimalCoordinator.set_animal_as_on_display(
      'African Penguin',
      'Africa Savanna',
      viewing_scope=AnimalViewingScope.INDOOR )

   assert get_animal_status_scopes(
      cursor,
      'African Penguin',
      'Africa Savanna' ) == [ 'outdoor' ]


def test_set_animal_as_on_display_removes_matching_scoped_status(
      db: DbControllers,
      cursor: Cursor,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )
   assert AnimalCoordinator.set_animal_as_off_display(
      'African Penguin',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Outdoor unavailable.',
      viewing_scope=AnimalViewingScope.OUTDOOR )

   assert AnimalCoordinator.set_animal_as_on_display(
      'African Penguin',
      'Africa Savanna',
      viewing_scope=AnimalViewingScope.INDOOR )

   assert get_animal_status_scopes(
      cursor,
      'African Penguin',
      'Africa Savanna' ) == [ 'outdoor' ]


def test_set_animal_as_off_display_rejects_missing_viewing_scope(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert not AnimalCoordinator.set_animal_as_off_display(
      'African Lion',
      'Africa Savanna',
      '2026-06-01',
      '2026-06-30',
      'Indoor unavailable.',
      viewing_scope=AnimalViewingScope.INDOOR )


def test_set_and_remove_animal_visibility_schedule_changes_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )
   assert AnimalCoordinator.remove_animal_visibility_schedule( 'African Lion', 'Africa Savanna' ) is False

   assert AnimalCoordinator.set_animal_limited_viewing_schedule(
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

   assert AnimalCoordinator.remove_animal_visibility_schedule( 'African Lion', 'Africa Savanna' ) is True

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_limited_viewing_schedule is False
   assert lion.limited_viewing_message is None


def test_set_and_remove_animal_viewing_alert_changes_visible_animal_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AnimalCoordinator.set_animal_viewing_alert( 'African Lion', 'Africa Savanna', '2026-06-01', '', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_viewing_alert is True
   assert lion.viewing_alert_message == 'The African Lion may be less visible than usual at this time.'

   assert AnimalCoordinator.remove_animal_viewing_alert( 'African Lion', 'Africa Savanna' ) is True

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.has_viewing_alert is False
   assert lion.viewing_alert_message is None


def test_set_exhibit_closed_and_open_changes_animal_and_closed_exhibit_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ExhibitCoordinator.set_exhibit_as_closed( 'Africa Savanna', '2026-06-01', '2026-06-30', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood == 0
   assert lion.off_display_message == 'The Africa Savanna is temporarily closed.'
   assert 'Africa Savanna' in ExhibitCoordinator.get_closed_exhibits_for_visit_date( month='June', day=15, year=2026 )

   assert ExhibitCoordinator.set_exhibit_as_open( 'Africa Savanna', '2026-06-01', '' )

   lion = get_animal( db, 'African Lion', 'Africa Savanna' )

   assert lion.likelihood > 0
   assert lion.off_display_message is None
   assert 'Africa Savanna' not in ExhibitCoordinator.get_closed_exhibits_for_visit_date( month='June', day=15, year=2026 )


def test_set_restaurant_closed_and_opening_schedule_changes_restaurant_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert RestaurantCoordinator.set_restaurant_as_closed( 'Africa Restaurant', '2026-06-01', '2026-06-30', '' )

   restaurant = get_restaurant( db, 'Africa Restaurant' )

   assert restaurant.is_closed is True
   assert restaurant.likelihood == 0
   assert restaurant.closed_message == 'The Africa Restaurant is temporarily closed.'
   assert all(
      item.name != 'Africa Restaurant'
      for item in RestaurantCoordinator.get_restaurants( day=15, month='June', year=2026, include_closed_restaurants=False )
   )

   assert RestaurantCoordinator.set_restaurant_opening_schedule(
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


def test_set_gift_shop_closed_and_opening_schedule_changes_gift_shop_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GiftShopController.set_gift_shop_as_closed( 'Zootique', '2026-06-01', '2026-06-30', '' )

   gift_shop = get_gift_shop( db, 'Zootique' )

   assert gift_shop.is_closed is True
   assert gift_shop.likelihood == 0
   assert gift_shop.closed_message == 'The Zootique is temporarily closed.'
   assert all(
      item.name != 'Zootique'
      for item in GiftShopController.get_gift_shops( day=15, month='June', year=2026, include_closed_gift_shops=False )
   )

   assert GiftShopController.set_gift_shop_opening_schedule(
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


def test_set_attraction_closed_and_opening_schedule_changes_attraction_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert AttractionController.set_attraction_as_closed( 'Conservation Carousel', '2026-06-01', '2026-06-30', '' )

   attraction = get_attraction( db, 'Conservation Carousel' )

   assert attraction.is_closed is True
   assert attraction.likelihood == 0
   assert attraction.closed_message == 'The Conservation Carousel is temporarily closed.'
   assert all(
      item.name != 'Conservation Carousel'
      for item in AttractionController.get_attractions( day=15, month='June', year=2026, include_closed_attractions=False )
   )

   assert AttractionController.set_attraction_opening_schedule(
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


def test_set_zoomobile_station_closed_and_open_changes_route_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ZoomobileController.set_zoomobile_station_as_closed( 'Africa Zoomobile Station', '2026-06-01', '2026-06-30', '' )

   route = ZoomobileController.get_zoomobile_route( route='summer', day=15, month='June', year=2026 )

   assert all( station.name != 'Africa Zoomobile Station' for station in route.zoomobile_stations )

   assert ZoomobileController.set_zoomobile_station_as_open( 'Africa Zoomobile Station' )

   route = ZoomobileController.get_zoomobile_route( route='summer', day=15, month='June', year=2026 )

   assert any( station.name == 'Africa Zoomobile Station' for station in route.zoomobile_stations )


def test_create_update_uses_today_when_start_date_is_blank(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert UpdateController.create_update(
      title='Zoomobile update',
      description='Route change today.',
      update_type='Closure',
      start_date='',
      end_date=None )

   updates = UpdateController.get_updates_for_visit_date( month='June', day=15, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].start_date == '2026-06-15'


def test_create_end_and_edit_updates_change_active_update_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   created = UpdateController.create_update(
      title='New baby giraffe',
      description='Come meet the new calf.',
      update_type='new arrival',
      start_date='2026-06-15',
      end_date=None )

   assert created is True

   updates = UpdateController.get_updates_for_visit_date( month='June', day=15, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Come meet the new calf.',
      'type': 'New Arrival',
      'start_date': '2026-06-15',
      'end_date': None
   }

   assert UpdateController.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      description='Updated calf details.',
      update_type='Closure',
      end_date='2026-07-15' ) is True

   updates = UpdateController.get_updates_for_visit_date( month='July', day=1, year=2026 )

   assert len( updates ) == 1
   assert updates[ 0 ].to_dict() == {
      'title': 'New baby giraffe',
      'description': 'Updated calf details.',
      'type': 'Closure',
      'start_date': '2026-06-15',
      'end_date': '2026-07-15'
   }

   assert UpdateController.edit_update(
      title='New baby giraffe',
      start_date='2026-06-15',
      description='Updated calf details.',
      update_type='Closure',
      end_date=None ) is True

   updates = UpdateController.get_updates_for_visit_date( month='August', day=1, year=2026 )

   assert updates[ 0 ].end_date is None

   assert UpdateController.end_update( 'New baby giraffe', '2026-06-15', '2026-06-14' ) is True
   assert UpdateController.get_updates_for_visit_date( month='June', day=15, year=2026 ) == []


def test_active_update_options_include_future_updates_but_not_expired_updates(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert UpdateController.create_update(
      title='Future update',
      description='This starts later.',
      update_type='Closure',
      start_date='2026-07-01',
      end_date='2026-07-31' )

   assert UpdateController.create_update(
      title='Expired update',
      description='This already ended.',
      update_type='Closure',
      start_date='2026-05-01',
      end_date='2026-05-31' )

   assert UpdateController.get_updates_for_visit_date( month='June', day=15, year=2026 ) == []

   update_options = UpdateController.get_unexpired_updates()

   assert [ update.title for update in update_options ] == [ 'Future update' ]


def test_set_current_zoomobile_route_changes_current_route_result(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert ZoomobileController.set_current_zoomobile_route( 'winter', '2026-06-01', '2026-06-30' )

   route = ZoomobileController.get_zoomobile_route( route='current', day=15, month='June', year=2026 )

   assert route.route == 'winter'
   assert route.route_source == 'override'


def test_set_end_and_cancel_guardians_talk_schedule_changes_talk_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert GuardiansController.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='10:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=''
   )

   talks = GuardiansController.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert any( talk.name == 'African Lion' and talk.start_time == '10:00' for talk in talks )

   assert GuardiansController.end_guardians_talk_schedule( 'African Lion', 'Africa Savanna', '2026-06-14' )

   talks = GuardiansController.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks )

   assert GuardiansController.set_guardians_talk_schedule(
      talk='African Lion',
      location='Africa Savanna',
      start_date='2026-06-01',
      end_date='2026-06-30',
      monday_time='10:00',
      tuesday_time=None,
      wednesday_time=None,
      thursday_time=None,
      friday_time=None,
      saturday_time=None,
      sunday_time=None,
      message=''
   )
   assert GuardiansController.cancel_guardians_talk_occurrence( 'African Lion', 'Africa Savanna', '2026-06-15', '10:00' )

   talks = GuardiansController.get_guardians_talk_schedule( month='June', day=15, year=2026 )

   assert all( not ( talk.name == 'African Lion' and talk.start_time == '10:00' ) for talk in talks )
   assert GuardiansController.cancel_guardians_talk_occurrence( 'African Lion', 'Africa Savanna', '2026-06-15', '10:00' ) is False


def test_set_end_and_cancel_wild_encounter_schedule_changes_wild_encounter_results(
      db: DbControllers,
      freeze_database_today: Callable[ [ date ], None ] ) -> None:
   freeze_database_today( date( 2026, 6, 15 ) )

   assert WildEncounterController.set_wild_encounter_schedule(
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

   encounters = WildEncounterController.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is True
   assert encounter.unavailable_message is None

   assert WildEncounterController.end_wild_encounter_schedule( 'African Rainforest', '2026-06-14' )

   encounters = WildEncounterController.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is False
   assert encounter.unavailable_message == 'African Rainforest is not scheduled on June 15.'

   assert WildEncounterController.set_wild_encounter_schedule(
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
   assert WildEncounterController.cancel_wild_encounter_occurrence( 'African Rainforest', '2026-06-15', '14:00' )

   encounters = WildEncounterController.get_wild_encounter_schedule( month='June', day=15, year=2026 )
   encounter = next( item for item in encounters if item.name == 'African Rainforest' and item.start_time == '14:00' )

   assert encounter.is_available is False
   assert encounter.unavailable_message == 'African Rainforest has been cancelled for this date.'
   assert WildEncounterController.cancel_wild_encounter_occurrence( 'African Rainforest', '2026-06-15', '14:00' ) is False


def test_console_status_and_schedule_guards( db: DbControllers ) -> None:
   assert UpdateController.create_update(
      'Animal birth',
      'A new animal was born.',
      'animal birth',
      '2026-06-01',
      '2026-06-30'
   ) is True
   assert UpdateController.create_update(
      'Animal passing',
      'An animal has passed.',
      'animal_passing',
      '2026-06-01',
      '2026-06-30'
   ) is True
