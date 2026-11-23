from __future__ import annotations

import subprocess
import sys

from api.app_string_provider import AppStringProvider
from tools.checks.paths import Paths


class AnimalsDatabaseSyncer():
   BRANCH = 'main'
   REMOTE = 'origin'
   DATABASE = 'animals.db'


   @classmethod
   def message( cls, key: str, **params: str ) -> str:
      return AppStringProvider.format( f'checks.animalsDatabaseSyncer.{ key }', **params )


   @classmethod
   def detail( cls, text: str ) -> str:
      stripped = text.strip()

      if stripped == '':
         return ''

      return AppStringProvider.format( 'checks.labelValue' ) + stripped


   @classmethod
   def run_git(
         cls,
         arguments: list[ str ],
         check: bool = True ) -> subprocess.CompletedProcess[ str ]:
      return subprocess.run(
         [ 'git', *arguments ],
         cwd=Paths.ROOT,
         capture_output=True,
         text=True,
         check=check,
      )


   @classmethod
   def current_branch( cls ) -> str | None:
      result = cls.run_git( [ 'branch', '--show-current' ], check=False )

      if result.returncode != 0:
         return None

      branch = result.stdout.strip()
      return branch or None


   @classmethod
   def animals_db_is_dirty( cls ) -> bool:
      worktree = cls.run_git(
         [ 'diff', '--quiet', '--', cls.DATABASE ],
         check=False,
      )
      staged = cls.run_git(
         [ 'diff', '--cached', '--quiet', '--', cls.DATABASE ],
         check=False,
      )
      return worktree.returncode != 0 or staged.returncode != 0


   @classmethod
   def is_fully_clean( cls ) -> bool:
      result = cls.run_git( [ 'status', '--porcelain' ], check=False )
      return result.returncode == 0 and result.stdout.strip() == ''


   @classmethod
   def matches_remote_database( cls ) -> bool:
      result = cls.run_git(
         [ 'diff', '--quiet', f'{ cls.REMOTE }/{ cls.BRANCH }', '--', cls.DATABASE ],
         check=False,
      )
      return result.returncode == 0


   @classmethod
   def fetch_main( cls ) -> bool:
      result = cls.run_git(
         [ 'fetch', cls.REMOTE, cls.BRANCH ],
         check=False,
      )

      if result.returncode != 0:
         message = ( result.stderr or result.stdout ).strip()
         print(
            cls.message(
               'skipCouldNotFetch',
               remote=cls.REMOTE,
               branch=cls.BRANCH,
               detail=cls.detail( message ),
            ),
            file=sys.stderr,
         )
         return False

      return True


   @classmethod
   def pull_main( cls ) -> bool:
      result = cls.run_git(
         [ 'pull', '--ff-only', cls.REMOTE, cls.BRANCH ],
         check=False,
      )

      if result.returncode != 0:
         return False

      print(
         cls.message(
            'pulledLatest',
            branch=cls.BRANCH,
            database=cls.DATABASE,
         )
      )
      return True


   @classmethod
   def restore_database( cls ) -> bool:
      result = cls.run_git(
         [
            'restore',
            f'--source={ cls.REMOTE }/{ cls.BRANCH }',
            '--worktree',
            '--',
            cls.DATABASE,
         ],
         check=False,
      )

      if result.returncode != 0:
         message = ( result.stderr or result.stdout ).strip()
         print(
            cls.message(
               'skipCouldNotRestore',
               database=cls.DATABASE,
               detail=cls.detail( message ),
            ),
            file=sys.stderr,
         )
         return False

      print(
         cls.message(
            'updatedDatabase',
            database=cls.DATABASE,
            remote=cls.REMOTE,
            branch=cls.BRANCH,
         )
      )
      return True


   @classmethod
   def sync( cls ) -> int:
      branch = cls.current_branch()

      if branch is None:
         print( cls.message( 'skipNotGitRepository' ) )
         return 0

      if branch != cls.BRANCH:
         print(
            cls.message(
               'skipWrongBranch',
               branch=branch,
               expected=cls.BRANCH,
            )
         )
         return 0

      if cls.animals_db_is_dirty():
         print(
            cls.message(
               'skipDirtyDatabase',
               database=cls.DATABASE,
            )
         )
         return 0

      if not cls.fetch_main():
         return 0

      if cls.matches_remote_database():
         print(
            cls.message(
               'alreadyMatches',
               remote=cls.REMOTE,
               branch=cls.BRANCH,
            )
         )
         return 0

      if cls.is_fully_clean() and cls.pull_main():
         return 0

      cls.restore_database()
      return 0


   @classmethod
   def main( cls ) -> int:
      try:
         return cls.sync()
      except OSError as error:
         print(
            cls.message( 'skipError', error=str( error ) ),
            file=sys.stderr,
         )
         return 0


if __name__ == '__main__':
   raise SystemExit( AnimalsDatabaseSyncer.main() )
