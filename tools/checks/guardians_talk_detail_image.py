from __future__ import annotations

from .asset_key_normalizer import AssetKeyNormalizer
from .paths import Paths


class GuardiansTalkDetailImage():
   @classmethod
   def source( cls, location: str, name: str ) -> str:
      image = (
         Paths.DETAIL_IMAGES
         / 'guardians-talks'
         / AssetKeyNormalizer.normalize( location )
         / AssetKeyNormalizer.file_name( name )
      )
      return image.relative_to( Paths.ROOT ).as_posix()
