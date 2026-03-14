from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import mimetypes
import os
import sys
from urllib.parse import unquote, urlparse

import database


class MyHandler( BaseHTTPRequestHandler ):
   database = database.Database()


   def _send_file( self, filepath, content_type=None ):
      if not os.path.isfile( filepath ):
         self.send_error( 404, "Not Found" )
         return

      self.send_response( 200 )
      if not content_type:
         content_type, _ = mimetypes.guess_type( filepath )
      self.send_header( "Content-type", content_type or "application/octet-stream" )
      self.end_headers()

      with open( filepath, "rb" ) as fp:
         while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )


   def do_GET( self ):
      parsed = urlparse( self.path )
      path = unquote( parsed.path )  # handles %20 etc

      # Pages
      if path == "/map.html":
         return self._send_file( "./pages/map.html", "text/html" )
      if path == "/animals.html":
         return self._send_file( "./pages/animals.html", "text/html" )
      if path == "/itinerary.html":
         return self._send_file( "./pages/itinerary.html", "text/html" )
      if path == "/console-operations.html":
         return self._send_file( "./pages/console-operations.html", "text/html" )

      # Static folders (serve anything inside)
      if path.startswith( "/styles/" ):
         return self._send_file( "." + path )
      if path.startswith( "/scripts/" ):
         return self._send_file("." + path )   # serves ALL modules
      if path.startswith( "/images/" ):
         return self._send_file( "." + path )

      # Otherwise
      self.send_error( 404, "Not Found" )


   def do_POST( self ):
      if self.path == '/get-visible-animals':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         include_off_display_animals = data.get( 'includeOffDisplayAnimals' )
         species_to_include = data.get( 'speciesToInclude' )

         animals = self.database.get_animals_viewable_on_day(
            month=month,
            day=day,
            temp=temp,
            include_off_display_animals=include_off_display_animals,
            species_to_include=species_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-exhibits-in-region':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         region = data.get( 'region' )

         exhibits = self.database.get_exhibits_in_region( region=region )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"exhibits": exhibits}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animals-in-exhibit':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )

         animals = self.database.get_animals_in_exhibit( exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": animals}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animal-information':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )

         animal_info = self.database.get_animal_information( species=species )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"information": [animal_info.to_dict()]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-pavilions':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         pavilions = self.database.get_pavilions()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"pavilions": [pavilion.to_dict() for pavilion in pavilions]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restaurants':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         include_closed_restaurants = data.get( 'includeClosedRestaurants' )
         restaurants_to_include = data.get( 'restaurantsToInclude' )

         restaurants = self.database.get_restaurants(
            month=month,
            day=day,
            include_closed_restaurants=include_closed_restaurants,
            restaurants_to_include=restaurants_to_include )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"restaurants": [restaurant.to_dict() for restaurant in restaurants]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-restrooms':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restrooms = self.database.get_restrooms()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"restrooms": [restroom.to_dict() for restroom in restrooms]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-gift-shops':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         include_closed_gift_shops = data.get( 'includeClosedGiftShops' )
         gift_shops_to_include = data.get( 'giftShopsToInclude' )

         gift_shops = self.database.get_gift_shops(
            month=month,
            day=day,
            include_closed_gift_shops=include_closed_gift_shops,
            gift_shops_to_include=gift_shops_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"gift_shops": [gift_shop.to_dict() for gift_shop in gift_shops]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-attractions':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         include_closed_attractions = data.get( 'includeClosedAttractions' )
         attractions_to_include = data.get( 'attractionsToInclude' )

         attractions = self.database.get_attractions(
            month=month,
            day=day,
            include_closed_attractions=include_closed_attractions,
            attractions_to_include=attractions_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"attractions": [attraction.to_dict() for attraction in attractions]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-zoomobile-route':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         route_type = data.get( 'zoomobileRouteType' )
         zoomobile_stations_to_include = data.get( 'zoomobileStationsToInclude' )

         zoomobile_route = self.database.get_zoomobile_route(
            route_type=route_type,
            zoomobile_stations_to_include=zoomobile_stations_to_include )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {
            "zoomobile_stations": [station.to_dict() for station in zoomobile_route[0]],
            "zoomobile_route_markers": [marker.to_dict() for marker in zoomobile_route[1]]
         }
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-meet-the-guardians-talks':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         meet_the_guardians_talks = self.database.get_meet_the_guardians_talks()
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"meet_the_guardians_talks": [meet_the_guardians_talk.to_dict() for meet_the_guardians_talk in meet_the_guardians_talks]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-wild-encounter-meeting-spots':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         wild_encounter_meeting_spots = self.database.get_wild_encounter_meeting_spots()
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"wild_encounter_meeting_spots": [wild_encounter_meeting_spot.to_dict() for wild_encounter_meeting_spot in wild_encounter_meeting_spots]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/search':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         query = ( data.get( 'query' ) or '' ).strip()
         include_animals = bool( data.get( 'includeAnimals' ) )
         include_pavilions = bool( data.get( 'includePavilions' ) )
         include_restaurants = bool( data.get( 'includeRestaurants') )
         include_restrooms = bool( data.get( 'includeRestrooms' ) )
         include_gift_shops = bool( data.get( 'includeGiftShops' ) )
         include_attractions = bool( data.get( 'includeAttractions' ) )
         include_zoomobile_stations = bool( data.get( 'includeZoomobileStations' ) )
         include_wild_encounter_meeting_spots = bool( data.get( 'includeWildEncounterMeetingSpots' ) )
         include_wild_encounters = bool( data.get( 'includeWildEncounters' ) )
         include_meet_the_guardians_talks = bool( data.get( 'includeMeetTheGuardiansTalks' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         day_of_week = data.get( 'dayOfWeek' )

         include_off_display_animals = bool( data.get( 'includeOffDisplayAnimals' ) )
         include_closed_restaurants = bool( data.get( 'includeClosedRestaurants' ) )
         include_closed_attractions = bool( data.get( 'includeClosedAttractions' ) )

         animals_json = []
         pavilions_json = []
         restaurants_json = []
         restrooms_json = []
         gift_shops_json = []
         attractions_json = []
         zoomobile_stations_json = []
         wild_encounter_meeting_spots_json = []
         wild_encounters_json = []
         meet_the_guardians_talks_json = []

         if include_animals:
            animals = self.database.get_animals_matching_query(
               query=query,
               month=month,
               day=day,
               temp=temp,
               include_off_display_animals=include_off_display_animals ) or []
            for animal in animals:
                  d = animal.to_dict()
                  d['type'] = d.get( 'type', 'animal' )
                  animals_json.append( d )

         if include_pavilions:
            pavilions = self.database.get_pavilions_matching_query( query=query ) or []
            for pavilion in pavilions:
                  d = pavilion.to_dict()
                  d['type'] = d.get( 'type', 'pavilion' )
                  pavilions_json.append( d )

         if include_restaurants:
            restaurants = self.database.get_restaurants_matching_query(
               query=query,
               month=month,
               day=day,
               include_closed_restaurants=include_closed_restaurants ) or []
            for restaurant in restaurants:
                  d = restaurant.to_dict()
                  d['type'] = d.get( 'type', 'restaurant' )
                  restaurants_json.append( d )

         if include_restrooms:
            restrooms = self.database.get_restrooms_matching_query( query=query ) or []
            for restroom in restrooms:
                  d = restroom.to_dict()
                  d['type'] = d.get( 'type', 'restroom' )
                  restrooms_json.append( d )

         if include_gift_shops:
            gift_shops = self.database.get_gift_shops_matching_query( query=query, month=month ) or []
            for gift_shop in gift_shops:
                  d = gift_shop.to_dict()
                  d['type'] = d.get( 'type', 'giftShop' )
                  gift_shops_json.append( d )

         if include_attractions:
            attractions = self.database.get_attractions_matching_query(
               query=query,
               month=month,
               day=day,
               include_closed_attractions=include_closed_attractions ) or []
            for attraction in attractions:
                  d = attraction.to_dict()
                  d['type'] = d.get( 'type', 'attraction' )
                  attractions_json.append( d )

         if include_zoomobile_stations:
            zoomobile_stations = self.database.get_zoomobile_stations_matching_query( query=query ) or []
            for zoomobile_station in zoomobile_stations:
                  d = zoomobile_station.to_dict()
                  d['type'] = d.get( 'type', 'zoomobileStation' )
                  zoomobile_stations_json.append( d )

         if include_wild_encounter_meeting_spots:
            wild_encounter_meeting_spots = self.database.get_wild_encounter_meeting_spots_matching_query( query=query ) or []
            for wild_encounter_meeting_spot in wild_encounter_meeting_spots:
                  d = wild_encounter_meeting_spot.to_dict()
                  d['type'] = d.get( 'type', 'wildEncounterMeetingSpot' )
                  wild_encounter_meeting_spots_json.append( d )

         if include_meet_the_guardians_talks:
            meet_the_guardians_talks = self.database.get_meet_the_guardians_talks_with_date_times_matching_query(
               query=query,
               day_of_week=day_of_week ) or []
            for meet_the_guardians_talk in meet_the_guardians_talks:
                  d = meet_the_guardians_talk.to_dict()
                  d['type'] = d.get( 'type', 'meetTheGuardiansTalk' )
                  meet_the_guardians_talks_json.append( d )

         if include_wild_encounters:
            wild_encounters = self.database.get_wild_encounters_matching_query( query=query, day_of_week=day_of_week ) or []
            for wild_encounter in wild_encounters:
                  d = wild_encounter.to_dict()
                  d['type'] = d.get( 'type', 'wildEncounter' )
                  wild_encounters_json.append( d )

         response = {
            'animals': animals_json,
            'pavilions': pavilions_json,
            'restaurants': restaurants_json,
            'restrooms': restrooms_json,
            'gift_shops': gift_shops_json,
            'attractions': attractions_json,
            'zoomobile_stations': zoomobile_stations_json,
            'wild_encounter_meeting_spots': wild_encounter_meeting_spots_json,
            'wild_encounters': wild_encounters_json,
            'meet_the_guardians_talks': meet_the_guardians_talks_json
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )

   
      elif self.path == '/build-itinerary':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )
         animals_to_include = data.get( 'animals' )
         attractions_to_include = data.get( 'attractions' )
         meet_the_guardians_talks_to_include = data.get( 'meetTheGuardiansTalks' )
         wild_encounters_to_include = data.get( 'wildEncounters' )

         animals_json = []
         attractions_json = []
         meet_the_guardians_talks_json = []
         wild_encounters_json = []

         if animals_to_include:
            animals = self.database.get_animals_viewable_on_day(
               month=month,
               day=day,
               temp=temp,
               species_to_include=animals_to_include,
               itinerary_mode=True )
            for animal in animals:
               d = animal.to_dict()
               d['type'] = d.get( 'type', 'animal' )
               animals_json.append( d )

         if attractions_to_include:
            attractions = self.database.get_attractions( month=month, attractions_to_include=attractions_to_include, itinerary_mode=True )
            for attraction in attractions:
                  d = attraction.to_dict()
                  d['type'] = d.get( 'type', 'attraction' )
                  attractions_json.append( d )
               
         if meet_the_guardians_talks_to_include:
            meet_the_guardians_talks = self.database.get_meet_the_guardians_talks_with_date_times(
               meet_the_guardians_talks_to_include=meet_the_guardians_talks_to_include,
               itinerary_mode=True )
            for meet_the_guardians_talk in meet_the_guardians_talks:
                  d = meet_the_guardians_talk.to_dict()
                  d['type'] = d.get( 'type', 'meetTheGuardiansTalk' )
                  meet_the_guardians_talks_json.append( d )

         if wild_encounters_to_include:
            wild_encounters = self.database.get_wild_encounter_meeting_spots_for_wild_encounters(
               wild_encounters_to_include=wild_encounters_to_include )
            for wild_encounter in wild_encounters:
                  d = wild_encounter.to_dict()
                  d['type'] = d.get( 'type', 'wildEncounter' )
                  wild_encounters_json.append( d )

         response = {
            'animals': animals_json,
            'attractions': attractions_json,
            'meet_the_guardians_talks': meet_the_guardians_talks_json,
            'wild_encounters': wild_encounters_json
         }

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      if self.path == '/get-species':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = self.database.get_species()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"species": species}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      if self.path == '/get-restaurant-names':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurants = self.database.get_restaurant_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"restaurants": restaurants}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )   


      if self.path == '/get-gift-shop-names':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shops = self.database.get_gift_shop_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"gift_shops": gift_shops}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )   


      if self.path == '/get-attraction-names':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attractions = self.database.get_attraction_names()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"attractions": attractions}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )          


      if self.path == '/get-exhibits':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibits = self.database.get_exhibits()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"exhibits": exhibits}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-off-display':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_animal_as_off_display(
            species=species,
            exhibit=exhibit,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'startDate': start_date,
            'endDate': end_date,
            'message': message,
         }

         if not success:
            response[ 'error' ] = f'No animal found with species "{species}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-on-display':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         success = self.database.set_animal_as_on_display(
            species=species,
            exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
         }

         if not success:
            response['error'] = f'No off-display entry found for "{species}" in "{exhibit}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-visibility-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )
         daily_start_time = data.get( 'dailyStartTime' )
         daily_end_time = data.get( 'dailyEndTime' )
         message = data.get( 'message' )

         success = self.database.set_animal_limited_viewing_schedule(
            species=species,
            exhibit=exhibit,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            daily_start_time=daily_start_time,
            daily_end_time=daily_end_time,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'dailyStartTime': daily_start_time,
            'dailyEndTime': daily_end_time,
            'message': message,
         }

         if not success:
            response[ 'error' ] = f'Could not set limited viewing schedule for "{species}" in "{exhibit}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )

   
      elif self.path == '/remove-animal-visibility-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         success = self.database.remove_animal_visibility_schedule( species=species, exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
         }

         if not success:
            response['error'] = f'Could not remove visibility schedule for "{species}" in "{exhibit}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-animal-viewing-alert':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )
         alert_start_date = data.get( 'alertStartDate' )
         alert_end_date = data.get( 'alertEndDate' )
         message = data.get( 'message' )

         success = self.database.set_animal_viewing_alert(
            species=species,
            exhibit=exhibit,
            alert_start_date=alert_start_date,
            alert_end_date=alert_end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit,
            'alertStartDate': alert_start_date,
            'alertEndDate': alert_end_date,
            'message': message,
         }

         if not success:
            response['error'] = f'Could not set viewing alert for "{species}" in "{exhibit}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/remove-animal-viewing-alert':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         species = data.get( 'species' )
         exhibit = data.get( 'exhibit' )

         success = self.database.remove_animal_viewing_alert( species=species, exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'species': species,
            'exhibit': exhibit
         }

         if not success:
            response['error'] = f'Could not remove viewing alert for "{species}" in "{exhibit}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-exhibit-closed':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_exhibit_as_closed( exhibit=exhibit, start_date=start_date, end_date=end_date, message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'exhibit': exhibit,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set "{exhibit}" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-exhibit-open':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         exhibit = data.get( 'exhibit' )

         success = self.database.set_exhibit_as_open( exhibit=exhibit )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'exhibit': exhibit
         }

         if not success:
            response['error'] = f'Could not set "{exhibit}" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restaurant-closed':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_restaurant_as_closed(
            restaurant=restaurant,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set "{restaurant}" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restaurant-open':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )

         success = self.database.set_restaurant_as_open( restaurant=restaurant )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant
         }

         if not success:
            response['error'] = f'Could not set "{restaurant}" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-restaurant-opening-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = self.database.set_restaurant_opening_schedule(
            restaurant=restaurant,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set opening schedule for "{restaurant}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/remove-restaurant-opening-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         restaurant = data.get( 'restaurant' )

         success = self.database.remove_restaurant_opening_schedule( restaurant=restaurant )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'restaurant': restaurant
         }

         if not success:
            response['error'] = f'Could not remove schedule for "{restaurant}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-closed':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_gift_shop_as_closed(
            gift_shop=gift_shop,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set "{gift_shop}" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-open':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'GiftShop' )

         success = self.database.set_gift_shop_as_open( gift_shop=gift_shop )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop
         }

         if not success:
            response['error'] = f'Could not set "{gift_shop}" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-gift-shop-opening-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = self.database.set_gift_shop_opening_schedule(
            gift_shop=gift_shop,
            start_date=schedule_start_date,
            end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set opening schedule for "{gift_shop}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/remove-gift-shop-opening-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         gift_shop = data.get( 'giftShop' )

         success = self.database.remove_gift_shop_opening_schedule( gift_shop=gift_shop )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'gift_shop': gift_shop
         }

         if not success:
            response['error'] = f'Could not remove schedule for "{gift_shop}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-closed':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         start_date = data.get( 'startDate' )
         end_date = data.get( 'endDate' )
         message = data.get( 'message' )

         success = self.database.set_attraction_as_closed(
            attraction=attraction,
            start_date=start_date,
            end_date=end_date,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'startDate': start_date,
            'endDate': end_date,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set "{attraction}" as closed.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-open':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )

         success = self.database.set_attraction_as_open( attraction=attraction )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction
         }

         if not success:
            response['error'] = f'Could not set "{attraction}" as open.'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/set-attraction-opening-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )
         schedule_start_date = data.get( 'scheduleStartDate' )
         schedule_end_date = data.get( 'scheduleEndDate' )

         monday = data.get( 'monday' )
         tuesday = data.get( 'tuesday' )
         wednesday = data.get( 'wednesday' )
         thursday = data.get( 'thursday' )
         friday = data.get( 'friday' )
         saturday = data.get( 'saturday' )
         sunday = data.get( 'sunday' )
         holidays_only = data.get( 'holidaysOnly' )

         message = data.get( 'message' )

         success = self.database.set_attraction_opening_schedule(
            attraction=attraction,
            schedule_start_date=schedule_start_date,
            schedule_end_date=schedule_end_date,
            monday=monday,
            tuesday=tuesday,
            wednesday=wednesday,
            thursday=thursday,
            friday=friday,
            saturday=saturday,
            sunday=sunday,
            holidays_only=holidays_only,
            message=message )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction,
            'scheduleStartDate': schedule_start_date,
            'scheduleEndDate': schedule_end_date,
            'monday': monday,
            'tuesday': tuesday,
            'wednesday': wednesday,
            'thursday': thursday,
            'friday': friday,
            'saturday': saturday,
            'sunday': sunday,
            'holidaysOnly': holidays_only,
            'message': message
         }

         if not success:
            response['error'] = f'Could not set opening schedule for "{attraction}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )
         

      elif self.path == '/remove-attraction-opening-schedule':
         content_length = int( self.headers['Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         attraction = data.get( 'attraction' )

         success = self.database.remove_attraction_opening_schedule( attraction=attraction )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()

         response = {
            'success': success,
            'attraction': attraction
         }

         if not success:
            response['error'] = f'Could not remove schedule for "{attraction}".'

         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )
         

if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()
