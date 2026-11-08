from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from tools.checks.app_catalogue_not_on_website_checker import AppCatalogueNotOnWebsiteChecker
from tools.checks.check_report_parser import CheckReportParser
from tools.checks.closure_off_display_extension_checker import ClosureOffDisplayExtensionChecker
from tools.checks.gift_shop_list_checker import GiftShopListChecker
from tools.checks.off_for_season_in_app_not_on_website_checker import OffForSeasonInAppNotOnWebsiteChecker
from tools.checks.off_for_season_on_website_not_in_app_checker import OffForSeasonOnWebsiteNotInAppChecker
from tools.checks.restaurant_list_checker import RestaurantListChecker
from tools.checks.schedule_checker import ScheduleChecker
from tools.checks.seasonal_gift_shop_closure_checker import SeasonalGiftShopClosureChecker
from tools.checks.seasonal_restaurant_closure_checker import SeasonalRestaurantClosureChecker
from tools.checks.temporary_off_display_in_app_not_on_website_checker import TemporaryOffDisplayInAppNotOnWebsiteChecker
from tools.checks.temporary_off_display_on_website_not_in_app_checker import TemporaryOffDisplayOnWebsiteNotInAppChecker
from tools.checks.website_catalogue_not_in_app_checker import WebsiteCatalogueNotInAppChecker


TODAY = date( 2026, 11, 2 )


