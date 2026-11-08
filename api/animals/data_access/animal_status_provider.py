from __future__ import annotations

from .animal_off_display_mapper import AnimalOffDisplayMapper
from .animal_off_display_record import AnimalOffDisplayRecord
from .animal_off_display_status_resolver import AnimalOffDisplayStatusResolver
from .closure_linked_off_display_animal_mapper import ClosureLinkedOffDisplayAnimalMapper
from ..domain.animal_viewing_scope import AnimalViewingScope
from ..domain.closure_linked_off_display_animal import ClosureLinkedOffDisplayAnimal
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
         message: str,
         is_off_display_for_season: bool,
         closure_update_title: str | None,
         closure_update_start: Types.DateInput ) -> None:
      cur.execute(
         """   INSERT INTO AnimalStatus (
                  SPECIES,
                  EXHIBIT,
                  VIEWING_SCOPE,
                  IS_OFF_DISPLAY,
                  OFF_DISPLAY_START,
                  OFF_DISPLAY_END,
                  OFF_DISPLAY_MESSAGE,
                  OFF_DISPLAY_FOR_SEASON,
                  CLOSURE_UPDATE_TITLE,
                  CLOSURE_UPDATE_START
               )
               VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?, ?);
         """,
         (
            species,
            exhibit,
            viewing_scope.enclosure_name,
            start_date,
            end_date,
            message,
            is_off_display_for_season,
            closure_update_title,
            closure_update_start,
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
         message: str,
         is_off_display_for_season: bool,
         closure_update_title: str | None,
         closure_update_start: Types.DateInput | None ) -> bool:
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
               message=message,
               is_off_display_for_season=is_off_display_for_season,
               closure_update_title=closure_update_title,
               closure_update_start=closure_update_start )

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


   @classmethod
   def fetch_off_display_records( cls, conn: Types.Connection ) -> list[ AnimalOffDisplayRecord ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     SPECIES,
                     IS_OFF_DISPLAY,
                     OFF_DISPLAY_START,
                     OFF_DISPLAY_END,
                     OFF_DISPLAY_FOR_SEASON
                  FROM AnimalStatus;
            """ )

         return AnimalOffDisplayMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def fetch_closure_linked_off_display_animals(
         cls,
         conn: Types.Connection ) -> list[ ClosureLinkedOffDisplayAnimal ]:
      cur = conn.cursor()

      try:
         data = cur.execute(
            """   SELECT
                     SPECIES,
                     EXHIBIT,
                     OFF_DISPLAY_END,
                     CLOSURE_UPDATE_TITLE,
                     CLOSURE_UPDATE_START
                  FROM AnimalStatus
                  WHERE IS_OFF_DISPLAY = 1
                     AND OFF_DISPLAY_FOR_SEASON = 0
                     AND CLOSURE_UPDATE_TITLE IS NOT NULL
                     AND CLOSURE_UPDATE_START IS NOT NULL;
            """ )

         return ClosureLinkedOffDisplayAnimalMapper.map_records( data.fetchall() )

      finally:
         cur.close()


   @classmethod
   def extend_closure_linked_off_display_end(
         cls,
         conn: Types.Connection,
         title: str,
         start_date: Types.DateInput,
         end_date: Types.DateInput ) -> None:
      cur = conn.cursor()

      try:
         cur.execute(
            """   UPDATE AnimalStatus
                  SET OFF_DISPLAY_END = ?
                  WHERE IS_OFF_DISPLAY = 1
                     AND OFF_DISPLAY_FOR_SEASON = 0
                     AND CLOSURE_UPDATE_TITLE = ?
                     AND CLOSURE_UPDATE_START = ?;
            """,
            (
               end_date,
               title,
               start_date,
            ) )
         conn.commit()

      finally:
         cur.close()
