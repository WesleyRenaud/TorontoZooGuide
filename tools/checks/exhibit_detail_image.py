from __future__ import annotations

from .asset_key_normalizer import AssetKeyNormalizer
from .exhibit_region_colors import ExhibitRegionColors
from .paths import Paths


class ExhibitDetailImage():
   @classmethod
   def source( cls, name: str ) -> str:
      folder = 'exhibits'

      if name.casefold() == ExhibitRegionColors.exhibit_region( name ).casefold():
         folder = 'regions'

      image = Paths.DETAIL_IMAGES / folder / AssetKeyNormalizer.file_name( name )
      return image.relative_to( Paths.ROOT ).as_posix()
