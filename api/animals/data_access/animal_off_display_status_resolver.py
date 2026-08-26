from __future__ import annotations

from ...shared.enums import AnimalViewingScope
from ...types import Cursor


class AnimalOffDisplayStatusResolver():
   @classmethod
   def delete_conflicting_animal_statuses(
         cls,
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
