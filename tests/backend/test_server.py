from io import BytesIO
import json

import pytest

import server
import zoo
from conftest import FakeHandler


ANIMAL_NAME = 'African Lion'
ANIMAL_EXHIBIT = 'Africa Savanna'
ATTRACTION_NAME = 'Conservation Carousel'
REMOVED_ATTRACTION_NAME = 'TundraAir Ride'
PAVILION_NAME = 'African Rainforest Pavilion'
RESTAURANT_NAME = 'Africa Restaurant'
RESTROOM_NAME = 'Entrance Restroom'
GIFT_SHOP_NAME = 'Zootique'
ZOOMOBILE_STATION_NAME = 'Main Zoomobile Station'
GUARDIANS_TALK_NAME = 'African Lion'
GUARDIANS_TALK_LOCATION = 'Africa Savanna'
WILD_ENCOUNTER_NAME = 'African Rainforest'
WILD_ENCOUNTER_MEETING_SPOT = 'Wild Encounter - Africa Meeting Spot'
WILD_ENCOUNTER_LINK = 'https://www.torontozoo.com/tickets/weafricarainforest'
DRINKING_FOUNTAIN_X_COORD = 18.191
DRINKING_FOUNTAIN_Y_COORD = 12.561
UPDATE_TITLE = 'New baby giraffe'


def make_handler( path='/', body=None ):
   encoded = json.dumps( body or {} ).encode( 'utf-8' )
   handler = server.MyHandler.__new__( server.MyHandler )
   handler.path = path
   handler.headers = { 'Content-Length': str( len( encoded ) ) }
   handler.rfile = BytesIO( encoded )
   handler.wfile = BytesIO()
   handler.statuses = []
   handler.sent_headers = []
   handler.errors = []
   handler.database = None
   handler.send_response = lambda code: handler.statuses.append( code )
   handler.send_header = lambda name, value: handler.sent_headers.append( ( name, value ) )
   handler.end_headers = lambda: None
   handler.send_error = lambda code, message=None: handler.errors.append( ( code, message ) )
   return handler


def response_json( handler ):
   handler.wfile.seek( 0 )
   return json.loads( handler.wfile.read().decode( 'utf-8' ) )


