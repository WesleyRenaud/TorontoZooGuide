from __future__ import annotations

import mimetypes

from api_test_support.fake_handler import FakeHandler

from api.static.static_file_handler_mixin import StaticFileHandlerMixin


class StaticFileHandlerTestDouble( StaticFileHandlerMixin, FakeHandler ):
   pass


def Test_SendFile_TestCssFile_ExpectDelegatesToStaticFileSender() -> None:
   handler = StaticFileHandlerTestDouble()
   filepath = './styles/styles.css'

   handler._send_file( filepath )

   content_type, _ = mimetypes.guess_type( filepath )
   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', content_type ) in handler.sent_headers
   assert handler.wfile.getvalue()
