from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from urllib.parse import urlparse


class MyHandler( BaseHTTPRequestHandler ):    
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


if __name__ == '__main__':
   httpd = HTTPServer( ( 'localhost', int( sys.argv[1] ) ), MyHandler )
   print( 'Server listing in port:  ', int( sys.argv[1] ) )
   httpd.serve_forever()