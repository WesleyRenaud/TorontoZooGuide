from __future__ import annotations

from api_test_support.fake_handler import FakeHandler

from api.static.static_file_sender import StaticFileSender


def Test_Send_TestCssFile_ExpectGuessesContentType() -> None:
   handler = FakeHandler()

   StaticFileSender.send( handler, './styles/styles.css' )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'text/css' ) in handler.sent_headers
   assert handler.wfile.getvalue()


def Test_Send_TestPngFile_ExpectServesBinaryInChunks() -> None:
   handler = FakeHandler()

   StaticFileSender.send(
      handler,
      './images/details/animals/indo-malaya-outdoor/cheetah.png' )

   assert handler.statuses == [ 200 ]
   assert handler.sent_headers[ 0 ][ 1 ] == 'image/png'
   assert handler.wfile.getvalue().startswith( b'\x89PNG' )
