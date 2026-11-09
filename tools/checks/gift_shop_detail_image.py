from __future__ import annotations

from .animal_detail_image import AnimalDetailImage
from .paths import Paths


class GiftShopDetailImage():
   @classmethod
   def source( cls, name: str ) -> str:
      image = Paths.DETAIL_IMAGES / 'gift-shops' / f'{ AnimalDetailImage.normalize( name ) }.png'
      return image.relative_to( Paths.ROOT ).as_posix()
