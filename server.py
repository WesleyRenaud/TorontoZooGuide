from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from urllib.parse import urlparse

import database


class MyHandler( BaseHTTPRequestHandler ):
   database = database.Database()

   def do_GET( self ):
      parsed = urlparse( self.path )

      if parsed.path in ['/map.html']:
         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/html' )
         self.end_headers()
         with open( './pages/map.html', 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )
      
      if parsed.path in ['/animals.html']:
         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/html' )
         self.end_headers()
         with open( './pages/animals.html', 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      if parsed.path in ['/itinerary.html']:
         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/html' )
         self.end_headers()
         with open( './pages/itinerary.html', 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      elif parsed.path == '/styles/styles.css':
         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/css' )
         self.end_headers()
         with open( './styles/styles.css', 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      elif parsed.path == '/scripts/scripts.js':
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/javascript' )
         self.end_headers()
         with open('./scripts/scripts.js', 'rb') as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )

      elif 'png' in parsed.path:
         image_path = parsed.path.replace( '%20', ' ' )
         image_path = image_path[1:]

         self.send_response( 200 )
         self.send_header( 'Content-type', 'image/png' )
         self.end_headers()
         with open( image_path, 'rb' ) as fp:
            while True:
               chunk = fp.read( 8192 )
               if not chunk:
                  break
               self.wfile.write( chunk )


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

         animals = self.database.get_animals_viewable_on_day( month, day, temp, include_off_display_animals, species_to_include )
         
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

         exhibits = self.database.get_exhibits_in_region( region )

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

         animals = self.database.get_animals_in_exhibit( exhibit )

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

         animal_info = self.database.get_animal_information( species )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"information": [animal_info.to_dict()]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/search-animals':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         query = data.get( 'query' )

         animals = self.database.get_animals_matching_query( query )

         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()
