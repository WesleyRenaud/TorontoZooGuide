from __future__ import annotations

from dataclasses import dataclass
from email.utils import make_msgid
from html import unescape
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

from .website_page import WebsitePage


@dataclass
class EmailImage:
   content_id: str
   path: Path
   content: bytes
   subtype: str
   filename: str


   @classmethod
   def subtype_for( cls, filename: str ) -> str:
      suffix = Path( filename ).suffix.casefold()
      subtypes = {
         '.jpg': 'jpeg',
         '.jpeg': 'jpeg',
         '.png': 'png',
         '.gif': 'gif',
         '.webp': 'webp',
      }
      return subtypes.get( suffix, 'jpeg' )


   @classmethod
   def from_file_uri( cls, src: str ) -> EmailImage:
      path = Path( unquote( urlparse( unescape( src ) ).path ) )
      return cls(
         content_id=make_msgid( domain='zoo.guide' ),
         path=path,
         content=path.read_bytes(),
         subtype=cls.subtype_for( path.name ),
         filename=path.name,
      )


   @classmethod
   def from_url( cls, url: str ) -> EmailImage:
      filename = unquote( urlparse( url ).path ).rsplit( '/', 1 )[ -1 ] or 'image'
      return cls(
         content_id=make_msgid( domain='zoo.guide' ),
         path=Path( filename ),
         content=WebsitePage.fetch_bytes( url ),
         subtype=cls.subtype_for( filename ),
         filename=filename,
      )


   def src( self ) -> str:
      return f'cid:{ self.content_id[ 1:-1 ] }'