class StubDatabase:
   instances = []
   default_success = True

   def __init__( self ):
      self.calls = []
      self.closed = False
      StubDatabase.instances.append( self )


   def close( self ):
      self.closed = True


   def get_animals_viewable_on_day( self, **kwargs ):
      self.calls.append( ( 'get_animals_viewable_on_day', kwargs ) )
      return [ zoo.Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT, likelihood=100 ) ]


   def get_exhibits_in_region( self, region ):
      self.calls.append( ( 'get_exhibits_in_region', { 'region': region } ) )
      return [ ANIMAL_EXHIBIT ]


   def get_regions( self ):
      self.calls.append( ( 'get_regions', {} ) )
      return [ { 'name': 'Africa', 'hasExhibits': True } ]


   def get_animals_in_exhibit( self, exhibit ):
      self.calls.append( ( 'get_animals_in_exhibit', { 'exhibit': exhibit } ) )
      return [ ANIMAL_NAME ]


   def get_animal_information( self, species ):
      self.calls.append( ( 'get_animal_information', { 'species': species } ) )
      return zoo.Animal( species=species, exhibit=ANIMAL_EXHIBIT )


   def get_pavilions( self ):
      self.calls.append( ( 'get_pavilions', {} ) )
      return [ zoo.Pavilion( name=PAVILION_NAME, region='Africa' ) ]


   def get_restaurants( self, **kwargs ):
      self.calls.append( ( 'get_restaurants', kwargs ) )
      return [ zoo.Restaurant( name=RESTAURANT_NAME, location='Africa', sub_location=None ) ]


   def get_restrooms( self, **kwargs ):
      self.calls.append( ( 'get_restrooms', kwargs ) )
      return [ zoo.Restroom( title=RESTROOM_NAME ) ]


   def get_gift_shops( self, **kwargs ):
      self.calls.append( ( 'get_gift_shops', kwargs ) )
      return [ zoo.GiftShop( name=GIFT_SHOP_NAME, location='Learning & Engagement Centre' ) ]


   def get_attractions( self, **kwargs ):
      self.calls.append( ( 'get_attractions', kwargs ) )
      return [ zoo.Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ]


   def get_zoomobile_route( self, **kwargs ):
      self.calls.append( ( 'get_zoomobile_route', kwargs ) )
      return {
         'route': 'summer',
         'route_source': 'manual',
         'zoomobile_stations': [ zoo.ZoomobileStation( name=ZOOMOBILE_STATION_NAME ) ]
      }


   def get_guardians_talks( self, **kwargs ):
      self.calls.append( ( 'get_guardians_talks', kwargs ) )
      return [ zoo.GuardiansTalk( name=GUARDIANS_TALK_NAME, location=GUARDIANS_TALK_LOCATION, x_coord=51.138, y_coord=41.279 ) ]


   def get_wild_encounters( self, **kwargs ):
      self.calls.append( ( 'get_wild_encounters', kwargs ) )
      return [
         zoo.WildEncounter(
            name=WILD_ENCOUNTER_NAME,
            meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
            link=WILD_ENCOUNTER_LINK )
      ]


   def get_available_wild_encounters( self, **kwargs ):
      self.calls.append( ( 'get_available_wild_encounters', kwargs ) )
      return [
         zoo.WildEncounter(
            name=WILD_ENCOUNTER_NAME,
            meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
            link=WILD_ENCOUNTER_LINK )
      ]


   def get_drinking_fountains( self, **kwargs ):
      self.calls.append( ( 'get_drinking_fountains', kwargs ) )
      return [
         zoo.DrinkingFountain(
            x_coord=DRINKING_FOUNTAIN_X_COORD,
            y_coord=DRINKING_FOUNTAIN_Y_COORD )
      ]


   def get_defibrillators( self ):
      self.calls.append( ( 'get_defibrillators', {} ) )
      return [ zoo.Defibrillator( x_coord=12.345, y_coord=67.890 ) ]


   def get_emergency_intercoms( self ):
      self.calls.append( ( 'get_emergency_intercoms', {} ) )
      return [ zoo.EmergencyIntercom( x_coord=23.456, y_coord=78.901 ) ]


   def get_guest_services( self ):
      self.calls.append( ( 'get_guest_services', {} ) )
      return [
         zoo.GuestService(
            service_type='Information',
            x_coord=34.567,
            y_coord=89.012 )
      ]


   def get_picnic_sites( self ):
      self.calls.append( ( 'get_picnic_sites', {} ) )
      return [
         zoo.PicnicSite(
            x_coord=45.678,
            y_coord=90.123 )
      ]


   def get_event_sites( self ):
      self.calls.append( ( 'get_event_sites', {} ) )
      return [
         zoo.EventSite(
            name='Special Events Center',
            x_coord=56.789,
            y_coord=12.345 )
      ]


   def get_updates( self, **kwargs ):
      self.calls.append( ( 'get_updates', kwargs ) )
      return [
         zoo.Update(
            title=UPDATE_TITLE,
            description='Come meet the new calf.',
            update_type='New Arrival',
            start_date='2026-06-01',
            end_date='2026-06-30' )
      ]


   def get_closed_exhibits( self, **kwargs ):
      self.calls.append( ( 'get_closed_exhibits', kwargs ) )
      return [ ANIMAL_EXHIBIT ]


   def get_animals_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_animals_matching_query', kwargs ) )
      return [ zoo.Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT, likelihood=100 ) ]


   def get_pavilions_matching_query( self, query ):
      self.calls.append( ( 'get_pavilions_matching_query', { 'query': query } ) )
      return [ zoo.Pavilion( name=PAVILION_NAME, region='Africa' ) ]


   def get_restaurants_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_restaurants_matching_query', kwargs ) )
      return [ zoo.Restaurant( name=RESTAURANT_NAME, location='Africa', sub_location=None ) ]


   def get_restrooms_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_restrooms_matching_query', kwargs ) )
      return [ zoo.Restroom( title=RESTROOM_NAME ) ]


   def get_gift_shops_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_gift_shops_matching_query', kwargs ) )
      return [ zoo.GiftShop( name=GIFT_SHOP_NAME, location='Learning & Engagement Centre' ) ]


   def get_attractions_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_attractions_matching_query', kwargs ) )
      return [ zoo.Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ]


   def get_zoomobile_stations_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_zoomobile_stations_matching_query', kwargs ) )
      return [ zoo.ZoomobileStation( name=ZOOMOBILE_STATION_NAME ) ]


   def get_guardians_talks_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_guardians_talks_matching_query', kwargs ) )
      return [ zoo.GuardiansTalk( name=GUARDIANS_TALK_NAME, location=GUARDIANS_TALK_LOCATION, x_coord=51.138, y_coord=41.279 ) ]


   def get_wild_encounters_matching_query( self, **kwargs ):
      self.calls.append( ( 'get_wild_encounters_matching_query', kwargs ) )
      return [
         zoo.WildEncounter(
            name=WILD_ENCOUNTER_NAME,
            meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
            link=WILD_ENCOUNTER_LINK )
      ]


   def set_itinerary( self, **kwargs ):
      self.calls.append( ( 'set_itinerary', kwargs ) )
      return True


   def get_itinerary( self ):
      self.calls.append( ( 'get_itinerary', {} ) )
      return zoo.Itinerary( date='2026-06-15' )


   def get_zoo_hours( self, date_value ):
      self.calls.append( ( 'get_zoo_hours', { 'date_value': date_value } ) )
      return {
         'date': date_value,
         'openTime': '09:30',
         'closeTime': '19:00',
         'lastAdmissionTime': '18:00'
      }


   def clear_itinerary( self ):
      self.calls.append( ( 'clear_itinerary', {} ) )
      return True


   def validate_animals( self, **kwargs ):
      self.calls.append( ( 'validate_animals', kwargs ) )
      return {
         'valid_animals': [ zoo.Animal( species=ANIMAL_NAME, exhibit=ANIMAL_EXHIBIT ) ],
         'removed_animals': [ zoo.Animal( species='Amur Tiger', off_display_message='Unavailable.' ) ]
      }


   def validate_attractions( self, **kwargs ):
      self.calls.append( ( 'validate_attractions', kwargs ) )
      return {
         'valid_attractions': [ zoo.Attraction( name=ATTRACTION_NAME, free_with_admission=0 ) ],
         'removed_attractions': [
            zoo.Attraction( name=REMOVED_ATTRACTION_NAME, free_with_admission=0, closed_message='Closed.' )
         ]
      }


   def validate_guardians_talks( self, **kwargs ):
      self.calls.append( ( 'validate_guardians_talks', kwargs ) )
      return {
         'valid_guardians_talks': [
            zoo.GuardiansTalk(
               name=GUARDIANS_TALK_NAME,
               location=GUARDIANS_TALK_LOCATION,
               x_coord=51.138,
               y_coord=41.279 )
         ],
         'removed_guardians_talks': [
            zoo.GuardiansTalk(
               name='Amur Tiger',
               location='Eurasia Wilds',
               x_coord=75.979,
               y_coord=74.707,
               unavailable_message='Cancelled.' )
         ]
      }


   def validate_wild_encounters( self, **kwargs ):
      self.calls.append( ( 'validate_wild_encounters', kwargs ) )
      return {
         'valid_wild_encounters': [
            zoo.WildEncounter(
               name=WILD_ENCOUNTER_NAME,
               meeting_spot=WILD_ENCOUNTER_MEETING_SPOT,
               link=WILD_ENCOUNTER_LINK )
         ],
         'removed_wild_encounters': [
            zoo.WildEncounter(
               name='Kangaroo',
               meeting_spot='Wild Encounter - Eurasia Meeting Spot',
               link='https://www.torontozoo.com/tickets/wekangaroo',
               unavailable_message='Unavailable.' )
         ]
      }


   def get_species( self ):
      self.calls.append( ( 'get_species', {} ) )
      return [ ANIMAL_NAME, 'Amur Tiger' ]


   def get_exhibits( self ):
      self.calls.append( ( 'get_exhibits', {} ) )
      return [ ANIMAL_EXHIBIT, 'Eurasia Wilds' ]


   def get_regions_with_exhibits( self, **kwargs ):
      self.calls.append( ( 'get_regions_with_exhibits', kwargs ) )
      return [
         {
            'name': 'Africa',
            'exhibits': [ ANIMAL_EXHIBIT ]
         }
      ]


   def get_restaurant_names( self ):
      self.calls.append( ( 'get_restaurant_names', {} ) )
      return [ RESTAURANT_NAME ]


   def get_restroom_names( self ):
      self.calls.append( ( 'get_restroom_names', {} ) )
      return [ RESTROOM_NAME ]


   def get_gift_shop_names( self ):
      self.calls.append( ( 'get_gift_shop_names', {} ) )
      return [ GIFT_SHOP_NAME ]


   def get_attraction_names( self ):
      self.calls.append( ( 'get_attraction_names', {} ) )
      return [ ATTRACTION_NAME ]


   def get_zoomobile_station_names( self ):
      self.calls.append( ( 'get_zoomobile_station_names', {} ) )
      return [ ZOOMOBILE_STATION_NAME ]


   def get_guardians_talk_locations( self ):
      self.calls.append( ( 'get_guardians_talk_locations', {} ) )
      return [ GUARDIANS_TALK_LOCATION ]


   def get_guardians_talk_names( self ):
      self.calls.append( ( 'get_guardians_talk_names', {} ) )
      return [ GUARDIANS_TALK_NAME ]


   def get_guardians_talk_names_at_location( self, location ):
      self.calls.append( ( 'get_guardians_talk_names_at_location', { 'location': location } ) )
      return [ GUARDIANS_TALK_NAME ]


   def get_guardians_talk_occurrences( self, **kwargs ):
      self.calls.append( ( 'get_guardians_talk_occurrences', kwargs ) )
      return [
         {
            'date': '2026-06-15',
            'time': '10:00'
         }
      ]


   def get_wild_encounter_names( self ):
      self.calls.append( ( 'get_wild_encounter_names', {} ) )
      return [ WILD_ENCOUNTER_NAME ]


   def get_wild_encounter_occurrences( self, **kwargs ):
      self.calls.append( ( 'get_wild_encounter_occurrences', kwargs ) )
      return [
         {
            'date': '2026-06-15',
            'time': '14:00'
         }
      ]


   def get_active_update_options( self ):
      self.calls.append( ( 'get_active_update_options', {} ) )
      return [
         {
            'title': UPDATE_TITLE,
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'start_date': '2026-06-01',
            'end_date': '2026-06-30'
         }
      ]


   def __getattr__( self, name ):
      mutation_prefixes = (
         'create_',
         'set_',
         'remove_',
         'end_',
         'edit_',
         'cancel_'
      )

      if not name.startswith( mutation_prefixes ):
         raise AttributeError( name )

      def mutation_stub( **kwargs ):
         self.calls.append( ( name, kwargs ) )
         return StubDatabase.default_success

      return mutation_stub


