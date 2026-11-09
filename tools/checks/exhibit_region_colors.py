from __future__ import annotations

from functools import cache
import json
import re
import subprocess

from api.app_string_provider import AppStringProvider
from .paths import Paths
from .region_color import RegionColor
from .region_slug import RegionSlug


class ExhibitRegionColors():
   TOKEN_RE = re.compile(
      r'--color-region-(?P<slug>[a-z0-9-]+)-(?P<part>bg|text):\s*(?P<color>#[0-9A-Fa-f]{6})'
   )


   @classmethod
   def _load_slugs( cls ) -> list[ RegionSlug ]:
      result = subprocess.run(
         [
            'node',
            '--input-type=module',
            '--eval',
            (
               "import { RegionColors } from './scripts/shared/regionColors.js';"
               'process.stdout.write(JSON.stringify(RegionColors.REGION_COLOR_SLUGS));'
            ),
         ],
         cwd=Paths.ROOT,
         check=True,
         capture_output=True,
         text=True,
      )
      loaded = json.loads( result.stdout )
      return [
         RegionSlug( region=region, slug=slug )
         for region, slug in loaded.items()
      ]


   @classmethod
   @cache
   def _load_colors( cls ) -> list[ RegionColor ]:
      matches = list( cls.TOKEN_RE.finditer( Paths.REGION_TOKENS.read_text() ) )
      return [
         RegionColor(
            region=item.region,
            background=next(
               match.group( 'color' )
               for match in matches
               if match.group( 'slug' ) == item.slug and match.group( 'part' ) == 'bg'
            ),
            foreground=next(
               match.group( 'color' )
               for match in matches
               if match.group( 'slug' ) == item.slug and match.group( 'part' ) == 'text'
            ),
         )
         for item in cls._load_slugs()
      ]


   @classmethod
   def attraction_region( cls, name: str ) -> str:
      folded = name.casefold()
      return next(
         row[ 'region' ]
         for row in json.loads( Paths.ATTRACTION_DATA.read_text() )
         if row[ 'name' ].casefold() == folded
      )


   @classmethod
   def listed_region( cls, name: str ) -> str:
      folded = name.casefold()
      return next(
         row[ 'region' ]
         for path in ( Paths.ATTRACTION_DATA, Paths.EXHIBIT_DATA )
         for row in json.loads( path.read_text() )
         if row[ 'name' ].casefold() == folded
      )


   @classmethod
   def exhibit_region( cls, exhibit: str ) -> str:
      folded = exhibit.casefold()
      return next(
         row[ 'region' ]
         for row in json.loads( Paths.EXHIBIT_DATA.read_text() )
         if row[ 'name' ].casefold() == folded
      )


   @classmethod
   def region_colors( cls, region: str ) -> RegionColor:
      return next( item for item in cls._load_colors() if item.region == region )


   @classmethod
   def exhibit_colors( cls, exhibit: str ) -> RegionColor:
      return cls.region_colors( cls.exhibit_region( exhibit ) )


   @classmethod
   def place_region( cls, place: str ) -> str:
      folded = place.casefold()
      regions = [
         row[ 'region' ]
         for row in json.loads( Paths.EXHIBIT_DATA.read_text() )
         if row[ 'name' ].casefold() == folded
      ]
      regions.extend(
         item.region
         for item in cls._load_colors()
         if item.region.casefold() == folded
      )
      return next( iter( regions ) )


   @classmethod
   def place_colors( cls, place: str ) -> RegionColor:
      return cls.region_colors( cls.place_region( place ) )


   @classmethod
   def restaurant_label( cls, name: str ) -> str:
      folded = name.casefold()
      return next(
         (
            AppStringProvider.format(
               'format.middleDotPair',
               first=name,
               second=cls.place_region( row[ 'location' ] ),
            )
            for row in json.loads( Paths.RESTAURANT_DATA.read_text() )
            if row[ 'name' ].casefold() == folded
         ),
      )


   @classmethod
   def gift_shop_label( cls, name: str ) -> str:
      folded = name.casefold()
      return next(
         (
            AppStringProvider.format(
               'format.middleDotPair',
               first=name,
               second=cls.place_region( row[ 'location' ] ),
            )
            for row in json.loads( Paths.GIFT_SHOP_DATA.read_text() )
            if row[ 'name' ].casefold() == folded
         ),
      )
