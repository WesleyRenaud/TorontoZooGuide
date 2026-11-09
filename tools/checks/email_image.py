from __future__ import annotations

from dataclasses import dataclass
from email.utils import make_msgid
from html import unescape
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

from PIL import Image

from .website_page import WebsitePage


@dataclass
class EmailImage:
   MAX_EDGE = 216
   JPEG_QUALITY = 80
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
   def rgb_image( cls, image: Image.Image ) -> Image.Image:
      if image.mode == 'RGB':
         return image

      rgba = image.convert( 'RGBA' )
      background = Image.new( 'RGB', rgba.size, ( 255, 255, 255 ) )
      background.paste( rgba, mask=rgba.getchannel( 'A' ) )
      return background


   @classmethod
   def fit( cls, content: bytes ) -> bytes:
      try:
         image = Image.open( BytesIO( content ) )
         image.load()
      except ( OSError, ValueError ):
         return content

      image = cls.rgb_image( image )
      image.thumbnail( ( cls.MAX_EDGE, cls.MAX_EDGE ), Image.Resampling.LANCZOS )
      output = BytesIO()
      image.save( output, format='JPEG', quality=cls.JPEG_QUALITY, optimize=True )
      return output.getvalue()


   @classmethod
   def from_bytes( cls, content: bytes, filename: str ) -> EmailImage:
      fitted = cls.fit( content )
      name = filename
      subtype = cls.subtype_for( filename )

      if fitted != content:
         name = f'{ Path( filename ).stem or "image" }.jpg'
         subtype = 'jpeg'
         content = fitted

      return cls(
         content_id=make_msgid( domain='zoo.guide' ),
         path=Path( name ),
         content=content,
         subtype=subtype,
         filename=name,
      )


   @classmethod
   def from_file_uri( cls, src: str ) -> EmailImage:
      path = Path( unquote( urlparse( unescape( src ) ).path ) )
      return cls.from_bytes( path.read_bytes(), path.name )


   @classmethod
   def from_url( cls, url: str ) -> EmailImage:
      filename = unquote( urlparse( url ).path ).rsplit( '/', 1 )[ -1 ] or 'image'
      return cls.from_bytes( WebsitePage.fetch_bytes( url ), filename )


   def src( self ) -> str:
      return f'cid:{ self.content_id[ 1:-1 ] }'
