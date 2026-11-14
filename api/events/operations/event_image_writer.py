from __future__ import annotations

import base64
from io import BytesIO

from PIL import Image

from api.shared.enums.image_format import ImageFormat
from tools.checks.asset_key_normalizer import AssetKeyNormalizer
from tools.checks.paths import Paths
from tools.checks.website_page import WebsitePage


class EventImageWriter():
   FOLDER = Paths.DETAIL_IMAGES / 'events'


   @classmethod
   def save( cls, name: str, image: str ) -> bool:
      if WebsitePage.is_absolute( image ):
         cls.write( name, WebsitePage.fetch_bytes( image ) )
         return True

      encoded = cls.payload( image )

      if encoded == '' or not ImageFormat.matches_data_url( image ):
         return True

      cls.write( name, base64.b64decode( encoded ) )
      return True


   @classmethod
   def write( cls, name: str, data: bytes ) -> None:
      destination = cls.FOLDER / AssetKeyNormalizer.file_name( name )
      destination.parent.mkdir( parents=True, exist_ok=True )
      destination.write_bytes( cls.png( data ) )


   @classmethod
   def png( cls, data: bytes ) -> bytes:
      webp = data.startswith( b'RIFF' ) and data[ 8:12 ] == b'WEBP'
      jpeg = data.startswith( b'\xff\xd8\xff' )
      gif = data.startswith( ( b'GIF87a', b'GIF89a' ) )

      if not webp and not jpeg and not gif:
         return data

      image = Image.open( BytesIO( data ) )
      image.load()
      converted = BytesIO()
      image.save( converted, format='PNG' )
      return converted.getvalue()


   @classmethod
   def payload( cls, data: str ) -> str:
      _header, _comma, encoded = data.partition( ',' )
      return encoded.strip()
