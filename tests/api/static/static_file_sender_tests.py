from __future__ import annotations

import mimetypes

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
   assert handler.wfile.getvalue()


def Test_Send_TestPngFile_ExpectServesBinaryInChunks() -> None:
   handler = FakeHandler()
   filepath = './images/details/animals/indo-malaya-outdoor/cheetah.png'

   StaticFileSender.send( handler, filepath )

   content_type, _ = mimetypes.guess_type( filepath )
   assert handler.statuses == [ 200 ]
   assert handler.sent_headers[ Position.FIRST ][ Position.SECOND ] == content_type
   assert handler.wfile.getvalue().startswith( b'\x89PNG' )