@pytest.fixture
def stub_database( monkeypatch ):
   StubDatabase.instances = []
   StubDatabase.default_success = True
   monkeypatch.setattr( server.database, 'Database', StubDatabase )
   return StubDatabase


def test_send_file_serves_existing_static_page():
   handler = FakeHandler( path='/map.html' )

   server.MyHandler._send_file( handler, './pages/map.html', 'text/html' )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'text/html' ) in handler.sent_headers
   assert handler.wfile.getvalue().startswith( b'<!DOCTYPE html>' )


def test_send_file_renders_shared_html_strings():
   handler = FakeHandler( path='/animals.html' )

   server.MyHandler._send_file( handler, './pages/animals.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert '<title>Toronto Zoo Guide</title>' in content
   assert '{{ site.titles.guide }}' not in content


def test_send_file_renders_itinerary_day_planner_strings():
   handler = FakeHandler( path='/itinerary.html' )

   server.MyHandler._send_file( handler, './pages/itinerary.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert 'Day Plan' in content
   assert '{{ itinerary.dayPlanner.title }}' not in content


def test_send_file_renders_console_operation_strings():
   handler = FakeHandler( path='/console-operations.html' )

   server.MyHandler._send_file( handler, './pages/console-operations.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert 'Operations menu' in content
   assert 'Set animal as off display' in content
   assert '{{ panelTitles.offDisplay }}' not in content


def test_send_file_returns_404_for_missing_file():
   handler = FakeHandler( path='/missing.html' )

   server.MyHandler._send_file( handler, './pages/missing.html' )

   assert handler.errors == [ ( 404, 'Not Found' ) ]


@pytest.mark.parametrize(
   'path',
   [
      '/map.html',
      '/animals.html',
      '/itinerary.html',
      '/console-operations.html',
      '/styles/site.css',
      '/scripts/app.js',
      '/images/icon%20name.png'
   ]
)
def test_get_static_routes( path ):
   handler = server.MyHandler.__new__( server.MyHandler )
   handler.path = path
   handler.statuses = []
   handler.files = []
   handler._send_file = lambda filepath, content_type=None: handler.files.append( ( filepath, content_type ) )

   server.MyHandler.do_GET( handler )

   assert len( handler.files ) == 1


def test_get_unknown_route_returns_404():
   missing = server.MyHandler.__new__( server.MyHandler )
   missing.path = '/unknown'
   missing.errors = []
   missing.send_error = lambda code, message=None: missing.errors.append( ( code, message ) )
   server.MyHandler.do_GET( missing )
   assert missing.errors == [ ( 404, 'Not Found' ) ]


def test_get_animals_by_exhibit_endpoint_adds_type_and_maps_payload( stub_database ):
   handler = make_handler(
      '/get-animals-by-exhibit',
      {
         'month': 'June',
         'day': 15,
         'temp': 22,
         'exhibitsToInclude': [ 'Africa Savanna' ]
      }
   )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert StubDatabase.instances[ 0 ].calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'month': 'June',
         'day': 15,
         'temp': 22,
         'include_off_display_animals': False,
         'threshold': 0,
         'exhibits_to_include': [ 'Africa Savanna' ]
      }
   )


def test_get_visible_animals_endpoint_maps_payload_and_response( stub_database ):
   handler = make_handler(
      '/get-visible-animals',
      {
         'month': 'June',
         'day': 15,
         'temp': 22,
         'includeOffDisplayAnimals': True
      }
   )

   server.MyHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_json( handler )[ 'animals' ][ 0 ][ 'species' ] == 'African Lion'
   assert StubDatabase.instances[ 0 ].calls[ 0 ] == (
      'get_animals_viewable_on_day',
      {
         'month': 'June',
         'day': 15,
         'temp': 22,
         'include_off_display_animals': True,
         'threshold': 0
      }
   )
   assert StubDatabase.instances[ 0 ].closed is True


@pytest.mark.parametrize(
   'path, body, response_key',
   [
      ( '/get-exhibits-in-region', { 'region': 'Africa' }, 'exhibits' ),
      ( '/get-regions', {}, 'regions' ),
      ( '/get-animal-names-by-exhibit', { 'exhibit': 'Africa Savanna' }, 'animals' ),
      ( '/get-animal-information', { 'species': 'African Lion' }, 'information' ),
      ( '/get-pavilions', {}, 'pavilions' ),
      ( '/get-restaurants', { 'month': 'June', 'day': 15 }, 'restaurants' ),
      ( '/get-restrooms', {}, 'restrooms' ),
      ( '/get-gift-shops', { 'month': 'June', 'day': 15 }, 'gift_shops' ),
      ( '/get-attractions', { 'month': 'June', 'day': 15 }, 'attractions' ),
      ( '/get-zoomobile-route', { 'zoomobileRoute': 'summer', 'month': 'June', 'day': 15 }, 'route' ),
      ( '/get-guardians-talks', { 'month': 'June', 'day': 15 }, 'guardians_talks' ),
      ( '/get-wild-encounters', { 'month': 'June', 'day': 15 }, 'wild_encounters' ),
      ( '/get-drinking-fountains', { 'month': 'June', 'day': 15 }, 'drinking_fountains' ),
      ( '/get-defibrillators', {}, 'defibrillators' ),
      ( '/get-emergency-intercoms', {}, 'emergency_intercoms' ),
      ( '/get-guest-services', {}, 'guest_services' ),
      ( '/get-picnic-sites', {}, 'picnic_sites' ),
      ( '/get-event-sites', {}, 'event_sites' ),
      ( '/get-updates', { 'month': 'June', 'day': 15 }, 'updates' ),
      ( '/get-closed-exhibits', { 'month': 'June', 'day': 15 }, 'closed_exhibits' ),
      ( '/get-zoo-hours', { 'date': '2026-06-20' }, 'hours' )
   ]
)
def test_read_endpoints_return_json_keys( stub_database, path, body, response_key ):
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   assert handler.statuses == [ 200 ]
   assert response_key in response_json( handler )


def test_get_restrooms_endpoint_maps_closed_toggle( stub_database ):
   handler = make_handler(
      '/get-restrooms',
      {
         'month': 'June',
         'day': 15,
         'includeClosedRestrooms': True
      }
   )

   server.MyHandler.do_POST( handler )

   assert StubDatabase.instances[ 0 ].calls == [
      (
         'get_restrooms',
         {
            'month': 'June',
            'day': 15,
            'include_closed_restrooms': True
         }
      )
   ]


def test_get_wild_encounters_endpoint_uses_available_database_results( stub_database ):
   handler = make_handler(
      '/get-wild-encounters',
      { 'month': 'June', 'day': 21 } )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubDatabase.instances[ 0 ].calls == [
      ( 'get_available_wild_encounters', { 'month': 'June', 'day': 21 } )
   ]
   assert [ item[ 'name' ] for item in result[ 'wild_encounters' ] ] == [
      WILD_ENCOUNTER_NAME
   ]


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/get-species',
         {},
         ( 'get_species', {} ),
         { 'species': [ 'African Lion', 'Amur Tiger' ] }
      ),
      (
         '/get-exhibits',
         {},
         ( 'get_exhibits', {} ),
         { 'exhibits': [ 'Africa Savanna', 'Eurasia Wilds' ] }
      ),
      (
         '/get-exhibits-by-region',
         { 'month': 'June', 'day': 15 },
         (
            'get_regions_with_exhibits',
            {
               'month': 'June',
               'day': 15
            }
         ),
         {
            'regions': [
               {
                  'name': 'Africa',
                  'exhibits': [ 'Africa Savanna' ]
               }
            ]
         }
      ),
      (
         '/get-restaurant-names',
         {},
         ( 'get_restaurant_names', {} ),
         { 'restaurants': [ 'Africa Restaurant' ] }
      ),
      (
         '/get-restroom-names',
         {},
         ( 'get_restroom_names', {} ),
         { 'restrooms': [ 'Entrance Restroom' ] }
      ),
      (
         '/get-gift-shop-names',
         {},
         ( 'get_gift_shop_names', {} ),
         { 'gift_shops': [ 'Zootique' ] }
      ),
      (
         '/get-attraction-names',
         {},
         ( 'get_attraction_names', {} ),
         { 'attractions': [ 'Conservation Carousel' ] }
      ),
      (
         '/get-zoomobile-station-names',
         {},
         ( 'get_zoomobile_station_names', {} ),
         { 'zoomobile_stations': [ 'Main Zoomobile Station' ] }
      ),
      (
         '/get-guardians-talk-locations',
         {},
         ( 'get_guardians_talk_locations', {} ),
         { 'guardians_talk_locations': [ 'Africa Savanna' ] }
      ),
      (
         '/get-guardians-talk-names',
         {},
         ( 'get_guardians_talk_names', {} ),
         { 'guardians_talks': [ 'African Lion' ] }
      ),
      (
         '/get-guardians-talk-names-at-location',
         { 'location': 'Africa Savanna' },
         (
            'get_guardians_talk_names_at_location',
            { 'location': 'Africa Savanna' }
         ),
         { 'guardians_talks': [ 'African Lion' ] }
      ),
      (
         '/get-guardians-talk-occurrences',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna'
         },
         (
            'get_guardians_talk_occurrences',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna'
            }
         ),
         {
            'occurrences': [
               {
                  'date': '2026-06-15',
                  'time': '10:00'
               }
            ],
            'talk': 'African Lion',
            'location': 'Africa Savanna'
         }
      ),
      (
         '/get-wild-encounter-names',
         {},
         ( 'get_wild_encounter_names', {} ),
         { 'wild_encounters': [ 'African Rainforest' ] }
      ),
      (
         '/get-wild-encounter-occurrences',
         { 'wildEncounter': 'African Rainforest' },
         (
            'get_wild_encounter_occurrences',
            { 'wild_encounter': 'African Rainforest' }
         ),
         {
            'occurrences': [
               {
                  'date': '2026-06-15',
                  'time': '14:00'
               }
            ],
            'wildEncounter': 'African Rainforest'
         }
      ),
      (
         '/get-active-update-options',
         {},
         ( 'get_active_update_options', {} ),
         {
            'updates': [
               {
                  'title': 'New baby giraffe',
                  'description': 'Come meet the new calf.',
                  'type': 'New Arrival',
                  'start_date': '2026-06-01',
                  'end_date': '2026-06-30'
               }
            ]
         }
      )
   ]
)
def test_console_options_endpoints_map_payloads_and_return_expected_keys(
      stub_database,
      path,
      body,
      expected_call,
      response_subset ):
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubDatabase.instances[ 0 ].calls == [ expected_call ]

   for key, value in response_subset.items():
      assert result[ key ] == value


