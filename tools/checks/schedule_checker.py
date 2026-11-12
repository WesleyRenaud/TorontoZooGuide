from __future__ import annotations

import argparse
from collections.abc import Callable
from datetime import date
from pathlib import Path
import sys

from .animal_app_catalogue_not_on_website_checker import AnimalAppCatalogueNotOnWebsiteChecker
from .animal_closure_off_display_extension_checker import AnimalClosureOffDisplayExtensionChecker
from .animal_off_for_season_in_app_not_on_website_checker import AnimalOffForSeasonInAppNotOnWebsiteChecker
from .animal_off_for_season_ramp_down_on_website_not_in_app_checker import AnimalOffForSeasonRampDownOnWebsiteNotInAppChecker
from .animal_temporary_off_display_in_app_not_on_website_checker import AnimalTemporaryOffDisplayInAppNotOnWebsiteChecker
from .animal_temporary_off_display_on_website_not_in_app_checker import AnimalTemporaryOffDisplayOnWebsiteNotInAppChecker
from .animal_website_catalogue_not_in_app_checker import AnimalWebsiteCatalogueNotInAppChecker
from api.app_string_provider import AppStringProvider
from api.shared.date_values import DateValues
from .attraction_list_checker import AttractionListChecker
from .attraction_window_checker import AttractionWindowChecker
from .check_args_parser import CheckArgsParser
from .check_exit_code import CheckExitCode
from .check_report import CheckReport
from .check_report_parser import CheckReportParser
from .closure_update_checker import ClosureUpdateChecker
from .exhibit_season_checker import ExhibitSeasonChecker
from .gift_shop_list_checker import GiftShopListChecker
from .gift_shop_window_checker import GiftShopWindowChecker
from .guardians_talk_schedule_checker import GuardiansTalkScheduleChecker
from .restaurant_list_checker import RestaurantListChecker
from .restaurant_window_checker import RestaurantWindowChecker
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
         AnimalOffForSeasonRampDownOnWebsiteNotInAppChecker.check_schedules( database, today )
         + AnimalOffForSeasonInAppNotOnWebsiteChecker.check_schedules( database, today )
         + AnimalClosureOffDisplayExtensionChecker.check_schedules( database, today )
         + AnimalTemporaryOffDisplayOnWebsiteNotInAppChecker.check_schedules( database, today )
         + AnimalTemporaryOffDisplayInAppNotOnWebsiteChecker.check_schedules( database, today )
         + AnimalWebsiteCatalogueNotInAppChecker.check_lists( database, today )
         + AnimalAppCatalogueNotOnWebsiteChecker.check_lists( database, today )
         + ClosureUpdateChecker.check_schedules( database, today )
      )


   @classmethod
   def check_attractions( cls, database: Path, today: date ) -> int:
      return (
         SeasonalAttractionClosureChecker.check_schedules( database, today )
         + AttractionWindowChecker.check_schedules( database, today )
      )


   @classmethod
   def check_restaurants( cls, database: Path, today: date ) -> int:
      return (
         SeasonalRestaurantClosureChecker.check_schedules( database, today )
         + RestaurantListChecker.check_lists( database, today )
         + RestaurantWindowChecker.check_schedules( database, today )
      )


   @classmethod
   def check_gift_shops( cls, database: Path, today: date ) -> int:
      return (
         SeasonalGiftShopClosureChecker.check_schedules( database, today )
         + GiftShopListChecker.check_lists( database, today )
         + GiftShopWindowChecker.check_schedules( database, today )
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
         zoo_hours_check: Callable[ [ Path, date ], int ],
         exhibit_check: Callable[ [ Path, date ], int ] ) -> int:
      CheckReport.reset_fixed_count()
      exhibit_issues = exhibit_check( database, today )
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
         exhibit_issues
         + encounter_issues
         + talk_issues
         + animal_issues
         + attraction_issues
         + restaurant_issues
         + gift_shop_issues
         + drinking_fountain_issues
         + attraction_list_issues
         + zoo_hours_issues
      )
      print( CheckReportParser.format_fixed_count( CheckReport.fixed_count ) )
      print()
      print( CheckReportParser.format_counts(
         exhibits=exhibit_issues,
         encounters=encounter_issues,
         talks=talk_issues,
         animals=animal_issues,
         attractions=attraction_issues,
         restaurants=restaurant_issues,
         gift_shops=gift_shop_issues,
         drinking_fountains=drinking_fountain_issues,
         attraction_list=attraction_list_issues,
         zoo_hours=zoo_hours_issues,
      ) )
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
            AppStringProvider.format( 'checks.couldNotFindDatabase' ),
            file=sys.stderr,
         )
         return CheckExitCode.COULD_NOT_FINISH

      try:
         return cls.run_checks(
            args.database,
            DateValues.today(),
            WildEncounterScheduleChecker.check_schedules,
            GuardiansTalkScheduleChecker.check_schedules,
            cls.check_animals,
            cls.check_attractions,
            cls.check_restaurants,
            cls.check_gift_shops,
            SeasonalDrinkingFountainClosureChecker.check_schedules,
            AttractionListChecker.check_lists,
            ZooHoursChecker.check_lists,
            ExhibitSeasonChecker.check_schedules,
         )
      except RuntimeError as error:
         print( error, file=sys.stderr )
         return CheckExitCode.COULD_NOT_FINISH


if __name__ == '__main__':
   raise SystemExit( ScheduleChecker.main() )
