from __future__ import annotations

from .runner import apply_seed_data


def main( db_path: str = 'animals.db' ) -> None:
   apply_seed_data( db_path )
   print( 'Database seed data applied successfully.' )


if __name__ == '__main__':
   main()