def test_search_endpoint_adds_type_fields( stub_database ):
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeAnimals': True,
         'includePavilions': True,
         'includeRestaurants': True,
         'includeRestrooms': True,
         'includeGiftShops': True,
         'includeAttractions': True,
         'includeZoomobileStations': True,
         'includeGuardiansTalks': True,
         'includeWildEncounters': True,
         'zoomobileRoute': 'summer',
         'month': 'June',
         'day': 15
      }
   )

   server.MyHandler.do_POST( handler )
   result = response_json( handler )

   assert result[ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert result[ 'pavilions' ][ 0 ][ 'type' ] == 'pavilion'
   assert result[ 'restaurants' ][ 0 ][ 'type' ] == 'restaurant'
   assert result[ 'restrooms' ][ 0 ][ 'type' ] == 'restroom'
   assert result[ 'gift_shops' ][ 0 ][ 'type' ] == 'giftShop'
   assert result[ 'attractions' ][ 0 ][ 'type' ] == 'attraction'
   assert result[ 'zoomobile_stations' ][ 0 ][ 'type' ] == 'zoomobileStation'
   assert result[ 'guardians_talks' ][ 0 ][ 'type' ] == 'guardiansTalk'
   assert result[ 'wild_encounters' ][ 0 ][ 'type' ] == 'wildEncounter'
   assert (
      'get_restrooms_matching_query',
      {
         'query': 'a',
         'month': 'June',
         'day': 15,
         'include_closed_restrooms': False
      }
   ) in StubDatabase.instances[ 0 ].calls


def test_search_endpoint_skips_unselected_types( stub_database ):
   handler = make_handler(
      '/search',
      {
         'query': 'a',
         'includeAnimals': False,
         'includePavilions': False,
         'includeRestaurants': False,
         'includeRestrooms': False,
         'includeGiftShops': False,
         'includeAttractions': False,
         'includeZoomobileStations': False,
         'includeGuardiansTalks': False,
         'includeWildEncounters': False
      }
   )

   server.MyHandler.do_POST( handler )
   result = response_json( handler )

   assert result == {
      'animals': [],
      'pavilions': [],
      'restaurants': [],
      'restrooms': [],
      'gift_shops': [],
      'attractions': [],
      'zoomobile_stations': [],
      'wild_encounters': [],
      'guardians_talks': []
   }
   assert StubDatabase.instances[ 0 ].calls == []


def test_itinerary_endpoints_return_success_payloads( stub_database ):
   set_handler = make_handler(
      '/set-itinerary',
      {
         'date': '2026-06-15',
         'animals': [],
         'attractions': [],
         'guardiansTalks': [],
         'wildEncounters': [],
         'isActive': True
      }
   )
   get_handler = make_handler( '/get-itinerary' )
   clear_handler = make_handler( '/clear-itinerary' )

   server.MyHandler.do_POST( set_handler )
   server.MyHandler.do_POST( get_handler )
   server.MyHandler.do_POST( clear_handler )

   assert response_json( set_handler )[ 'success' ] is True
   assert response_json( get_handler )[ 'itinerary' ][ 'date' ] == '2026-06-15'
   assert response_json( clear_handler )[ 'success' ] is True


def test_validate_itinerary_endpoint_returns_previous_validated_and_removed_payloads( stub_database ):
   handler = make_handler(
      '/validate-itinerary',
      {
         'date': '2026-06-15',
         'month': 'June',
         'day': 15,
         'temp': 22,
         'animals': [ 'African Lion' ],
         'attractions': [ 'Conservation Carousel' ],
         'guardiansTalks': [ 'African Lion' ],
         'wildEncounters': [ 'African Rainforest' ]
      }
   )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert result[ 'success' ] is True
   assert result[ 'previous' ][ 'animals' ] == []
   assert result[ 'validated' ][ 'animals' ][ 0 ][ 'type' ] == 'animal'
   assert result[ 'validated' ][ 'attractions' ][ 0 ][ 'type' ] == 'attraction'
   assert result[ 'validated' ][ 'guardiansTalks' ][ 0 ][ 'type' ] == 'guardiansTalk'
   assert result[ 'validated' ][ 'wildEncounters' ][ 0 ][ 'type' ] == 'wildEncounter'
   assert result[ 'removed' ][ 'animals' ][ 0 ][ 'removalReason' ] == 'Unavailable.'
   assert result[ 'removed' ][ 'attractions' ][ 0 ][ 'removalReason' ] == 'Closed.'
   assert result[ 'removed' ][ 'guardiansTalks' ][ 0 ][ 'removalReason' ] == 'Cancelled.'
   assert result[ 'removed' ][ 'wildEncounters' ][ 0 ][ 'removalReason' ] == 'Unavailable.'
   assert StubDatabase.instances[ 0 ].calls[ -2: ] == [
      ( 'clear_itinerary', {} ),
      (
         'set_itinerary',
         {
            'date': '2026-06-15',
            'animals': result[ 'validated' ][ 'animals' ],
            'attractions': result[ 'validated' ][ 'attractions' ],
            'guardians_talks': result[ 'validated' ][ 'guardiansTalks' ],
            'wild_encounters': result[ 'validated' ][ 'wildEncounters' ],
            'is_active': True
         }
      )
   ]


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-animal-off-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Unavailable.'
         },
         (
            'set_animal_as_off_display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Unavailable.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Unavailable.'
         }
      ),
      (
         '/set-animal-on-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         },
         (
            'set_animal_as_on_display',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         }
      ),
      (
         '/set-animal-visibility-schedule',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'dailyStartTime': '09:00',
            'dailyEndTime': '10:00',
            'message': 'Morning only.'
         },
         (
            'set_animal_limited_viewing_schedule',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'daily_start_time': '09:00',
               'daily_end_time': '10:00',
               'message': 'Morning only.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'dailyStartTime': '09:00',
            'dailyEndTime': '10:00',
            'message': 'Morning only.'
         }
      ),
      (
         '/remove-animal-visibility-schedule',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         },
         (
            'remove_animal_visibility_schedule',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         }
      ),
      (
         '/set-animal-viewing-alert',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Hard to spot.'
         },
         (
            'set_animal_viewing_alert',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna',
               'alert_start_date': '2026-06-01',
               'alert_end_date': '2026-06-30',
               'message': 'Hard to spot.'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Hard to spot.'
         }
      ),
      (
         '/remove-animal-viewing-alert',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         },
         (
            'remove_animal_viewing_alert',
            {
               'species': 'African Lion',
               'exhibit': 'Africa Savanna'
            }
         ),
         {
            'success': True,
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         }
      ),
      (
         '/set-exhibit-closed',
         {
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_exhibit_as_closed',
            {
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-exhibit-open',
         {
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'set_exhibit_as_open',
            {
               'exhibit': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'exhibit': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/set-restaurant-closed',
         {
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_restaurant_as_closed',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'restaurant': 'Africa Restaurant',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restroom-closed',
         {
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_restroom_as_closed',
            {
               'restroom': 'Entrance Restroom',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-restroom-open',
         {
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': None
         },
         (
            'set_restroom_as_open',
            {
               'restroom': 'Entrance Restroom',
               'start_date': '2026-06-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'startDate': '2026-06-01',
            'endDate': None
         }
      ),
      (
         '/set-restroom-alert',
         {
            'restroom': 'Entrance Restroom',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Women\'s restroom is temporarily unavailable.'
         },
         (
            'set_restroom_alert',
            {
               'restroom': 'Entrance Restroom',
               'alert_start_date': '2026-06-01',
               'alert_end_date': '2026-06-30',
               'message': 'Women\'s restroom is temporarily unavailable.'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom',
            'alertStartDate': '2026-06-01',
            'alertEndDate': '2026-06-30',
            'message': 'Women\'s restroom is temporarily unavailable.'
         }
      ),
      (
         '/remove-restroom-alert',
         {
            'restroom': 'Entrance Restroom'
         },
         (
            'remove_restroom_alert',
            {
               'restroom': 'Entrance Restroom'
            }
         ),
         {
            'success': True,
            'restroom': 'Entrance Restroom'
         }
      ),
      (
         '/create-update',
         {
            'title': 'New baby giraffe',
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         },
         (
            'create_update',
            {
               'title': 'New baby giraffe',
               'description': 'Come meet the new calf.',
               'update_type': 'New Arrival',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'description': 'Come meet the new calf.',
            'type': 'New Arrival',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/end-update',
         {
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'endDate': '2026-06-15'
         },
         (
            'end_update',
            {
               'title': 'New baby giraffe',
               'start_date': '2026-06-01',
               'end_date': '2026-06-15'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'endDate': '2026-06-15'
         }
      ),
      (
         '/edit-update',
         {
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'description': 'Updated calf details.',
            'type': 'Closure',
            'endDate': '2026-07-15'
         },
         (
            'edit_update',
            {
               'title': 'New baby giraffe',
               'start_date': '2026-06-01',
               'description': 'Updated calf details.',
               'update_type': 'Closure',
               'end_date': '2026-07-15'
            }
         ),
         {
            'success': True,
            'title': 'New baby giraffe',
            'startDate': '2026-06-01',
            'description': 'Updated calf details.',
            'type': 'Closure',
            'endDate': '2026-07-15'
         }
      ),
      (
         '/set-gift-shop-closed',
         {
            'giftShop': 'Zootique',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_gift_shop_as_closed',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'gift_shop': 'Zootique',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-attraction-closed',
         {
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_attraction_as_closed',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'attraction': 'Conservation Carousel',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-zoomobile-station-closed',
         {
            'zoomobileStation': 'Africa Zoomobile Station',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_zoomobile_station_as_closed',
            {
               'zoomobile_station': 'Africa Zoomobile Station',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'zoomobile_station': 'Africa Zoomobile Station',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-zoomobile-station-open',
         {
            'zoomobileStation': 'Africa Zoomobile Station'
         },
         (
            'set_zoomobile_station_as_open',
            {
               'zoomobile_station': 'Africa Zoomobile Station'
            }
         ),
         {
            'success': True,
            'zoomobile_station': 'Africa Zoomobile Station'
         }
      ),
      (
         '/set-drinking-fountains-closed',
         {
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         },
         (
            'set_drinking_fountains_as_closed',
            {
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'message': 'Closed.'
            }
         ),
         {
            'success': True,
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'message': 'Closed.'
         }
      ),
      (
         '/set-drinking-fountains-open',
         {
            'startDate': '2026-07-01',
            'endDate': None
         },
         (
            'set_drinking_fountains_as_open',
            {
               'start_date': '2026-07-01',
               'end_date': None
            }
         ),
         {
            'success': True,
            'startDate': '2026-07-01',
            'endDate': None
         }
      )
   ]
)
def test_console_mutation_endpoints_map_payloads_and_success_responses(
      stub_database,
      path,
      body,
      expected_call,
      response_subset ):
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubDatabase.instances[ 0 ].calls == [ expected_call ]

   for key, value in response_subset.items():
      assert result[ key ] == value

   assert 'error' not in result


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-restaurant-opening-schedule',
         {
            'restaurant': 'Africa Restaurant',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidaysOnly': False,
            'message': 'Schedule.'
         },
         (
            'set_restaurant_opening_schedule',
            {
               'restaurant': 'Africa Restaurant',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'holidays_only': False,
               'message': 'Schedule.'
            }
         ),
         {
            'restaurant': 'Africa Restaurant',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30'
         }
      ),
      (
         '/set-gift-shop-opening-schedule',
         {
            'giftShop': 'Zootique',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidaysOnly': False,
            'message': 'Schedule.'
         },
         (
            'set_gift_shop_opening_schedule',
            {
               'gift_shop': 'Zootique',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'holidays_only': False,
               'message': 'Schedule.'
            }
         ),
         {
            'gift_shop': 'Zootique',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30'
         }
      ),
      (
         '/set-attraction-opening-schedule',
         {
            'attraction': 'Conservation Carousel',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'holidaysOnly': False,
            'message': 'Schedule.'
         },
         (
            'set_attraction_opening_schedule',
            {
               'attraction': 'Conservation Carousel',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'holidays_only': False,
               'message': 'Schedule.'
            }
         ),
         {
            'attraction': 'Conservation Carousel',
            'scheduleStartDate': '2026-06-01',
            'scheduleEndDate': '2026-06-30'
         }
      )
   ]
)
def test_weekly_schedule_endpoints_map_payloads_and_success_responses(
      stub_database,
      path,
      body,
      expected_call,
      response_subset ):
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubDatabase.instances[ 0 ].calls == [ expected_call ]
   assert result[ 'success' ] is True

   for key, value in response_subset.items():
      assert result[ key ] == value

   assert result[ 'monday' ] is True
   assert result[ 'tuesday' ] is False
   assert result[ 'wednesday' ] is True
   assert result[ 'thursday' ] is False
   assert result[ 'friday' ] is True
   assert result[ 'saturday' ] is False
   assert result[ 'sunday' ] is True
   assert result[ 'holidaysOnly' ] is False
   assert result[ 'message' ] == 'Schedule.'


@pytest.mark.parametrize(
   'path, body, expected_call, response_subset',
   [
      (
         '/set-current-zoomobile-route',
         {
            'route': 'winter',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         },
         (
            'set_current_zoomobile_route',
            {
               'route': 'winter',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30'
            }
         ),
         {
            'route': 'winter',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/set-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'time': '10:00',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'message': 'Schedule.'
         },
         (
            'set_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'talk_time': '10:00',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'message': 'Schedule.'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'time': '10:00'
         }
      ),
      (
         '/end-guardians-talk-schedule',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30'
         },
         (
            'end_guardians_talk_schedule',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'schedule_end_date': '2026-06-30'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/cancel-guardians-talk-occurrence',
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'time': '10:00'
         },
         (
            'cancel_guardians_talk_occurrence',
            {
               'talk': 'African Lion',
               'location': 'Africa Savanna',
               'date': '2026-06-15',
               'time': '10:00'
            }
         ),
         {
            'talk': 'African Lion',
            'location': 'Africa Savanna',
            'date': '2026-06-15',
            'time': '10:00'
         }
      ),
      (
         '/set-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'time': '14:00',
            'monday': True,
            'tuesday': False,
            'wednesday': True,
            'thursday': False,
            'friday': True,
            'saturday': False,
            'sunday': True,
            'message': 'Schedule.'
         },
         (
            'set_wild_encounter_schedule',
            {
               'wild_encounter': 'African Rainforest',
               'start_date': '2026-06-01',
               'end_date': '2026-06-30',
               'encounter_time': '14:00',
               'monday': True,
               'tuesday': False,
               'wednesday': True,
               'thursday': False,
               'friday': True,
               'saturday': False,
               'sunday': True,
               'message': 'Schedule.'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'startDate': '2026-06-01',
            'endDate': '2026-06-30',
            'time': '14:00'
         }
      ),
      (
         '/end-wild-encounter-schedule',
         {
            'wildEncounter': 'African Rainforest',
            'endDate': '2026-06-30'
         },
         (
            'end_wild_encounter_schedule',
            {
               'wild_encounter': 'African Rainforest',
               'schedule_end_date': '2026-06-30'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'endDate': '2026-06-30'
         }
      ),
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'time': '14:00'
         },
         (
            'cancel_wild_encounter_occurrence',
            {
               'wild_encounter': 'African Rainforest',
               'date': '2026-06-15',
               'time': '14:00'
            }
         ),
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'time': '14:00'
         }
      )
   ]
)
def test_schedule_and_occurrence_endpoints_map_payloads_and_success_responses(
      stub_database,
      path,
      body,
      expected_call,
      response_subset ):
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert StubDatabase.instances[ 0 ].calls == [ expected_call ]
   assert result[ 'success' ] is True

   for key, value in response_subset.items():
      assert result[ key ] == value

   assert 'error' not in result


@pytest.mark.parametrize(
   'path, body, expected_error',
   [
      (
         '/set-animal-off-display',
         {
            'species': 'African Lion',
            'exhibit': 'Africa Savanna'
         },
         'No animal found with species "African Lion".'
      ),
      (
         '/set-exhibit-closed',
         {
            'exhibit': 'Africa Savanna'
         },
         'Could not set "Africa Savanna" as closed.'
      ),
      (
         '/set-restaurant-opening-schedule',
         {
            'restaurant': 'Africa Restaurant'
         },
         'Could not set opening schedule for "Africa Restaurant".'
      ),
      (
         '/set-current-zoomobile-route',
         {
            'route': 'winter'
         },
         'Could not set Zoomobile route to "winter".'
      ),
      (
         '/cancel-wild-encounter-occurrence',
         {
            'wildEncounter': 'African Rainforest',
            'date': '2026-06-15',
            'time': '14:00'
         },
         'Could not cancel "African Rainforest" on 2026-06-15 at 14:00.'
      )
   ]
)
def test_console_mutation_endpoints_return_error_when_database_returns_false(
      stub_database,
      path,
      body,
      expected_error ):
   StubDatabase.default_success = False
   handler = make_handler( path, body )

   server.MyHandler.do_POST( handler )

   result = response_json( handler )

   assert handler.statuses == [ 200 ]
   assert result[ 'success' ] is False
   assert result[ 'error' ] == expected_error
