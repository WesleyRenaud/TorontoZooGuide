from __future__ import annotations

import runpy

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

def Test_ModuleMain_TestAppliesSeedData_ExpectDelegatesToSeedRunner(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []

   def apply_seed_data( db_path: str ) -> None:
      calls.append( db_path )

   monkeypatch.setattr( 'api.seed.seed_data_applier.SeedRunner.apply_seed_data', apply_seed_data )

   runpy.run_module( 'api.seed.seed_data_applier', run_name='__main__' )

   assert calls == [ 'animals.db' ]
   assert 'Database seed data applied successfully.' in capsys.readouterr().out
