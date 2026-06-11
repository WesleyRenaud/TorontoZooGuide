from __future__ import annotations

from api.static.file_server import send_file
from conftest import FakeHandler


def test_send_file_guesses_content_type_for_binary_files() -> None:
   handler = FakeHandler()

   send_file( handler, './styles/styles.css' )

   assert handler.statuses == [ 200 ]
   assert ( 'Content-type', 'text/css' ) in handler.sent_headers
   assert handler.wfile.getvalue()


def test_send_file_serves_binary_files_in_chunks() -> None:
   handler = FakeHandler()

   send_file(
      handler,
      './images/details/animals/indo-malaya-outdoor/cheetah.png' )

   assert handler.statuses == [ 200 ]
   assert handler.sent_headers[ 0 ][ 1 ] == 'image/png'
   assert handler.wfile.getvalue().startswith( b'\x89PNG' )
