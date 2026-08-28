from __future__ import annotations

from api.defibrillators.coordinators.defibrillator_coordinator import DefibrillatorCoordinator
from api.drinking_fountains.coordinators.drinking_fountain_coordinator import DrinkingFountainCoordinator
from api.emergency_intercoms.coordinators.emergency_intercom_coordinator import EmergencyIntercomCoordinator
from api.event_sites.coordinators.event_site_coordinator import EventSiteCoordinator
from api.exhibits.coordinators.exhibit_coordinator import ExhibitCoordinator
from api.guest_services.coordinators.guest_service_coordinator import GuestServiceCoordinator
from api.pavilions.coordinators.pavilion_coordinator import PavilionCoordinator
from api.picnic_sites.coordinators.picnic_site_coordinator import PicnicSiteCoordinator
from api.restrooms.coordinators.restroom_coordinator import RestroomCoordinator
from api.types import Cursor
from conftest import DbControllers

def test_region_and_static_location_queries( db: DbControllers ) -> None:
   regions = ExhibitCoordinator.get_regions()

   assert [
      region.to_dict()
      for region in regions
   ] == [
      { 'name': 'Africa', 'hasExhibits': True },
      { 'name': 'Americas', 'hasExhibits': True },
      { 'name': 'Australasia', 'hasExhibits': True },
      { 'name': 'Canadian Domain', 'hasExhibits': False },
      { 'name': 'Discovery Zone', 'hasExhibits': True },
      { 'name': 'Eurasia Wilds', 'hasExhibits': False },
      { 'name': 'Indo-Malaya', 'hasExhibits': True },
      { 'name': 'Tundra Trek', 'hasExhibits': False }
   ]

   assert ExhibitCoordinator.get_exhibits_in_region( 'Africa' ) == [
      'Africa Savanna',
      'African Rainforest Pavilion'
   ]
   assert ExhibitCoordinator.get_exhibits() == [
      'Africa Savanna',
      'African Rainforest Pavilion',
      'Americas Outdoor Mayan Temple Ruins',
      'Americas Pavilion',
      'Australasia Outdoor',
      'Australasia Pavilion',
      'Canadian Domain',
      'Eurasia Wilds',
      'Goat World',
      'Indo-Malaya Outdoor',
      'Indo-Malaya Pavilion',
      'Kids Zoo',
      'Malayan Woods Pavilion',
      'Tundra Trek'
   ]

   region_exhibits = ExhibitCoordinator.get_regions_with_exhibits()
   africa = next(
      region for region in region_exhibits
      if region.name == 'Africa'
   )
   assert africa.exhibits == [
      'Africa Savanna',
      'African Rainforest Pavilion'
   ]

   pavilions = {
      pavilion.name: pavilion
      for pavilion in PavilionCoordinator.get_pavilions()
   }
   restrooms = {
      restroom.title: restroom
      for restroom in RestroomCoordinator.get_restrooms( day=15, month='June', year=2026 )
   }
   drinking_fountains = DrinkingFountainCoordinator.get_drinking_fountains( day=15, month='June', year=2026 )

   assert pavilions[ 'African Rainforest Pavilion' ].region == 'Africa'
   restroom_names = RestroomCoordinator.get_restroom_names()

   assert 'Entrance Restroom' in restroom_names
   assert 'Entrance Restroom' in restrooms
   assert 'Africa Restaurant Restroom' in restrooms
   assert len( drinking_fountains ) > 0
   assert all( 0 <= drinking_fountain.x_coord <= 100 for drinking_fountain in drinking_fountains )
   assert all( 0 <= drinking_fountain.y_coord <= 100 for drinking_fountain in drinking_fountains )
   assert all( drinking_fountain.is_closed is False for drinking_fountain in drinking_fountains )


def test_defibrillators_have_coordinates( db: DbControllers ) -> None:
   defibrillators = DefibrillatorCoordinator.get_defibrillators()

   assert len( defibrillators ) > 0
   assert all( 0 <= defibrillator.x_coord <= 100 for defibrillator in defibrillators )
   assert all( 0 <= defibrillator.y_coord <= 100 for defibrillator in defibrillators )


def test_emergency_intercoms_have_coordinates( db: DbControllers ) -> None:
   emergency_intercoms = EmergencyIntercomCoordinator.get_emergency_intercoms()

   assert len( emergency_intercoms ) > 0
   assert all( 0 <= emergency_intercom.x_coord <= 100 for emergency_intercom in emergency_intercoms )
   assert all( 0 <= emergency_intercom.y_coord <= 100 for emergency_intercom in emergency_intercoms )


def test_guest_services_have_types_and_coordinates( db: DbControllers, cursor: Cursor ) -> None:
   guest_services = GuestServiceCoordinator.get_guest_services()
   service_types = { service.service_type for service in guest_services }
   primary_key_columns = cursor.execute(
      """ SELECT
             NAME
          FROM PRAGMA_TABLE_INFO( 'GuestService' )
          WHERE PK > 0
          ORDER BY PK;
      """ ).fetchall()

   assert service_types == {
      'First Aid & Family Center',
      'Information',
      'Rentals & Accessibility',
      'Wheelchairs'
   }
   assert [ row[ 'name' ] for row in primary_key_columns ] == [
      'SERVICE_TYPE',
      'X_COORD',
      'Y_COORD'
   ]
   assert all( 0 <= service.x_coord <= 100 for service in guest_services )
   assert all( 0 <= service.y_coord <= 100 for service in guest_services )


def test_picnic_sites_have_coordinates( db: DbControllers ) -> None:
   picnic_sites = PicnicSiteCoordinator.get_picnic_sites()

   assert len( picnic_sites ) > 0
   assert all( 0 <= picnic_site.x_coord <= 100 for picnic_site in picnic_sites )
   assert all( 0 <= picnic_site.y_coord <= 100 for picnic_site in picnic_sites )


def test_event_sites_have_names_and_coordinates( db: DbControllers ) -> None:
   event_sites = EventSiteCoordinator.get_event_sites()
   event_site_names = { event_site.name for event_site in event_sites }

   assert event_site_names == {
      'Special Events Center',
      'Wildlife Marquee',
      'Conservation Clubhouse',
      'Learning & Engagement Auditorium',
      'Canopy Classroom',
      'Serengeti Bush Camp'
   }
   assert all( 0 <= event_site.x_coord <= 100 for event_site in event_sites )
   assert all( 0 <= event_site.y_coord <= 100 for event_site in event_sites )

