from __future__ import annotations

from .animal_detail_image import AnimalDetailImage
from .paths import Paths


class GuardiansTalkDetailImage():
   @classmethod
   def source( cls, location: str, name: str ) -> str:
      image = (
         Paths.DETAIL_IMAGES
         / 'guardians-talks'
         / AnimalDetailImage.normalize( location )
         / f'{ AnimalDetailImage.normalize( name ) }.png'
      )
      return image.relative_to( Paths.ROOT ).as_posix()
