from __future__ import annotations

import pytest

from api.seed.seed_data_applier import SeedDataApplier
from api.seed.seed_runner import SeedRunner


DB_PATH = 'test-animals.db'


def Test_Main_TestAppliesSeedData_ExpectDelegatesToSeedRunner(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []

   def apply_seed_data( db_path: str ) -> None:
      calls.append( db_path )

   monkeypatch.setattr( SeedRunner, 'apply_seed_data', apply_seed_data )

   SeedDataApplier.main( DB_PATH )

   assert calls == [ DB_PATH ]
   assert 'Database seed data applied successfully.' in capsys.readouterr().out
