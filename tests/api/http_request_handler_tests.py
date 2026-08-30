from __future__ import annotations

from api_test_support.fake_handler import FakeHandler
from api_test_support.post_handler import make_handler
import pytest

import api.http_request_handler as server


def Test_SendFile_TestExistingStaticPage_ExpectServesHtml() -> None:
   handler = FakeHandler( path='/map.html' )

   server.HttpRequestHandler._send_file( handler, './pages/map.html', 'text/html' )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'text/html' ) in handler.sent_headers
   assert handler.wfile.getvalue().startswith( b'<!DOCTYPE html>' )


def Test_SendFile_TestAnimalsPage_ExpectRendersSharedHtmlStrings() -> None:
   handler = FakeHandler( path='/animals.html' )

   server.HttpRequestHandler._send_file( handler, './pages/animals.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert '<title>Toronto Zoo Guide</title>' in content
   assert '{{ site.titles.guide }}' not in content


def Test_SendFile_TestAnimalsPage_ExpectRendersNavInStandardOrder() -> None:
   handler = FakeHandler( path='/animals.html' )

   server.HttpRequestHandler._send_file( handler, './pages/animals.html', 'text/html' )

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


def Test_SendFile_TestItineraryPage_ExpectRendersStaticStrings() -> None:
   handler = FakeHandler( path='/itinerary.html' )

   server.HttpRequestHandler._send_file( handler, './pages/itinerary.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert 'Itinerary panel' in content
   assert '{{ itinerary.aria.panel }}' not in content


def Test_SendFile_TestConsoleOperationsPage_ExpectRendersOperationStrings() -> None:
   handler = FakeHandler( path='/console-operations.html' )

   server.HttpRequestHandler._send_file( handler, './pages/console-operations.html', 'text/html' )

   content = handler.wfile.getvalue().decode( 'utf-8' )

   assert 'Operations menu' in content
   assert 'Set animal as off display' in content
   assert '{{ panelTitles.offDisplay }}' not in content


def Test_SendFile_TestMissingFile_ExpectReturns404() -> None:
   handler = FakeHandler( path='/missing.html' )

   server.HttpRequestHandler._send_file( handler, './pages/missing.html' )

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
def Test_DoGet_TestStaticRoutes_ExpectSendsFile( path: str ) -> None:
   handler = server.HttpRequestHandler.__new__( server.HttpRequestHandler )
   handler.path = path
   handler.statuses = []
   handler.files = []
   handler._send_file = lambda filepath, content_type=None: handler.files.append( ( filepath, content_type ) )

   server.HttpRequestHandler.do_GET( handler )

   assert len( handler.files ) == 1


def Test_DoGet_TestUnknownRoute_ExpectReturns404() -> None:
   missing = server.HttpRequestHandler.__new__( server.HttpRequestHandler )
   missing.path = '/unknown'
   missing.errors = []
   missing.send_error = lambda code, message=None: missing.errors.append( ( code, message ) )
   server.HttpRequestHandler.do_GET( missing )
   assert missing.errors == [ ( 404, 'Not Found' ) ]


def Test_DoPost_TestUnknownRoute_ExpectReturns404() -> None:
   handler = make_handler( '/unknown-post-route' )

   server.HttpRequestHandler.do_POST( handler )

   assert handler.errors == [ ( 404, 'Not Found' ) ]
