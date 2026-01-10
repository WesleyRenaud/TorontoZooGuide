from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
from urllib.parse import urlparse

import database


class MyHandler( BaseHTTPRequestHandler ):
   database = database.Database()

   def do_GET( self ):
      parsed = urlparse( self.path )

      if parsed.path in ['/home.html']:
         fp = open( './pages/home.html' )
         content = fp.read()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/html' )
         self.send_header( 'Content-length', len( content ) )
         self.end_headers()
         self.wfile.write( bytes( content, 'utf-8' ) )


      elif parsed.path == '/styles/styles.css':
         fp = open( './styles/styles.css', 'r' )
         content = fp.read()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/css' )
         self.send_header( 'Content-length', len( content ) )
         self.end_headers()
         self.wfile.write( bytes( content, 'utf-8' ) )


      elif parsed.path == '/scripts/scripts.js':
         fp = open( './scripts/scripts.js', 'r' )
         content = fp.read()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'text/css' )
         self.send_header( 'Content-length', len( content ) )
         self.end_headers()
         self.wfile.write( bytes( content, 'utf-8' ) )


      elif 'png' in parsed.path:
         image_path = parsed.path.replace( '%20', ' ' )
         image_path = image_path[1:]

         fp = open( image_path, 'rb' )
         content = fp.read()

         self.send_response( 200 )
         self.send_header( 'Content-type', 'image/png' )
         self.send_header( 'Content-length', str( len( content ) ) )
         self.end_headers()
         self.wfile.write( content )


   def do_POST( self ):
      if self.path == '/get-summer-animals':
         animals = self.database.get_summer_animals()
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-winter-animals':
         animals = self.database.get_winter_animals()
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animals-viewable-in-month':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )

         animals = self.database.get_animals_viewable_in_month( month )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


      elif self.path == '/get-animals-viewable-in-day':
         content_length = int( self.headers[ 'Content-Length'] )
         post_data = self.rfile.read( content_length )
         data = json.loads( post_data.decode( 'utf-8' ) )

         month = data.get( 'month' )
         day = data.get( 'day' )
         temp = data.get( 'temp' )

         animals = self.database.get_animals_viewable_on_day( month, day, temp )
         
         self.send_response( 200 )
         self.send_header( 'Content-type', 'application/json' )
         self.end_headers()
         response = {"animals": [animal.to_dict() for animal in animals]}
         self.wfile.write( json.dumps( response ).encode( 'utf-8' ) )


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()
