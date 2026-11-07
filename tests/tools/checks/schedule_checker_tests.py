from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from tools.checks.animal_list_checker import AnimalListChecker
from tools.checks.gift_shop_list_checker import GiftShopListChecker
from tools.checks.restaurant_list_checker import RestaurantListChecker
from tools.checks.schedule_checker import ScheduleChecker
from tools.checks.seasonal_animal_off_display_checker import SeasonalAnimalOffDisplayChecker
from tools.checks.seasonal_gift_shop_closure_checker import SeasonalGiftShopClosureChecker
from tools.checks.seasonal_restaurant_closure_checker import SeasonalRestaurantClosureChecker


TODAY = date( 2026, 11, 2 )


def Test_CheckAnimals_TestOffDisplayAndCatalog_ExpectOneCount(
      tmp_path: Path,
      monkeypatch: pytest.MonkeyPatch ) -> None:
   calls = []

   def check_off_display( database: Path, today: date ) -> int:
      calls.append( 'off display' )
      return 1

   def check_animal_catalog( database: Path, today: date ) -> int:
      calls.append( 'catalog' )
      return 7

   monkeypatch.setattr( SeasonalAnimalOffDisplayChecker, 'check_schedules', check_off_display )
   monkeypatch.setattr( AnimalListChecker, 'check_lists', check_animal_catalog )

   result = ScheduleChecker.check_animals( tmp_path / 'animals.db', TODAY )

   assert result == 8
   assert calls == [ 'off display', 'catalog' ]


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
      '2 for Encounters, 0 for Guardians Talks, 8 for Animals, 4 for Attractions, '
      '3 for Restaurants, 5 for Gift shops, 6 for Drinking fountains, '
      '8 for Attraction list, 11 for Zoo hours\n'
      '\n'
      '47 errors\n'
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
      '0 for Encounters, 0 for Guardians Talks, 0 for Animals, 0 for Attractions, '
      '0 for Restaurants, 0 for Gift shops, 0 for Drinking fountains, '
      '0 for Attraction list, 0 for Zoo hours\n'
      '\n'
      '0 errors\n'
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
   assert output.endswith( '\n1 error\n' )
