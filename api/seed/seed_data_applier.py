from __future__ import annotations

from .seed_runner import SeedRunner


class SeedDataApplier():
   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      SeedRunner.apply_seed_data( db_path )
      print( 'Database seed data applied successfully.' )


if __name__ == '__main__':
   SeedDataApplier.main()
