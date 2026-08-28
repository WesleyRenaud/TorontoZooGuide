from __future__ import annotations

from .seed_runner import SeedRunner


class SchemaApplier():
   @classmethod
   def main( cls, db_path: str = 'animals.db' ) -> None:
      SeedRunner.apply_schema( db_path )
      print( 'Database schema applied successfully.' )


if __name__ == '__main__':
   SchemaApplier.main()
