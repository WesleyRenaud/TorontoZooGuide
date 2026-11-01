from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from tools.scheduleCheck import run_checks


TODAY = date( 2026, 11, 1 )


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

   result = run_checks( database, TODAY, check_encounters, check_talks )
   output = capsys.readouterr().out

   assert result == 1
   assert output.index( 'encounters\n' ) < output.index( 'talks\n' )
   assert output.endswith( '2 for encounters, 0 for talks\n' )


def Test_RunChecks_TestNoIssues_ExpectSuccess(
      tmp_path: Path,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   database = tmp_path / 'animals.db'

   def check_encounters( checked_database: Path, today: date ) -> int:
      return 0

   def check_talks( checked_database: Path, today: date ) -> int:
      return 0

   result = run_checks( database, TODAY, check_encounters, check_talks )
   output = capsys.readouterr().out

   assert result == 0
   assert output == '0 for encounters, 0 for talks\n'
