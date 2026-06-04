from __future__ import annotations

from .runner import apply_schema


def main( db_path: str = 'animals.db' ) -> None:
   apply_schema( db_path )
   print( 'Database schema applied successfully.' )


if __name__ == '__main__':
   main()
