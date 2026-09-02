from __future__ import annotations

from api.database_connection_provider import DatabaseConnectionProvider
from api.request_connection_provider import RequestConnectionProvider
from api.types import Types


class SeededDatabase:
   def __init__( self, connection: Types.Connection ) -> None:
      self.conn: Types.Connection | None = connection
      self._closed = False


   def close( self ) -> None:
      if self._closed:
         return

      if self.conn is not None:
         DatabaseConnectionProvider.close( self.conn )

      RequestConnectionProvider.clear()
      self.conn = None
      self._closed = True
