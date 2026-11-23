from __future__ import annotations

import subprocess

import pytest

from api.app_string_provider import AppStringProvider
from tools.animals_database_syncer import AnimalsDatabaseSyncer


def _result(
      returncode: int = 0,
      stdout: str = '',
      stderr: str = '' ) -> subprocess.CompletedProcess[ str ]:
   return subprocess.CompletedProcess(
      args=[],
      returncode=returncode,
      stdout=stdout,
      stderr=stderr,
   )


def Test_Sync_TestNotOnMain_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'current_branch',
      classmethod( lambda cls: 'feature' ),
   )

   assert AnimalsDatabaseSyncer.sync() == 0
   assert AppStringProvider.format(
      'checks.animalsDatabaseSyncer.skipWrongBranch',
      branch='feature',
      expected='main',
   ) in capsys.readouterr().out


def Test_Sync_TestDirtyDatabase_ExpectSkipped(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'current_branch',
      classmethod( lambda cls: 'main' ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'animals_db_is_dirty',
      classmethod( lambda cls: True ),
   )

   assert AnimalsDatabaseSyncer.sync() == 0
   assert AppStringProvider.format(
      'checks.animalsDatabaseSyncer.skipDirtyDatabase',
      database='animals.db',
   ) in capsys.readouterr().out


def Test_Sync_TestAlreadyMatches_ExpectNoPull(
      monkeypatch: pytest.MonkeyPatch,
      capsys: pytest.CaptureFixture[ str ] ) -> None:
   calls: list[ str ] = []

   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'current_branch',
      classmethod( lambda cls: 'main' ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'animals_db_is_dirty',
      classmethod( lambda cls: False ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'fetch_main',
      classmethod( lambda cls: True ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'matches_remote_database',
      classmethod( lambda cls: True ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'pull_main',
      classmethod( lambda cls: calls.append( 'pull' ) or True ),
   )

   assert AnimalsDatabaseSyncer.sync() == 0
   assert calls == []
   assert AppStringProvider.format(
      'checks.animalsDatabaseSyncer.alreadyMatches',
      remote='origin',
      branch='main',
   ) in capsys.readouterr().out


def Test_Sync_TestCleanTreeBehind_ExpectPull(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def fail_restore( cls: type[ AnimalsDatabaseSyncer ] ) -> bool:
      raise AssertionError( 'restore' )

   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'current_branch',
      classmethod( lambda cls: 'main' ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'animals_db_is_dirty',
      classmethod( lambda cls: False ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'fetch_main',
      classmethod( lambda cls: True ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'matches_remote_database',
      classmethod( lambda cls: False ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'is_fully_clean',
      classmethod( lambda cls: True ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'pull_main',
      classmethod( lambda cls: True ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'restore_database',
      classmethod( fail_restore ),
   )

   assert AnimalsDatabaseSyncer.sync() == 0


def Test_Sync_TestDirtyTreeBehind_ExpectRestore(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   restored = { 'value': False }

   def restore( cls: type[ AnimalsDatabaseSyncer ] ) -> bool:
      restored[ 'value' ] = True
      return True

   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'current_branch',
      classmethod( lambda cls: 'main' ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'animals_db_is_dirty',
      classmethod( lambda cls: False ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'fetch_main',
      classmethod( lambda cls: True ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'matches_remote_database',
      classmethod( lambda cls: False ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'is_fully_clean',
      classmethod( lambda cls: False ),
   )
   monkeypatch.setattr(
      AnimalsDatabaseSyncer,
      'restore_database',
      classmethod( restore ),
   )

   assert AnimalsDatabaseSyncer.sync() == 0
   assert restored[ 'value' ] is True


def Test_AnimalsDbIsDirty_TestWorktreeDirty_ExpectTrue(
      monkeypatch: pytest.MonkeyPatch ) -> None:
   def run_git(
         cls: type[ AnimalsDatabaseSyncer ],
         arguments: list[ str ],
         check: bool = True ) -> subprocess.CompletedProcess[ str ]:
      if arguments[ :2 ] == [ 'diff', '--quiet' ] and '--cached' not in arguments:
         return _result( 1 )

      return _result( 0 )

   monkeypatch.setattr( AnimalsDatabaseSyncer, 'run_git', classmethod( run_git ) )
   assert AnimalsDatabaseSyncer.animals_db_is_dirty() is True
