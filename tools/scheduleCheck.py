from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys

from tools.animalListCheck import check_lists as check_animal_catalog
from tools.attractionListCheck import check_lists as check_attraction_list
from tools.giftShopListCheck import check_lists as check_gift_shop_list
from tools.guardiansTalkScheduleCheck import check_schedules as check_talks
from tools.restaurantListCheck import check_lists as check_restaurant_list
from tools.seasonalAttractionClosureCheck import check_schedules as check_attractions
from tools.seasonalDrinkingFountainClosureCheck import check_schedules as check_drinking_fountains
from tools.seasonalGiftShopClosureCheck import check_schedules as check_gift_shops
from tools.seasonalOffDisplayCheck import check_schedules as check_off_display
from tools.seasonalRestaurantClosureCheck import check_schedules as check_restaurants
from tools.wildEncounterScheduleCheck import check_schedules as check_encounters
from tools.zooHoursCheck import check_lists as check_zoo_hours


ROOT = Path( __file__ ).resolve().parents[ 1 ]


def parse_args() -> argparse.Namespace:
   parser = argparse.ArgumentParser(
      description=(
         'Compare wild encounters, guardians talks, animals, attractions closed '
         'for the season, restaurants closed for the season, gift shops closed '
         'for the season, drinking fountains closed for the season, listed '
         'attractions, restaurants, and gift shops, and zoo hours with the '
         'Toronto Zoo website.'
      )
   )
   parser.add_argument(
      '--database',
      type=Path,
      default=ROOT / 'animals.db',
      help='Path to animals.db. The file is opened read-only.',
   )
   return parser.parse_args()


def check_animals( database: Path, today: date ) -> int:
   return (
      check_off_display( database, today )
      + check_animal_catalog( database, today )
   )


def run_checks(
      database: Path,
      today: date,
      encounter_check: Callable[ [ Path, date ], int ],
      talk_check: Callable[ [ Path, date ], int ],
      animal_check: Callable[ [ Path, date ], int ],
      attraction_check: Callable[ [ Path, date ], int ],
      restaurant_check: Callable[ [ Path, date ], int ],
      gift_shop_check: Callable[ [ Path, date ], int ],
      drinking_fountain_check: Callable[ [ Path, date ], int ],
      attraction_list_check: Callable[ [ Path, date ], int ],
      restaurant_list_check: Callable[ [ Path, date ], int ],
      gift_shop_list_check: Callable[ [ Path, date ], int ],
      zoo_hours_check: Callable[ [ Path, date ], int ] ) -> int:
   encounter_issues = encounter_check( database, today )
   talk_issues = talk_check( database, today )
   animal_issues = animal_check( database, today )
   attraction_issues = attraction_check( database, today )
   restaurant_issues = restaurant_check( database, today )
   gift_shop_issues = gift_shop_check( database, today )
   drinking_fountain_issues = drinking_fountain_check( database, today )
   attraction_list_issues = attraction_list_check( database, today )
   restaurant_list_issues = restaurant_list_check( database, today )
   gift_shop_list_issues = gift_shop_list_check( database, today )
   zoo_hours_issues = zoo_hours_check( database, today )
   issues = (
      encounter_issues
      + talk_issues
      + animal_issues
      + attraction_issues
      + restaurant_issues
      + gift_shop_issues
      + drinking_fountain_issues
      + attraction_list_issues
      + restaurant_list_issues
      + gift_shop_list_issues
      + zoo_hours_issues
   )
   print(
      f'{ encounter_issues } for encounters, '
      f'{ talk_issues } for Guardians Talks, '
      f'{ animal_issues } for animals, '
      f'{ attraction_issues } for attractions, '
      f'{ restaurant_issues } for restaurants, '
      f'{ gift_shop_issues } for gift shops, '
      f'{ drinking_fountain_issues } for drinking fountains, '
      f'{ attraction_list_issues } for the attraction list, '
      f'{ restaurant_list_issues } for the restaurant list, '
      f'{ gift_shop_list_issues } for the gift shop list, '
      f'{ zoo_hours_issues } for zoo hours'
   )
   print()
   print( f'{ issues } error' if issues == 1 else f'{ issues } errors' )

   if issues:
      return 1

   return 0


def main() -> int:
   args = parse_args()

   if not args.database.exists():
      print( f'Could not find { args.database }.', file=sys.stderr )
      return 2

   try:
      return run_checks(
         args.database,
         date.today(),
         check_encounters,
         check_talks,
         check_animals,
         check_attractions,
         check_restaurants,
         check_gift_shops,
         check_drinking_fountains,
         check_attraction_list,
         check_restaurant_list,
         check_gift_shop_list,
         check_zoo_hours,
      )
   except RuntimeError as error:
      print( error, file=sys.stderr )
      return 2


if __name__ == '__main__':
   raise SystemExit( main() )
