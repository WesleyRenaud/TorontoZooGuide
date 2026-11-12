from __future__ import annotations

from .asset_key_normalizer import AssetKeyNormalizer
from .paths import Paths


class AnimalDetailImage():
   @classmethod
   def source( cls, exhibit: str, species: str ) -> str:
      image = (
         Paths.DETAIL_IMAGES
         / 'animals'
         / AssetKeyNormalizer.normalize( exhibit )
         / AssetKeyNormalizer.file_name( species )
      )
      return image.relative_to( Paths.ROOT ).as_posix()
