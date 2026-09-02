from __future__ import annotations

import pytest

from api.seed.schema_applier import SchemaApplier
from api.seed.seed_runner import SeedRunner


DB_PATH = 'test-animals.db'


def Test_Main_TestAppliesSchema_ExpectDelegatesToSeedRunner(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []

   def apply_schema( db_path: str ) -> None:
      calls.append( db_path )

   monkeypatch.setattr( SeedRunner, 'apply_schema', apply_schema )

   SchemaApplier.main( DB_PATH )

   assert calls == [ DB_PATH ]
   assert 'Database schema applied successfully.' in capsys.readouterr().out
