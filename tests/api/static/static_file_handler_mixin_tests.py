from __future__ import annotations

from api_test_support.fake_handler import FakeHandler

from api.static.static_file_handler_mixin import StaticFileHandlerMixin


class StaticFileHandlerTestDouble( StaticFileHandlerMixin, FakeHandler ):
   pass


def Test_SendFile_TestCssFile_ExpectDelegatesToStaticFileSender() -> None:
   handler = StaticFileHandlerTestDouble()

   handler._send_file( './styles/styles.css' )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'text/css' ) in handler.sent_headers
   assert handler.wfile.getvalue()
