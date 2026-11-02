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

   result = run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
   )
   output = capsys.readouterr().out

   assert result == 1
   assert output.index( 'encounters\n' ) < output.index( 'talks\n' )
   assert output.index( 'talks\n' ) < output.index( 'animals\n' )
   assert output.endswith( '2 for encounters, 0 for talks, 1 for animals\n' )


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

   result = run_checks(
      database,
      TODAY,
      check_encounters,
      check_talks,
      check_animals,
   )
   output = capsys.readouterr().out

   assert result == 0
   assert output == '0 for encounters, 0 for talks, 0 for animals\n'
