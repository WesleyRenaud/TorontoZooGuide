from __future__ import annotations

from ..domain.enclosure_off_display_month import EnclosureOffDisplayMonth
from .enclosure_off_display_month_mapper import EnclosureOffDisplayMonthMapper
from ...types import Types


class EnclosureOffDisplayMonthProvider():
   @classmethod
   def fetch_off_display_months(
         cls,
         conn: Types.Connection ) -> list[ EnclosureOffDisplayMonth ]:
      rows = conn.execute(
         """   SELECT
                  SPECIES,
                  EXHIBIT,
                  OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH
               FROM Enclosure
               ORDER BY SPECIES, EXHIBIT;
         """ ).fetchall()

      return EnclosureOffDisplayMonthMapper.map_records( rows )


   @classmethod
   def fetch_until_month(
         cls,
         conn: Types.Connection,
         species: str,
         exhibit: str ) -> int | None:
      row = conn.execute(
         """   SELECT OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH
               FROM Enclosure
               WHERE SPECIES = ?
                  AND EXHIBIT = ?;
         """,
         (
            species,
            exhibit,
         ) ).fetchone()

      return row[ 'OFF_DISPLAY_FOR_SEASON_UNTIL_MONTH' ]
