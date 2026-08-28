from __future__ import annotations

from .static_file_handler import StaticFileHandler
from .static_file_sender import StaticFileSender

class StaticFileHandlerMixin():
   def _send_file(
         self: StaticFileHandler,
         filepath: str,
         content_type: str | None = None ) -> None:
      StaticFileSender.send( self, filepath, content_type )
