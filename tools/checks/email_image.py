from __future__ import annotations

from dataclasses import dataclass
from email.utils import make_msgid
from html import unescape
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse


@dataclass
class EmailImage:
   content_id: str
   path: Path


   @classmethod
   def from_file_uri( cls, src: str ) -> EmailImage:
      return cls(
         content_id=make_msgid( domain='zoo.guide' ),
         path=Path( unquote( urlparse( unescape( src ) ).path ) ),
      )


   def src( self ) -> str:
      return f'cid:{ self.content_id[ 1:-1 ] }'
