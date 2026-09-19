from __future__ import annotations

from .animal_off_display_status_resolver import AnimalOffDisplayStatusResolver
from ..domain.animal_viewing_scope import AnimalViewingScope
from ...types import Types


class AnimalStatusProvider():
   @classmethod
   def _insert_animal_off_display_status(
         cls,
         cur: Types.Cursor,
         species: str,
         exhibit: str,
         viewing_scope: AnimalViewingScope,
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> None:
      cur.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  VIEWING_SCOPE,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE
               )
               VALUES (?, ?, ?, 1, ?, ?, ?);
         """,
         (
            species,
            exhibit,
            viewing_scope.enclosure_name,
            start_date,
            end_date,
            message,
         ) )


   @classmethod
   def save_animal_off_display_status(
         cls,
         conn: Types.Connection,
         species: str,
         exhibit: str,
         viewing_scopes: list[ AnimalViewingScope ],
         start_date: Types.DateInput,
         end_date: Types.DateInput,
         message: str ) -> bool:
      cur = conn.cursor()

      try:
         AnimalOffDisplayStatusResolver.delete_conflicting_animal_statuses(
            cur,
            species=species,
            exhibit=exhibit,
            viewing_scopes=viewing_scopes )

         for viewing_scope in viewing_scopes:
            cls._insert_animal_off_display_status(
               cur,
               species=species,
               exhibit=exhibit,
               viewing_scope=viewing_scope,
               start_date=start_date,
               end_date=end_date,
               message=message )

         conn.commit()
         return True

      finally:
         cur.close()


   @classmethod
   def save_animal_on_display_status(
         cls,
         conn: Types.Connection,
         species: str,
         exhibit: str,
         viewing_scopes: list[ AnimalViewingScope ] ) -> bool:
      cur = conn.cursor()

      try:
         AnimalOffDisplayStatusResolver.delete_conflicting_animal_statuses(
            cur,
            species=species,
            exhibit=exhibit,
            viewing_scopes=viewing_scopes )
         rowcount = cur.rowcount
         conn.commit()
         return rowcount > 0

      finally:
         cur.close()
