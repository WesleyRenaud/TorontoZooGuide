from __future__ import annotations

from .asset_key_normalizer import AssetKeyNormalizer
from .paths import Paths


class RestaurantDetailImage():
   @classmethod
   def source( cls, name: str ) -> str:
      image = Paths.DETAIL_IMAGES / 'restaurants' / AssetKeyNormalizer.file_name( name )
      return image.relative_to( Paths.ROOT ).as_posix()
