from __future__ import annotations

from typing import Any

import pytest

from api.http_request_handler import HttpRequestHandler
from api.server_address import ServerAddress
import api.server_runner as server_runner
from api.server_runner import ServerRunner
from api.shared.enums.position import Position


class _FakeServer:
   address: ServerAddress
   handler: Any
   served: bool


   def __init__( self, address: ServerAddress, handler: Any ) -> None:
      self.address = address
      self.handler = handler
      self.served = False


   def serve_forever( self ) -> None:
      self.served = True


def Test_Run_TestDefaultPort_ExpectStartsThreadedHttpServer(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   created: list[ _FakeServer ] = []

   def fake_server( address: ServerAddress, handler: Any ) -> _FakeServer:
      server = _FakeServer( address, handler )
      created.append( server )
      return server

   monkeypatch.setattr( server_runner, 'ThreadedHttpServer', fake_server )

   ServerRunner.run()

   assert len( created ) == 1
   assert created[ Position.FIRST ].address == ServerAddress(
      'localhost',
      ServerRunner.DEFAULT_PORT,
   )
   assert created[ Position.FIRST ].handler is HttpRequestHandler
   assert created[ Position.FIRST ].served is True
