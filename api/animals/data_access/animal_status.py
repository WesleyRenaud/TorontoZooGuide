from __future__ import annotations

from ...shared.enums import AnimalViewingScope
from ...types import Connection, Cursor, DateInput, Row


def animal_viewing_scope_exists(
      cur: Cursor,
      species: str,
      exhibit: str,
      viewing_scope: AnimalViewingScope ) -> bool:
   if viewing_scope == AnimalViewingScope.ALL:
      return cur.execute(
         """   SELECT 1
               FROM EnclosureViewing
               WHERE SPECIES = ?
                  AND EXHIBIT = ?
               LIMIT 1;
         """,
         (
            species,
            exhibit,
         ) ).fetchone() != None

   return cur.execute(
      """   SELECT 1
            FROM EnclosureViewing
            WHERE SPECIES = ?
               AND EXHIBIT = ?
               AND LOWER( ENCLOSURE_TYPE ) = ?
            LIMIT 1;
      """,
      (
         species,
         exhibit,
         viewing_scope.value,
      ) ).fetchone() != None


def delete_conflicting_animal_statuses(
      cur: Cursor,
      species: str,
      exhibit: str,
      viewing_scope: AnimalViewingScope ) -> None:
   if viewing_scope == AnimalViewingScope.ALL:
      cur.execute(
         """   DELETE FROM AnimalStatus
               WHERE SPECIES = ?
                  AND EXHIBIT = ?;
         """,
         ( species, exhibit ) )
      return

   cur.execute(
      """   DELETE FROM AnimalStatus
            WHERE SPECIES = ?
               AND EXHIBIT = ?
               AND VIEWING_SCOPE IN ( ?, ? );
      """,
      (
         species,
         exhibit,
         AnimalViewingScope.ALL.value,
         viewing_scope.value,
      ) )


def insert_animal_off_display_status(
      cur: Cursor,
      species: str,
      exhibit: str,
      viewing_scope: AnimalViewingScope,
      start_date: DateInput,
      end_date: DateInput,
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
         viewing_scope.value,
         start_date,
         end_date,
         message,
      ) )


def save_animal_off_display_status(
      conn: Connection,
      species: str,
      exhibit: str,
      viewing_scope: AnimalViewingScope,
      start_date: DateInput,
      end_date: DateInput,
      message: str ) -> bool:
   cur = conn.cursor()

   try:
      if not animal_viewing_scope_exists(
            cur,
            species=species,
            exhibit=exhibit,
            viewing_scope=viewing_scope ):
         return False

      delete_conflicting_animal_statuses(
         cur,
         species=species,
         exhibit=exhibit,
         viewing_scope=viewing_scope )
      insert_animal_off_display_status(
         cur,
         species=species,
         exhibit=exhibit,
         viewing_scope=viewing_scope,
         start_date=start_date,
         end_date=end_date,
         message=message )

      conn.commit()
      return cur.rowcount > 0

   finally:
      cur.close()


def fetch_animal_status(
      cur: Cursor,
      species: str,
      exhibit: str,
      viewing_scope: AnimalViewingScope ) -> Row | None:
   return cur.execute(
      """   SELECT
               OFF_DISPLAY_START,
               OFF_DISPLAY_END,
               OFF_DISPLAY_MESSAGE
            FROM AnimalStatus
            WHERE SPECIES = ?
               AND EXHIBIT = ?
               AND VIEWING_SCOPE = ?;
      """,
      (
         species,
         exhibit,
         viewing_scope.value,
      ) ).fetchone()


def save_animal_on_display_status(
      conn: Connection,
      species: str,
      exhibit: str,
      viewing_scope: AnimalViewingScope ) -> bool:
   cur = conn.cursor()

   try:
      if not animal_viewing_scope_exists(
            cur,
            species=species,
            exhibit=exhibit,
            viewing_scope=viewing_scope ):
         return False

      if viewing_scope == AnimalViewingScope.ALL:
         cur.execute(
            """   DELETE FROM AnimalStatus
                  WHERE SPECIES = ?
                     AND EXHIBIT = ?;
            """,
            ( species, exhibit ) )
         rowcount = cur.rowcount
      else:
         all_status = fetch_animal_status(
            cur,
            species=species,
            exhibit=exhibit,
            viewing_scope=AnimalViewingScope.ALL )
         opposite_scope = AnimalViewingScope.opposite_scope( viewing_scope )

         cur.execute(
            """   DELETE FROM AnimalStatus
                  WHERE SPECIES = ?
                     AND EXHIBIT = ?
                     AND VIEWING_SCOPE IN ( ?, ? );
            """,
            (
               species,
               exhibit,
               AnimalViewingScope.ALL.value,
               viewing_scope.value,
            ) )
         rowcount = cur.rowcount

         if all_status != None and opposite_scope != None:
            insert_animal_off_display_status(
               cur,
               species=species,
               exhibit=exhibit,
               viewing_scope=opposite_scope,
               start_date=all_status[ 'OFF_DISPLAY_START' ],
               end_date=all_status[ 'OFF_DISPLAY_END' ],
               message=all_status[ 'OFF_DISPLAY_MESSAGE' ] )

      conn.commit()
      return rowcount > 0

   finally:
      cur.close()