def Test_CheckAnimals_TestBothOffDisplayCasesAndCatalog_ExpectOneCount(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = []

   def check_website( database: Path, today: date ) -> list[ str ]:
      calls.append( 'website off for season' )
      return [ 'website' ]

   def check_app( database: Path, today: date ) -> list[ str ]:
      calls.append( 'app off for season' )
      return [ 'app', 'app' ]

   def check_closure( database: Path, today: date ) -> int:
      calls.append( 'closure off display' )
      return 0

   def check_temporary( database: Path, today: date ) -> int:
      calls.append( 'temporary off display' )
      return 0

   def check_temporary_app( database: Path, today: date ) -> int:
      calls.append( 'temporary off display app' )
      return 0

   def check_website_catalogue( database: Path, today: date ) -> int:
      calls.append( 'website catalogue' )
      return 4

   def check_app_catalogue( database: Path, today: date ) -> int:
      calls.append( 'app catalogue' )
      return 3

   monkeypatch.setattr(
      OffForSeasonOnWebsiteNotInAppChecker,
      'category_lines',
      check_website,
   )
   monkeypatch.setattr( OffForSeasonInAppNotOnWebsiteChecker, 'category_lines', check_app )
   monkeypatch.setattr(
      ClosureOffDisplayExtensionChecker,
      'check_schedules',
      check_closure,
   )
   monkeypatch.setattr(
      TemporaryOffDisplayOnWebsiteNotInAppChecker,
      'check_schedules',
      check_temporary,
   )
   monkeypatch.setattr(
      TemporaryOffDisplayInAppNotOnWebsiteChecker,
      'check_schedules',
      check_temporary_app,
   )
   monkeypatch.setattr(
      WebsiteCatalogueNotInAppChecker,
      'check_lists',
      check_website_catalogue,
   )
   monkeypatch.setattr(
      AppCatalogueNotOnWebsiteChecker,
      'check_lists',
      check_app_catalogue,
   )

   result = ScheduleChecker.check_animals( tmp_path / 'animals.db', TODAY )

   assert result == 10
   assert calls == [
      'website off for season',
      'app off for season',
      'closure off display',
      'temporary off display',
      'temporary off display app',
      'website catalogue',
      'app catalogue',
   ]


def Test_CheckRestaurants_TestClosureAndCatalog_ExpectOneCount(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = []

   def check_closure( database: Path, today: date ) -> int:
      calls.append( 'closure' )
      return 1

   def check_catalog( database: Path, today: date ) -> int:
      calls.append( 'catalog' )
      return 4

   monkeypatch.setattr( SeasonalRestaurantClosureChecker, 'check_schedules', check_closure )
   monkeypatch.setattr( RestaurantListChecker, 'check_lists', check_catalog )

   result = ScheduleChecker.check_restaurants( tmp_path / 'animals.db', TODAY )

   assert result == 5
   assert calls == [ 'closure', 'catalog' ]


def Test_CheckGiftShops_TestClosureAndCatalog_ExpectOneCount(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = []

   def check_closure( database: Path, today: date ) -> int:
      calls.append( 'closure' )
      return 2

   def check_catalog( database: Path, today: date ) -> int:
      calls.append( 'catalog' )
      return 6

   monkeypatch.setattr( SeasonalGiftShopClosureChecker, 'check_schedules', check_closure )
   monkeypatch.setattr( GiftShopListChecker, 'check_lists', check_catalog )

   result = ScheduleChecker.check_gift_shops( tmp_path / 'animals.db', TODAY )

   assert result == 8
   assert calls == [ 'closure', 'catalog' ]


def Test_RunChecks_TestIssueCounts_ExpectSummary(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'

   def check_encounters( checked_database: Path, today: date ) -> int:
      print( 'encounters' )
      return 2

   def check_talks( checked_database: Path, today: date ) -> int:
      print( 'talks' )
      return 0

   def check_animals( checked_database: Path, today: date ) -> int:
      print( 'animals' )
      return 8

   def check_attractions( checked_database: Path, today: date ) -> int:
      print( 'attractions' )
      return 4

   def check_restaurants( checked_database: Path, today: date ) -> int:
      print( 'restaurants' )
      return 3

   def check_gift_shops( checked_database: Path, today: date ) -> int:
      print( 'gift shops' )
      return 5

   def check_drinking_fountains( checked_database: Path, today: date ) -> int:
      print( 'drinking fountains' )
      return 6

   def check_attraction_list( checked_database: Path, today: date ) -> int:
      print( 'attraction list' )
      return 8

   def check_zoo_hours( checked_database: Path, today: date ) -> int:
      print( 'zoo hours' )
      return 11

   result = ScheduleChecker.run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
      check_attractions,
      check_restaurants,
      check_gift_shops,
      check_drinking_fountains,
      check_attraction_list,
      check_zoo_hours,
   )
   output = capsys.readouterr().out

   assert result == 1
   assert output.index( 'encounters\n' ) < output.index( 'talks\n' )
   assert output.index( 'talks\n' ) < output.index( 'animals\n' )
   assert output.index( 'animals\n' ) < output.index( 'attractions\n' )
   assert output.index( 'attractions\n' ) < output.index( 'restaurants\n' )
   assert output.index( 'restaurants\n' ) < output.index( 'gift shops\n' )
   assert output.index( 'gift shops\n' ) < output.index( 'drinking fountains\n' )
   assert output.index( 'drinking fountains\n' ) < output.index( 'attraction list\n' )
   assert output.index( 'attraction list\n' ) < output.index( 'zoo hours\n' )
   assert output.endswith(
      CheckReportParser.format_fixed_count( 0 ) + '\n'
      '\n'
      + CheckReportParser.format_counts(
         encounters=2,
         animals=8,
         attractions=4,
         restaurants=3,
         gift_shops=5,
         drinking_fountains=6,
         attraction_list=8,
         zoo_hours=11,
      )
      + '\n'
      '\n'
      + CheckReportParser.format_error_count( 47 )
      + '\n'
   )


def Test_RunChecks_TestNoIssues_ExpectSuccess(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'

   def check_encounters( checked_database: Path, today: date ) -> int:
      return 0

   def check_talks( checked_database: Path, today: date ) -> int:
      return 0

   def check_animals( checked_database: Path, today: date ) -> int:
      return 0

   def check_attractions( checked_database: Path, today: date ) -> int:
      return 0

   def check_restaurants( checked_database: Path, today: date ) -> int:
      return 0

   def check_gift_shops( checked_database: Path, today: date ) -> int:
      return 0

   def check_drinking_fountains( checked_database: Path, today: date ) -> int:
      return 0

   def check_attraction_list( checked_database: Path, today: date ) -> int:
      return 0

   def check_zoo_hours( checked_database: Path, today: date ) -> int:
      return 0

   result = ScheduleChecker.run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
      check_attractions,
      check_restaurants,
      check_gift_shops,
      check_drinking_fountains,
      check_attraction_list,
      check_zoo_hours,
   )
   output = capsys.readouterr().out

   assert result == 0
   assert output == (
      CheckReportParser.format_fixed_count( 0 ) + '\n'
      '\n'
      + CheckReportParser.format_counts()
      + '\n'
      '\n'
      + CheckReportParser.format_error_count( 0 )
      + '\n'
   )


def Test_RunChecks_TestOneIssue_ExpectSingularError(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'

   def check_encounters( checked_database: Path, today: date ) -> int:
      return 1

   def check_talks( checked_database: Path, today: date ) -> int:
      return 0

   def check_animals( checked_database: Path, today: date ) -> int:
      return 0

   def check_attractions( checked_database: Path, today: date ) -> int:
      return 0

   def check_restaurants( checked_database: Path, today: date ) -> int:
      return 0

   def check_gift_shops( checked_database: Path, today: date ) -> int:
      return 0

   def check_drinking_fountains( checked_database: Path, today: date ) -> int:
      return 0

   def check_attraction_list( checked_database: Path, today: date ) -> int:
      return 0

   def check_zoo_hours( checked_database: Path, today: date ) -> int:
      return 0

   result = ScheduleChecker.run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
      check_attractions,
      check_restaurants,
      check_gift_shops,
      check_drinking_fountains,
      check_attraction_list,
      check_zoo_hours,
   )
   output = capsys.readouterr().out

   assert result == 1
   assert output.endswith( '\n' + CheckReportParser.format_error_count( 1 ) + '\n' )
