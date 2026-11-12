from __future__ import annotations

from tools.checks.exhibit_detail_image import ExhibitDetailImage


def Test_Source_TestMayanTemple_ExpectExhibitIcon() -> None:
   assert ExhibitDetailImage.source( 'Americas Outdoor Mayan Temple Ruins' ) == (
      'images/details/exhibits/americas-outdoor-mayan-temple-ruins.png'
   )


def Test_Source_TestCanadianDomain_ExpectRegionIcon() -> None:
   assert ExhibitDetailImage.source( 'Canadian Domain' ) == (
      'images/details/regions/canadian-domain.png'
   )
