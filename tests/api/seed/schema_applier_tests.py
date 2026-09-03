from __future__ import annotations

import runpy

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

def Test_ModuleMain_TestAppliesSchema_ExpectDelegatesToSeedRunner(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []

   def apply_schema( db_path: str ) -> None:
      calls.append( db_path )

   monkeypatch.setattr( 'api.seed.schema_applier.SeedRunner.apply_schema', apply_schema )

   runpy.run_module( 'api.seed.schema_applier', run_name='__main__' )

   assert calls == [ 'animals.db' ]
   assert 'Database schema applied successfully.' in capsys.readouterr().out
