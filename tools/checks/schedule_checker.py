from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys

from .animal_list_checker import AnimalListChecker
from api.app_string_provider import AppStringProvider
from .attraction_list_checker import AttractionListChecker
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report_parser import CheckReportParser
from .gift_shop_list_checker import GiftShopListChecker
from .guardians_talk_schedule_checker import GuardiansTalkScheduleChecker
from .restaurant_list_checker import RestaurantListChecker
from .seasonal_animal_off_display_checker import SeasonalAnimalOffDisplayChecker
from .seasonal_attraction_closure_checker import SeasonalAttractionClosureChecker
from .seasonal_drinking_fountain_closure_checker import SeasonalDrinkingFountainClosureChecker
from .seasonal_gift_shop_closure_checker import SeasonalGiftShopClosureChecker
from .seasonal_restaurant_closure_checker import SeasonalRestaurantClosureChecker
from .wild_encounter_schedule_checker import WildEncounterScheduleChecker
from .zoo_hours_checker import ZooHoursChecker


class ScheduleChecker():
   @classmethod
   def parse_args( cls ) -> argparse.Namespace:
      return CheckArgsParser.parse( AppStringProvider.format( 'reports.schedule.description' ) )


   @classmethod
   def check_animals( cls, database: Path, today: date ) -> int:
      return (
         SeasonalAnimalOffDisplayChecker.check_schedules( database, today )
         + AnimalListChecker.check_lists( database, today )
      )


   @classmethod
   def check_restaurants( cls, database: Path, today: date ) -> int:
      return (
         SeasonalRestaurantClosureChecker.check_schedules( database, today )
         + RestaurantListChecker.check_lists( database, today )
      )


   @classmethod
   def check_gift_shops( cls, database: Path, today: date ) -> int:
      return (
         SeasonalGiftShopClosureChecker.check_schedules( database, today )
         + GiftShopListChecker.check_lists( database, today )
      )


   @classmethod
   def run_checks(
         cls,
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
         zoo_hours_check: Callable[ [ Path, date ], int ] ) -> int:
      encounter_issues = encounter_check( database, today )
      talk_issues = talk_check( database, today )
      animal_issues = animal_check( database, today )
      attraction_issues = attraction_check( database, today )
      restaurant_issues = restaurant_check( database, today )
      gift_shop_issues = gift_shop_check( database, today )
      drinking_fountain_issues = drinking_fountain_check( database, today )
      attraction_list_issues = attraction_list_check( database, today )
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
         + zoo_hours_issues
      )
      print( CheckReportParser.format_counts( [
         encounter_issues,
         talk_issues,
         animal_issues,
         attraction_issues,
         restaurant_issues,
         gift_shop_issues,
         drinking_fountain_issues,
         attraction_list_issues,
         zoo_hours_issues,
      ] ) )
      print()
      print( CheckReportParser.format_error_count( issues ) )

      if issues:
         return CheckExitCode.DIFFERENCES

      return CheckExitCode.CLEAR


   @classmethod
   def main( cls ) -> int:
      args = cls.parse_args()

      if not args.database.exists():
         print(
            AppStringProvider.format(
               'checks.couldNotFindDatabase',
               database=args.database,
            ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         return cls.run_checks(
            args.database,
            date.today(),
            WildEncounterScheduleChecker.check_schedules,
            GuardiansTalkScheduleChecker.check_schedules,
            cls.check_animals,
            SeasonalAttractionClosureChecker.check_schedules,
            cls.check_restaurants,
            cls.check_gift_shops,
            SeasonalDrinkingFountainClosureChecker.check_schedules,
            AttractionListChecker.check_lists,
            ZooHoursChecker.check_lists,
         )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH


if __name__ == '__main__':
   raise SystemExit( ScheduleChecker.main() )
