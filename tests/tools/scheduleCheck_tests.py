from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from tools.scheduleCheck import run_checks


TODAY = date( 2026, 11, 2 )


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
      return 1

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

   def check_animal_list( checked_database: Path, today: date ) -> int:
      print( 'animal list' )
      return 7

   def check_attraction_list( checked_database: Path, today: date ) -> int:
      print( 'attraction list' )
      return 8

   def check_restaurant_list( checked_database: Path, today: date ) -> int:
      print( 'restaurant list' )
      return 9

   result = run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
      check_attractions,
      check_restaurants,
      check_gift_shops,
      check_drinking_fountains,
      check_animal_list,
      check_attraction_list,
      check_restaurant_list,
   )
   output = capsys.readouterr().out

   assert result == 1
   assert output.index( 'encounters\n' ) < output.index( 'talks\n' )
   assert output.index( 'talks\n' ) < output.index( 'animals\n' )
   assert output.index( 'animals\n' ) < output.index( 'attractions\n' )
   assert output.index( 'attractions\n' ) < output.index( 'restaurants\n' )
   assert output.index( 'restaurants\n' ) < output.index( 'gift shops\n' )
   assert output.index( 'gift shops\n' ) < output.index( 'drinking fountains\n' )
   assert output.index( 'drinking fountains\n' ) < output.index( 'animal list\n' )
   assert output.index( 'animal list\n' ) < output.index( 'attraction list\n' )
   assert output.index( 'attraction list\n' ) < output.index( 'restaurant list\n' )
   assert output.endswith(
      '2 for encounters, 0 for talks, 1 for animals, 4 for attractions, '
      '3 for restaurants, 5 for gift shops, 6 for drinking fountains, '
      '7 for the animal list, 8 for the attraction list, 9 for the restaurant list\n'
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

   def check_animal_list( checked_database: Path, today: date ) -> int:
      return 0

   def check_attraction_list( checked_database: Path, today: date ) -> int:
      return 0

   def check_restaurant_list( checked_database: Path, today: date ) -> int:
      return 0

   result = run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
      check_attractions,
      check_restaurants,
      check_gift_shops,
      check_drinking_fountains,
      check_animal_list,
      check_attraction_list,
      check_restaurant_list,
   )
   output = capsys.readouterr().out

   assert result == 0
   assert output == (
      '0 for encounters, 0 for talks, 0 for animals, 0 for attractions, '
      '0 for restaurants, 0 for gift shops, 0 for drinking fountains, '
      '0 for the animal list, 0 for the attraction list, 0 for the restaurant list\n'
   )
