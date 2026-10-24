from __future__ import annotations

from email.utils import formatdate
import mimetypes
from pathlib import Path
import time

from api_test_support.fake_handler import FakeHandler

from api.shared.enums.position import Position
from api.static.static_file_sender import StaticFileSender


def Test_Send_TestCssFile_ExpectGuessesContentType() -> None:
   handler = FakeHandler()
   filepath = './styles/styles.css'

   StaticFileSender.send( handler, filepath )

   content_type, _ = mimetypes.guess_type( filepath )
   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', content_type ) in handler.sent_headers
   assert ( 'Cache-Control', StaticFileSender.STATIC_CACHE_CONTROL ) in handler.sent_headers
   assert handler.wfile.getvalue()


def Test_Send_TestPngFile_ExpectServesBinaryInChunks() -> None:
   handler = FakeHandler()
   filepath = './images/details/animals/indo-malaya-outdoor/cheetah.png'

   StaticFileSender.send( handler, filepath )

   content_type, _ = mimetypes.guess_type( filepath )
   assert handler.statuses == [ 200 ]
   assert handler.sent_headers[ Position.FIRST ][ Position.SECOND ] == content_type
   assert handler.wfile.getvalue().startswith( b'\x89PNG' )
   assert ( 'Cache-Control', StaticFileSender.STATIC_CACHE_CONTROL ) in handler.sent_headers


def Test_Send_TestHtmlFile_ExpectRevalidates() -> None:
   handler = FakeHandler()

   StaticFileSender.send( handler, './pages/animals.html', 'text/html' )

   body = handler.wfile.getvalue()
   assert handler.statuses == [ 200 ]
   assert ( 'Cache-Control', StaticFileSender.HTML_CACHE_CONTROL ) in handler.sent_headers
   assert body.startswith( b'<!DOCTYPE html>' )
   assert b'rel="modulepreload"' in body
   assert b'href="/scripts/pages/animalsBootstrap.js"' in body


def Test_Send_TestAnimalsPageWithModifiedSince_ExpectFullBody() -> None:
   handler = FakeHandler( headers={
      'If-Modified-Since': formatdate( time.time() + 60, usegmt=True ),
   } )

   StaticFileSender.send( handler, './pages/animals.html', 'text/html' )

   assert handler.statuses == [ 200 ]
   assert b'rel="modulepreload"' in handler.wfile.getvalue()


def Test_Send_TestPlainHtml_ExpectSendsBody( tmp_path: Path ) -> None:
   page = tmp_path / 'plain.html'
   page.write_text( '<!DOCTYPE html><html></html>', encoding='utf-8' )
   handler = FakeHandler()

   StaticFileSender.send( handler, str( page ), 'text/html' )

   assert handler.statuses == [ 200 ]
   assert handler.wfile.getvalue().startswith( b'<!DOCTYPE html>' )


def Test_Send_TestPlainHtmlUnmodified_ExpectNotModified( tmp_path: Path ) -> None:
   page = tmp_path / 'plain.html'
   page.write_text( '<!DOCTYPE html><html></html>', encoding='utf-8' )
   handler = FakeHandler( headers={
      'If-Modified-Since': formatdate( time.time() + 60, usegmt=True ),
   } )

   StaticFileSender.send( handler, str( page ), 'text/html' )

   assert handler.statuses == [ 304 ]
   assert handler.wfile.getvalue() == b''


def Test_Send_TestMissingModuleEntry_ExpectNotModified( tmp_path: Path ) -> None:
   page = tmp_path / 'page.html'
   page.write_text(
      '<script type="module" src="./missing-entry.js"></script>',
      encoding='utf-8',
   )
   handler = FakeHandler( headers={
      'If-Modified-Since': formatdate( time.time() + 60, usegmt=True ),
   } )

   StaticFileSender.send( handler, str( page ), 'text/html' )

   assert handler.statuses == [ 304 ]
   assert handler.wfile.getvalue() == b''


def Test_Send_TestUnmodifiedScript_ExpectNotModified() -> None:
   handler = FakeHandler( headers={
      'If-Modified-Since': formatdate( time.time() + 60, usegmt=True ),
   } )

   StaticFileSender.send( handler, './scripts/strings.js' )

   assert handler.statuses == [ 304 ]
   assert handler.wfile.getvalue() == b''
   assert ( 'Cache-Control', StaticFileSender.STATIC_CACHE_CONTROL ) in handler.sent_headers


def Test_Send_TestStaleScript_ExpectFullBody() -> None:
   handler = FakeHandler( headers={
      'If-Modified-Since': formatdate( 0, usegmt=True ),
   } )

   StaticFileSender.send( handler, './scripts/strings.js' )

   assert handler.statuses == [ 200 ]
   assert b'export class Strings' in handler.wfile.getvalue()


def Test_Send_TestMissingFile_ExpectReturns404() -> None:
   handler = FakeHandler()

   StaticFileSender.send( handler, './pages/missing-static-file.html' )

   assert handler.errors == [ ( 404, 'Not Found' ) ]


def Test_Send_TestMissingHeaders_ExpectSendsBody() -> None:
   handler = FakeHandler()
   handler.headers = None

   StaticFileSender.send( handler, './scripts/strings.js' )

   assert handler.statuses == [ 200 ]
   assert b'export class Strings' in handler.wfile.getvalue()


def Test_Send_TestInvalidModifiedSince_ExpectSendsBody() -> None:
   handler = FakeHandler( headers={
      'If-Modified-Since': 'not-a-date',
   } )

   StaticFileSender.send( handler, './scripts/strings.js' )

   assert handler.statuses == [ 200 ]
   assert b'export class Strings' in handler.wfile.getvalue()


def Test_CacheControl_TestHtmlPath_ExpectRevalidates() -> None:
   cache_control = StaticFileSender.cache_control(
      './pages/animals.html',
      'application/octet-stream' )

   assert cache_control == StaticFileSender.HTML_CACHE_CONTROL


def Test_Send_TestUnknownFileType_ExpectOctetStream( tmp_path: Path ) -> None:
   filepath = tmp_path / 'notes'
   filepath.write_bytes( b'hello' )
   handler = FakeHandler()

   StaticFileSender.send( handler, str( filepath ) )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'application/octet-stream' ) in handler.sent_headers
   assert handler.wfile.getvalue() == b'hello'
