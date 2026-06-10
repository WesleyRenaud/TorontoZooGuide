from __future__ import annotations

import pytest

import api.server as server
from conftest import FakeHandler

def test_send_file_serves_existing_static_page() -> None:
   handler = FakeHandler( path='/map.html' )

   server.MyHandler._send_file( handler, './pages/map.html', 'text/html' )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'text/html' ) in handler.sent_headers
   assert handler.wfile.getvalue().startswith( b'<!DOCTYPE html>' )


def test_send_file_renders_shared_html_strings() -> None:
   handler = FakeHandler( path='/animals.html' )

   server.MyHandler._send_file( handler, './pages/animals.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert '<title>Toronto Zoo Guide</title>' in content
   assert '{{ site.titles.guide }}' not in content


def test_send_file_renders_animals_page_nav_in_standard_order() -> None:
   handler = FakeHandler( path='/animals.html' )

   server.MyHandler._send_file( handler, './pages/animals.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   nav_items = [
      '<a href="map.html">Map</a>',
      '<a href="animals.html">Animals</a>',
      '<a href="https://www.torontozoo.com/meettheguardians">Meet The Guardians</a>',
      '<a href="https://www.torontozoo.com/wildencounters">Wild Encounters</a>',
      '<a href="itinerary.html">Itinerary</a>'
   ]

   nav_positions = [ content.index( item ) for item in nav_items ]

   assert nav_positions == sorted( nav_positions )


def test_send_file_renders_itinerary_static_strings() -> None:
   handler = FakeHandler( path='/itinerary.html' )

   server.MyHandler._send_file( handler, './pages/itinerary.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert 'Itinerary panel' in content
   assert '{{ itinerary.aria.panel }}' not in content


def test_send_file_renders_console_operation_strings() -> None:
   handler = FakeHandler( path='/console-operations.html' )

   server.MyHandler._send_file( handler, './pages/console-operations.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert 'Operations menu' in content
   assert 'Set animal as off display' in content
   assert '{{ panelTitles.offDisplay }}' not in content


def test_send_file_returns_404_for_missing_file() -> None:
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
def test_get_static_routes( path: str ) -> None:
   handler = server.MyHandler.__new__( server.MyHandler )
   handler.path = path
   handler.statuses = []
   handler.files = []
   handler._send_file = lambda filepath, content_type=None: handler.files.append( ( filepath, content_type ) )

   server.MyHandler.do_GET( handler )

   assert len( handler.files ) == 1


def test_get_unknown_route_returns_404() -> None:
   missing = server.MyHandler.__new__( server.MyHandler )
   missing.path = '/unknown'
   missing.errors = []
   missing.send_error = lambda code, message=None: missing.errors.append( ( code, message ) )
   server.MyHandler.do_GET( missing )
   assert missing.errors == [ ( 404, 'Not Found' ) ]
